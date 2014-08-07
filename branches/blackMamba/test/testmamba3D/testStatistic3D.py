"""
Test cases for the statistic functions found in the statistic3D module of
mamba3D package. 

Python functions:
    getHistogram3D
    getMean3D
    getMedian3D
    getVariance3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestStatistic3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,64,8)
        self.im8_2 = image3DMb(64,64,64,8)
        self.im8_3 = image3DMb(64,64,64,8)
        self.im8_4 = image3DMb(64,64,64,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(64,64,64,32)
        self.im32_2 = image3DMb(64,64,64,32)
        self.im32_3 = image3DMb(64,64,64,32)
        self.im32_4 = image3DMb(64,64,64,32)
        self.im32_5 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im1_5)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)
        
    def _drawValueByPlane(self, im):
        im.reset()
        for i,im2D in enumerate(im):
            im2D.fill(i)
        
    def testGetHistogram3D(self):
        """Verifies the computation of the histogram on 3D images"""
        (w,h,l) = self.im8_1.getSize()
        self._drawValueByPlane(self.im8_1)
        histo = getHistogram3D(self.im8_1)
        for i in range(64):
            self.assertEqual(histo[i], w*h,"%d : %d!=%d" %(i,histo[i],w*h))
        
    def testGetMean3D(self):
        """Verifies the correct computation of pixel mean value in 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        # creating a random image
        s = 0
        for wi in range(w):
            for hi in range(h):
                for li in range(l):
                    vi = random.randint(0,255)
                    self.im8_1.setPixel(vi, (wi,hi,li))
                    s += vi
                    
        exp_mean = float(s)/(l*h*w)
        mean = getMean3D(self.im8_1)
        self.assertEqual(exp_mean, mean, "%f!=%f" % (mean,exp_mean))
        
    def testGetMedian3D(self):
        """Verifies the correct computation of pixel median value in 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        # creating a random image
        his = 256*[0]
        for wi in range(w):
            for hi in range(h):
                for li in range(l):
                    vi = random.randint(0,255)
                    self.im8_1.setPixel(vi, (wi,hi,li))
                    his[vi] += 1
                    
        i = 0;
        n = 0
        while n<(l*h*w)//2 and i<256:
            n += his[i]
            i += 1
        exp_median = i-1
        median = getMedian3D(self.im8_1)
        self.assertEqual(exp_median, median, "%d!=%d" % (median,exp_median))
        
    def testGetVariance3D(self):
        """Verifies the correct computation of the variance value of a 3D image"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(2):
            lis = 256*[0]
            s = 0
            # creating a random image
            for li in range(l):
                vi = random.randint(0,255)
                self.im8_1[li].fill(vi)
                lis[vi] += h*w
                s += (w*h*vi)
            mean = (float(s)/float(l*w*h))
            var = 0
            for i in range(256):
                var += lis[i]*(i-mean)*(i-mean)
            var = var/(l*w*h-1)
            self.assertEqual(getVariance3D(self.im8_1), var, "var %f %f" % (var,getVariance3D(self.im8_1)) )

