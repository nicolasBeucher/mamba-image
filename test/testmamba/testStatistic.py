"""
Test cases for the statistical functions found in the statistic module of 
mamba package.

Python functions and classes:
    getMean
    getMedian
    getVariance
"""

from mamba import *
import unittest
import random

class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        
    def testGetMean(self):
        """Verifies the correct computation of the mean value of an image"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            s = 0
            # creating a random image
            for wi in range(w):
                vi = random.randint(0,255)
                drawLine(self.im8_1, (wi,0,wi,h-1), vi)
                s += (h*vi)
            self.assertEqual(getMean(self.im8_1), (float(s)/float(w*h)))
        
    def testGetMedian(self):
        """Verifies the correct computation of the median value of an image"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            l = 256*[0]
            # creating a random image
            for wi in range(w):
                vi = random.randint(0,255)
                drawLine(self.im8_1, (wi,0,wi,h-1), vi)
                l[vi] += h
            s = 0
            for i in range(256):
                s += l[i]
                if s>((w*h)//2):
                    break
            self.assertEqual(getMedian(self.im8_1), i, "%d!=%d: %d %d"%(i,getMedian(self.im8_1),s,w*h//2))
        
    def testGetVariance(self):
        """Verifies the correct computation of the variance value of an image"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            l = 256*[0]
            s = 0
            # creating a random image
            for wi in range(w):
                vi = random.randint(0,255)
                drawLine(self.im8_1, (wi,0,wi,h-1), vi)
                l[vi] += h
                s += (h*vi)
            mean = (float(s)/float(w*h))
            var = 0
            for i in range(256):
                var += l[i]*(i-mean)*(i-mean)
            var = var/(w*h-1)
            self.assertEqual(getVariance(self.im8_1), var, "var %f %f" % (var,getVariance(self.im8_1)) )

