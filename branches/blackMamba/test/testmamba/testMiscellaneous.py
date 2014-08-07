"""
Test cases for the various uncategorized functions found in the miscellaneous
module of mamba package.

Python functions:
    drawEdge
    multiSuperpose
    mix
    Mamba2PIL
    PIL2Mamba
"""

from mamba import *
import unittest
import random
from PIL import Image

class TestMiscellaneous(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im8s2_3 = imageMb(128,128,8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
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
        
    def testDrawEdge(self):
        """Verifies that the edge is correctly drawn"""
        (w,h) = self.im8_1.getSize()
        
        for thick in range(10):
            self.im8_1.reset()
            drawEdge(self.im8_1, thick)
            self.im8_3.fill(255)
            drawSquare(self.im8_3, (thick, thick, w-1-thick, h-1-thick), 0)
            (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
            self.assertLess(x, 0)

    def testMultiSuperpose(self):
        """Verifies the multisuperpose operator"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(100)

        self.im1_1.reset()
        drawLine(self.im1_1, (0,0,0,h-1), 1)
        self.im1_2.reset()
        drawLine(self.im1_2, (1,0,1,h-1), 1)

        self.im8_3.fill(98)
        drawLine(self.im8_3, (0,0,0,h-1), 254)
        drawLine(self.im8_3, (1,0,1,h-1), 255)

        multiSuperpose(self.im8_1, self.im1_1, self.im1_2)
        (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
        self.assertLess(x, 0)

    def testMixSplitDepthAcceptance(self):
        """Verifies that mix and split refuse non greyscale input images"""
        self.assertRaises(MambaError, mix, self.im8_1, self.im8_2, self.im32_3)
        self.assertRaises(MambaError, mix, self.im8_1, self.im32_2, self.im8_3)
        self.assertRaises(MambaError, mix, self.im1_1, self.im8_2, self.im8_3)
        pilim = Image.new("RGB", (256,256))
        self.assertRaises(MambaError, split, pilim, self.im8_1, self.im8_2, self.im32_3)
        self.assertRaises(MambaError, split, pilim, self.im8_1, self.im32_2, self.im8_3)
        self.assertRaises(MambaError, split, pilim, self.im1_1, self.im8_2, self.im8_3)
        
    def testMixSplitSizeAcceptance(self):
        """Verifies that mix and split control image size"""
        self.assertRaises(MambaError, mix, self.im8_1, self.im8_2, self.im8s2_3)
        self.assertRaises(MambaError, mix, self.im8_1, self.im8s2_2, self.im8_3)
        self.assertRaises(MambaError, mix, self.im8s2_1, self.im8_2, self.im8_3)
        pilim = Image.new("RGB", (256,256))
        self.assertRaises(MambaError, split, pilim, self.im8_1, self.im8_2, self.im8s2_3)
        self.assertRaises(MambaError, split, pilim, self.im8_1, self.im8s2_2, self.im8_3)
        self.assertRaises(MambaError, split, pilim, self.im8s2_1, self.im8_2, self.im8_3)

    def testMix(self):
        """Verifies the mix operator"""
        self.im8_1.fill(128)
        self.im8_2.fill(255)
        self.im8_3.fill(7)

        pilim = mix(self.im8_1, self.im8_2, self.im8_3)

        self.assertEqual(pilim.mode, "RGB")
        (r,g,b) = pilim.getpixel((0,0))
        self.assertEqual(r, 128)
        self.assertEqual(g, 255)
        self.assertEqual(b, 7)

    def testSplit(self):
        """Verifies the split operator"""
        pilim = Image.new("RGB", (270, 270), 0)
        pilim.putpixel((0,0), (127,254,8))

        split(pilim, self.im8_1, self.im8_2, self.im8_3)

        v = computeVolume(self.im8_1)
        self.assertEqual(v, 127)
        v = computeVolume(self.im8_2)
        self.assertEqual(v, 254)
        v = computeVolume(self.im8_3)
        self.assertEqual(v, 8)
