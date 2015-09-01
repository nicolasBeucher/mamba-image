"""
Test cases for the image supremum by vector function.

The function works on all images depths. All images, both input and output, must
have the same depth.

Here is the list of legal operations :
    supVector( 1, 1) = 1
    supVector( 8, 8) = 8
    supVector(32,32) =32
    
The result in output is the supremum value (see testSup for a definition). In
this case however, the pixels inside the second input image (which is also the 
output image) are compared with their corresponding pixel inside the first 
image after it had been moved by the specified vector.

The result depends on edge configuration.

Python function:
    supVector
    
C functions:
    MB_SupVectorb
    MB_SupVector8
    MB_SupVector32
"""

from mamba import *
import unittest
import random

class TestSupVector(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        
        self.directions = [
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
        del(self.im8s2_1)
        del(self.im8s2_2)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        #self.assertRaises(MambaError, supVector, self.im1_1, self.im1_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im1_1, self.im8_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im1_1, self.im32_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im8_1, self.im1_2,(0,1))
        #self.assertRaises(MambaError, supVector, self.im8_1, self.im8_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im8_1, self.im32_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im32_1, self.im1_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im32_1, self.im8_2,(0,1))
        #self.assertRaises(MambaError, supVector, self.im32_1, self.im32_2,(0,1))

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, supVector, self.im8s2_1, self.im8_2,(0,1))
        self.assertRaises(MambaError, supVector, self.im8_1, self.im8s2_2,(0,1))
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        self.assertRaises(TypeError, supVector, self.im1_1, self.im1_2, 5)
            
    def testComputation_1(self):
        """Tests supremum by vector computations on binary images"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(10):
            xi = random.randint(1,w//2-1)
            yi = random.randint(1,h//2-1)
            for vect in self.directions:
                self.im1_1.reset()
                self.im1_1.setPixel(1, (w//2,h//2))
                self.im1_2.reset()
                self.im1_2.setPixel(1, (w//2,h//2))
                self.im1_2.setPixel(1, (w//2+xi*vect[0],h//2+yi*vect[1]))
                supVector(self.im1_1, self.im1_1, (xi*vect[0],yi*vect[1]), edge=EMPTY)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
            
    def testComputation_8(self):
        """Tests supremum by vector computations on greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            xi = random.randint(1,w//2-1)
            yi = random.randint(1,h//2-1)
            wi = random.randint(0,255)
            for vect in self.directions:
                self.im8_1.fill(wi)
                self.im8_1.setPixel(255, (w//2,h//2))
                self.im8_2.fill(wi)
                self.im8_2.setPixel(255, (w//2,h//2))
                self.im8_2.setPixel(255, (w//2+xi*vect[0],h//2+yi*vect[1]))
                supVector(self.im8_1, self.im8_1, (xi*vect[0],yi*vect[1]), edge=EMPTY)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)

    def testComputation_32(self):
        """Tests supremum by vector computations on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(10):
            xi = random.randint(1,w//2-1)
            yi = random.randint(1,h//2-1)
            wi = random.randint(0,0xfffffffe)
            for vect in self.directions:
                self.im32_1.fill(wi)
                self.im32_1.setPixel(0xffffffff, (w//2,h//2))
                self.im32_2.fill(wi)
                self.im32_2.setPixel(0xffffffff, (w//2,h//2))
                self.im32_2.setPixel(0xffffffff, (w//2+xi*vect[0],h//2+yi*vect[1]))
                supVector(self.im32_1, self.im32_1, (xi*vect[0],yi*vect[1]), edge=EMPTY)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)
                
    def testEdgeEffect_1(self):
        """Verifies that edge value is correctly taken into account on binary image"""
        (w,h) = self.im1_1.getSize()
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d,vect in enumerate(self.directions):
            self.im1_1.reset()
            supVector(self.im1_1, self.im1_1, vect, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_1(self):
        """Verifies edge inocuity when computing binary image"""
        (w,h) = self.im1_1.getSize()
        for vect in self.directions:
            self.im1_1.fill(1)
            supVector(self.im1_1, self.im1_1, vect, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
        for vect in self.directions:
            self.im1_1.fill(0)
            supVector(self.im1_1, self.im1_1, vect, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, 0)
            self.im1_1.fill(1)
            supVector(self.im1_1, self.im1_1, vect, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
                
    def testEdgeEffect_8(self):
        """Verifies that edge value is correctly taken into account on 8-bit image"""
        (w,h) = self.im8_1.getSize()
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d,vect in enumerate(self.directions):
            self.im8_1.reset()
            supVector(self.im8_1, self.im8_1, vect, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol//255, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_8(self):
        """Verifies edge inocuity when computing 8-bit image"""
        (w,h) = self.im8_1.getSize()
        for vect in self.directions:
            self.im8_1.fill(255)
            supVector(self.im8_1, self.im8_1, vect, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
        for vect in self.directions:
            self.im8_1.fill(0)
            supVector(self.im8_1, self.im8_1, vect, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, 0)
            self.im8_1.fill(255)
            supVector(self.im8_1, self.im8_1, vect, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
                
    def testEdgeEffect_32(self):
        """Verifies that edge value is correctly taken into account on 32-bit image"""
        (w,h) = self.im32_1.getSize()
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d,vect in enumerate(self.directions):
            self.im32_1.reset()
            supVector(self.im32_1, self.im32_1, vect, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol//0xffffffff, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_32(self):
        """Verifies edge inocuity when computing 32-bit image"""
        (w,h) = self.im32_1.getSize()
        for vect in self.directions:
            self.im32_1.fill(0xffffffff)
            supVector(self.im32_1, self.im32_1, vect, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)
        for vect in self.directions:
            self.im32_1.fill(0)
            supVector(self.im32_1, self.im32_1, vect, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, 0)
            self.im32_1.fill(0xffffffff)
            supVector(self.im32_1, self.im32_1, vect, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)

