"""
Test cases for the image supremum mask creation function.

The function works with all image depths as input and puts the output in a binary
image.

Here is the list of legal operations :
    supmask( 1, 1) = 1
    supmask( 8, 8) = 1
    supmask(32,32) = 1
    
The result in output is a binary image where pixels are set to True if the 
corresponding pixel in the first input image is greater (strictly or not,
depending on a function parameter) than the pixel in the second input image.

Python function:
    generateSupMask
    
C function:
    MB_SupMask
"""

from mamba import *
import unittest
import random

class TestAnd(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im1s2_1 = imageMb(128,128,1)
        self.im1s2_2 = imageMb(128,128,1)
        self.im1s2_3 = imageMb(128,128,1)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im1s2_1)
        del(self.im1s2_2)
        del(self.im1s2_3)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        #self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im1_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im1_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im8_2, self.im1_1, 0)
        #self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im8_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im8_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im32_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im32_2, self.im1_1, 0)
        #self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im32_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im1_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im1_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im8_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im8_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im8_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im32_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im32_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im32_2, self.im8_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im1_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im1_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im8_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im8_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im8_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im32_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im8_3, self.im32_2, self.im32_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im32_3, self.im32_2, self.im32_1, 0)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1_2, self.im1s2_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1s2_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1_3, self.im1s2_2, self.im1s2_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1s2_3, self.im1_2, self.im1_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1s2_3, self.im1_2, self.im1s2_1, 0)
        self.assertRaises(MambaError, generateSupMask, self.im1s2_3, self.im1s2_2, self.im1_1, 0)

    def testComputation_1(self):
        """Computes the supremum mask on binary images"""
        (w,h) = self.im1_1.getSize()
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        
        drawSquare(self.im1_3,[0,0,w//2-1,h//2-1],1)
        drawSquare(self.im1_1,[w//2,0,w-1,h//2-1],1)
        drawSquare(self.im1_1,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_3,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[w//2,h//2,w-1,h-1],1)
        drawSquare(self.im1_3,[w//2,h//2,w-1,h-1],1)
        
        generateSupMask(self.im1_2, self.im1_1, self.im1_2, 0)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testComputationStrict_1(self):
        """Computes the supremum mask (strictly) on binary images"""
        (w,h) = self.im1_1.getSize()
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        
        drawSquare(self.im1_1,[w//2,0,w-1,h//2-1],1)
        drawSquare(self.im1_1,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[w//2,h//2,w-1,h-1],1)
        drawSquare(self.im1_3,[w//2,h//2,w-1,h-1],1)
        
        generateSupMask(self.im1_2, self.im1_1, self.im1_2, 1)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testComputation_8(self):
        """Computes the supremum mask on 8-bit images"""
        for i in range(100):
            self.im1_3.reset()
            v1 = random.randint(0, 255)
            v2 = random.randint(0, 255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            generateSupMask(self.im8_2, self.im8_1, self.im1_3, 0)
            self.im1_2.fill(v2>=v1 and 1 or 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0)

    def testComputationStrict_8(self):
        """Computes the supremum mask (strictly) on 8-bit images"""
        for i in range(100):
            self.im1_3.reset()
            v1 = random.randint(0, 255)
            v2 = random.randint(0, 255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            generateSupMask(self.im8_2, self.im8_1, self.im1_3, 1)
            self.im1_2.fill(v2>v1 and 1 or 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0)

    def testComputation_32(self):
        """Computes the supremum mask on 32-bit images"""
        for i in range(100):
            self.im1_3.reset()
            v1 = random.randint(0,500000)
            v2 = random.randint(0,500000)
            self.im32_1.fill(v1)
            self.im32_2.fill(v2)
            generateSupMask(self.im32_2, self.im32_1, self.im1_3, 0)
            self.im1_2.fill(v2>=v1 and 1 or 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0)

    def testComputationStrict_32(self):
        """Computes the supremum mask on 32-bit images"""
        for i in range(100):
            self.im1_3.reset()
            v1 = random.randint(0,500000)
            v2 = random.randint(0,500000)
            self.im32_1.fill(v1)
            self.im32_2.fill(v2)
            generateSupMask(self.im32_2, self.im32_1, self.im1_3, 1)
            self.im1_2.fill(v2>v1 and 1 or 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0)

