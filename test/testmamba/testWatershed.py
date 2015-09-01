"""
Test cases for the image watershed segmentation function.

The function works on 8-bit images and returns in a 32-bit image, the watershed
segmentation (only the catchment basins and watershed lines) as found using 
the same 32-bit image as an initialisation for wells.

The function is idempotent. You can control the level reached by the flooding 
process.
    
Python function:
    watershedSegment
    
C function:
    MB_Watershed
"""

from mamba import *
import unittest
import random

class TestWatershed(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
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
        self.im32s2_1 = imageMb(128,128,32)
        
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
        del(self.im32s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, watershedSegment, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, watershedSegment, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, watershedSegment, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment, self.im8_1, self.im8_2)
        #self.assertRaises(MambaError, watershedSegment, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, watershedSegment, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, watershedSegment, self.im32_1, self.im8_2)
        #self.assertRaises(MambaError, watershedSegment, self.im32_1, self.im32_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, watershedSegment, self.im8s2_1, self.im32_1)
        self.assertRaises(MambaError, watershedSegment, self.im8_1, self.im32s2_1)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        for i in range(257,400):
            self.assertRaises(MambaError, watershedSegment, self.im8_1, self.im32_2, max_level=i)

    def testIdempotencySquare(self):
        """Makes sure the computed watershed is idempotent in square grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(25):
            # creating a random image
            for wi in range(w):
                for hi in range(h):
                    vi = random.randint(0,255)
                    self.im8_1.setPixel(vi, (wi,hi))
                    
            # adding 10 random well
            self.im32_1.reset()
            self.im32_2.reset()
            for vi in range(1,11):
                hi = random.randint(0,h-1)
                wi = random.randint((w*(vi-1))//10, (w*vi)//10-1)
                self.im32_1.setPixel(vi*10, (wi,hi))
                self.im32_2.setPixel(vi*10, (wi,hi))
            
            watershedSegment(self.im8_1, self.im32_1, grid=SQUARE)
            copyBytePlane(self.im32_1, 3, self.im8_2)
            copyBytePlane(self.im32_1, 0, self.im8_3)
            diff(self.im8_3, self.im8_2, self.im8_3)
            copyBytePlane(self.im8_3, 0, self.im32_2)
            watershedSegment(self.im8_1, self.im32_2, grid=SQUARE)
            copyBytePlane(self.im32_1, 3, self.im8_3)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

    def testComputationSquare(self):
        """Verifies that the watershed computation returns a correct line in square grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(w//4,(3*w)//4):
            # creating a wall image
            self.im8_1.reset()
            for hi in range(h):
                self.im8_1.setPixel(255, (i,hi))
                    
            # adding 2 well
            self.im32_1.reset()
            self.im32_1.setPixel(50, (w//4-1,h//2))
            self.im32_1.setPixel(100, ((3*w)//4,h//2))
            
            watershedSegment(self.im8_1, self.im32_1, grid=SQUARE)
            copyBytePlane(self.im32_1, 3, self.im8_2)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))

    def testIdempotencyHexagonal(self):
        """Makes sure the computed watershed is idempotent in hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(25):
            # creating a random image
            for wi in range(w):
                for hi in range(h):
                    vi = random.randint(0,255)
                    self.im8_1.setPixel(vi, (wi,hi))
                    
            # adding 10 random well
            self.im32_1.reset()
            self.im32_2.reset()
            for vi in range(1,11):
                hi = random.randint(0,h-1)
                wi = random.randint((w*(vi-1))//10, (w*vi)//10-1)
                self.im32_1.setPixel(vi*10, (wi,hi))
                self.im32_2.setPixel(vi*10, (wi,hi))
            
            watershedSegment(self.im8_1, self.im32_1, grid=HEXAGONAL)
            copyBytePlane(self.im32_1, 3, self.im8_2)
            copyBytePlane(self.im32_1, 0, self.im8_3)
            diff(self.im8_3, self.im8_2, self.im8_3)
            copyBytePlane(self.im8_3, 0, self.im32_2)
            watershedSegment(self.im8_1, self.im32_2, grid=HEXAGONAL)
            copyBytePlane(self.im32_1, 3, self.im8_3)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

    def testComputationHexagonal(self):
        """Verifies that the watershed computation returns a correct line in hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(w//4,(3*w)//4):
            # creating a wall image
            self.im8_1.reset()
            for hi in range(h):
                self.im8_1.setPixel(255, (i,hi))
                    
            # adding 2 well
            self.im32_1.reset()
            self.im32_1.setPixel(50, (w//4-1,h//2))
            self.im32_1.setPixel(100, ((3*w)//4,h//2))
            
            watershedSegment(self.im8_1, self.im32_1, grid=HEXAGONAL)
            copyBytePlane(self.im32_1, 3, self.im8_2)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))

    def testComputationControl(self):
        """Verifies that the waterlevel control parameter works correctly"""
        (w,h) = self.im8_1.getSize()
        
        for wi in range(w):
            for hi in range(h):
                self.im8_1.setPixel(wi, (wi,hi))
                
        for max_level in range(0,257):
                
            # adding well
            self.im32_1.reset()
            self.im32_1.setPixel(1, (0,0))
        
            watershedSegment(self.im8_1, self.im32_1, max_level=max_level)
            copyBytePlane(self.im32_1, 0, self.im8_2)
            if max_level==0:
                exp_vol = 256*h
            else:
                exp_vol = max(max_level*h,1)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, exp_vol)

    def testComputationInit(self):
        """Tests that the watershed correctly handles an image with values in MSByte"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(w//4,(3*w)//4):
            # creating a wall image
            self.im8_1.reset()
            for hi in range(h):
                self.im8_1.setPixel(255, (i,hi))
                    
            # adding 2 well
            self.im32_1.fill(0x01000000)
            self.im32_1.setPixel(0x01000000+50, (w//4-1,h//2))
            self.im32_1.setPixel(0x01000000+100, ((3*w)//4,h//2))
            
            watershedSegment(self.im8_1, self.im32_1, grid=SQUARE)
            copyBytePlane(self.im32_1, 3, self.im8_2)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))
            
    def _draw(self,im,draws,x,y):
        for j,line in enumerate(draws):
            for i,pixel in enumerate(line):
                im.setPixel(pixel, (x+i,y+j))
                
    def _get(self,im,x,y,w,h):
        draws = []
        for j in range(h):
            line = []
            for i in range(w):
                line.append(im.getPixel((x+i,y+j)))
            draws.append(line)
        return draws
        
    def testComputationButtonHole(self):
        """Tests that the watershed is correctly computed in a button hole"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.fill(7)
        self._draw(self.im8_1, [[2,2,2,2,2,2],
                                [7,7,7,7,7,7],
                                [2,7,5,6,2,2],
                                [2,6,5,6,2,2],
                                [2,2,6,4,3,2],
                                [2,2,3,4,2,2],
                                [2,2,2,2,4,2]], w//2, h//2)
        self.im32_1.reset()
        self._draw(self.im32_1,[[1,1,1,1,1,1],
                                [0,0,0,0,0,0],
                                [2,0,0,0,3,3],
                                [2,0,0,0,3,3],
                                [2,2,0,0,0,3],
                                [2,2,0,0,3,3],
                                [2,2,2,2,0,3]], w//2, h//2)
        
        watershedSegment(self.im8_1, self.im32_1, grid=HEXAGONAL)
        copyBytePlane(self.im32_1, 3, self.im8_2)
        obt_draws = self._get(self.im8_2, w//2, h//2, 6, 7)
        exp_draws = [[0,0,0,0,0,0],
                     [255,0,255,255,255,255],
                     [0,255,255,0,0,0],
                     [0,0,255,0,0,0],
                     [0,0,0,255,0,0],
                     [0,0,0,255,0,0],
                     [0,0,0,0,255,0]]
        self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
        copyBytePlane(self.im32_1, 0, self.im8_2)
        obt_draws = self._get(self.im8_2, w//2, h//2, 6, 7)
        exp_draws = [[1,1,1,1,1,1],
                     [1,1,1,1,1,1],
                     [2,1,3,3,3,3],
                     [2,2,3,3,3,3],
                     [2,2,2,3,3,3],
                     [2,2,2,3,3,3],
                     [2,2,2,2,3,3]]
        self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
            
    def testComputationThickWTS(self):
        """Tests that thick watershed are correctly computed by the operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.fill(6)
        self._draw(self.im8_1, [[2,6,2,6,2],[2,2,6,6,2],[6,6,6,6,6],[2,2,6,6,2],[2,6,2,6,2]], w//2, h//2+1)
        self.im32_1.reset()
        self._draw(self.im32_1, [[1,0,2,0,3],[1,1,0,0,3],[0,0,0,0,0],[4,4,0,0,5],[4,0,6,0,5]], w//2, h//2+1)
        
        watershedSegment(self.im8_1, self.im32_1, grid=HEXAGONAL)
        copyBytePlane(self.im32_1, 3, self.im8_2)
        obt_draws = self._get(self.im8_2, w//2, h//2+1, 5, 5)
        exp_draws = [[0,255,0,255,0],[0,0,255,255,0],[255,255,255,255,255],[0,0,255,255,0],[0,255,0,255,0]]
        self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
        
    def testwatershedSegmentSquare(self):
        """Verifies the 32-bit watershed segment operator with SQUARE grid"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(w//4,(3*w)//4):
            # creating a wall image
            self.im32_1.reset()
            self.im8_1.reset()
            for hi in range(h):
                self.im32_1.setPixel(127*(i-w//4+1), (i,hi))
                self.im8_1.setPixel(255, (i,hi))
                
            exp_vol = (i*50+(w-1-i)*100)*h
            exp_vol1 = exp_vol+50*h
            exp_vol2 = exp_vol+100*h
                    
            # adding 2 well
            self.im32_2.reset()
            self.im32_2.setPixel(50, (w//4-1,h//2))
            self.im32_2.setPixel(100, ((3*w)//4,h//2))
            
            if i%4==0:
                level = 127*(i-w//4+1)+1
                watershedSegment(self.im32_1, self.im32_2, max_level=level, grid=SQUARE)
                copyBytePlane(self.im32_2, 3, self.im8_2)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))
            elif i%4==1:
                level = 0
                watershedSegment(self.im32_1, self.im32_2, max_level=level, grid=SQUARE)
                copyBytePlane(self.im32_2, 3, self.im8_2)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))
            elif i%4==2:
                level = 128
                watershedSegment(self.im32_1, self.im32_2, max_level=level, grid=SQUARE)
                copyBytePlane(self.im32_2, 0, self.im8_2)
                vol = computeVolume(self.im8_2)
                self.assertEqual(exp_vol, vol)
                copyBytePlane(self.im32_2, 3, self.im8_2)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertGreater(x, 0)
            else:
                level = 384
                watershedSegment(self.im32_1, self.im32_2, max_level=level, grid=SQUARE)
                copyBytePlane(self.im32_2, 0, self.im8_2)
                vol = computeVolume(self.im8_2)
                self.assertEqual(exp_vol, vol)
                copyBytePlane(self.im32_2, 3, self.im8_2)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertGreater(x, 0)

    def testwatershedSegmentHexagonal(self):
        """Verifies the 32-bit watershed segment operator with HEXAGONAL grid"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(w//4,(3*w)//4):
            # creating a wall image
            self.im32_1.reset()
            self.im8_1.reset()
            for hi in range(h):
                self.im32_1.setPixel(5000, (i,hi))
                self.im8_1.setPixel(255, (i,hi))
                    
            # adding 2 well
            self.im32_2.reset()
            self.im32_2.setPixel(50, (w//4-1,h//2))
            self.im32_2.setPixel(100, ((3*w)//4,h//2))
            
            if i%2==0:
                level = 5001
            else:
                level = 0
            watershedSegment(self.im32_1, self.im32_2, max_level=level, grid=HEXAGONAL)
            copyBytePlane(self.im32_2, 3, self.im8_2)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "wall at %d [%d,%d]: %d,%d" %(i,w//4,(3*w)//4,x,y))
            
    def _draw(self,im,draws,x,y):
        for j,line in enumerate(draws):
            for i,pixel in enumerate(line):
                im.setPixel(pixel, (x+i,y+j))
                
    def _get(self,im,x,y,w,h):
        draws = []
        for j in range(h):
            line = []
            for i in range(w):
                line.append(im.getPixel((x+i,y+j)))
            draws.append(line)
        return draws
        
    def testwatershedSegmentButtonHole(self):
        """Tests that the watershed 32-bit is correctly computed in a button hole"""
        (w,h) = self.im32_1.getSize()

        for i in range(4):
            self.im32_1.fill(7)
            self._draw(self.im32_1, [[2,2,2,2,2,2],
                                    [7,7,7,7,7,7],
                                    [2,7,5,6,2,2],
                                    [2,6,5,6,2,2],
                                    [2,2,6,4,3,2],
                                    [2,2,3,4,2,2],
                                    [2,2,2,2,4,2]], w//2, h//2)
            mulConst(self.im32_1, random.randint(20,105), self.im32_1)
            self.im32_2.reset()
            self._draw(self.im32_2,[[1,1,1,1,1,1],
                                    [0,0,0,0,0,0],
                                    [2,0,0,0,3,3],
                                    [2,0,0,0,3,3],
                                    [2,2,0,0,0,3],
                                    [2,2,0,0,3,3],
                                    [2,2,2,2,0,3]], w//2, h//2)
            
            watershedSegment(self.im32_1, self.im32_2, grid=HEXAGONAL)
            copyBytePlane(self.im32_2, 3, self.im8_2)
            obt_draws = self._get(self.im8_2, w//2, h//2, 6, 7)
            exp_draws = [[0,0,0,0,0,0],
                         [255,0,255,255,255,255],
                         [0,255,255,0,0,0],
                         [0,0,255,0,0,0],
                         [0,0,0,255,0,0],
                         [0,0,0,255,0,0],
                         [0,0,0,0,255,0]]
            self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
            copyBytePlane(self.im32_2, 0, self.im8_2)
            obt_draws = self._get(self.im8_2, w//2, h//2, 6, 7)
            exp_draws = [[1,1,1,1,1,1],
                         [1,1,1,1,1,1],
                         [2,1,3,3,3,3],
                         [2,2,3,3,3,3],
                         [2,2,2,3,3,3],
                         [2,2,2,3,3,3],
                         [2,2,2,2,3,3]]
            self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
            
    def testwatershedSegmentThickWTS(self):
        """Tests that thick watershed are correctly computed by the 32-bit operator"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(4):
            self.im32_1.fill(6)
            self._draw(self.im32_1, [[2,6,2,6,2],
                                     [2,2,6,6,2],
                                     [6,6,6,6,6],
                                     [2,2,6,6,2],
                                     [2,6,2,6,2]], w//2, h//2+1)
            mulConst(self.im32_1, random.randint(20,105), self.im32_1)
            self.im32_2.reset()
            self._draw(self.im32_2, [[1,0,2,0,3],
                                     [1,1,0,0,3],
                                     [0,0,0,0,0],
                                     [4,4,0,0,5],
                                     [4,0,6,0,5]], w//2, h//2+1)
            
            watershedSegment(self.im32_1, self.im32_2, grid=HEXAGONAL)
            copyBytePlane(self.im32_2, 3, self.im8_2)
            obt_draws = self._get(self.im8_2, w//2, h//2+1, 5, 5)
            exp_draws = [[0,255,0,255,0],[0,0,255,255,0],[255,255,255,255,255],[0,0,255,255,0],[0,255,0,255,0]]
            self.assertEqual(obt_draws, exp_draws, "%s!=%s" % (str(obt_draws), str(exp_draws)))
            

