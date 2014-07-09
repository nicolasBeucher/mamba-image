"""
Test cases for the frame extraction function

The function works with all depths.

The function returns four values that are coordinates of a window inside the
input image containing all the pixels that are greater or equal to the given
parameter.
    
Python function:
    extractFrame
    
C function:
    MB_Frame
"""

from mamba import *
import unittest
import random

class TestFrame(unittest.TestCase):

    def setUp(self):
        # Creating images 
        self.im1 = imageMb(1)
        self.im8 = imageMb(8)
        self.im32 = imageMb(32)
        
    def tearDown(self):
        del(self.im1)
        del(self.im8)
        del(self.im32)

    def testComputation_1(self):
        """Computes the containing frame of a binary image"""
        (w,h) = self.im1.getSize()
        self.im1.reset()
        (x1,y1,x2,y2) = extractFrame(self.im1,0)
        self.assertGreater(x1, x2)
        
        for i in range(100):
            self.im1.reset()
            w1 = random.randint(0,w-1)
            h1 = random.randint(0,h-1)
            w2 = random.randint(0,w-1)
            h2 = random.randint(0,h-1)
            self.im1.setPixel(1, (w1,h1))
            self.im1.setPixel(1, (w2,h2))
            (x1,y1,x2,y2) = extractFrame(self.im1,0)
            self.assertTrue(x1==min(w1,w2) and x2==max(w1,w2) and y1==min(h1,h2) and y2==max(h1,h2))

    def testComputation_8(self):
        """Computes the containing frame of a 8-bit image"""
        (w,h) = self.im8.getSize()
        self.im8.reset()
        (x1,y1,x2,y2) = extractFrame(self.im8,1)
        self.assertGreater(x1, x2)
        self.im8.reset()
        (x1,y1,x2,y2) = extractFrame(self.im8,0)
        self.assertTrue(x1==0 and x2==(w-1) and y1==0 and y2==(h-1))
        
        for i in range(10):
            self.im8.reset()
            for vi in range(1,256):
                w1 = random.randint(0,w-1)
                h1 = random.randint(0,h-1)
                w2 = random.randint(0,w-1)
                h2 = random.randint(0,h-1)
                self.im8.setPixel(vi, (w1,h1))
                self.im8.setPixel(vi, (w2,h2))
                (x1,y1,x2,y2) = extractFrame(self.im8,vi)
                self.assertTrue(x1==min(w1,w2) and x2==max(w1,w2) and y1==min(h1,h2) and y2==max(h1,h2),
                             "%d : 1-[%d,%d] 2-[%d,%d] : %d,%d,%d,%d" % (vi,w1,h1,w2,h2,x1,y1,x2,y2)
                            )

    def testComputation_32(self):
        """Computes the containing frame of a 32-bit image"""
        (w,h) = self.im32.getSize()
        self.im32.reset()
        (x1,y1,x2,y2) = extractFrame(self.im32,1)
        self.assertGreater(x1, x2)
        self.im32.reset()
        (x1,y1,x2,y2) = extractFrame(self.im32,0)
        self.assertTrue(x1==0 and x2==(w-1) and y1==0 and y2==(h-1))
        
        for i in range(10):
            self.im32.fill(0)
            for vi in range(1,2500):
                w1 = random.randint(0,w-1)
                h1 = random.randint(0,h-1)
                w2 = random.randint(0,w-1)
                h2 = random.randint(0,h-1)
                self.im32.setPixel(vi, (w1,h1))
                self.im32.setPixel(vi, (w2,h2))
                (x1,y1,x2,y2) = extractFrame(self.im32,vi)
                self.assertTrue(x1==min(w1,w2) and x2==max(w1,w2) and y1==min(h1,h2) and y2==max(h1,h2),
                             "%d : 1-[%d,%d] 2-[%d,%d] : %d,%d,%d,%d" % (vi,w1,h1,w2,h2,x1,y1,x2,y2)
                            )

