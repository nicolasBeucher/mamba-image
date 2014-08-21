"""
Test cases for the base class and functions found in the base3D module of
mamba3D package.

Python classes:
    image3DMb
    sequenceMb
"""

from mamba import *
from mamba3D import *
import unittest
import random
import os
import shutil
import glob
from PIL import Image

class TestBase3D(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        files = glob.glob("./[0-9][0-9][0-9].*")
        for f in files:
            os.remove(f)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        im1 = image3DMb(128,128,16,1)
        rawData = (128*128*2)*b"\x00"
        self.assertRaises(MambaError,im1.loadRaw,rawData)
        self.assertRaises(MambaError,im1.extractRaw)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        im1 = image3DMb()
        (w,h,l) = im1.getSize()
        self.assertRaises(MambaError,im1.setPixel,0,(0,0,-1))
        self.assertRaises(MambaError,im1.setPixel,0,(0,0,l))
        self.assertRaises(MambaError,im1.getPixel,(0,0,-1))
        self.assertRaises(MambaError,im1.getPixel,(0,0,l))
        
    def testImage3DMbConstructor(self):
        """Verifies the image3DMb class constructor"""
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(10,25)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        
        for i in range(li):
            ci = random.randint(0,255)
            # Creating an image and saving it
            Image.new("RGB", (wi,hi), (ci,ci,ci)).save("%03d.jpg" % (i))
        
        # first case
        im = image3DMb()
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (256,256,256))
        self.assertEqual(len(im), 256)
        self.assertNotEqual(im.getName(), '')
        self.assertEqual(str(im), 'Mamba 3D image object : '+im.getName()+' - 8')
        self.assertIsInstance(next(im), imageMb)
        self.assertIsInstance(im.__next__(), imageMb)
        self.assertTrue(isinstance(im, image3DMb))
        # third case
        im2D = imageMb(wi,hi,1)
        im = image3DMb(im2D)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc,256))
        self.assertEqual(len(im), 256)
        # second case
        im2 = image3DMb(im)
        self.assertEqual(im2.getDepth(), 1)
        self.assertEqual(im2.getSize(), (wc,hc,256))
        self.assertEqual(len(im2), 256)
        # fourth case
        im = image3DMb(32)
        self.assertEqual(im.getDepth(), 32)
        self.assertEqual(im.getSize(), (256,256,256))
        self.assertEqual(len(im), 256)
        # fifth case
        im = image3DMb(".")
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc,li))
        self.assertEqual(len(im), li)
        self.assertEqual(im.getName(), ".")
        # sixth case
        im2 = image3DMb(im, 32)
        self.assertEqual(im2.getDepth(), 32)
        self.assertEqual(im2.getSize(), (wc,hc,li))
        self.assertEqual(len(im2), li)
        # seventh case
        im = image3DMb(im2D, li)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc,li))
        self.assertEqual(len(im), li)
        # eighth case
        im = image3DMb(".", 1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc,li))
        self.assertEqual(len(im), li)
        # ninth case
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(10,45)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        im = image3DMb(wi, hi, li)
        self.assertEqual(im.getDepth(), 8)
        self.assertEqual(im.getSize(), (wc,hc,li), "%s %s" % (im.getSize(), (wc,hc,li)))
        self.assertEqual(len(im), li)
        # tenth case
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(10,45)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        im = image3DMb(wi, hi, li, 1)
        self.assertEqual(im.getDepth(), 1)
        self.assertEqual(im.getSize(), (wc,hc,li))
        self.assertEqual(len(im), li)
        
        seq = sequenceMb(wi, hi, li, 1)
        self.assertEqual(seq.getDepth(), 1)
        self.assertEqual(seq.getSize(), (wc,hc,li))
        
    def testImage3DMbPixels(self):
        """Verifies pixel extraction and setting in 3D images"""
        im1 = image3DMb()
        im2 = image3DMb(1)
        (w,h,l) = im1.getSize()
        
        for i in range(100):
            im1.reset()
            im2.reset()
            
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            zi = random.randint(0,l-1)
            vi = random.randint(0,255)
            
            im1.setPixel(vi, (xi,yi,zi))
            vol = computeVolume3D(im1)
            self.assertEqual(vol, vi)
            v = im1.getPixel((xi,yi,zi))
            self.assertEqual(v, vi)
            
            im2.setPixel(1, (xi,yi,zi))
            vol = computeVolume3D(im2)
            self.assertEqual(vol, 1)
            v = im2.getPixel((xi,yi,zi))
            self.assertEqual(v, 1)
            
    def _preprocfunc(self, data):
        return len(data)*b"\x22"
            
    def testLoadRaw3D(self):
        """Ensures that the load raw method works correctly in 3D"""
        im8 = image3DMb(64,64,4,8)
        im32 = image3DMb(64,64,4,32)
        f = open("test.dat","wb")
        f.write((64*64*4-1)*b"\x11")
        f.close()
        self.assertRaises(AssertionError, im8.loadRaw, "test.dat")
        f = open("test.dat","wb")
        f.write(64*64*4*b"\x11")
        f.close()
        im8.loadRaw("test.dat")
        vol = computeVolume3D(im8)
        self.assertEqual(vol,  64*64*4*0x11)
        f = open("test.dat","wb")
        f.write(64*64*4*b"\x12")
        f.close()
        im8.loadRaw("test.dat", preprocfunc=self._preprocfunc)
        vol = computeVolume3D(im8)
        self.assertEqual(vol,  64*64*4*0x22)
        f = open("test.dat","wb")
        f.write((64*64*4-1)*b"\x11\x00\x00\x00")
        f.close()
        self.assertRaises(AssertionError, im32.loadRaw, "test.dat")
        f = open("test.dat","wb")
        f.write(64*64*4*b"\x11\x00\x00\x00")
        f.close()
        im32.loadRaw("test.dat")
        vol = computeVolume3D(im32)
        self.assertEqual(vol,  64*64*4*0x11, "32: %d,%d" %(vol,128*128*0x11))
        
        os.remove("test.dat")
        
    def testExtractRaw(self):
        """Ensures that the extract raw method works properly in 3D"""
        im8 = image3DMb(64,64,6,8)
        im32 = image3DMb(64,64,6,32)
        im8.fill(0x11)
        rawdata = im8.extractRaw()
        self.assertEqual(len(rawdata), 64*64*6)
        self.assertEqual(rawdata, 64*64*6*b"\x11")
        im32.fill(0x11223344)
        rawdata = im32.extractRaw()
        self.assertEqual(len(rawdata), 64*64*6*4)
        self.assertEqual(rawdata, 64*64*6*b"\x44\x33\x22\x11")
        
    def testImage3DMbLoad(self):
        """Verifies the loading method of the image3DMb class"""
        im = image3DMb(256,256,9,8)
        
        li = random.randint(10,15)
        ci = []
        for i in range(li):
            ci.append(random.randint(0,255))
            # Creating an image and saving it
            Image.new("RGB", (256,256), (ci[-1],ci[-1],ci[-1])).save("%03d.jpg" % (i))
            
        im.load(".")
        for i,im in enumerate(im):
            vol = computeVolume(im)
            self.assertEqual(vol, ci[i]*256*256)

    def testImage3DMbSave(self):
        """Verifies the saving method of the image3DMb class"""
        im3D = image3DMb(256,256,9,8)
        
        ci = []
        for im in im3D:
            ci.append(random.randint(0,255))
            im.fill(ci[-1])
        im3D.save("test", ".bmp")
        
        im2 = image3DMb("test")
        for i,im in enumerate(im2):
            vol = computeVolume(im)
            self.assertEqual(vol, 256*256*ci[i])
            
        im3D.save("test", ".bmp")
        
        im2 = image3DMb("test")
        for i,im in enumerate(im2):
            vol = computeVolume(im)
            self.assertEqual(vol, 256*256*ci[i])
        
        shutil.rmtree("test")
            
    def testImage3DMbRGBFilter(self):
        """Verifies that the RGB filtering used when loading sequence works"""
        ri = random.randint(0,255)
        gi = random.randint(0,255)
        bi = random.randint(0,255)
        w = 256
        h = 256
        
        for i in range(5):
            # Creating an image and saving it
            Image.new("RGB", (w,h), (ri,gi,bi)).save("%03d.bmp" % (i))
            
        im3D = image3DMb(".", rgbfilter=(1.0,0.0,0.0))
        for i,im in enumerate(im3D):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*ri or vol==w*h*(ri-1) or vol==w*h*(ri+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
        im3D = image3DMb(".", rgbfilter=(0.0,1.0,0.0))
        for i,im in enumerate(im3D):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*gi or vol==w*h*(gi-1) or vol==w*h*(gi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
        im3D = image3DMb(".", rgbfilter=(0.0,0.0,1.0))
        for i,im in enumerate(im3D):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*bi or vol==w*h*(bi-1) or vol==w*h*(bi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
    def testImage3DMbFillAndReset(self):
        """Verifies the fill and reset methods of the image3DMb class"""
        im3D = image3DMb(256,256,9,8)
        
        ci = random.randint(0,255)
        
        im3D.fill(ci)
        for im in im3D:
            vol = computeVolume(im)
            self.assertEqual(vol, ci*256*256)
        im3D.reset()
        for im in im3D:
            vol = computeVolume(im)
            self.assertEqual(vol, 0)
        
    def testImageNaming(self):
        """Verifies that image names methods are correctly working"""
        im3D = image3DMb(64,64,9,8)
        nb = random.randint(-10000, -1000)
        im3D.setName("test %d" % (nb))
        self.assertEqual(im3D.getName(), "test %d" % (nb))

