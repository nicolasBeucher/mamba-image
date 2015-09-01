"""
Test cases for the image depth conversion function.

The function works can perform all the possible conversion.
The function also acts as a copy function when the two given images (input
and output) have the same depth.

Here is the list of legal operations:
     8 -> 1
     1 -> 8
    32 -> 1
     1 -> 32
    32 -> 8 (downscaling)
     8 -> 32
     and copy :
     1 -> 1
     8 -> 8
    32 ->32
    
When converting from 8-bit/32-bit to binary, only the pixels that have a value
of 255/0xffffffff are set to true(1) in the binary image.
All the others are set to False(0). In the other way, binary to 8-bit/32-bit,
the True pixels are set to 255/0xffffffff and 0 for the False ones.
The 32bit to 8bit conversion is a downscaling and the 8-bit to 32-bit is
equivalent to copyBytePlane for plane 0.

Python function:
    convert
    imageMb.convert
    
C function:
    MB_Convert
"""

from mamba import *
import unittest
import random

class TestConvert(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im8s2_1 = imageMb(128,128,8)
        self.im1s2_1 = imageMb(128,128,1)
        
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
        del(self.im8s2_1)
        del(self.im1s2_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, convert, self.im8s2_1, self.im1_1)
        self.assertRaises(MambaError, convert, self.im8_1, self.im1s2_1)

    def testConversion_1_8(self):
        """Verifies that converting a binary image into an 8-bit image works fine"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.fill(1)
        self.im8_2.fill(255)
        convert(self.im1_1, self.im8_1)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im8_2.fill(0)
        convert(self.im1_1, self.im8_1)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im8_2.reset()
        for wi in range(w):
            for hi in range(h):
                if wi%2==0:
                    self.im1_1.setPixel(1, (wi,hi))
                    self.im8_2.setPixel(255, (wi,hi))
                else:
                    self.im1_1.setPixel(0, (wi,hi))
                    self.im8_2.setPixel(0, (wi,hi))
        convert(self.im1_1, self.im8_1)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        self.im1_1.convert(8)
        (x,y) = compare(self.im8_2, self.im1_1, self.im8_3)
        self.assertLess(x, 0)
        self.im1_1.convert(1)

    def testConversion_8_1(self):
        """Verifies that converting an 8-bit image into a binary image works fine"""
                
        for i in range(256):
            self.im8_1.fill(i)
            if i==255:
                self.im1_2.fill(1)
            else:
                self.im1_2.reset()
            convert(self.im8_1, self.im1_1)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0)
            self.im8_1.convert(1)
            (x,y) = compare(self.im8_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0)
            self.im8_1.convert(8)

        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-w//4, h//2-h//4, w//2+w//4, h//2+h//4), 255)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//2-w//4, h//2-h//4, w//2+w//4, h//2+h//4), 1)
        
        convert(self.im8_1, self.im1_1)
        (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testConversion_1_32(self):
        """Verifies that converting a binary image into an 32-bit image works fine"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.fill(1)
        self.im32_2.fill(0xffffffff)
        convert(self.im1_1, self.im32_1)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im32_2.fill(0)
        convert(self.im1_1, self.im32_1)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im32_2.reset()
        for wi in range(w):
            for hi in range(h):
                if wi%2==0:
                    self.im1_1.setPixel(1, (wi,hi))
                    self.im32_2.setPixel(0xffffffff, (wi,hi))
                else:
                    self.im1_1.setPixel(0, (wi,hi))
                    self.im32_2.setPixel(0, (wi,hi))
        convert(self.im1_1, self.im32_1)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        self.im1_1.convert(32)
        (x,y) = compare(self.im32_2, self.im1_1, self.im32_3)
        self.assertLess(x, 0)
        self.im1_1.convert(1)

    def testConversion_32_1(self):
        """Verifies that converting an 32-bit image into a binary image works fine"""
                
        for i in [0, 0x1000, 0x80000000, 0xfffffffe, 0xffffffff]:
            self.im32_1.fill(i)

            if i==0xffffffff:
                self.im1_2.fill(1)
            else:
                self.im1_2.reset()
            convert(self.im32_1, self.im1_1)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0)
            self.im32_1.convert(1)
            (x,y) = compare(self.im32_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0)
            self.im32_1.convert(32)

        (w,h) = self.im32_1.getSize()
        self.im32_1.reset()
        drawSquare(self.im32_1, (w//2-w//4, h//2-h//4, w//2+w//4, h//2+h//4), 0xffffffff)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//2-w//4, h//2-h//4, w//2+w//4, h//2+h//4), 1)
        
        convert(self.im32_1, self.im1_1)
        (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testConversion_32_8(self):
        """Verifies that converting an 32-bit image into a greyscale image works fine"""
        (w,h) = self.im32_1.getSize()
        self.im32_1.reset()
        drawSquare(self.im32_1, (w//3,0,(2*w)//3-1,h-1), 0x80000000)
        drawSquare(self.im32_1, ((w*2)//3,0,w-1,h-1), 0xffffffff)
        self.im8_2.reset()
        drawSquare(self.im8_2, (w//3,0,(2*w)//3-1,h-1), 127)
        drawSquare(self.im8_2, ((w*2)//3,0,w-1,h-1), 255)
        convert(self.im32_1, self.im8_1)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testConversion_8_32(self):
        """Verifies that converting an 8-bit image into a 32-bit image works fine"""
        (w,h) = self.im8_1.getSize()
        self.im32_2.reset()
        drawSquare(self.im32_2, (w//3,0,(2*w)//3-1,h-1), 127)
        drawSquare(self.im32_2, ((w*2)//3,0,w-1,h-1), 255)
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//3,0,(2*w)//3-1,h-1), 127)
        drawSquare(self.im8_1, ((w*2)//3,0,w-1,h-1), 255)
        convert(self.im8_1, self.im32_1)
        (x,y) = compare(self.im32_1, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

    def testComputation_1_1(self):
        """Verifies that converting a binary image into a binary image amounts to copy it"""
        self.im1_1.fill(1)
        convert(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        self.im1_1.reset()
        convert(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
    def testComputation_8_8(self):
        """Verifies that converting a 8-bit image into a 8-bit image amounts to copy it"""
        for i in range(100):
            vi = random.randint(0,255)
            self.im8_1.fill(vi)
            convert(self.im8_1, self.im8_2)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0)

    def testComputation_32_32(self):
        """Verifies that converting a 32-bit image into a 32-bit image amounts to copy it"""
        for i in range(100):
            vi = random.randint(1,0xffffffff)
            self.im32_1.fill(vi)
            convert(self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0)

