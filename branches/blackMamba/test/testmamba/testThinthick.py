"""
Test cases for the thinning and thickening functions found in the thinthick
module of mamba package.

Python functions and classes:
    doubleStructuringElement
    thin
    thick
    rotatingThin
    rotatingThick
    infThin
    supThick
    fullThin
    fullThick
    thinL
    thinM
    thinD
    thickL
    thickM
    thickD
    endPoints
    multiplePoints
    whiteClip
    blackClip
    homotopicReduction
    computeSKIZ
    geodesicThin
    geodesicThick
    rotatingGeodesicThick
    rotatingGeodesicThin
    fullGeodesicThick
    fullGeodesicThin
"""

from mamba import *
import unittest
import random

class TestThinthick(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
            
    def testDoubleStructuringElement(self):
        """Verifies the double structuring element class and its methods"""
        se1 = structuringElement([1,2,3,8], SQUARE)
        se2 = structuringElement([4,5,7], SQUARE)
        se3 = structuringElement([1,3], HEXAGONAL)
        se4 = structuringElement([5,6], HEXAGONAL)
        
        dse1 = doubleStructuringElement(se1, se2)
        idse1 = doubleStructuringElement(se2, se1)
        dse2 = doubleStructuringElement([1,2,3,8], [4,5,7], SQUARE)
        dse3 = doubleStructuringElement(se3, se4)
        dse4 = doubleStructuringElement([1,3], [5,6], HEXAGONAL)
        
        self.assertRaises(ValueError, doubleStructuringElement, se1, se3)
        self.assertRaises(ValueError, doubleStructuringElement, se1, se2, SQUARE, [1,2])
        
        self.assertNotEqual(repr(dse1), "")
        
        self.assertEqual(dse1.getGrid(), SQUARE)
        self.assertEqual(dse3.getGrid(), HEXAGONAL)
        
        self.assertEqual(dse2.getStructuringElement(0), se1)
        self.assertEqual(dse2.getStructuringElement(1), se2)
        self.assertEqual(dse4.getStructuringElement(0), se3)
        self.assertEqual(dse4.getStructuringElement(1), se4)
        
        self.assertEqual(dse1.getCSE(), (2+4+8+256,16+32+128))

        dse = dse1.rotate(1)
        self.assertEqual(dse.getStructuringElement(0), structuringElement([2,3,4,1], SQUARE))
        self.assertEqual(dse.getStructuringElement(1), structuringElement([5,6,8], SQUARE))
        dse = dse1.rotate(3)
        self.assertEqual(dse.getStructuringElement(0), structuringElement([4,5,6,3], SQUARE))
        self.assertEqual(dse.getStructuringElement(1), structuringElement([7,8,2], SQUARE))

        dse = dse1.flip()
        self.assertEqual(dse.getStructuringElement(0), se2)
        self.assertEqual(dse.getStructuringElement(1), se1)
        
    def testThin(self):
        """Verifies the thinning generic operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [0,3], mamba.SQUARE)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        drawLine(self.im1_1, (w-1, 0, w-1, h-1), 1)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 1)
        drawLine(self.im1_3, (w-1, 0, w-1, h-1), 1)
        thin(self.im1_1, self.im1_2, dse, EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 1)
        thin(self.im1_1, self.im1_2, dse, FILLED)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThick(self):
        """Verifies the thickening generic operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [3], mamba.SQUARE)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-2, h//2-1, w//2+1, h//2+1), 1)
        thick(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testRotatingThin(self):
        """Verifies the rotating thinning generic operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [2,3,4], mamba.SQUARE)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        drawLine(self.im1_1, (w-1, 0, w-1, h-1), 1)
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_3.setPixel(0, (w//2  ,h//2))
        self.im1_3.setPixel(0, (w//2-1,h//2))
        drawLine(self.im1_3, (w-1, 0, w-1, h-1), 1)
        rotatingThin(self.im1_1, self.im1_2, dse, EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_3.setPixel(0, (w//2  ,h//2))
        self.im1_3.setPixel(0, (w//2-1,h//2))
        rotatingThin(self.im1_1, self.im1_2, dse, FILLED)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testRotatingThick(self):
        """Verifies the rotating thickening generic operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [3], mamba.SQUARE)
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2  ,h//2))
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-3, h//2-1, w//2+3, h//2+1), 1)
        drawSquare(self.im1_3, (w//2-2, h//2-2, w//2+2, h//2+2), 1)
        drawSquare(self.im1_3, (w//2-1, h//2-3, w//2+1, h//2+3), 1)
        rotatingThick(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testInfThin(self):
        """Verifies the infimum of thinnings operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([2,4], [0,3], mamba.SQUARE)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_1.setPixel(1, (w//2+2, h//2))
        self.im1_1.setPixel(1, (w//2-2, h//2))
        self.im1_1.setPixel(1, (w//2, h//2+2))
        self.im1_1.setPixel(1, (w//2, h//2-2))
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_3.setPixel(1, (w//2+2, h//2))
        self.im1_3.setPixel(1, (w//2-2, h//2))
        self.im1_3.setPixel(0, (w//2+1, h//2))
        self.im1_3.setPixel(0, (w//2-1, h//2))
        self.im1_3.setPixel(1, (w//2, h//2+2))
        self.im1_3.setPixel(1, (w//2, h//2-2))
        self.im1_3.setPixel(0, (w//2, h//2+1))
        self.im1_3.setPixel(0, (w//2, h//2-1))
        
        infThin(self.im1_1, self.im1_2, dse, EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testSupThick(self):
        """Verifies the supremum of thickenings operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [3], mamba.SQUARE)
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2  ,h//2))
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        supThick(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testFullThin(self):
        """Verifies the full thinning operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [2,3,4], mamba.SQUARE)
        self.im1_1.fill(1)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w-1, 0, w-1, h-1), 1)
        drawLine(self.im1_3, (0, 0, w-1, 0), 1)
        drawLine(self.im1_3, (0, h-1, w-1, h-1), 1)
        fullThin(self.im1_1, self.im1_2, dse, EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        dse = doubleStructuringElement([2,4], [0,3], mamba.SQUARE)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_1.setPixel(1, (w//2+2, h//2))
        self.im1_1.setPixel(1, (w//2-2, h//2))
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2+1, h//2+1))
        self.im1_3.setPixel(1, (w//2-1, h//2-1))
        fullThin(self.im1_1, self.im1_2, dse, FILLED)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testFullThick(self):
        """Verifies the full thickening operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([], [3], mamba.SQUARE)
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2  ,h//2))
        
        self.im1_3.fill(1)
        fullThick(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThinL(self):
        """Verifes the thinning with a L double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2-1, h//2-1, w//2-1, h//2+1), 1)
        drawLine(self.im1_3, (w//2-1, h//2, w//2+1, h//2), 1)
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2), 1)
        thinL(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2-1, h//2, w//2+1, h//2), 1)
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2), 1)
        thinL(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThinM(self):
        """Verifes the thinning with a M double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2-1, h//2-1, w//2-1, h//2+1), 1)
        drawLine(self.im1_3, (w//2-1, h//2, w//2+1, h//2), 1)
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 1)
        thinM(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2, h//2, w//2+1, h//2), 1)
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 1)
        self.im1_3.setPixel(1, (w//2-1,h//2-1))
        self.im1_3.setPixel(1, (w//2-1,h//2+1))
        thinM(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThinD(self):
        """Verifes the thinning with a D double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2, h//2, w//2, h//2+1), 1)
        thinD(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2+1,h//2))
        thinD(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThickL(self):
        """Verifes the thickening with a L double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        negate(self.im1_1, self.im1_1)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2-1,h//2+1))
        drawLine(self.im1_3, (w//2-1, h//2, w//2+1, h//2), 0)
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 0)
        thickL(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2,h//2))
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 0)
        thickL(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThickM(self):
        """Verifes the thickening with a M double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        negate(self.im1_1, self.im1_1)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2,h//2))
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 0)
        drawLine(self.im1_3, (w//2-1, h//2-1, w//2-1, h//2+1), 0)
        thickM(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2-1,h//2-1))
        self.im1_3.setPixel(0, (w//2-1,h//2+1))
        drawLine(self.im1_3, (w//2+1, h//2-1, w//2+1, h//2+1), 0)
        drawLine(self.im1_3, (w//2, h//2, w//2+1, h//2), 0)
        thickM(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testThickD(self):
        """Verifes the thickening with a D double structuring element"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.fill(1)
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 0)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2,h//2))
        self.im1_3.setPixel(0, (w//2,h//2+1))
        thickD(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.fill(1)
        self.im1_3.setPixel(0, (w//2+1,h//2))
        thickD(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testEndPoints(self):
        """Verifies the ending points extractor operator"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawLine(self.im1_1, (w//2-2, h//2, w//2+2, h//2), 1)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2-2,h//2))
        self.im1_3.setPixel(1, (w//2+2,h//2))
        endPoints(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testMultiplePoints(self):
        """Verifies the multiple points extractor operator"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawLine(self.im1_1, (w//2-2, h//2, w//2+2, h//2), 1)
        drawLine(self.im1_1, (w//2, h//2-2, w//2, h//2+2), 1)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2,h//2))
        multiplePoints(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2,h//2))
        self.im1_3.setPixel(1, (w//2+1,h//2))
        self.im1_3.setPixel(1, (w//2,h//2-1))
        self.im1_3.setPixel(1, (w//2,h//2+1))
        multiplePoints(self.im1_1, self.im1_2, HEXAGONAL)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testWhiteClip(self):
        """Verifies the correct computation of a white clipping"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.fill(1)
        drawSquare(self.im1_1, (w//4-1,h//4-1,w//4+1,h//4+1), 0)
        drawSquare(self.im1_1, (w//4-1,3*h//4-1,w//4+1,3*h//4+1), 0)
        drawSquare(self.im1_1, (3*w//4-1,h//4-1,3*w//4+1,h//4+1), 0)
        drawSquare(self.im1_1, (3*w//4-1,3*h//4-1,3*w//4+1,3*h//4+1), 0)
        
        self.im1_3.fill(1)
        drawSquare(self.im1_3, (w//4-2,h//4-1,w//4+2,h//4+1), 0)
        drawSquare(self.im1_3, (w//4-1,h//4-2,w//4+1,h//4+2), 0)
        drawSquare(self.im1_3, (w//4-2,3*h//4-1,w//4+2,3*h//4+1), 0)
        drawSquare(self.im1_3, (w//4-1,3*h//4-2,w//4+1,3*h//4+2), 0)
        drawSquare(self.im1_3, (3*w//4-2,h//4-1,3*w//4+2,h//4+1), 0)
        drawSquare(self.im1_3, (3*w//4-1,h//4-2,3*w//4+1,h//4+2), 0)
        drawSquare(self.im1_3, (3*w//4-2,3*h//4-1,3*w//4+2,3*h//4+1), 0)
        drawSquare(self.im1_3, (3*w//4-1,3*h//4-2,3*w//4+1,3*h//4+2), 0)
        whiteClip(self.im1_1, self.im1_2, 1, grid=SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        drawLine(self.im1_3, (w//2,0,w//2,h-1), 1)
        drawLine(self.im1_3, (0,h//2,w-1,h//2), 1)
        whiteClip(self.im1_1, self.im1_2, grid=SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testBlackClip(self):
        """Verifies the correct computation of a black clipping"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.fill(0)
        drawSquare(self.im1_1, (w//4-1,h//4-1,w//4+1,h//4+1), 1)
        drawSquare(self.im1_1, (w//4-1,3*h//4-1,w//4+1,3*h//4+1), 1)
        drawSquare(self.im1_1, (3*w//4-1,h//4-1,3*w//4+1,h//4+1), 1)
        drawSquare(self.im1_1, (3*w//4-1,3*h//4-1,3*w//4+1,3*h//4+1), 1)
        
        self.im1_3.fill(0)
        drawSquare(self.im1_3, (w//4-2,h//4-1,w//4+2,h//4+1), 1)
        drawSquare(self.im1_3, (w//4-1,h//4-2,w//4+1,h//4+2), 1)
        drawSquare(self.im1_3, (w//4-2,3*h//4-1,w//4+2,3*h//4+1), 1)
        drawSquare(self.im1_3, (w//4-1,3*h//4-2,w//4+1,3*h//4+2), 1)
        drawSquare(self.im1_3, (3*w//4-2,h//4-1,3*w//4+2,h//4+1), 1)
        drawSquare(self.im1_3, (3*w//4-1,h//4-2,3*w//4+1,h//4+2), 1)
        drawSquare(self.im1_3, (3*w//4-2,3*h//4-1,3*w//4+2,3*h//4+1), 1)
        drawSquare(self.im1_3, (3*w//4-1,3*h//4-2,3*w//4+1,3*h//4+2), 1)
        blackClip(self.im1_1, self.im1_2, 1, grid=SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
        self.im1_3.fill(1)
        drawLine(self.im1_3, (w//2,0,w//2,h-1), 0)
        drawLine(self.im1_3, (0,h//2,w-1,h//2), 0)
        blackClip(self.im1_1, self.im1_2, grid=SQUARE)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0)
        
    def testHomotopicReduction(self):
        """Tests the homotopic reduction operator"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-3,h//2-2,w//2-1,h//2+2), 1)
        drawSquare(self.im1_1, (w//2-3,h//2-2,w//2+3,h//2), 1)
        drawSquare(self.im1_1, (w//2+1,h//2-2,w//2+3,h//2+2), 1)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2,h//2-1))
        homotopicReduction(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testComputeSKIZ(self):
        """Verifies the computation of the slow SKIZ operator"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self.im1_3.fill(1)
        drawLine(self.im1_3, (w//2,0,w//2,h-1), 0)
        drawLine(self.im1_3, (0,h//2,w-1,h//2), 0)
        computeSKIZ(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testGeodesicThin(self):
        """Verifies the geodesic thinning operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([3],[0,7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-6,h//2-1,w//2-4,h//2+1), 1)
        drawSquare(self.im1_1, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-6,h//2-1,w//2-5,h//2+1), 1)
        drawSquare(self.im1_3, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        geodesicThin(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testGeodesicThick(self):
        """Verifies the geodesic thickening operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([0,3],[7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-6,h//2-1,w//2-4,h//2+1), 1)
        drawSquare(self.im1_1, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-6,h//2-1,w//2-3,h//2+1), 1)
        drawSquare(self.im1_3, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        geodesicThick(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testRotatingGeodesicThin(self):
        """Verifies the rotating geodesic thinning operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([3],[0,7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-6,h//2-1,w//2-4,h//2+1), 1)
        drawSquare(self.im1_1, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2-5,h//2-1))
        self.im1_3.setPixel(1, (w//2+5,h//2-1))
        
        rotatingGeodesicThin(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testRotatingGeodesicThick(self):
        """Verifies the rotating geodesic thickening operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([0,3],[7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2-6,h//2))
        self.im1_1.setPixel(1, (w//2+6,h//2))
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-6,h//2-1,w//2-3,h//2+1), 1)
        self.im1_3.setPixel(1, (w//2-5,h//2-3))
        drawLine(self.im1_3, (w//2-6,h//2-2,w//2-4,h//2-2), 1)
        drawLine(self.im1_3, (w//2-6,h//2+2,w//2-4,h//2+2), 1)
        drawLine(self.im1_3, (w//2-6,h//2+3,w//2-5,h//2+3), 1)
        drawSquare(self.im1_3, (w//2+3,h//2-1,w//2+6,h//2+1), 1)
        drawLine(self.im1_3, (w//2+5,h//2-3,w//2+6,h//2-3), 1)
        drawLine(self.im1_3, (w//2+4,h//2-2,w//2+6,h//2-2), 1)
        drawLine(self.im1_3, (w//2+4,h//2+2,w//2+5,h//2+2), 1)
        
        rotatingGeodesicThick(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testFullGeodesicThin(self):
        """Verifies the full geodesic thinning operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([3],[0,7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-6,h//2-1,w//2-4,h//2+1), 1)
        drawSquare(self.im1_1, (w//2+4,h//2-1,w//2+6,h//2+1), 1)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (w//2-5,h//2-1))
        self.im1_3.setPixel(1, (w//2+5,h//2-1))
        
        fullGeodesicThin(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testFullGeodesicThick(self):
        """Verifies the full geodesic thickening operator"""
        (w,h) = self.im1_1.getSize()
        
        dse = doubleStructuringElement([0,3],[7],SQUARE)
        
        self.im1_4.reset()
        drawSquare(self.im1_4, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2-6,h//2))
        
        self.im1_3.reset()
        drawSquare(self.im1_3, (w//2-6,h//2-6,w//2+6,h//2+6), 1)
        
        fullGeodesicThick(self.im1_1, self.im1_4, self.im1_2, dse)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

