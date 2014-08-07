"""
Test cases for the erosion and dilation functions found in the erodil
module of mamba package. Also performs verifications on the structuring
element class.

Python functions and classes:
    structuringElement
    erode
    dilate
    conjugateHexagonalErode
    conjugateHexagonalDilate
    doublePointErode
    doublePointDilate
    isotropicDistance
    dodecagonalDilate
    dodecagonalErode
    linearDilate
    linearErode
    octogonalDilate
    octogonalErode
"""

from mamba import *
import unittest
import random

class TestErodil(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
        self.dirS = [
            (0,0),
            (0,-1),
            (1,-1),
            (1,0),
            (1,1),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1)
        ]
        
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

    def _drawMat(self, im, mat, x, y):
        # draws a matrix centered in x,y
        for i in range(3):
            for j in range(3):
                im.setPixel(mat[j][i], ((x-1)+i, (y-1)+j))
        
    def testErode(self):
        """Verifies the default erosion"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,0,255],[0,0,0],[0,0,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3)
        vol = computeVolume(self.im8_3)
        exp_vol = w*h*255-7*255
        self.assertEqual(vol, exp_vol, "volume %d!=%d" % (vol, exp_vol))
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testErodeSize(self):
        """Verifies that the size is properly taken into account with erosion"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        for n in range(20):
            erode(self.im8_1, self.im8_3, n, se=SQUARE3X3)
            vol = computeVolume(self.im8_3)
            exp_vol = 255*(w*h-(2*n+1)*(2*n+1))
            self.assertEqual(vol, exp_vol, "for %d : volume %d!=%d" % (n, vol, exp_vol))
        
    def testErodeEdge(self):
        """Verifies the edge effect for an erosion"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        erode(self.im8_1, self.im8_3, se=SQUARE3X3, edge=EMPTY)
        vol = computeVolume(self.im8_3)
        exp_vol = 255*(w*h-2*w-2*(h-2))
        self.assertEqual(vol, exp_vol, "volume %d!=%d" % (vol, exp_vol))
        
    def testDilate(self):
        """Verifies the default dilation"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(255, (w//2,h//2))
        self.im8_2.reset()
        self._drawMat(self.im8_2, [[255,255,0],[255,255,255],[255,255,0]], w//2,h//2)
        dilate(self.im8_1, self.im8_3)
        vol = computeVolume(self.im8_3)
        exp_vol = 7*255
        self.assertEqual(vol, exp_vol, "volume %d!=%d" % (vol, exp_vol))
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testDilateSize(self):
        """Verifies that the size is properly taken into account with dilation"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(255, (w//2,h//2))
        for n in range(20):
            dilate(self.im8_1, self.im8_3, n, se=SQUARE3X3)
            vol = computeVolume(self.im8_3)
            exp_vol = 255*(2*n+1)*(2*n+1)
            self.assertEqual(vol, exp_vol, "for %d : volume %d!=%d" % (n, vol, exp_vol))
        
    def testDilateEdge(self):
        """Verifies the edge effect for a dilation"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        dilate(self.im8_1, self.im8_3, se=SQUARE3X3, edge=FILLED)
        vol = computeVolume(self.im8_3)
        exp_vol = 255*(2*w+2*(h-2))
        self.assertEqual(vol, exp_vol, "volume %d!=%d" % (vol, exp_vol))
        
    def testSeHEXAGON(self):
        """Verifies the structuring element HEXAGON"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,0,255],[0,0,0],[0,0,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=HEXAGON)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSeSQUARE3X3(self):
        """Verifies the structuring element SQUARE3X3"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,0,0],[0,0,0],[0,0,0]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=SQUARE3X3)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        edw0 = SQUARE3X3.getEncodedDirections(True)
        self.assertEqual(edw0, 0x1fe)
        ed = SQUARE3X3.getEncodedDirections(False)
        self.assertEqual(ed, 0x1ff)
        
    def testSeTRIANGLE(self):
        """Verifies the structuring element TRIANGLE"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,0,255],[255,0,255],[255,255,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=TRIANGLE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSeSQUARE2X2(self):
        """Verifies the structuring element SQUARE2X2"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[255,255,255],[0,0,255],[0,0,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=SQUARE2X2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSeTRIPOD(self):
        """Verifies the structuring element TRIPOD"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,255,255],[255,0,0],[0,255,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=TRIPOD)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSeDIAMOND(self):
        """Verifies the structuring element DIAMOND"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[255,0,255],[0,0,0],[255,0,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=DIAMOND)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSeSEGMENT(self):
        """Verifies the structuring element SEGMENT"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[255,255,255],[0,0,255],[255,255,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3, se=SEGMENT)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testSEClass(self):
        """Verifies the structuringElement class constructor and methods"""
        se = structuringElement([0,0,1,1,2,2,3,3], grid=SQUARE)
        self.assertEqual(se.getGrid(), SQUARE)
        self.assertEqual(se.getDirections(), [0,1,2,3])
        self.assertEqual(se.getDirections(True), [1,2,3])
        self.assertNotEqual(repr(se), "")
        ed = 1
        ser = structuringElement([ed], grid=SQUARE)
        for i in range(10):
            ed = ed%8+1
            ser = ser.rotate()
            d = ser.getDirections()[0]
            self.assertEqual(d, ed)
        ed = 1
        ser = structuringElement([ed], grid=HEXAGONAL)
        for i in range(10):
            ed = ed%6+1
            ser = ser.rotate()
            d = ser.getDirections()[0]
            self.assertEqual(d, ed)
        for i in range(1,7):
            se_t = structuringElement([i], grid=HEXAGONAL)
            se_t = se_t.transpose()
            d = se_t.getDirections()[0]
            self.assertEqual(d, (i+2)%6+1)
        for i in range(1,9):
            se_t = structuringElement([i], grid=SQUARE)
            se_t = se_t.transpose()
            d = se_t.getDirections()[0]
            self.assertEqual(d, (i+3)%8+1)
            
        se = structuringElement([0,1,2,3,4,5,6,7,8], grid=SQUARE)
        self.assertEqual(se, SQUARE3X3)
        self.assertNotEqual(se, HEXAGON)
            
    def testSetDefault(self):
        """Verifies that setting as default works correctly"""
        DEFAULT_SE.setAs(TRIPOD)
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, [[0,255,255],[255,0,0],[0,255,255]], w//2,h//2)
        erode(self.im8_1, self.im8_3)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        DEFAULT_SE.setAs(HEXAGON)
        
    def testErodeNoZero(self):
        """Verifies that non centered se erosion are correctly computed"""
        se = structuringElement([3], grid=SQUARE)
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        self.im8_2.fill(255)
        self.im8_2.setPixel(0, (w//2,h//2))
        erode(self.im8_1, self.im8_3, se=se)
        shift(self.im8_2, self.im8_2, 7, 1, 255, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def testDilateNoZero(self):
        """Verifies that non centered se dilation are correctly computed"""
        se = structuringElement([4], grid=SQUARE)
        (w,h) = self.im8_1.getSize()
        self.im8_1.fill(0)
        self.im8_1.setPixel(255, (w//2,h//2))
        self.im8_2.fill(0)
        self.im8_2.setPixel(255, (w//2,h//2))
        dilate(self.im8_1, self.im8_3, se=se)
        shift(self.im8_2, self.im8_2, 8, 1, 0, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0)
        
    def _drawConjHexag(self, im, x, y, value):
        drawSquare(im, (x-1,y-1,x+1,y+1), value)
        im.setPixel(value, (x,y-2))
        im.setPixel(value, (x,y+2))
        if (y%2)==0:
            im.setPixel(value, (x-2,y-1))
            im.setPixel(value, (x-2,y+1))
        else:
            im.setPixel(value, (x+2,y-1))
            im.setPixel(value, (x+2,y+1))
        
    def testConjugateHexagonalErode(self):
        """Verifies the conjugate hexagonal erode operation"""
        (w,h) = self.im8_1.getSize()
        for i in range(2):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2+i))
            self.im8_2.fill(255)
            self._drawConjHexag(self.im8_2, w//2, h//2+i, 0)
            conjugateHexagonalErode(self.im8_1, self.im8_1, 1)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testConjugateHexagonalDilate(self):
        """Verifies the conjugate hexagonal dilate operation"""
        (w,h) = self.im8_1.getSize()
        for i in range(2):
            self.im8_1.fill(0)
            self.im8_1.setPixel(255, (w//2,h//2+i))
            self.im8_2.fill(0)
            self._drawConjHexag(self.im8_2, w//2, h//2+i, 255)
            conjugateHexagonalDilate(self.im8_1, self.im8_1, 1)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def _squarePixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
    
        xpre = x-amp*self.dirS[d][0]
        ypre = y-amp*self.dirS[d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testDoublePointErode(self):
        """Verifies the erosion by a doublet operation"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(10):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im1_1.fill(1)
                self.im1_3.fill(1)
                self.im1_1.setPixel(0, (xi,yi))
                self.im1_3.setPixel(0, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 0)
                doublePointErode(self.im1_1, self.im1_2, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0)

    def testDoublePointDilate(self):
        """Verifies the dilation by a doublet operation"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(10):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im1_1.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (xi,yi))
                self.im1_3.setPixel(1, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 1)
                doublePointDilate(self.im1_1, self.im1_2, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0)
        
    def testIsotropicDistanceDepthAcceptance(self):
        """Verifies that isotropicDistance refuses non binary input images"""
        self.assertRaises(MambaError, isotropicDistance, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, isotropicDistance, self.im32_1, self.im8_2)
        
    def testIsotropicDistance(self):
        """Tests the computation of an isotropic distance"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        
        self.im8_3.reset()
        drawSquare(self.im8_3, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im8_3.setPixel(2, (w//2, h//2))
        isotropicDistance(self.im1_1, self.im8_1)
        (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
        self.assertLess(x, 0)

