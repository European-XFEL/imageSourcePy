import unittest

from karabo.bound import Configurator, Hash, PythonDevice
from ..CameraImageSource import CameraImageSource
from ..ImageSource import ImageSource


class ImageSourcer_TestCase(unittest.TestCase):
    def test_image_source(self):
        config = Hash("Logger.priority", "WARN",
                      "deviceId", "ImageSourceTest")
        dev = Configurator(PythonDevice).create("ImageSource", config)
        dev.startFsm()

    def test_camera_image_source(self):
        config = Hash("Logger.priority", "WARN",
                      "deviceId", "CameraImageSourceTest")
        dev = Configurator(PythonDevice).create("CameraImageSource", config)
        dev.startFsm()
