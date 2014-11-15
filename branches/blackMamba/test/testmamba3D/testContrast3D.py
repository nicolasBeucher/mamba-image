"""
Test cases for the contrast operators found in the contrast3D
module of mamba3D package. 

Python functions:
    gradient3D
    halfGradient3D
    whiteTopHat3D
    blackTopHat3D
    supWhiteTopHat3D
    supBlackTopHat3D
    regularisedGradient3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestContrast3D(unittest.TestCase):

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
        
    def _drawBox3D(self, im, size, value):
        (w,h,l) = im.getSize()
        (x1,y1,z1,x2,y2,z2) = size
        
        drawSquare(im[z1], (x1,y1,x2,y2), value)
        drawSquare(im[z2], (x1,y1,x2,y2), value)
        for i in range(z1+1,z2):
            drawBox(im[i], (x1,y1,x2,y2), value)

    def testGradient3D(self):
        """Verifies the 3D gradient operation"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.reset()
        drawCube(self.im8_1, (w//2-1, h//2-1, l//2-1, w//2+1, h//2+1, l//2+1), 255)
        self.im8_2.reset()
        self._drawBox3D(self.im8_2, (w//2-1, h//2-1, l//2-1, w//2+1, h//2+1, l//2+1), 255)
        self._drawBox3D(self.im8_2, (w//2-2, h//2-2, l//2-2, w//2+2, h//2+2, l//2+2), 255)
        gradient3D(self.im8_1, self.im8_1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

    def testHalfGradient(self):
        """Verifies the 3D half-gradient operation"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        drawCube(self.im8_1, (w//2-1, h//2-1, l//2-1, w//2+1, h//2+1, l//2+1), 255)
        self.im8_2.reset()
        self._drawBox3D(self.im8_2, (w//2-1, h//2-1, l//2-1, w//2+1, h//2+1, l//2+1), 255)
        halfGradient3D(self.im8_1, self.im8_1, type="intern", se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
        self.im8_1.reset()
        drawCube(self.im8_1, (w//2-1, h//2-1, l//2-1, w//2+1, h//2+1, l//2+1), 255)
        self.im8_2.reset()
        self._drawBox3D(self.im8_2, (w//2-2, h//2-2, l//2-2, w//2+2, h//2+2, l//2+2), 255)
        halfGradient3D(self.im8_1, self.im8_1, type="extern", se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _growingSpot3D(self, imOut, n=None, se=CUBOCTAHEDRON1, inv=False):
        (w,h,l) = imOut.getSize()
        imOut.reset()
        prov = image3DMb(imOut)
        if n==None:
            n = l
        z = 10
        size = 0
        while((z+size)<l and size<n):
            prov.reset()
            prov.setPixel(255, (w//2, h//2, z))
            dilate3D(prov, prov, size, se)
            logic3D(imOut, prov, imOut, "sup")
            z += 10+2*size
            size += 1
        if inv:
            negate3D(imOut, imOut)
        return size
        
    def testWhiteTopHat3D(self):
        """Tests the 3D white top hat operation"""
        size = self._growingSpot3D(self.im8_1, se=CUBOCTAHEDRON1)
        for i in range(size+1):
            whiteTopHat3D(self.im8_1, self.im8_2, i, se=CUBOCTAHEDRON1)
            self._growingSpot3D(self.im8_3, i, se=CUBOCTAHEDRON1)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        size = self._growingSpot3D(self.im8_1, se=CUBE3X3X3)
        for i in range(size+1):
            whiteTopHat3D(self.im8_1, self.im8_2, i, se=CUBE3X3X3)
            self._growingSpot3D(self.im8_3, i, se=CUBE3X3X3)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testBlackTopHat3D(self):
        """Tests the 3D black top hat operation"""
        size = self._growingSpot3D(self.im8_1, se=CUBOCTAHEDRON1, inv=True)
        for i in range(size+1):
            blackTopHat3D(self.im8_1, self.im8_2, i, se=CUBOCTAHEDRON1)
            self._growingSpot3D(self.im8_3, i, se=CUBOCTAHEDRON1)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        size = self._growingSpot3D(self.im8_1, se=CUBE3X3X3, inv=True)
        for i in range(size+1):
            blackTopHat3D(self.im8_1, self.im8_2, i, se=CUBE3X3X3)
            self._growingSpot3D(self.im8_3, i, se=CUBE3X3X3)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _growingLineSpot3D(self, imOut, n=None, inv=False):
        (w,h,l) = imOut.getSize()
        imOut.reset()
        prov = image3DMb(imOut)
        if n==None:
            n = l
        z = 10
        size = 0
        dir = 1
        while((z+size)<l and size<n):
            prov.reset()
            prov.setPixel(255, (w//2, h//2, z))
            linearDilate3D(prov, prov, dir, size, FACE_CENTER_CUBIC)
            logic3D(imOut, prov, imOut, "sup")
            z += 10+2*size
            size += 1
            dir = (dir+1)%13
            if dir==0:
                dir = 1
        if inv:
            negate3D(imOut, imOut)
        return size
        
    def testSupWhiteTopHat3D(self):
        """Tests the 3D sup white top hat operation"""
        size = self._growingLineSpot3D(self.im8_1)
        for i in range(size+1):
            supWhiteTopHat3D(self.im8_1, self.im8_2, i, grid=FACE_CENTER_CUBIC)
            self._growingLineSpot3D(self.im8_3, i)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

    def testSupBlackTopHat3D(self):
        """Tests the 3D sup black top hat operation"""
        size = self._growingLineSpot3D(self.im8_1, inv=True)
        for i in range(size+1):
            supBlackTopHat3D(self.im8_1, self.im8_2, i, grid=FACE_CENTER_CUBIC)
            self._growingLineSpot3D(self.im8_3, i)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _drawSlope3D(self, imOut, imRes, size):
        (w,h,l) = imOut.getSize()
        imOut.reset()
        for i in range(30,30+size):
            imOut[i].fill(i-30)
        drawCube(imOut, (0, 0, i+1, w-1, h-1, l-1), i-30)
        imRes.reset()
        for i in range(2-size%2):
            imRes[29+size//2+size%2+i].fill(1)
            
    def testRegularisedGradient(self):
        """Verifies the correct computation of a regularised gradient"""
        m = random.randint(10,20)
        self._drawSlope3D(self.im8_1, self.im8_3, m)
        for n in range(10):
            regularisedGradient3D(self.im8_1, self.im8_2, n, CUBIC)
            vol = computeVolume3D(self.im8_2)
            if m<(4*n+1):
                self.assertNotEqual(vol, 0, "m=%d : n=%d (vol %d)" % (m,n,vol))
                (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_2)
                self.assertLess(x, 0, "m=%d : n=%d diff in (%d,%d,%d)"%(m,n,x,y,z))
            else:
                self.assertEqual(vol, 0, "m=%d : n=%d (vol %d)" % (m,n,vol))

