"""
Test cases for the thinning and thickening functions found in the thinthick
module of mamba package.

Python functions:
    hierarchy
    hierarchicalLevel
    waterfalls
    enhancedWaterfalls
    standardSegment
    segmentByP
    generalSegment
    extendedSegment
"""

from mamba import *
import unittest
import random

class TestHierarchies(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
            
    def drawFakeWatershed1(self, imOut):
        (w,h) = imOut.getSize()
        
        imOut.reset()
        drawLine(imOut, (20,0,20,h-1), 30)
        drawLine(imOut, (40,0,40,h-1), 10)
        drawLine(imOut, (60,0,60,h-1), 60)
        drawLine(imOut, (80,0,80,h-1), 50)
        drawLine(imOut, (110,0,110,h-1), 10)
        drawLine(imOut, (130,0,130,h-1), 100)
        drawLine(imOut, (160,0,160,h-1), 110)
        drawLine(imOut, (200,0,200,h-1), 20)
        drawLine(imOut, (240,0,240,h-1), 50)
            
    def drawFakeHierarchy1(self, imOut):
        (w,h) = imOut.getSize()
        
        imOut.reset()
        drawSquare(imOut, (0,0,20,h-1), 30)
        drawSquare(imOut, (21,0,59,h-1), 10)
        drawLine(imOut, (60,0,60,h-1), 60)
        drawSquare(imOut, (61,0,80,h-1), 50)
        drawSquare(imOut, (81,0,129,h-1), 10)
        drawSquare(imOut, (130,0,159,h-1), 100)
        drawLine(imOut, (160,0,160,h-1), 110)
        drawSquare(imOut, (161,0,239,h-1), 20)
        drawSquare(imOut, (240,0,w-1,h-1), 50)
        
    def drawFakeWatershed2(self, imOut):
        (w,h) = imOut.getSize()
        
        imOut.reset()
        drawLine(imOut, (10,0,10,h-1), 5)
        drawLine(imOut, (20,0,20,h-1), 30)
        drawLine(imOut, (40,0,40,h-1), 5)
        drawLine(imOut, (60,0,60,h-1), 10)
        drawLine(imOut, (80,0,80,h-1), 5)
        drawLine(imOut, (100,0,100,h-1), 70)
        drawLine(imOut, (120,0,120,h-1), 25)
        drawLine(imOut, (140,0,140,h-1), 70)
        drawLine(imOut, (160,0,160,h-1), 5)
        drawLine(imOut, (180,0,180,h-1), 10)
        drawLine(imOut, (200,0,200,h-1), 5)
        drawLine(imOut, (220,0,220,h-1), 30)
        drawLine(imOut, (230,0,230,h-1), 5)
        
    def testHierarchy(self):
        """Verifies the proper computation of the hierarchy image"""
        self.drawFakeWatershed1(self.im8_1)
        self.drawFakeHierarchy1(self.im8_3)
        threshold(self.im8_1, self.im1_1, 1, 255)
        
        hierarchy(self.im8_1, self.im1_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testHierarchicalLevel(self):
        """Verifies the proper computation of the next hierarchal level"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (60,0,60,h-1), 60)
        drawLine(self.im8_3, (160,0,160,h-1), 110)
        
        hierarchicalLevel(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testWaterfalls(self):
        """Verifies the proper computation of the waterfalls algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 1)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 1)
        drawLine(self.im8_3, (160,0,160,h-1), 2)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        waterfalls(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testEnhancedWaterfalls(self):
        """Tests the proper computation of the enhanced waterfalls algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 1)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 2)
        drawLine(self.im8_3, (160,0,160,h-1), 2)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        enhancedWaterfalls(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testStandardSegment(self):
        """Tests the proper computation of the standard segment algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 2)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 2)
        drawLine(self.im8_3, (160,0,160,h-1), 2)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        standardSegment(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testGeneralSegment(self):
        """Tests the proper computation of the general segment algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 2)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 2)
        drawLine(self.im8_3, (160,0,160,h-1), 2)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        generalSegment(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        
    def testSegmentByP(self):
        """Tests the proper computation of the P algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 2)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 2)
        drawLine(self.im8_3, (160,0,160,h-1), 2)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        n = segmentByP(self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        self.assertEqual(n, 2, "levels = %d"%(n))
        
        self.drawFakeWatershed2(self.im8_1)
        n = segmentByP(self.im8_1, self.im8_2)
        self.assertEqual(n, 3, "levels = %d"%(n))
        
    def testExtendedSegment(self):
        """Tests the proper computation of the extended segment algorithm"""
        self.drawFakeWatershed1(self.im8_1)
        self.drawFakeWatershed1(self.im8_4)
        drawSquare(self.im8_4, (150,0,255,255), 0)
        
        (w,h) = self.im8_3.getSize()
        self.im8_3.reset()
        drawLine(self.im8_3, (20,0,20,h-1), 1)
        drawLine(self.im8_3, (40,0,40,h-1), 1)
        drawLine(self.im8_3, (60,0,60,h-1), 2)
        drawLine(self.im8_3, (80,0,80,h-1), 1)
        drawLine(self.im8_3, (110,0,110,h-1), 1)
        drawLine(self.im8_3, (130,0,130,h-1), 2)
        drawLine(self.im8_3, (160,0,160,h-1), 1)
        drawLine(self.im8_3, (200,0,200,h-1), 1)
        drawLine(self.im8_3, (240,0,240,h-1), 1)
        
        extendedSegment(self.im8_1, self.im8_4, self.im8_2)
        (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0)

