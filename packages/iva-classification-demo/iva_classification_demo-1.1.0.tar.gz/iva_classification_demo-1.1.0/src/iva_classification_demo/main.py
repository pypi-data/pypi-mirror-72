from PyQt5.QtWidgets import QApplication, QWidget,\
	QLabel, QMainWindow, QGridLayout, QPushButton, QSizePolicy, QComboBox, QFileDialog, QScrollArea,\
	QSpinBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QTimer, QDir, QFile, QIODevice, Qt
from PyQt5.QtGui import QImage, QPixmap, QImageReader

from iva_classification_demo.comp_view import comp_view
from iva_applications.imagenet.config import CLASS_DICT
import sys
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

class mainwin(QMainWindow):

	def __init__(self, dir_path=None, labels_path=None, prog_path_tpu=None, prog_path_tf=None, parent=None):
		super(mainwin, self).__init__(parent)
		self.initUI()

		self._feed_tmr.timeout.connect(self.tryFeed)
		self._feed_tmr.start(1000)
		self._img_dir = None
		self._images = None
		self._started = False
		self._labels_list = None

		self._graph_width=100

		self._tpu_view = comp_view(local=False,
			cps_label=self._lbl_cps_tpu,
			top1_lbl=self._top1_label_tpu,
			top5_lbl=self._top5_label_tpu,
			graph_widget=self._graph_widget,
			graph_width=self._graph_width,
			pen1 = pg.mkPen(color=(255, 0, 0)),
			pen5 = pg.mkPen(color=(0, 255, 0)),
			name1 = "top1 tpu",
			name5 = "top5 tpu",
			prog_path=prog_path_tpu)

		self._tpu_view.gotLabels.connect(self.process_labels)

		self._tf_view = comp_view(local=True,
			cps_label=self._lbl_cps_tf,
			top1_lbl=self._top1_label_tf,
			top5_lbl=self._top5_label_tf,
			graph_widget=self._graph_widget,
			graph_width=self._graph_width,
			pen1 = pg.mkPen(color=(127, 0, 0)),
			pen5 = pg.mkPen(color=(0, 127, 0)),
			name1 = "top1 tf",
			name5 = "top5 tf",
			prog_path=prog_path_tf)

		if(dir_path is not None):
			self._load_dir(dir_path)
			self._load_labels(labels_path)
			self._tpu_view.set_network(prog_path_tpu)
			self._tf_view.set_network(prog_path_tf)

		if(prog_path_tf is None):
			self._tf_view.set_placeholders(0.7563, 0.9235)

	def _load_dir(self, path:str):
		self._img_dir = QDir(path)
		self._img_dir_iter = 0
		filt = ["*.JPEG", "*.jpg", "*.png"]
		self._images = self._img_dir.entryInfoList(filt)

	def _load_labels(self, path:str):
		path = QDir.currentPath()+"/"+path
		list_file = QFile(path)
		list_file.open(QIODevice.ReadOnly)
		self._labels_list = []
		while(not list_file.atEnd()):
			file_lbl = list_file.readLine()
			fname = str(file_lbl.split(" ")[0].data(), encoding='utf-8')
			num = str(file_lbl.split(" ")[1].data(), encoding='utf-8')[:-1]
			self._labels_list.append([fname, num]);

	@pyqtSlot()
	def start_process(self):
		self._tpu_view.start()
		self._tf_view.start()
		self._started = True

	@pyqtSlot(int)
	def process_speed(self, speed:int):
		self._feed_tmr.setInterval(speed)

	@pyqtSlot(list)
	def process_labels(self, labels):
		self._lbl_labels.setText("; ".join(labels))

	def initUI(self):
		self._central = QWidget(self)
		grid = QGridLayout(self)
		self._img_holder = QScrollArea()
		self._img_holder.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding) 
		self._img_holder.setAlignment(Qt.AlignVCenter)
		self._speed_box = QSpinBox()
		self._speed_box.setRange(0, 1000)
		self._speed_box.setValue(1000)
		self._speed_box.setSingleStep(100)
		self._speed_box.valueChanged.connect(self.process_speed)
		self._lbl_img = QLabel("img_lbl")
		self._lbl_img.scaledContents=True
		self._img_holder.setWidget(self._lbl_img)
		self._lbl_rl_labels = QLabel("guessed classes")
		self._lbl_rl_labels.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		self._lbl_labels = QLabel("guessed classes")
		self._lbl_labels.setWordWrap(True)
		self._lbl_labels.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		self._lbl_cps_tf = QLabel("cps tf:")
		self._lbl_cps_tpu = QLabel("cps tpu:")
		self._lbl_classes = QLabel("cps tpu:")
		self._btn_open_dir = QPushButton("open dir")
		self._btn_open_net = QPushButton("open NN")
		self._btn_start = QPushButton("start")
		self._feed_tmr = QTimer(self)
		self._graph_widget = pg.PlotWidget()
		self._graph_widget.addLegend()
		self._top1_label_tf = QLabel("top1 tf")
		self._top1_label_tpu = QLabel("top1 tpu")
		self._top5_label_tf = QLabel("top5 tf")
		self._top5_label_tpu = QLabel("top5 tpu")
		self._top1_label_tf.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
		self._top1_label_tpu.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
		self._top5_label_tf.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
		self._top5_label_tpu.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
		grid.addWidget(self._img_holder,	0, 0, 4, 6)
		grid.addWidget(self._lbl_rl_labels,	4, 0, 1, 6)
		grid.addWidget(self._lbl_labels,	5, 0, 1, 6)
		grid.addWidget(self._top1_label_tf,	0, 6, 1, 1)
		grid.addWidget(self._top1_label_tpu,	0, 7, 1, 1)
		grid.addWidget(self._top5_label_tf,	0, 8, 1, 1)
		grid.addWidget(self._top5_label_tpu,	0, 9, 1, 1)
		grid.addWidget(self._graph_widget,	1, 6, 6, 4)
		grid.addWidget(self._lbl_cps_tf,	6, 0, 1, 1)
		grid.addWidget(self._lbl_cps_tpu,	6, 1, 1, 1)
		grid.addWidget(self._btn_open_dir,	6, 2, 1, 1)
		grid.addWidget(self._btn_open_net,	6, 3, 1, 1)
		grid.addWidget(self._speed_box,		6, 4, 1, 1)
		grid.addWidget(self._btn_start,		6, 5, 1, 1)
		self.setCentralWidget(self._central)
		self._central.setLayout(grid)
		self._btn_start.clicked.connect(self.start_process)
		self._btn_open_net.clicked.connect(self.openFile)
		self._btn_open_dir.clicked.connect(self.openDir)
		self.resize(800, 600)

	@pyqtSlot()
	def openFile(self):
		fname = QFileDialog.getOpenFileName(self, 'Open tpu program')
		self._tpu_view.set_network(fname[0])
		fname = QFileDialog.getOpenFileName(self, 'Open tf graph')
		if(len(fname) == 0):
			self._tf_view.set_network(None)
		else:
			self._tf_view.set_network(fname[0])

	@pyqtSlot()
	def openDir(self):
		fname = str(QFileDialog.getExistingDirectory(self, 'Open directory with dataset'))
		self._load_dir(fname)
		fname = QFileDialog.getOpenFileName(self, 'Open labels list')[0]
		self._load_labels(fname)

	@pyqtSlot()
	def tryFeed(self):
		if(self._img_dir is None and self._images is None):
			return
		if(not self._tpu_view.got_class or
			not self._tf_view.got_class):
			return
		if(not self._started):
			return
		if(self._img_dir_iter == len(self._images)):
			self._img_dir_iter = 0
		path = self._images[self._img_dir_iter].absoluteFilePath()
		rdr = QImageReader(path)
		path = self._images[self._img_dir_iter].fileName()
		img = rdr.read()
		real_lbl = ""
		for lbl_lst in self._labels_list:
			if(path == lbl_lst[0]):
				real_lbl = str(lbl_lst[1])
		if(real_lbl == ""):
			print("WARNING, img "+path+" is not in labels list!")
			self._img_dir_iter += 1
			return
		self._lbl_rl_labels.setText(CLASS_DICT[int(real_lbl)-1])
		real_lbl = str(int(real_lbl)-1)
		self._tpu_view.process(img, real_lbl)
		self._tf_view.process(img, real_lbl)
		self._img_dir_iter += 1
		self.drawImage(img)

	@pyqtSlot(QImage)
	def drawImage(self, img:QImage):
		px = QPixmap.fromImage(img)
		px = px.scaled(self._img_holder.width(), self._img_holder.height(),
			Qt.KeepAspectRatio)
		self._lbl_img.setPixmap(px)
		self._lbl_img.resize(px.width(), px.height())

def main():
	app = QApplication(sys.argv)
	argc = len(sys.argv)
	print(argc)
	if(argc == 1):
		win = mainwin()
	elif(argc == 5):
		win = mainwin(dir_path = sys.argv[1], labels_path = sys.argv[2], prog_path_tpu = sys.argv[3], prog_path_tf = sys.argv[4])
	elif(argc == 4):
		win = mainwin(dir_path = sys.argv[1], labels_path = sys.argv[2], prog_path_tpu = sys.argv[3])
	else:
		print("UNKNOWN ARGS")
		return
	import qtmodern.styles
	import qtmodern.windows
	qtmodern.styles.dark(app)
	mw = qtmodern.windows.ModernWindow(win)
	mw.show()
	app.exec_()

if __name__ =="__main__":
	main()
