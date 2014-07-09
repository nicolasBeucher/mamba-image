"""
Test cases for the residual operators functions found in the residues
module of mamba package.

Python functions:
    binaryUltimateErosion
    ultimateErosion
    binarySkeletonByOpening
    skeletonByOpening
    ultimateOpening
    ultimateIsotropicOpening
    ultimateBuildOpening
    quasiDistance
    fullRegularisedGradient
"""

from mamba import *
import unittest
import random

class TestResidues(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im8_5 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im32_4 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
            
    def testBinaryUltimateErosion(self):
        """Tests the ultimate erosion operator for binary images"""
        (w,h) = self.im1_1.getSize()
        
        for n in range(4,10):
            self.im1_1.reset()
            drawSquare(self.im1_1, (w//2-n, h//2-n+1, w//2+n, h//2+n-1), 1)
            self.im1_3.reset()
            drawLine(self.im1_3, (w//2-1, h//2, w//2+1, h//2), 1)
            self.im32_3.reset()
            drawLine(self.im32_3, (w//2-1, h//2, w//2+1, h//2), n)
            
            binaryUltimateErosion(self.im1_1, self.im1_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_2)
            self.assertLess(x, 0)
            
            ultimateErosion(self.im1_1, self.im1_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_2)
            self.assertLess(x, 0)
        
    def testUltimateErosion(self):
        """Tests the ultimate erosion generic operator"""
        (w,h) = self.im8_1.getSize()
        
        for n in range(4,10):
            self.im8_1.reset()
            drawSquare(self.im8_1, (w//2-n, h//2-n+1, w//2+n, h//2+n-1), 255)
            self.im8_3.reset()
            drawLine(self.im8_3, (w//2-1, h//2, w//2+1, h//2), 255)
            self.im32_3.reset()
            drawLine(self.im32_3, (w//2-1, h//2, w//2+1, h//2), n)
            
            ultimateErosion(self.im8_1, self.im8_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
            self.assertLess(x, 0)

    def testBinarySkeletonByOpening(self):
        """Verifies the skeleton by opening operator for binary images"""
        (w,h) = self.im1_1.getSize()
        
        for n in range(5,10):
            self.im1_1.reset()
            drawSquare(self.im1_1, (w//2-6*n, h//2-h//4, w//2-4*n, h//2+h//4), 1)
            drawSquare(self.im1_1, (w//2-4*n, h//2-h//4, w//2, h//2-h//4+2*n), 1)
            drawSquare(self.im1_1, (w//2, h//2-h//4, w//2+4*n, h//2+h//4), 1)
            
            self.im1_3.reset()
            drawLine(self.im1_3, (w//2-5*n, h//2-h//4+n, w//2-5*n, h//2+h//4-n), 1)
            drawLine(self.im1_3, (w//2-5*n, h//2-h//4+n, w//2+n-1, h//2-h//4+n), 1)
            drawLine(self.im1_3, (w//2+2*n, h//2-h//4+2*n, w//2+2*n, h//2+h//4-2*n), 1)
            
            self.im32_3.reset()
            drawLine(self.im32_3, (w//2-5*n, h//2-h//4+n, w//2-5*n, h//2+h//4-n), n+1)
            drawLine(self.im32_3, (w//2-5*n, h//2-h//4+n, w//2+n-1, h//2-h//4+n), n+1)
            drawLine(self.im32_3, (w//2+2*n, h//2-h//4+2*n, w//2+2*n, h//2+h//4-2*n), 2*n+1)
            
            binarySkeletonByOpening(self.im1_1, self.im1_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_2)
            self.assertLess(x, 0)
            
            skeletonByOpening(self.im1_1, self.im1_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_2)
            self.assertLess(x, 0)
        
    def testSkeletonByOpening(self):
        """Verifies the skeleton by opening generic operator"""
        (w,h) = self.im8_1.getSize()
        
        for n in range(5,10):
            self.im8_1.reset()
            drawSquare(self.im8_1, (w//2-6*n, h//2-h//4, w//2-4*n, h//2+h//4), 255)
            drawSquare(self.im8_1, (w//2-4*n, h//2-h//4, w//2, h//2-h//4+2*n), 255)
            drawSquare(self.im8_1, (w//2, h//2-h//4, w//2+4*n, h//2+h//4), 255)
            
            self.im8_3.reset()
            drawLine(self.im8_3, (w//2-5*n, h//2-h//4+n, w//2-5*n, h//2+h//4-n), 255)
            drawLine(self.im8_3, (w//2-5*n, h//2-h//4+n, w//2+n-1, h//2-h//4+n), 255)
            drawLine(self.im8_3, (w//2+2*n, h//2-h//4+2*n, w//2+2*n, h//2+h//4-2*n), 255)
            
            self.im32_3.reset()
            drawLine(self.im32_3, (w//2-5*n, h//2-h//4+n, w//2-5*n, h//2+h//4-n), n+1)
            drawLine(self.im32_3, (w//2-5*n, h//2-h//4+n, w//2+n-1, h//2-h//4+n), n+1)
            drawLine(self.im32_3, (w//2+2*n, h//2-h//4+2*n, w//2+2*n, h//2+h//4-2*n), 2*n+1)
            
            skeletonByOpening(self.im8_1, self.im8_2, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
            self.assertLess(x, 0)
            
    def testUltimateOpeningHexagonal(self):
        """Verifies the ultimate opening residual operator on hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(100, (w//2,h//2))
        dilate(self.im8_1, self.im8_1, 50, se=HEXAGON)
        self.im8_2.reset()
        self.im8_2.setPixel(200, (w//2+40,h//2))
        dilate(self.im8_2, self.im8_2, 25, se=HEXAGON)
        lut = list(range(256))
        lut[0]=255
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        logic(self.im8_2, self.im8_1, self.im8_3, "inf")
        lut = list(range(256))
        lut[255]=0
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        lookup(self.im8_3, self.im8_3, lut)
        logic(self.im8_1, self.im8_2, self.im8_1, "sup")
        self.im32_1.reset()
        self.im32_1.setPixel(51, (w//2,h//2))
        dilate(self.im32_1, self.im32_1, 50, se=HEXAGON)
        self.im32_2.reset()
        self.im32_2.setPixel(26, (w//2+40,h//2))
        dilate(self.im32_2, self.im32_2, 25, se=HEXAGON)
        logic(self.im32_1, self.im32_2, self.im32_3, "sup")
        
        ultimateOpening(self.im8_1, self.im8_2, self.im32_2, grid=HEXAGONAL)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)
            
    def testUltimateOpeningSquare(self):
        """Verifies the ultimate opening residual operator on square grid"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-40,h//2-40,w//2+40,h//2+40), 100)
        drawSquare(self.im8_1, (w//2,h//2-30,w//2+60,h//2+30), 200)
        self.im8_3.reset()
        drawSquare(self.im8_3, (w//2,h//2-30,w//2+60,h//2+30), 200)
        drawSquare(self.im8_3, (w//2-40,h//2-40,w//2+40,h//2+40), 100)
        self.im32_3.reset()
        drawSquare(self.im32_3, (w//2,h//2-30,w//2+60,h//2+30), 31)
        drawSquare(self.im32_3, (w//2-40,h//2-40,w//2+40,h//2+40), 41)
        
        ultimateOpening(self.im8_1, self.im8_2, self.im32_2, grid=SQUARE)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

    def testUltimateIsotropicOpeningSquare(self):
        """Verifies the ultimate isotropic opening residual operator on square grid"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(100, (w//2,h//2))
        octogonalDilate(self.im8_1, self.im8_1, 50)
        self.im8_2.reset()
        self.im8_2.setPixel(200, (w//2+40,h//2))
        octogonalDilate(self.im8_2, self.im8_2, 30)
        lut = list(range(256))
        lut[0]=255
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        self.im8_3.fill(255)
        self.im8_3.setPixel(100, (w//2+30,h//2))
        octogonalErode(self.im8_3, self.im8_3, 29)
        drawLine(self.im8_3, (w//2+59, h//2-12, w//2+59, h//2+12), 200)
        logic(self.im8_2, self.im8_3, self.im8_3, "inf")
        logic(self.im8_1, self.im8_3, self.im8_3, "inf")
        lut = list(range(256))
        lut[255]=0
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        lookup(self.im8_3, self.im8_3, lut)
        logic(self.im8_1, self.im8_2, self.im8_1, "sup")
        self.im32_1.reset()
        self.im32_1.setPixel(51, (w//2,h//2))
        octogonalDilate(self.im32_1, self.im32_1, 50)
        self.im32_2.reset()
        self.im32_2.setPixel(31, (w//2+46,h//2))
        octogonalDilate(self.im32_2, self.im32_2, 30)
        logic(self.im32_1, self.im32_2, self.im32_3, "sup")
        
        ultimateIsotropicOpening(self.im8_1, self.im8_2, self.im32_2, grid=SQUARE)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        #self.assertLess(x, 0) # no means to verify
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

    def testUltimateIsotropicOpeningHexagonal(self):
        """Verifies the ultimate isotropic opening residual operator on hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(100, (w//2,h//2))
        dodecagonalDilate(self.im8_1, self.im8_1, 50)
        self.im8_2.reset()
        self.im8_2.setPixel(200, (w//2+40,h//2))
        dodecagonalDilate(self.im8_2, self.im8_2, 30)
        lut = list(range(256))
        lut[0]=255
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        self.im8_3.fill(255)
        self.im8_3.setPixel(100, (w//2+27,h//2))
        dodecagonalErode(self.im8_3, self.im8_3, 31)
        #drawLine(self.im8_3, (w//2+59, h//2-12, w//2+59, h//2+12), 200)
        logic(self.im8_2, self.im8_3, self.im8_3, "inf")
        logic(self.im8_1, self.im8_3, self.im8_3, "inf")
        lut = list(range(256))
        lut[255]=0
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        lookup(self.im8_3, self.im8_3, lut)
        logic(self.im8_1, self.im8_2, self.im8_1, "sup")
        self.im32_1.reset()
        self.im32_1.setPixel(51, (w//2,h//2))
        dodecagonalDilate(self.im32_1, self.im32_1, 50)
        self.im32_2.reset()
        self.im32_2.setPixel(31, (w//2+46,h//2))
        dodecagonalDilate(self.im32_2, self.im32_2, 30)
        logic(self.im32_1, self.im32_2, self.im32_3, "sup")
        
        ultimateIsotropicOpening(self.im8_1, self.im8_2, self.im32_2, grid=HEXAGONAL)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        #self.assertLess(x, 0) # no means to verify
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)
            
    def testUltimateBuildOpening(self):
        """Verifies the ultimate opening residual operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(100, (w//2,h//2))
        dilate(self.im8_1, self.im8_1, 50, se=HEXAGON)
        self.im8_2.reset()
        self.im8_2.setPixel(200, (w//2+40,h//2))
        dilate(self.im8_2, self.im8_2, 25, se=HEXAGON)
        lut = list(range(256))
        lut[0]=255
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        logic(self.im8_2, self.im8_1, self.im8_3, "inf")
        lut = list(range(256))
        lut[255]=0
        lookup(self.im8_1, self.im8_1, lut)
        lookup(self.im8_2, self.im8_2, lut)
        lookup(self.im8_3, self.im8_3, lut)
        lut = list(range(256))
        lut[200]=100
        lookup(self.im8_3, self.im8_3, lut)
        logic(self.im8_1, self.im8_2, self.im8_1, "sup")
        self.im32_1.reset()
        self.im32_1.setPixel(51, (w//2,h//2))
        dilate(self.im32_1, self.im32_1, 50, se=HEXAGON)
        self.im32_2.reset()
        self.im32_2.setPixel(51, (w//2+40,h//2))
        dilate(self.im32_2, self.im32_2, 25, se=HEXAGON)
        logic(self.im32_1, self.im32_2, self.im32_3, "sup")
        
        ultimateBuildOpening(self.im8_1, self.im8_2, self.im32_2, grid=HEXAGONAL)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

    def testQuasiDistance(self):
        """Verifies the computation of the quasi-distance residue"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-w//4, h//2-h//4, w//2+w//4, h//2+h//4), 255)
        
        convert(self.im8_1, self.im1_1)
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE)
        
        quasiDistance(self.im8_1, self.im8_2, self.im32_2, grid=SQUARE)
        (x,y) = compare(self.im32_1, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def _drawSlope(self, imOut, imRes1, imRes2, size):
        w,h = imOut.getSize()
        imOut.reset()
        for i in range(50,50+size):
            drawLine(imOut, (i,0,i,h-1), i-50)
        drawSquare(imOut, (i+1, 0, w-1, h-1), i-50)
        imRes1.reset()
        for i in range(2-size%2):
            drawLine(imRes1, (49+size//2+size%2+i,0,49+size//2+size%2+i,h-1), 1)
        imRes2.reset()
        for i in range(2-size%2):
            drawLine(imRes2, (49+size//2+size%2+i,0,49+size//2+size%2+i,h-1), 16)
            
    def testFullRegularisedGradient(self):
        """Verifies the correct computation of a regularised gradient"""
        for i in range(10):
            m = random.randint(30,60)
            self._drawSlope(self.im8_1, self.im8_3, self.im8_5, m)
            fullRegularisedGradient(self.im8_1, self.im8_2, self.im8_4, SQUARE)
            vol = computeVolume(self.im8_2)
            self.assertNotEqual(vol, 0, "m=%d : (vol %d)" % (m,vol))
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
            self.assertLess(x, 0)
            (x,y) = compare(self.im8_5, self.im8_4, self.im8_4)
            self.assertLess(x, 0)

