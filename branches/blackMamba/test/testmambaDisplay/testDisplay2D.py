"""
Test cases for 2D display front-end fonctions

Python functions and method:
    imageMb.show
    imageMb.hide
    imageMb.update
    imageMb.freeze
    imageMb.unfreeze
    imageMb.setName
    setShowImages
    getShowImages
"""

from mamba import *
import mambaDisplay
import unittest
from PIL import Image
import os

class testDisplayer(mambaDisplay.Displayer):

    def __init__(self):
        self.dict_fun = {
            "addWindow" : 0,
            "showWindow" : 0,
            "controlWindow" : 0,
            "updateWindow" : 0,
            "hideWindow" : 0,
            "reconnectWindow" : 0,
            "colorizeWindow" : 0,
            "destroyWindow" : 0,
            "retitleWindow" : 0,
            "tidyWindows" : 0
        }

    def addWindow(self, im):
        self.dict_fun["addWindow"] += 1
        return 'dummy_key'
        
    def showWindow(self, wKey):
        self.dict_fun["showWindow"] += 1
        
    def controlWindow(self, wKey, ctrl):
        self.dict_fun["controlWindow"] += 1
       
    def updateWindow(self, wKey):
        self.dict_fun["updateWindow"] += 1
       
    def hideWindow(self, wKey):
        self.dict_fun["hideWindow"] += 1
       
    def reconnectWindow(self, wKey, im):
        self.dict_fun["reconnectWindow"] += 1
       
    def colorizeWindow(self, wKey, pal=None):
        self.dict_fun["colorizeWindow"] += 1

    def destroyWindow(self, wKey):
        self.dict_fun["destroyWindow"] += 1
       
    def retitleWindow(self, wKey, name):
        self.dict_fun["retitleWindow"] += 1
        
    def tidyWindows(self):
        self.dict_fun["tidyWindows"] += 1
        
    def getStatsOnFun(self, fun):
        return self.dict_fun[fun]
        
    def eraseStatsOnFun(self):
        for k in self.dict_fun.keys():
            self.dict_fun[k] = 0
            
testDisp = testDisplayer()
mambaDisplay.setDisplayer(testDisp)

class TestDisplay2D(unittest.TestCase):

    def tearDown(self):
        global testDisp
        testDisp.eraseStatsOnFun()
            
    def testShowAndHide(self):
        """Verifies the activation/deactivation of the display front-end methods"""
        global testDisp
        im = imageMb()
        
        im.hide()
        self.assertEqual(testDisp.getStatsOnFun("hideWindow"), 0)
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        im.hide()
        self.assertEqual(testDisp.getStatsOnFun("hideWindow"), 1)
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 2)
        
        im2 = imageMb()
        im2.show()
        del(im2)
        self.assertEqual(testDisp.getStatsOnFun("destroyWindow"), 1)
        
    def testUpdate(self):
        """Verifies the display update front-end method"""
        global testDisp
        im = imageMb()
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        testDisp.eraseStatsOnFun()
        
        im.update()
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 1)
        
    def testModification(self):
        """Verifies that the display is notified of some internal changes"""
        global testDisp
        im = imageMb()
        (w,h) = im.getSize()
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        Image.new("RGB", (w,h), (10,10,10)).save("test.jpg")
        im.load("test.jpg")
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 1)
        rawdata = 256*256*b"\x11"
        im.loadRaw(rawdata)
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 2)
        
        im.convert(1)
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 3)
        os.remove("test.jpg")
        
    def testFreeze(self):
        """Verifies the display freeze and unfreeze front-end methods"""
        global testDisp
        im = imageMb()
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        im.freeze()
        self.assertEqual(testDisp.getStatsOnFun("controlWindow"), 1)
        im.unfreeze()
        self.assertEqual(testDisp.getStatsOnFun("controlWindow"), 2)
        
    def testName(self):
        """Verifies that display is informed when image name change"""
        global testDisp
        im = imageMb()
        
        im.setName("test1")
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 0)
        
        im.show()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        im.setName("test1")
        self.assertEqual(testDisp.getStatsOnFun("updateWindow"), 1)
        
    def testSetShowImages(self):
        """Verifies that the automatic display activation is working"""
        global testDisp
        self.assertEqual(getShowImages(), False)
        
        setShowImages(True)
        self.assertEqual(getShowImages(), True)
        im1 = imageMb()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 1)
        
        testDisp.eraseStatsOnFun()
        
        setShowImages(False)
        self.assertEqual(getShowImages(), False)
        im2 = imageMb()
        self.assertEqual(testDisp.getStatsOnFun("addWindow"), 0)
        self.assertEqual(testDisp.getStatsOnFun("showWindow"), 0)
        
