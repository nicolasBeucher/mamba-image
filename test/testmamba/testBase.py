"""
Test cases for the image creation (base module).
    
Python function:
    imageMb   class constructor
    imageMb.getSize
    imageMb.getDepth
    imageMb.setName
    imageMb.getName
    imageMb.load
    imageMb.save
    imageMb.loadRaw
    imageMb.extractRaw
    setImageIndex
    getImageCounter
    
C function:
    MB_Create
    MB_Load
    MB_Extract
"""

from mamba import *
import mambaDisplay
import mamba.core as core
import unittest
from PIL import Image
import random
import os

class TestCreate(unittest.TestCase):

    def testAcceptedSize(self):
        """Verifies that requests for too large or too small ones are refused"""
        self.assertRaises(MambaError, imageMb, 0,0)
        self.assertRaises(MambaError, imageMb, 65536, 65537)
        self.assertRaises(MambaError, imageMb, 0xFFFFFFFF,2)

    def testAcceptedDepth(self):
        """Verifies that request for incorrect depth is refused"""
        for i in range(100):
            if i!=1 and i!=8 and i!=32:
                self.assertRaises(MambaError, imageMb, i)
        im1 = imageMb(128,128,1)
        self.assertRaises(MambaError, im1.extractRaw)
        self.assertRaises(MambaError, im1.loadRaw, 128*16*b"\x00")
        
    def testSizeDepthParameters(self):
        """Verifies that the size and depth given are correctly handled"""
        for i in range(100):
            wi = random.randint(1,4000)
            hi = random.randint(1,4000)
            wc = ((wi+63)//64)*64
            hc = ((hi+1)//2)*2
            im1 = imageMb(wi,hi,1)
            im8 = imageMb(wi,hi,8)
            im32 = imageMb(wi,hi,32)
            self.assertEqual(im1.getDepth(), 1)
            self.assertEqual(im1.getSize(), (wc,hc), "%s : %d,%d" %(str(im1.getSize()), wc, hc))
            self.assertEqual(im8.getDepth(), 8)
            self.assertEqual(im8.getSize(), (wc,hc))
            self.assertEqual(im32.getDepth(), 32)
            self.assertEqual(im32.getSize(), (wc,hc))
            
    def testConstructor(self):
        """Verifies that imageMb constructor works correctly"""
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        ci = random.randint(0,255)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        imref = imageMb(wi,hi,1)
        # Creating an image and saving it
        Image.new("RGB", (wi,hi), (ci,ci,ci)).save("test.jpg")
        
        im = imageMb()
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (256,256))
        im = imageMb(imref)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (256,256))
        im = imageMb(8)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (256,256))
        im = imageMb(32)
        self.assertEqual(im.getDepth(), 32)
        self.assertEqual(im.getSize(), (256,256))
        im = imageMb("test.jpg")
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(imref, 1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(imref, 8)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(imref, 32)
        self.assertEqual(im.getDepth(), 32)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb("test.jpg", 1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb("test.jpg", 8)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb("test.jpg", 32)
        self.assertEqual(im.getDepth(), 32)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(wi,hi)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(wi,hi,1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(wi,hi,8)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc))
        im = imageMb(wi,hi,32)
        self.assertEqual(im.getDepth(), 32)
        self.assertEqual(im.getSize(), (wc,hc))
        
        os.remove("test.jpg")
        
        self.assertEqual(getImageCounter(), 2)
        del(im)
        self.assertEqual(getImageCounter(), 1)
        del(imref)
        self.assertEqual(getImageCounter(), 0)

    def testLoad(self):
        """Ensures that the load method works properly"""
        for i in range(5):
            wi = random.randint(1,4000)
            hi = random.randint(1,4000)
            ci = random.randint(0,255)
            wc = ((wi+63)//64)*64
            hc = ((hi+1)//2)*2
            # Creating an image and saving it
            Image.new("RGB", (wi,hi), (ci,ci,ci)).save("test.jpg")
            im = imageMb("test.jpg")
            self.assertEqual(im.getSize(), (wc,hc), "%s : %d,%d" %(str(im.getSize()), wc, hc))
            vol = computeVolume(im)
            self.assertEqual(vol, ci*wi*hi)
            os.remove("test.jpg")
            
            ci = random.randint(0,255)
            # Creating an image and saving it
            Image.new("RGB", (wi,hi), (ci,ci,ci)).save("test.jpg")
            im.load("test.jpg")
            vol = computeVolume(im)
            self.assertEqual(vol, ci*wi*hi)
            im1 = imageMb(wi,hi,1)
            im1.load("test.jpg")
            self.assertEqual(im1.getDepth(), 1)
            im32 = imageMb(wi,hi,32)
            im32.load("test.jpg")
            vol = computeVolume(im32)
            self.assertEqual(vol, ci*wi*hi)
            os.remove("test.jpg")
            
            del(im)
            
    def testSave(self):
        """Ensures that the save method works properly"""
        for i in range(5):
            wi = random.randint(1,4000)
            hi = random.randint(1,4000)
            wc = ((wi+63)//64)*64
            hc = ((hi+1)//2)*2
            im1 = imageMb(wi,hi,1)
            im8 = imageMb(wi,hi,8)
            im32 = imageMb(wi,hi,32)
            im1.save("test1.jpg")
            os.remove("test1.jpg")
            im8.save("test8.jpg")
            os.remove("test8.jpg")
            im32.save("test32.tif")
            os.remove("test32.tif")
        im8.save("test8.jpg", palette=mambaDisplay.getPalette("rainbow"))
        os.remove("test8.jpg")
            
    def testLoadRaw(self):
        """Ensures that the load raw method works correctly"""
        im8 = imageMb(128,128,8)
        im32 = imageMb(128,128,32)
        rawdata = 128*128*b"\x11"
        self.assertRaises(AssertionError, im8.loadRaw, rawdata[1:])
        im8.loadRaw(rawdata)
        vol = computeVolume(im8)
        self.assertEqual(vol, 128*128*0x11)
        rawdata = 128*128*b"\x11\x00\x00\x00"
        self.assertRaises(AssertionError, im32.loadRaw, rawdata[1:])
        im32.loadRaw(rawdata)
        vol = computeVolume(im32)
        self.assertEqual(vol, 128*128*0x11, "32: %d,%d" %(vol,128*128*0x11))
            
    def _preprocfunc(self, data):
        return len(data)*b"\x22"
        
    def testLoadRawFile(self):
        """Ensures that the load raw method works correctly"""
        im8 = imageMb(64,64,8)
        f = open("test.dat","wb")
        f.write(64*64*b"\x12")
        f.close()
        im8.loadRaw("test.dat", preprocfunc=self._preprocfunc)
        vol = computeVolume(im8)
        self.assertEqual(vol, 64*64*0x22)
        os.remove("test.dat")
        
    def testExtractRaw(self):
        """Ensures that the extract raw method works properly"""
        im8 = imageMb(128,128,8)
        im32 = imageMb(128,128,32)
        im8.fill(0x11)
        rawdata = im8.extractRaw()
        self.assertEqual(len(rawdata), 128*128)
        self.assertEqual(rawdata, 128*128*b"\x11")
        im32.fill(0x11223344)
        rawdata = im32.extractRaw()
        self.assertEqual(len(rawdata), 128*128*4)
        self.assertEqual(rawdata, 128*128*b"\x44\x33\x22\x11")
        
    def testImageNaming(self):
        """Verifies that image names methods are correctly working"""
        im8 = imageMb(128,128,8)
        nb = random.randint(-10000, -1000)
        im8.setName("test %d" % (nb))
        self.assertEqual(im8.getName(), "test %d" % (nb))
        
        setImageIndex(nb)
        im = imageMb()
        self.assertEqual(im.getName(), "Image %d" % (nb))
        im = imageMb()
        self.assertEqual(im.getName(), "Image %d" % (nb+1))
        
        self.assertNotEqual(str(im), "")
        
    def testRGBFilter(self):
        """Verifies that the RGB filtering used when loading image works"""
        imref = imageMb()
        (w,h) = imref.getSize()
        
        for i in range(20):
            ri = random.randint(0,255)
            gi = random.randint(0,255)
            bi = random.randint(0,255)
            
            # Creates an image and saving it
            Image.new("RGB", (w,h), (ri,gi,bi)).save("test.bmp")
            
            im = imageMb("test.bmp", rgbfilter=(1.0,0.0,0.0))
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*ri or vol==w*h*(ri-1) or vol==w*h*(ri+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
            im = imageMb("test.bmp", rgbfilter=(0.0,1.0,0.0))
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*gi or vol==w*h*(gi-1) or vol==w*h*(gi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
            im = imageMb("test.bmp", rgbfilter=(0.0,0.0,1.0))
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*bi or vol==w*h*(bi-1) or vol==w*h*(bi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
            os.remove("test.bmp")

