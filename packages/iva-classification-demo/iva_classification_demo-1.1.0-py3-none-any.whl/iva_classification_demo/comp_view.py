from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from pyqtgraph import PlotWidget, plot
from iva_classification_demo.class_computer import classComputer

class comp_view(QObject):
	setNetwork = pyqtSignal(str)
	startProcessSig = pyqtSignal()
	gotImg = pyqtSignal(QImage)
	gotLabels = pyqtSignal(list)

	def __init__(self, local:bool, top1_lbl:QLabel, top5_lbl:QLabel,
		cps_label:QLabel, graph_widget:PlotWidget, graph_width:int,
		pen1, name1, pen5, name5,
		prog_path=None, parent=None):
		super(comp_view, self).__init__(parent)

		self._graph_width = graph_width
		self._graph_widget = graph_widget
		self._local=local

		self._cps_label = cps_label
		self._comp_thread = QThread()
		self._cls_cmp = classComputer(local)
		self._cls_cmp.moveToThread(self._comp_thread)
		self._cls_cmp.computed.connect(self.computedSlot)
		self._cls_cmp.got_class.connect(self.processClasses)
		self.setNetwork.connect(self._cls_cmp.setNetwork)
		self.gotImg.connect(self._cls_cmp.process)
		self.startProcessSig.connect(self._cls_cmp.startProcessing)
		self._comp_thread.start()
		self.got_class = True #on first iter to start loop

		self._img_path=None
		self._prog_path=None
		if(prog_path is not None):
			self.set_network(prog_path)

		self._x = [0]
		self._top1_fixed = 1
		self._top5_fixed = 1
		self._top1_count = 1
		self._top1_data = [self._top1_fixed]
		self._top1_graph = self._graph_widget.plot(self._x, self._top1_data,
			pen=pen1, name=name1)

		self._top1_lbl = top1_lbl
		self._top1_lbl_prefix = name1

		self._top5_count = 1
		self._top5_data = [self._top5_fixed]
		self._top5_graph = self._graph_widget.plot(self._x, self._top5_data,
			pen=pen5, name=name5)
		self._top5_lbl = top5_lbl
		self._top5_lbl_prefix = name5

		self._computed_count = 1
	
	def set_network(self, path):
		self._prog_path = path
		self.setNetwork.emit(path)

	def set_placeholders(self, top1, top5):
		self._top1_fixed = top1
		self._top5_fixed = top5

	@pyqtSlot(float)
	def computedSlot(self, cps:float):
		if(self._local):
			self._cps_label.setText("cps tf:"+str(int(cps)))
		else:
			self._cps_label.setText("cps tpu:"+str(int(cps)))

	def process(self, img:QImage, path:str):
		self.got_class = False
		self._img_path = path
		self.gotImg.emit(img)

	def start(self):
		self._cls_cmp.startProcessing()

	def _get_tops(self, labels, real_num:str):
		num1 = str(labels[0][1])
		nums = []
		for lbl, n in labels[1:]:
			nums.append(str(n))
		if(num1 == real_num):
			return [1, 1] #both top1 and top5
		else:
			for num in nums:
				if(real_num == num):
					return [0, 1] #only top5
		return [0, 0] #nothing found

	def _crop_data(self, data):
		if(len(data) == self._graph_width):
			return data[1:]
		return data

	@pyqtSlot(list)
	def processClasses(self, labels):
		lbl_list = []
		for lbl, n in labels:
			lbl_list.append(str(lbl))
		self.gotLabels.emit(lbl_list)

		if(len(self._x) == self._graph_width):
			self._x = self._x[1:]
		if(len(self._top1_data) == self._graph_width):
			self._top1_data = self._top1_data[1:]
		if(len(self._top5_data) == self._graph_width):
			self._top5_data = self._top5_data[1:]
		self._x.append(self._x[-1]+1)
		self._computed_count += 1
		if(self._local and self._prog_path is None):
			top1_val = self._top1_fixed
			top5_val = self._top5_fixed
		else:
			deltas = self._get_tops(labels, self._img_path)
			self._top1_count += deltas[0]
			self._top5_count += deltas[1]
			top1_val = self._top1_count/self._computed_count
			top5_val = self._top5_count/self._computed_count

		self._top1_lbl.setText(f"{self._top1_lbl_prefix}:{'%.4f' % top1_val}")
		self._top5_lbl.setText(f"{self._top5_lbl_prefix}:{'%.4f' % top5_val}")
		self._top1_data.append(top1_val)
		self._top5_data.append(top5_val)

		self._top1_graph.setData(self._x, self._top1_data)
		self._top5_graph.setData(self._x, self._top5_data)
		self.got_class = True
