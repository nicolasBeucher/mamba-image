"""
Test cases for the image pixel value set and get functions.

The functions either return the value of a pixel inside the image or set it to
a given value.

Python functions:
    imageMb.getPixel
    imageMb.setPixel
    
C functions:
    MB_GetPixel
    MB_PutPixel
"""

from mamba import *
import unittest
import random

class TestPixel(unittest.TestCase):

    def setUp(self):
        self.im1 = imageMb(1)
        self.im8 = imageMb(8)
        self.im32 = imageMb(32)
        
    def tearDown(self):
        del(self.im1)
        del(self.im8)
        del(self.im32)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        (w,h) = self.im1.getSize()
        self.assertRaises(MambaError, self.im1.setPixel, 0, (w,h-1))
        self.assertRaises(MambaError, self.im1.setPixel, 0, (w,h))
        self.assertRaises(MambaError, self.im1.setPixel, 0, (w-1,h))
        self.assertRaises(MambaError, self.im1.getPixel, (w,h-1))
        self.assertRaises(MambaError, self.im1.getPixel, (w,h))
        self.assertRaises(MambaError, self.im1.getPixel, (w-1,h))
        self.assertRaises(MambaError, self.im8.setPixel, 0, (w,h-1))
        self.assertRaises(MambaError, self.im8.setPixel, 0, (w,h))
        self.assertRaises(MambaError, self.im8.setPixel, 0, (w-1,h))
        self.assertRaises(MambaError, self.im8.getPixel, (w,h-1))
        self.assertRaises(MambaError, self.im8.getPixel, (w,h))
        self.assertRaises(MambaError, self.im8.getPixel, (w-1,h))
        self.assertRaises(MambaError, self.im32.setPixel, 0, (w,h-1))
        self.assertRaises(MambaError, self.im32.setPixel, 0, (w,h))
        self.assertRaises(MambaError, self.im32.setPixel, 0, (w-1,h))
        self.assertRaises(MambaError, self.im32.getPixel, (w,h-1))
        self.assertRaises(MambaError, self.im32.getPixel, (w,h))
        self.assertRaises(MambaError, self.im32.getPixel, (w-1,h))

    def testPixel_1(self):
        """Tests the correct pixel manipulation in binary image"""
        (w,h) = self.im1.getSize()
        self.im1.reset()
        for wi in range(w):
            for hi in range(h):
                self.assertEqual(self.im1.getPixel((wi,hi)), 0)
                self.im1.setPixel(1, (wi,hi))
                self.assertEqual(self.im1.getPixel((wi,hi)), 1)
        self.im1.fill(1)
        for wi in range(w):
            for hi in range(h):
                self.assertEqual(self.im1.getPixel((wi,hi)), 1, "%d,%d" % (wi,hi))
                self.im1.setPixel(0, (wi,hi))
                self.assertEqual(self.im1.getPixel((wi,hi)), 0)

    def testPixel_8(self):
        """Tests the correct pixel manipulation in 8-bit image"""
        (w,h) = self.im8.getSize()
        self.im8.reset()
        for i in range(10):
            for wi in range(w):
                for hi in range(h):
                    vi = random.randint(0,255)
                    self.im8.setPixel(vi, (wi,hi))
                    self.assertEqual(self.im8.getPixel((wi,hi)), vi)

    def testPixel_32(self):
        """Tests the correct pixel manipulation in 32-bit image"""
        (w,h) = self.im32.getSize()
        self.im32.reset()
        for i in range(10):
            for wi in range(w):
                for hi in range(h):
                    vi = random.randint(0,0xffffffff)
                    self.im32.setPixel(vi, (wi,hi))
                    self.assertEqual(self.im32.getPixel((wi,hi)), vi)

