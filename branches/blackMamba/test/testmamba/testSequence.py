"""
Test cases for the sequence classes and fonctions found in the sequence module
of mamba package.

Python functions and classes:
    sequenceMb:
    copySequence
    erodeByCylinderSequence
    dilateByCylinderSequence
    openByCylinderSequence
    closeByCylinderSequence
"""

from mamba import *
import unittest
from PIL import Image
import random
import os
import shutil
import glob

class TestSequence(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        files = glob.glob("./[0-9][0-9][0-9].*")
        for f in files:
            os.remove(f)
            
    def testSequenceMbConstructor(self):
        """Verifies the sequenceMb class constructor"""
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
        seq = sequenceMb()
        self.assertEqual(seq.getDepth(), 8)
        self.assertEqual(seq.getSize(), (256,256))
        self.assertEqual(seq.getLength(), 256)
        self.assertEqual(len(seq), 256)
        self.assertEqual(seq.getName(), "Mamba image sequence")
        self.assertEqual(str(seq), 'Mamba sequence object : Mamba image sequence - 8')
        self.assertIsInstance(next(seq), imageMb)
        self.assertIsInstance(seq.__next__(), imageMb)
        # third case
        im = imageMb(wi,hi,1)
        seq = sequenceMb(im)
        self.assertEqual(seq.getDepth(), 1)
        self.assertEqual(seq.getSize(), (wc,hc))
        self.assertEqual(seq.getLength(), 256)
        self.assertEqual(len(seq), 256)
        # second case
        seq2 = sequenceMb(seq)
        self.assertEqual(seq2.getDepth(), 1)
        self.assertEqual(seq2.getSize(), (wc,hc))
        self.assertEqual(seq2.getLength(), 256)
        self.assertEqual(len(seq2), 256)
        # fourth case
        seq = sequenceMb(32)
        self.assertEqual(seq.getDepth(), 32)
        self.assertEqual(seq.getSize(), (256,256))
        self.assertEqual(seq.getLength(), 256)
        self.assertEqual(len(seq), 256)
        # fifth case
        seq = sequenceMb(".")
        self.assertEqual(seq.getDepth(), 8)
        self.assertEqual(seq.getSize(), (wc,hc))
        self.assertEqual(seq.getLength(), li)
        self.assertEqual(len(seq), li)
        self.assertEqual(seq.getName(), ".")
        # sixth case
        seq2 = sequenceMb(seq, 32)
        self.assertEqual(seq2.getDepth(), 32)
        self.assertEqual(seq2.getSize(), (wc,hc))
        self.assertEqual(seq2.getLength(), li)
        self.assertEqual(len(seq2), li)
        # seventh case
        im = imageMb(wi,hi,1)
        seq = sequenceMb(im, li)
        self.assertEqual(seq.getDepth(), 1)
        self.assertEqual(seq.getSize(), (wc,hc))
        self.assertEqual(seq.getLength(), li)
        self.assertEqual(len(seq), li)
        # height case
        seq = sequenceMb(".", 1)
        self.assertEqual(seq.getDepth(), 1)
        self.assertEqual(seq.getSize(), (wc,hc))
        self.assertEqual(seq.getLength(), li)
        self.assertEqual(len(seq), li)
        # ninth case
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(10,45)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        seq = sequenceMb(wi, hi, li)
        self.assertEqual(seq.getDepth(), 8)
        self.assertEqual(seq.getSize(), (wc,hc), "%s %s" % (seq.getSize(), (wc,hc)))
        self.assertEqual(seq.getLength(), li)
        self.assertEqual(len(seq), li)
        # tenth case
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(10,45)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        seq = sequenceMb(wi, hi, li, 1)
        self.assertEqual(seq.getDepth(), 1)
        self.assertEqual(seq.getSize(), (wc,hc))
        self.assertEqual(seq.getLength(), li)
        self.assertEqual(len(seq), li)

    def testSequenceMbLoad(self):
        """Verifies the loading method of the sequenceMb class"""
        seq = sequenceMb(256,256,9,8)
        
        li = random.randint(10,15)
        ci = []
        for i in range(li):
            ci.append(random.randint(0,255))
            # Creating an image and saving it
            Image.new("RGB", (256,256), (ci[-1],ci[-1],ci[-1])).save("%03d.jpg" % (i))
            
        seq.load(".")
        for i,im in enumerate(seq):
            vol = computeVolume(im)
            self.assertEqual(vol, ci[i]*256*256)

    def testSequenceMbSave(self):
        """Verifies the saving method of the sequenceMb class"""
        seq = sequenceMb(256,256,9,8)
        
        ci = []
        for im in seq:
            ci.append(random.randint(0,255))
            im.fill(ci[-1])
        seq.save("test", ".bmp")
        
        seq2 = sequenceMb("test")
        for i,im in enumerate(seq2):
            vol = computeVolume(im)
            self.assertEqual(vol, 256*256*ci[i])
            
        seq.save("test", ".bmp")
        
        seq2 = sequenceMb("test")
        for i,im in enumerate(seq2):
            vol = computeVolume(im)
            self.assertEqual(vol, 256*256*ci[i])
        
        shutil.rmtree("test")
            
    def testSequenceRGBFilter(self):
        """Verifies that the RGB filtering used when loading sequence works"""
        ri = random.randint(0,255)
        gi = random.randint(0,255)
        bi = random.randint(0,255)
        w = 256
        h = 256
        
        for i in range(5):
            # Creating an image and saving it
            Image.new("RGB", (w,h), (ri,gi,bi)).save("%03d.bmp" % (i))
            
        seq = sequenceMb(".", rgbfilter=(1.0,0.0,0.0))
        for i,im in enumerate(seq):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*ri or vol==w*h*(ri-1) or vol==w*h*(ri+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
        seq = sequenceMb(".", rgbfilter=(0.0,1.0,0.0))
        for i,im in enumerate(seq):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*gi or vol==w*h*(gi-1) or vol==w*h*(gi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
        seq = sequenceMb(".", rgbfilter=(0.0,0.0,1.0))
        for i,im in enumerate(seq):
            vol = computeVolume(im)
            self.assertTrue(vol==w*h*bi or vol==w*h*(bi-1) or vol==w*h*(bi+1),
                         "%d %d %d %d %d" %(vol, ri, gi, bi, im.getPixel((0,0))) )
            
    def testSequenceMbFillAndReset(self):
        """Verifies the fill and reset methods of the sequenceMb class"""
        seq = sequenceMb(256,256,9,8)
        
        ci = random.randint(0,255)
        
        seq.fill(ci)
        for im in seq:
            vol = computeVolume(im)
            self.assertEqual(vol, ci*256*256)
        seq.reset()
        for im in seq:
            vol = computeVolume(im)
            self.assertEqual(vol, 0)
            
    def testSequenceMbPalette(self):
        """Verifies the palette methods of the sequenceMb class"""
        seq = sequenceMb(256,256,9,8)
        seq.setPalette(rainbow)
        seq.resetPalette()
    
    def testCopySequenceProtection(self):
        """Verifies that the sequence copy raises errors properly"""
        seq1 = sequenceMb(256,256,9,8)
        seq2 = sequenceMb(320,256,9,8)
        self.assertRaises(MambaError, copySequence, seq1, seq2)
        seq1 = sequenceMb(256,256,9,8)
        seq2 = sequenceMb(256,256,9,1)
        self.assertRaises(MambaError, copySequence, seq1, seq2)
        
    def testCopySequence(self):
        """Verifies the sequence copy"""
        wi = random.randint(1,4000)
        hi = random.randint(1,4000)
        li = random.randint(5,15)
        wc = ((wi+63)//64)*64
        hc = ((hi+1)//2)*2
        
        ci = []
        for i in range(li):
            ci.append(random.randint(0,255))
            # Creating an image and saving it
            Image.new("RGB", (wi,hi), (ci[-1],ci[-1],ci[-1])).save("%03d.jpg" % (i))
        seq1 = sequenceMb(".")
        seq2 = sequenceMb(wi,hi,li+10)
        copySequence(seq1, seq2)
        for i in range(li):
            im = seq2[i]
            vol = computeVolume(im)
            self.assertEqual(vol, ci[i]*wi*hi, "%d: %d!=%d, %d %d %d" % (i,vol,ci[i]*wi*hi,ci[i],wi,hi))
        for i in range(li, li+10):
            im = seq2[i]
            vol = computeVolume(im)
            self.assertEqual(vol, 0)
            
    def testDilateByCylinderSequence(self):
        """Verifies the dilation by a cylinder of a sequence"""
        seq = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        im2 = imageMb(128, 128)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        dilateByCylinderSequence(seq, 1, 0)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255, "%d" %(vol))
        self.assertEqual(seq[1].getPixel((64,64)), 255)
        vol = computeVolume(seq[2])
        self.assertEqual(vol, 255)
        self.assertEqual(seq[2].getPixel((64,64)), 255)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255)
        self.assertEqual(seq[3].getPixel((64,64)), 255)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        im.reset()
        im.setPixel(255, (64,64))
        im.setPixel(255, (65,64))
        im.setPixel(255, (63,64))
        im.setPixel(255, (63,63))
        im.setPixel(255, (63,65))
        im.setPixel(255, (64,63))
        im.setPixel(255, (64,65))
        dilateByCylinderSequence(seq, 0, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        dilateByCylinderSequence(seq, 1, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        (x,y) = compare(seq[1], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[3], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
            
    def testErodeByCylinderSequence(self):
        """Verifies the erosion by a cylinder of a sequence"""
        seq = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        im2 = imageMb(128, 128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        erodeByCylinderSequence(seq, 1, 0)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255*128*128-255, "%d" %(vol))
        self.assertEqual(seq[1].getPixel((64,64)), 0)
        vol = computeVolume(seq[2])
        self.assertEqual(vol, 255*128*128-255)
        self.assertEqual(seq[2].getPixel((64,64)), 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255*128*128-255)
        self.assertEqual(seq[3].getPixel((64,64)), 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        im.fill(255)
        im.setPixel(0, (64,64))
        im.setPixel(0, (65,64))
        im.setPixel(0, (63,64))
        im.setPixel(0, (63,63))
        im.setPixel(0, (63,65))
        im.setPixel(0, (64,63))
        im.setPixel(0, (64,65))
        erodeByCylinderSequence(seq, 0, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255*128*128)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        erodeByCylinderSequence(seq, 1, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        (x,y) = compare(seq[1], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[3], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
    def testOpenByCylinderSequence(self):
        """Verifies the opening by cylinder of a sequence"""
        seq1 = sequenceMb(128,128,5)
        seq2 = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        seq1.fill(0)
        seq1[2].setPixel(255, (64,64))
        seq2.fill(0)
        seq2[2].setPixel(255, (64,64))
        dilateByCylinderSequence(seq1, 1, 1)
        dilateByCylinderSequence(seq2, 1, 1)
        openByCylinderSequence(seq1, 1, 1)
        for i in range(5):
            (x,y) = compare(seq1[i], seq2[i], im)
            self.assertLess(x, 0)
        copySequence(seq2, seq1)
        openByCylinderSequence(seq1, 2, 2)
        for i in range(5):
            vol = computeVolume(seq1[i])
            self.assertEqual(vol, 0)
        
    def testCloseByCylinderSequence(self):
        """Verifies the opening by cylinder of a sequence"""
        seq1 = sequenceMb(128,128,5)
        seq2 = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        seq1.fill(255)
        seq1[2].setPixel(0, (64,64))
        seq2.fill(255)
        seq2[2].setPixel(0, (64,64))
        erodeByCylinderSequence(seq1, 1, 1)
        erodeByCylinderSequence(seq2, 1, 1)
        closeByCylinderSequence(seq1, 1, 1)
        for i in range(5):
            (x,y) = compare(seq1[i], seq2[i], im)
            self.assertLess(x, 0)
        copySequence(seq2, seq1)
        closeByCylinderSequence(seq1, 2, 2)
        for i in range(5):
            vol = computeVolume(seq1[i])
            self.assertEqual(vol, 255*128*128)

