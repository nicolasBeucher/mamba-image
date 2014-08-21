"""
Test cases for 3D display front-end fonctions

Python functions and method:
    image3DMb.show
    image3DMb.hide
    image3DMb.update
    image3DMb.freeze
    image3DMb.unfreeze
"""

from mamba3D import *
import mambaDisplay
import unittest
from PIL import Image

class TestDisplay3D(unittest.TestCase):

    def setUp(self):
        self.testDisp = mambaDisplay.getDisplayer()
        self.testDisp.eraseStatsOnFun()
        
    def testShowAndHide(self):
        """Verifies the activation/deactivation of the display front-end methods"""
        im = image3DMb()
        
        im.hide()
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), 0)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.hide()
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), 1)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 2)
        
        im2 = image3DMb()
        im2.show()
        del(im2)
        self.assertEqual(self.testDisp.getStatsOnFun("destroyWindow"), 1)
        
    def testUpdate(self):
        """Verifies the display update front-end method"""
        im = image3DMb()
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        self.testDisp.eraseStatsOnFun()
        
        im.update()
        self.assertEqual(self.testDisp.getStatsOnFun("updateWindow"), 1)
        
    def testFreeze(self):
        """Verifies the display freeze and unfreeze front-end methods"""
        im = image3DMb()
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.freeze()
        self.assertEqual(self.testDisp.getStatsOnFun("controlWindow"), 1)
        im.unfreeze()
        self.assertEqual(self.testDisp.getStatsOnFun("controlWindow"), 2)
        
    def testName(self):
        """Verifies that display is informed when image name change"""
        im = image3DMb()
        
        im.setName("test1")
        self.assertEqual(self.testDisp.getStatsOnFun("updateWindow"), 0)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.setName("test1")
        self.assertEqual(self.testDisp.getStatsOnFun("updateWindow"), 1)
        
