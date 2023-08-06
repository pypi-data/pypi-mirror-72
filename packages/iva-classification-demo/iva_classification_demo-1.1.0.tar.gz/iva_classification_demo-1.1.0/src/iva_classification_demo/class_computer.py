from typing import List
import numpy as np
import io
import tensorflow as tf

from iva_applications.utils import tpu_runner
from iva_applications.imagenet.postprocess import tpu_tensor_to_classes, tpu_tensor_to_num_classes
from iva_applications import vgg19
from iva_applications import resnet50
from PIL import Image

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QBuffer
from PyQt5.QtGui import QImage, QPixmap
import time

class classComputer(QObject):
	got_class = pyqtSignal(list)
	started = pyqtSignal()
	computed = pyqtSignal(float)

	def __init__(self, local:bool, parent=None):
		super(classComputer, self).__init__(parent)
		self._local = local
		self._runner = None
		self._path = None
		self._sess = tf.Session()

	@pyqtSlot(str)
	def setNetwork(self, path:str):
		self._path = path

	@pyqtSlot()
	def startProcessing(self):
		if(self._path is None or self._path == ""):
			print("WARN: no program path in classifier")
			return
		if(self._local):
			from iva_applications.utils import TFRunnerDict
			self._runner = TFRunnerDict(
				input_nodes=["Placeholder:0"],
				output_nodes=["logits:0"],
				graph_path=self._path)
		else:
			self._runner = tpu_runner.TPURunner(self._path)


	def __del__(self):
		if(self._sess is not None):
			self._sess.close()

	@pyqtSlot(QImage)
	def process(self, img:QImage):
		class_ = []
		if(self._runner is None):
			self.got_class.emit(class_)
			return

		buffer = QBuffer()
		buffer.open(QBuffer.ReadWrite)
		img.save(buffer, "JPEG")
		image = Image.open(io.BytesIO(buffer.data()))
		buffer.close()
 
		tensor = resnet50.preprocess.image_to_tensor(image)
		tensor = np.expand_dims(tensor, axis=0)
		input_nodes = self._runner.input_nodes
		output_nodes = self._runner.output_nodes
		time_0 = time.time()
		output = self._runner({input_nodes[0]:tensor})
		time_1 = time.time()
		cps = 1.0 / (time_1 - time_0)
		self.computed.emit(cps)

		class_ = tpu_tensor_to_classes(output[output_nodes[0]], top=5)
		nums = tpu_tensor_to_num_classes(output[output_nodes[0]], top=5)
		class_ = list(zip(class_, nums))
		self.got_class.emit(class_)
