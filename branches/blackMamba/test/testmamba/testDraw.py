"""
Test cases for the drawing functions found in the mambaDraw module.

Python functions and classes:
    drawLine
    drawBox
    drawSquare
    drawCircle
    drawFillCircle
    getIntensityAlongLine
"""

from mamba import *
import unittest
import random

class TestDraw(unittest.TestCase):

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
            
    def testDrawLine(self):
        """Verifies the line drawing function"""
        (w,h) = self.im8_1.getSize()
        
        size = 5
        l = [(-size,-size), (-size,0), (-size,size),
             (0,-size), (0,0), (0,size),
             (size,-size), (size,0), (size,size)]
        for el in l:
            self.im8_1.reset()
            drawLine(self.im8_1, (w//2,h//2,w//2+el[0],h//2+el[1]), 255)
            vol = computeVolume(self.im8_1)
            if el[0]==0 and el[1]==0:
                self.assertEqual(vol, 255)
            else:
                self.assertEqual(vol, 255*(size+1), "%d %d" %(vol,255*(size+1)))
    
    def testDrawBox(self):
        """Tests the empty square (box) drawing function"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            size = random.randint(10,20)
            vi = random.randint(1,255)
            self.im8_1.reset()
            drawBox(self.im8_1, (w//2-size,h//2-size,w//2+size,h//2+size), vi)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*(8*size), "%d %d %d %d" %(vol,vi,size,vi*(8*size)))
            self.im8_2.reset()
            drawBox(self.im8_2, (w//2+size,h//2+size,w//2-size,h//2-size), vi)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
    
    def testDrawSquare(self):
        """Tests the filled square drawing function"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            size = random.randint(10,20)
            vi = random.randint(1,255)
            self.im8_1.reset()
            drawSquare(self.im8_1, (w//2-size,h//2-size,w//2+size,h//2+size), vi)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*(2*size+1)*(2*size+1), "%d %d %d %d" %(vol,vi,size,vi*(2*size+1)*(2*size+1)))
            self.im8_2.reset()
            drawSquare(self.im8_2, (w//2+size,h//2+size,w//2-size,h//2-size), vi)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
    
    def testDrawCircle(self):
        """Tests the circle drawing function"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            size = random.randint(10,20)
            vi = random.randint(1,255)
            self.im8_1.reset()
            drawCircle(self.im8_1, (w//2,h//2,size), vi)
            vol = computeVolume(self.im8_1)
            self.im8_2.reset()
            drawCircle(self.im8_2, (w//2,h//2,size), vi)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
    
    def testDrawFillCircle(self):
        """Tests the circle drawing function"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(10):
            size = random.randint(10,20)
            vi = random.randint(1,255)
            self.im8_1.reset()
            drawFillCircle(self.im8_1, (w//2,h//2,size), vi)
            vol = computeVolume(self.im8_1)
            self.im8_2.reset()
            drawFillCircle(self.im8_2, (w//2,h//2,size), vi)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testGetIntensityAlongLine(self):
        """Verifies the intensity on a line extraction function"""
        (w,h) = self.im8_1.getSize()
        
        size = 5
        l = [(-size,-size), (-size,0), (-size,size),
             (0,-size), (0,0), (0,size),
             (size,-size), (size,0), (size,size)]
        
        for i in range(w):
            drawLine(self.im8_1, (i,0,i,h-1), i)
        for el in l:
            intensity = getIntensityAlongLine(self.im8_1, (w//2,h//2,w//2+el[0],h//2+el[1]))
            if el[0]==0 and el[1]==0:
                exp_intensity = [w//2]
            elif el[0]==0:
                exp_intensity = (size+1)*[w//2]
            elif el[0]>0: 
                exp_intensity = list(range(w//2,w//2+size+1))
            else: 
                exp_intensity = list(range(w//2,w//2-size-1,-1))
            self.assertEqual(intensity, exp_intensity, "%d,%d : %s %s" %(el[0],el[1],repr(intensity),repr(exp_intensity)))
        
        for i in range(h):
            drawLine(self.im8_1, (0,i,w-1,i), i)
        for el in l:
            intensity = getIntensityAlongLine(self.im8_1, (w//2,h//2,w//2+el[0],h//2+el[1]))
            if el[0]==0 and el[1]==0:
                exp_intensity = [h//2]
            elif el[1]==0:
                exp_intensity = (size+1)*[h//2]
            elif el[1]>0: 
                exp_intensity = list(range(h//2,h//2+size+1))
            else: 
                exp_intensity = list(range(h//2,h//2-size-1,-1))
            self.assertEqual(intensity, exp_intensity, "%d,%d : %s %s" %(el[0],el[1],repr(intensity),repr(exp_intensity)))

