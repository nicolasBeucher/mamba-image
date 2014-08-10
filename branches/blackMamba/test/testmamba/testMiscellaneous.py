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
        
    def testMamba2PIL(self):
        """Verifies the conversion from a mamba image to a pil image"""
        self.im1_1.reset()
        self.im1_1.setPixel(1, (128,128))
        im1 = Mamba2PIL(self.im1_1)
        self.assertEqual(im1.mode, "L")
        self.assertEqual(im1.size, (256,256))
        self.assertEqual(im1.getpixel((127,128)), 0)
        self.assertEqual(im1.getpixel((128,128)), 255)
        
        self.im8_1.reset()
        self.im8_1.setPixel(128, (128,128))
        im8 = Mamba2PIL(self.im8_1)
        self.assertEqual(im8.mode, "L")
        self.assertEqual(im8.size, (256,256))
        self.assertEqual(im8.getpixel((128,129)), 0)
        self.assertEqual(im8.getpixel((128,128)), 128)
        
        self.im32_1.reset()
        self.im32_1.setPixel(0x80000000, (128,128))
        self.im32_1.setPixel(0xffffffff, (130,128))
        self.im32_1.setPixel(0x10000000, (132,128))
        im32 = Mamba2PIL(self.im32_1)
        self.assertEqual(im32.mode, "I")
        self.assertEqual(im32.size, (256,256))
        self.assertEqual(im32.getpixel((128,129)), 0)
        self.assertEqual(im32.getpixel((128,128)), -0x80000000)
        self.assertEqual(im32.getpixel((130,128)), -1)
        self.assertEqual(im32.getpixel((132,128)), 0x10000000)
        
    def testPIL2Mamba(self):
        """Verifies the conversion from a mamba image to a pil image"""
        im = Image.new("RGB", (256,256))
        im.putpixel((128,128), (128,128,128))
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 128)
        
        im = Image.new("RGBA", (256,256))
        im.putpixel((128,128), (127,127,127,255))
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 127)
        
        im = Image.new("CMYK", (256,256))
        im.putpixel((128,128), (17,17,17,0))
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 256*256*255-17)
        
        im = Image.new("1", (256,256))
        im.putpixel((128,128), 1)
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 255)
        PIL2Mamba(im, self.im1_1)
        v = computeVolume(self.im1_1)
        self.assertEqual(v, 1)
        
        im = Image.new("P", (256,256))
        im.putpixel((128,128), 245)
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 245)
        
        im = Image.new("L", (256,256))
        im.putpixel((138,128), 245)
        PIL2Mamba(im, self.im8_1)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 245)
        
        im = Image.new("I", (256,256))
        im.putpixel((128,128), -0x80000000)
        im.putpixel((130,128), -1)
        im.putpixel((132,128), 0x10000000)
        PIL2Mamba(im, self.im32_1)
        self.assertEqual(self.im32_1.getPixel((128,128)), 0x80000000)
        self.assertEqual(self.im32_1.getPixel((130,128)), 0xffffffff)
        self.assertEqual(self.im32_1.getPixel((132,128)), 0x10000000)
        
        im = Image.new("F", (256,256))
        im.putpixel((128,128), 3.51)
        im.putpixel((130,128), 4.001)
        im.putpixel((132,128), 1.6e6)
        PIL2Mamba(im, self.im32_1)
        self.assertEqual(self.im32_1.getPixel((128,128)), 3)
        self.assertEqual(self.im32_1.getPixel((130,128)), 4)
        self.assertEqual(self.im32_1.getPixel((132,128)), 1600000)
        
