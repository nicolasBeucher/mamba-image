"""
Test cases for the image histogram extraction function

The function works only with 8-bit images.

The function returns a list containing 256 values representing the histogram of
the input image.

Python function:
    getHistogram
    
C function:
    MB_Histo
"""

from mamba import *
import unittest
import random

class TestHisto(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        self.im1 = imageMb(1)
        self.im8 = imageMb(8)
        self.im32 = imageMb(32)
        
    def tearDown(self):
        del(self.im1)
        del(self.im8)
        del(self.im32)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, getHistogram, self.im32)
        self.assertRaises(MambaError, getHistogram, self.im1)

    def testComputation_8(self):
        """Tests the result of two binary images added into a third one"""
        (w,h) = self.im8.getSize()
        
        for i in range(20):
            exp_histo = 256*[0]
            for wi in range(w):
                for hi in range(h):
                    vi = random.randint(0,255)
                    self.im8.setPixel(vi, (wi,hi))
                    exp_histo[vi] = exp_histo[vi]+1
            obt_histo = getHistogram(self.im8)
            self.assertEqual(len(obt_histo), 256)
            self.assertEqual(obt_histo, exp_histo)

