"""
Test cases for the various measure functions found in the measure
module of mamba package.

Python functions:
    computeArea
    computeDiameter
    computePerimeter
    computeConnectivityNumber
    computeComponentsNumber
    computeFeretDiameters
"""

from mamba import *
import unittest
import random
import math

class TestMeasure(unittest.TestCase):

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
            
    def testDepthAcceptance(self):
        """Verifies that the measure functions work only with binary images"""
        self.assertRaises(MambaError, computeArea, self.im8_1)
        self.assertRaises(MambaError, computeArea, self.im32_1)
        self.assertRaises(MambaError, computeDiameter, self.im8_1, 1)
        self.assertRaises(MambaError, computeDiameter, self.im32_1, 1)
        self.assertRaises(MambaError, computePerimeter, self.im8_1)
        self.assertRaises(MambaError, computePerimeter, self.im32_1)
        self.assertRaises(MambaError, computeConnectivityNumber, self.im8_1)
        self.assertRaises(MambaError, computeConnectivityNumber, self.im32_1)
        
    def testComputeArea(self):
        """Verifies the area computation function"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-1, h//2-1, w//2+1, h//2+1), 1)
        area = computeArea(self.im1_1)
        self.assertAlmostEqual(area,9.0, msg = "%f" %(area))
        
    def testComputeDiameter(self):
        """Verifies the diameter computation function"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-2, h//2-2, w//2+2, h//2+2), 1)
        diameter = computeDiameter(self.im1_1, 0, grid=SQUARE)
        self.assertEqual(diameter, 0.0)
        
        for i in getDirections(SQUARE)[1:]:
            exp_diameter = ((i%2)==0) and 9/math.sqrt(2) or 5
            diameter = computeDiameter(self.im1_1, i, grid=SQUARE)
            self.assertAlmostEqual(diameter,exp_diameter, msg = "%d %f %f" % (i, diameter, exp_diameter))
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//2))
        dilate(self.im1_1, self.im1_1, 2, se=HEXAGON)
        diameter = computeDiameter(self.im1_1, 0, grid=HEXAGONAL)
        self.assertEqual(diameter, 0.0)
        
        for i in getDirections(HEXAGONAL)[1:]:
            if i==2 or i==5:
                exp_diameter = 5.0
            else:
                exp_diameter = 10/math.sqrt(5)
            diameter = computeDiameter(self.im1_1, i, grid=HEXAGONAL)
            self.assertAlmostEqual(diameter,exp_diameter, msg = "%d %f %f" % (i, diameter, exp_diameter))
        
    def testComputePerimeter(self):
        """Verifies the perimeter computation function"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-2, h//2-2, w//2+2, h//2+2), 1)
        perimeter = computePerimeter(self.im1_1, grid=SQUARE)
        
        exp_perimeter = 0.0
        for i in getDirections(SQUARE)[1:5]:
            exp_diameter = ((i%2)==0) and 9/math.sqrt(2) or 5
            exp_perimeter += exp_diameter
        exp_perimeter = (exp_perimeter/4)*math.pi
        self.assertAlmostEqual(perimeter,exp_perimeter, msg = "%f %f" % (perimeter, exp_perimeter))
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//2))
        dilate(self.im1_1, self.im1_1, 2, se=HEXAGON)
        perimeter = computePerimeter(self.im1_1, grid=HEXAGONAL)
        
        exp_perimeter = 0.0
        for i in getDirections(HEXAGONAL)[1:4]:
            if i==2 or i==5:
                exp_diameter = 5.0
            else:
                exp_diameter = 10/math.sqrt(5)
            exp_perimeter += exp_diameter
        exp_perimeter = (exp_perimeter/3)*math.pi
        self.assertAlmostEqual(perimeter,exp_perimeter, msg = "%f %f" % (perimeter, exp_perimeter))
        
            
    def testComputeConnectivityNumber(self):
        """Verifies the connectivity number computation"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-30,h//2-30,w//2-28,h//2-28), 1)
        
        connb = computeConnectivityNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 1)
        connb = computeConnectivityNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 1)
        
        drawSquare(self.im1_1, (w//2-20,h//2-30,w//2+28,h//2+28), 1)
        
        connb = computeConnectivityNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 2)
        connb = computeConnectivityNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 2)
        
        drawBox(self.im1_1, (w//2-35,h//2-35,w//2+35,h//2+35), 1)
        
        connb = computeConnectivityNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 2)
        connb = computeConnectivityNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 2)
        
    def testComputeComponentsNumber(self):
        """Verifies the number of components computation"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-30,h//2-30,w//2-28,h//2-28), 1)
        
        connb = computeComponentsNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 1)
        connb = computeComponentsNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 1)
        
        drawSquare(self.im1_1, (w//2-20,h//2-30,w//2+28,h//2+28), 1)
        
        connb = computeComponentsNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 2)
        connb = computeComponentsNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 2)
        
        drawBox(self.im1_1, (w//2-35,h//2-35,w//2+35,h//2+35), 1)
        
        connb = computeComponentsNumber(self.im1_1, SQUARE)
        self.assertEqual(connb, 3)
        connb = computeComponentsNumber(self.im1_1, HEXAGONAL)
        self.assertEqual(connb, 3)
        
    def testComputeFeretDiameters(self):
        """Verifies the Feret diameters computation function"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2-10,h//2-30,w//2-8,h//2-28), 1)
        
        diams = computeFeretDiameters(self.im1_1)
        self.assertEqual(diams[0], 2)
        self.assertEqual(diams[1], 2)
        
        drawSquare(self.im1_1, (w//2-20,h//2-30,w//2+28,h//2+28), 1)
        
        diams = computeFeretDiameters(self.im1_1)
        self.assertEqual(diams[0], 48, "%s" % (str(diams)))
        self.assertEqual(diams[1], 58)
        
        drawBox(self.im1_1, (w//2-35,h//2-35,w//2+35,h//2+35), 1)
        
        diams = computeFeretDiameters(self.im1_1)
        self.assertEqual(diams[0], 70)
        self.assertEqual(diams[1], 70)

