"""
Test cases for the segmentation operators found in the segment3D
module of mamba3D package. 

Python functions:
    label3D
    watershedSegment3D
    basinSegment3D
    markerControlledWatershed3D
    valuedWatershed3D
    fastSKIZ3D
    mosaic3D
    mosaicGradient3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestSegment3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,64,8)
        self.im8_2 = image3DMb(64,64,64,8)
        self.im8_3 = image3DMb(64,64,64,8)
        self.im8_4 = image3DMb(64,64,64,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(64,64,64,32)
        self.im32_2 = image3DMb(64,64,64,32)
        self.im32_3 = image3DMb(64,64,64,32)
        self.im32_4 = image3DMb(64,64,64,32)
        self.im32_5 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im1_5)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, watershedSegment3D, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment3D, self.im32_1, self.im8_2)
        self.assertRaises(MambaError, basinSegment3D, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, basinSegment3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, basinSegment3D, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, basinSegment3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, basinSegment3D, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, basinSegment3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, basinSegment3D, self.im32_1, self.im8_2)
        self.assertRaises(MambaError, label3D, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, label3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, label3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, label3D, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, label3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, label3D, self.im32_1, self.im8_2)

    def testGridAcceptation(self):
        """Tests that incorrect grid raises an exception"""
        self.assertRaises(MambaError, watershedSegment3D, self.im8_1, self.im32_2, grid=CENTER_CUBIC)
        self.assertRaises(MambaError, basinSegment3D, self.im8_1, self.im32_2, grid=CENTER_CUBIC)
        self.assertRaises(MambaError, label3D, self.im1_1, self.im32_2, grid=CENTER_CUBIC)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError, watershedSegment3D, self.im8_1, self.im32_5)
        self.assertRaises(MambaError, basinSegment3D, self.im8_1, self.im32_5)
        self.assertRaises(MambaError, label3D, self.im1_1, self.im32_5)
        
    def _drawBox3D(self, im, size, value):
        (w,h,l) = im.getSize()
        
        drawSquare(im[l//2-size], (w//2-size,h//2-size,w//2+size,h//2+size), value)
        drawSquare(im[l//2+size], (w//2-size,h//2-size,w//2+size,h//2+size), value)
        for i in range(l//2-size+1,l//2+size):
            drawBox(im[i], (w//2-size,h//2-size,w//2+size,h//2+size), value)

    def testBasinSegment3D(self):
        """Verifies that the basin segmentation 3D operator works correctly"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(l//4,(3*l)//4,3):
            # creating a wall image
            self.im8_1.reset()
            self.im8_1[i-1].fill(130)
            self.im8_1[i].fill(255)
            self.im8_1[i+1].fill(176)
                
            exp_vol = (i*50+(l-1-i)*100)*h*w
            exp_vol1 = exp_vol+50*h*w
            exp_vol2 = exp_vol+100*h*w
                    
            # adding 2 well
            self.im32_1.reset()
            self.im32_1.setPixel(50, (w//2,h//2,l//4-1))
            self.im32_1.setPixel(100, (w//2,h//2,(3*l)//4))
            
            basinSegment3D(self.im8_1, self.im32_1, grid=CUBIC)
            copyBytePlane3D(self.im32_1, 0, self.im8_2)
            vol = computeVolume3D(self.im8_2)
            self.assertTrue(exp_vol1<=vol and exp_vol2>=vol, "wall at %d [%d,%d]: %d//%d//%d" %(i,l//4,(3*l)//4,vol,exp_vol1,exp_vol2))
        
    def testWatershedSegment3D(self):
        """Tests the 3D watershed segmentation operator"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(l//4,3*l//4,3):
            self.im8_1.reset()
            self.im8_1[i].fill(i)
            self.im8_2.reset()
            self.im8_2[i].fill(255)
            self.im32_1.reset()
            self.im32_1.setPixel(1, (w//2,h//2,0))
            self.im32_1.setPixel(2, (w//2,h//2,l-1))
            grid = CUBIC if i%2==0 else FACE_CENTER_CUBIC
            watershedSegment3D(self.im8_1, self.im32_1, grid=grid)
            copyBytePlane3D(self.im32_1, 3, self.im8_3)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
            
        self.im8_1.reset()
        self._drawBox3D(self.im8_1, 10, 51)
        self._drawBox3D(self.im8_1, 5, 21)
        self.im8_2.reset()
        self._drawBox3D(self.im8_2, 10, 255)
        self.im32_1.reset()
        self.im32_1.setPixel(1, (w//2,h//2,0))
        self.im32_1.setPixel(2, (w//2,h//2,l//2))
        watershedSegment3D(self.im8_1, self.im32_1, grid=CUBIC)
        copyBytePlane3D(self.im32_1, 3, self.im8_3)
        (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        self.im8_2.reset()
        self._drawBox3D(self.im8_2, 10, 255)
        self._drawBox3D(self.im8_2, 5, 255)
        self.im32_1.reset()
        self.im32_1.setPixel(1, (w//2,h//2,0))
        self.im32_1.setPixel(2, (w//2,h//2,l//2))
        self.im32_1.setPixel(3, (w//2-7,h//2,l//2))
        watershedSegment3D(self.im8_1, self.im32_1, grid=CUBIC)
        copyBytePlane3D(self.im32_1, 3, self.im8_3)
        (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_3)
        self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testIdempotencyWatershedSegment3D(self):
        """Makes sure the computed watershed is idempotent"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(2):
            grid = CUBIC if i%2==0 else FACE_CENTER_CUBIC
            
            # creating a random image
            for wi in range(w):
                for hi in range(h):
                    for li in range(l):
                        vi = random.randint(0,255)
                        self.im8_1.setPixel(vi, (wi,hi,li))
                    
            # adding 10 random well
            self.im32_1.reset()
            self.im32_2.reset()
            for vi in range(1,11):
                hi = random.randint(0,h-1)
                wi = random.randint((w*(vi-1))//10, (w*vi)//10-1)
                li = random.randint((l*(vi-1))//10, (l*vi)//10-1)
                self.im32_1.setPixel(vi*10, (wi,hi,li))
                self.im32_2.setPixel(vi*10, (wi,hi,li))
            
            watershedSegment3D(self.im8_1, self.im32_1, grid=grid)
            copyBytePlane3D(self.im32_1, 3, self.im8_2)
            copyBytePlane3D(self.im32_1, 0, self.im8_3)
            diff3D(self.im8_3, self.im8_2, self.im8_3)
            copyBytePlane3D(self.im8_3, 0, self.im32_2)
            watershedSegment3D(self.im8_1, self.im32_2, grid=grid)
            copyBytePlane3D(self.im32_1, 3, self.im8_3)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testLabel3D_1(self):
        """Verifies the labelling 3D operator on binary"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (31,30,30))
        self.im1_1.setPixel(1, (31,31,31))
        
        n = label3D(self.im1_1, self.im32_1, grid=FACE_CENTER_CUBIC)
        self.assertEqual(n, 2, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(1, (31,30,30))
        self.im32_2.setPixel(2, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
        n = label3D(self.im1_1, self.im32_1, lblow=10, grid=CUBIC)
        self.assertEqual(n, 1, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(10, (31,30,30))
        self.im32_2.setPixel(10, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
    def testLabel3D_8(self):
        """Verifies the labelling 3D operator on greyscale"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(1, (31,30,30))
        self.im8_1.setPixel(1, (31,31,31))
        
        n = label3D(self.im8_1, self.im32_1, grid=FACE_CENTER_CUBIC)
        self.assertEqual(n, 2, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(1, (31,30,30))
        self.im32_2.setPixel(2, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
        n = label3D(self.im8_1, self.im32_1, lblow=10, grid=CUBIC)
        self.assertEqual(n, 1, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(10, (31,30,30))
        self.im32_2.setPixel(10, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
    def testLabel3D_32(self):
        """Verifies the labelling 3D operator on 32 bit"""
        (w,h,l) = self.im32_3.getSize()
        
        self.im32_3.reset()
        self.im32_3.setPixel(1, (31,30,30))
        self.im32_3.setPixel(1, (31,31,31))
        
        n = label3D(self.im32_3, self.im32_1, grid=FACE_CENTER_CUBIC)
        self.assertEqual(n, 2, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(1, (31,30,30))
        self.im32_2.setPixel(2, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_2)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
        n = label3D(self.im32_3, self.im32_1, lblow=10, grid=CUBIC)
        self.assertEqual(n, 1, "%d" %(n))
        self.im32_2.reset()
        self.im32_2.setPixel(10, (31,30,30))
        self.im32_2.setPixel(10, (31,31,31))
        (x,y,z) = compare3D(self.im32_2, self.im32_1, self.im32_2)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
    def testWatershedSegment3D_32(self):
        """Verifies the 32-bit watershed segment 3D operator"""
        (w,h,l) = self.im32_1.getSize()
        
        for i in range(l//2,(3*l)//4):
            # creating a wall image
            self.im32_1.reset()
            self.im8_1.reset()
            
            self.im32_1[i].fill(127*(i-l//2+1))
            self.im8_1[i].fill(255)
                
            exp_vol = (i*50+(l-1-i)*100)*h*w
                    
            # adding 2 well
            self.im32_2.reset()
            self.im32_2.setPixel(50, (w//2,h//2,l//2-1))
            self.im32_2.setPixel(100, (w//2,h//2,(3*l)//4))
            
            if i%4==0:
                level = 127*(i-l//2+1)+1
                watershedSegment3D(self.im32_1, self.im32_2, max_level=level, grid=CUBIC)
                copyBytePlane3D(self.im32_2, 3, self.im8_2)
                (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(z, 0)
            elif i%4==1:
                level = 0
                watershedSegment3D(self.im32_1, self.im32_2, max_level=level, grid=CUBIC)
                copyBytePlane3D(self.im32_2, 3, self.im8_2)
                (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(z, 0)
            elif i%4==2:
                level = 128
                watershedSegment3D(self.im32_1, self.im32_2, max_level=level, grid=CUBIC)
                copyBytePlane3D(self.im32_2, 0, self.im8_2)
                vol = computeVolume3D(self.im8_2)
                self.assertEqual(exp_vol, vol, "wall %d [%d]: %d=!%d" %(i,l,vol,exp_vol))
                copyBytePlane3D(self.im32_2, 3, self.im8_2)
                (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
                self.assertGreater(z, 0, "wall %d [%d]: %d,%d,%d" %(i,l,x,y,z))
            else:
                level = 384
                watershedSegment3D(self.im32_1, self.im32_2, max_level=level, grid=CUBIC)
                copyBytePlane3D(self.im32_2, 0, self.im8_2)
                vol = computeVolume3D(self.im8_2)
                self.assertEqual(exp_vol, vol)
                copyBytePlane3D(self.im32_2, 3, self.im8_2)
                (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
                self.assertGreater(z, 0)
            
    def testBasinSegment3D_32(self):
        """Verifies the 32-bit basin segment 3D operator"""
        (w,h,l) = self.im32_1.getSize()
        
        for i in range(l//2,(3*l)//4):
            # creating a wall image
            self.im32_1.reset()
            self.im32_1[i].fill(127*(i-l//2+1))
                
            exp_vol = (i*50+(l-1-i)*100)*h*w
            exp_vol1 = exp_vol+50*h*w
            exp_vol2 = exp_vol+100*h*w
                    
            # adding 2 well
            self.im32_2.reset()
            self.im32_2.setPixel(50, (w//2,h//2,l//2-1))
            self.im32_2.setPixel(100, (w//2,h//2,(3*l)//4))
            
            if i%4==0:
                level = 127*(i-l//2+1)+1
            elif i%4==1:
                level = 0
            elif i%4==2:
                level = 128
            else:
                level = 384
            basinSegment3D(self.im32_1, self.im32_2, max_level=level, grid=CUBIC)
            copyBytePlane3D(self.im32_2, 0, self.im8_2)
            vol = computeVolume3D(self.im8_2)
            self.assertTrue(exp_vol1<=vol and exp_vol2>=vol, "wall at %d [%d,%d]: %d//%d//%d" %(i,l//2,(3*l)//4,vol,exp_vol1,exp_vol2))
            
    def _drawWells(self, imOut, wall=[1,2,3,4]):
        (w,h,l) = imOut.getSize()
        
        imOut.reset()
        if wall.count(1)>0:
            drawSquare(imOut[l//2], (0,0,w-1,h//2), 20)
            #drawLine(imOut, (w//2,0,w//2,h//2), 20)
        if wall.count(2)>0:
            for i in range(l//2):
                drawLine(imOut[i], (0,h//2,w-1,h//2), 40)
            #drawLine(imOut, (0,h//2,w//2,h//2), 40)
        if wall.count(3)>0:
            drawSquare(imOut[l//2], (0,h//2+1,w-1,h-1), 60)
            #drawLine(imOut, (w//2,h//2+1,w//2,h-1), 60)
        if wall.count(4)>0:
            for i in range(l//2+1,l):
                drawLine(imOut[i], (0,h//2,w-1,h//2), 80)
            #drawLine(imOut, (w//2+1,h//2,w-1,h//2), 80)
        drawLine(imOut[l//2], (0,h//2,w-1,h//2), 255)
        #imOut.setPixel(255, (w//2,h//2))
        
    def testMarkerControlledWatershed3D(self):
        """Verifies the marker controlled valued watershed 3D computation"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawWells(self.im8_1)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//2,h//4,l//4))
        self.im1_1.setPixel(1, (w//2,3*h//4,l//4))
        self.im1_1.setPixel(1, (w//2,3*h//4,3*l//4))
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//2,h//4,l//4))
        self._drawWells(self.im8_3, wall=[1,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
#        self.im8_2.showDisplay("PROJECTION")
#        self.im8_2.setPalette(rainbow)
#        self.im8_1.showDisplay("PROJECTION")
#        self.im8_1.setPalette(rainbow)
#        a = raw_input()
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4,l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4,l//4))
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self._drawWells(self.im8_3, wall=[2,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4,3*l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self._drawWells(self.im8_3, wall=[2,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//4,h//4,l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[1,3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[2,3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//4,h//4,l//4))
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self._drawWells(self.im8_3, wall=[1,2,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4,l//4))
        self.im1_1.setPixel(1, (w//4,3*h//4,l//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4,3*l//4))
        self._drawWells(self.im8_3, wall=[2,3,4])
        markerControlledWatershed3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testValuedWatershed3D(self):
        """Verifies the minima controlled valued watershed 3D computation"""
        self._drawWells(self.im8_1)
        
        valuedWatershed3D(self.im8_1,self.im8_2, CUBIC)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testFastSKIZ3D(self):
        """Verifies the fast SKIZ 3D operator based on watershed"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//4,3*l//4))
        self.im1_1.setPixel(1, (w//2,h//4,l//4))
        self.im1_1.setPixel(1, (w//2,3*h//4,l//4))
        self.im1_1.setPixel(1, (w//2,3*h//4,3*l//4))
        self.im1_3.fill(1)
        for i in range(l):
            drawLine(self.im1_3[i], (0,h//2,w-1,h//2), 0)
        self.im1_3[l//2].reset()
        
        fastSKIZ3D(self.im1_1, self.im1_2, CUBIC)
        (x,y,z) = compare3D(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def _drawCubes(self, imOut):
        (w,h,l) = imOut.getSize()
        
        for i in range(w//4):
            drawCube(imOut, (i,i,i,w-1-i,h-1-i,l-1-i), i+1)
        for i in range(w//4):
            drawCube(imOut, (i+w//4,i+w//4,i+w//4,w-1-i-w//4,h-1-i-w//4,l-1-i-w//4), w//2+i*2)
        
    def testMosaic3D(self):
        """Verifies the computation of mosaic 3D image using watershed segment"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawCubes(self.im8_1)
        mosaic3D(self.im8_1, self.im8_2, self.im8_3, CUBIC)
            
        self.im8_4.fill(1)
        drawCube(self.im8_4, (w//4,w//4+1,w//4,w-2-w//4,h-1-w//4,l-1-w//4), w-2)
        drawSquare(self.im8_2[w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        drawSquare(self.im8_2[l-1-w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        for i in range(w//4+1,l-1-w//4):
            drawBox(self.im8_2[i], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        drawSquare(self.im8_4[w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        drawSquare(self.im8_4[l-1-w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        for i in range(w//4+1,l-1-w//4):
            drawBox(self.im8_4[i], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        (x,y,z) = compare3D(self.im8_2, self.im8_4, self.im8_4)
        self.assertLess(x, 0, "%d,%d,%d - %d" % (x,y,z,w//4))
        self.im8_4.reset()
        drawSquare(self.im8_4[w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        drawSquare(self.im8_4[l-1-w//4], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        for i in range(w//4+1,l-1-w//4):
            drawBox(self.im8_4[i], (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        (x,y,z) = compare3D(self.im8_3, self.im8_4, self.im8_4)
        self.assertLess(x, 0)
        
    def testMosaicGradient3D(self):
        """Verifies the computation of 3D mosaic gradient using watershed segment"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawCubes(self.im8_1)
        mosaicGradient3D(self.im8_1, self.im8_2, CUBIC)
            
        self.im8_4.reset()
        drawSquare(self.im8_4[w//4], (w//4,w//4,w-1-w//4,h-1-w//4), w-3)
        drawSquare(self.im8_4[l-1-w//4], (w//4,w//4,w-1-w//4,h-1-w//4), w-3)
        for i in range(w//4+1,l-1-w//4):
            drawBox(self.im8_4[i], (w//4,w//4,w-1-w//4,h-1-w//4), w-3)
        (x,y,z) = compare3D(self.im8_2, self.im8_4, self.im8_4)
        self.assertLess(x, 0, "%d,%d,%d - %d" % (x,y,z,w//4))

