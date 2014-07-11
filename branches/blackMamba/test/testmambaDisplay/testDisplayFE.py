"""
Test cases for display front-end fonction and optional user-defined displayer

Python functions and method:
    imageMb.show
    imageMb.hide
    imageMb.update
    imageMb.freeze
    imageMb.unfreeze
    imageMb.setName
    imageMb.setPalette
    imageMb.resetPalette
    tidyDisplays
    setShowImages
    getShowImages
    sequenceMb.showAllImages
    sequenceMb.showImage
    sequenceMb.hideAllImages
    sequenceMb.hideImage
"""

from mamba import *
import mambaDisplay as display
import unittest
import random
from PIL import Image

class testDisplayer(display.mambaDisplayer):

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

class TestDisplayFE(unittest.TestCase):

    def setUp(self):
        self.testDisp = testDisplayer()
        
    def tearDown(self):
        del(self.testDisp)
            
    def testShowAndHide(self):
        """Verifies the activation/deactivation of the display front-end methods"""
        im = imageMb(displayer=self.testDisp)
        
        im.hide()
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), 0)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.hide()
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), 1, "hideWindow = %d" % (self.testDisp.getStatsOnFun("hideWindow")))
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 2)
        
        im2 = imageMb()
        im2.show()
        del(im2)
        
    def testUpdate(self):
        """Verifies the display update front-end method"""
        im = imageMb(displayer=self.testDisp)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        self.testDisp.eraseStatsOnFun()
        
        im.update()
        self.assertEqual(self.testDisp.getStatsOnFun("updateWindow"), 1)
        
    def testModification(self):
        """Verifies that the display is notified of some internal changes"""
        im = imageMb(displayer=self.testDisp)
        (w,h) = im.getSize()
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        Image.new("RGB", (w,h), (10,10,10)).save("test.jpg")
        im.load("test.jpg")
        self.assertEqual(self.testDisp.getStatsOnFun("reconnectWindow"), 1)
        os.remove("test.jpg")
        
        im.convert(1)
        self.assertEqual(self.testDisp.getStatsOnFun("reconnectWindow"), 2)
        
    def testFreeze(self):
        """Verifies the display freeze and unfreeze front-end methods"""
        im = imageMb(displayer=self.testDisp)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.freeze()
        self.assertEqual(self.testDisp.getStatsOnFun("controlWindow"), 1)
        im.unfreeze()
        self.assertEqual(self.testDisp.getStatsOnFun("controlWindow"), 2)
        
    def testName(self):
        """Verifies that display is informed when image name change"""
        im = imageMb(displayer=self.testDisp)
        
        im.setName("test1")
        self.assertEqual(self.testDisp.getStatsOnFun("retitleWindow"), 0)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.setName("test1")
        self.assertEqual(self.testDisp.getStatsOnFun("retitleWindow"), 1)
        
    def testPalette(self):
        """Verifies that the palette is correctly transmitted to display"""
        im = imageMb(displayer=self.testDisp)
        
        im.setPalette(rainbow)
        self.assertEqual(self.testDisp.getStatsOnFun("colorizeWindow"), 0)
        im.resetPalette()
        self.assertEqual(self.testDisp.getStatsOnFun("colorizeWindow"), 0)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        im.setPalette(rainbow)
        self.assertEqual(self.testDisp.getStatsOnFun("colorizeWindow"), 1)
        im.resetPalette()
        self.assertEqual(self.testDisp.getStatsOnFun("colorizeWindow"), 2)
        
    def testTidyDisplays(self):
        """Verifies that the tidyDisplays function correctly calls the displayer"""
        im = imageMb(displayer=self.testDisp)
        
        im.show()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        tidyDisplays(displayer=self.testDisp)
        self.assertEqual(self.testDisp.getStatsOnFun("tidyWindows"), 1)
        
        tidyDisplays() # Standard displayer call (no effect on the test displayer
        self.assertEqual(self.testDisp.getStatsOnFun("tidyWindows"), 1)
        
    def testSetShowImages(self):
        """Verifies that the automatic display activation is working"""
        self.assertEqual(getShowImages(), False)
        
        setShowImages(True)
        self.assertEqual(getShowImages(), True)
        im1 = imageMb(displayer=self.testDisp)
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 1)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 1)
        
        self.testDisp.eraseStatsOnFun()
        
        setShowImages(False)
        self.assertEqual(getShowImages(), False)
        im2 = imageMb(displayer=self.testDisp)
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), 0)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), 0)
        
    def testSequence(self):
        """Verifies sequence display front-end method"""
        li = random.randint(10,25)
        im = imageMb(displayer=self.testDisp)
        seq = sequenceMb(im, li, displayer=self.testDisp)
        
        seq.showAllImages()
        self.assertEqual(self.testDisp.getStatsOnFun("addWindow"), li)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), li)
        
        seq.hideAllImages()
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), li)
        
        seq.showImage(li//2)
        self.assertEqual(self.testDisp.getStatsOnFun("showWindow"), li+1)
        
        seq.hideImage(li//2)
        self.assertEqual(self.testDisp.getStatsOnFun("hideWindow"), li+1)


        
    def testImage3DMbDisplay(self):
        """Verifies display management in 3D images"""
        opa = range(256)
        im1 = image3DMb(64,64,64)
        im2 = image3DMb(64,64,64)
        im3 = image3DMb(64,64,64)
        im4 = image3DMb(64,64,64,displayer=image3DDisplay)
        im5 = image3DMb(64,64,64,displayer=image3DDisplay)
        
        im1.show()
        im2.show("VTK")
        im3.show("PROJECTION")
        im4.show("USER")
        im5.show()
        
        im1.setPalette(rainbow)
        im2.setPalette(rainbow)
        im3.setPalette(rainbow)
        im4.setPalette(rainbow)
        im5.setPalette(rainbow)
        
        im1.resetPalette()
        im2.resetPalette()
        im3.resetPalette()
        im4.resetPalette()
        im5.resetPalette()
        
        im1.setOpacity(opa)
        im2.setOpacity(opa)
        im3.setOpacity(opa)
        im4.setOpacity(opa)
        im5.setOpacity(opa)
        
        im1.resetOpacity()
        im2.resetOpacity()
        im3.resetOpacity()
        im4.resetOpacity()
        im5.resetOpacity()
        
        im1.hide()
        im2.hide()
        im3.hide()
        im4.hide()
        im5.hide()
        
        im1.show()
        im2.show()
        im3.show()
        im4.show()
        im5.show()
        
        im1.update()
        im2.update()
        im3.update()
        im4.update()
        im5.update()
        
        im1.hide()
        im2.hide()
        im3.hide()
        im4.hide()
        im5.hide()
        
        im1.show()
        im2.show("VTK")
        im3.show("PROJECTION")
        im4.show("USER")
        im5.show()

