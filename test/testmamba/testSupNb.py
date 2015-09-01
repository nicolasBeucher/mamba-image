"""
Test cases for the image supremum by neighbor function.

The function works on all images depths. All images, both input and output, must
have the same depth.

Here is the list of legal operations :
    supNeighbor( 1, 1) = 1
    supNeighbor( 8, 8) = 8
    supNeighbor(32,32) =32
    
The result in output is the supremum value (see testSup for a definition). In
this case however, the pixels inside the second input image (which is also the 
output image) are compared with their neighbor (specified to the function) 
inside the first image.

The result depends on grid and edge configurations. Allowed values for neighbor
are restricted according to grid configuration.

Python function:
    supNeighbor
    
C functions:
    MB_SupNbb
    MB_SupNb8
    MB_SupNb32
"""

from mamba import *
import unittest
import functools
import random

class TestSupNb(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im1_5 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im8_5 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im32_4 = imageMb(32)
        self.im32_5 = imageMb(32)
        self.im1s2_1 = imageMb(128,128,1)
        self.im1s2_2 = imageMb(128,128,1)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im32s2_1 = imageMb(128,128,32)
        self.im32s2_2 = imageMb(128,128,32)
        
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
        del(self.im1s2_1)
        del(self.im1s2_2)
        del(self.im8s2_1)
        del(self.im8s2_2)
        del(self.im32s2_1)
        del(self.im32s2_2)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        #self.assertRaises(MambaError, supNeighbor, self.im1_1, self.im1_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im1_1, self.im8_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im1_1, self.im32_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im8_1, self.im1_2,1)
        #self.assertRaises(MambaError, supNeighbor, self.im8_1, self.im8_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im8_1, self.im32_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im32_1, self.im1_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im32_1, self.im8_2,1)
        #self.assertRaises(MambaError, supNeighbor, self.im32_1, self.im32_2,1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, supNeighbor, self.im8s2_1, self.im8_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im8_1, self.im8s2_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im1s2_1, self.im1_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im1_1, self.im1s2_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im32s2_1, self.im32_2,1)
        self.assertRaises(MambaError, supNeighbor, self.im32_1, self.im32s2_2,1)
            
    def _shiftMat(self, mat, d, fill=0):
        ret_mat = [[fill,fill,fill],[fill,fill,fill],[fill,fill,fill]]
        dx, dy = self.directions[d]
        for i in range(3):
            for j in range(3):
                if j+dy>=0 and j+dy<3 and i+dx>=0 and i+dx<3:
                    ret_mat[j][i] = mat[j+dy][i+dx]
        
        return ret_mat

    def _copyMat(self, mat):
        ret_mat = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            for j in range(3):
                ret_mat[j][i] = mat[j][i]
        return ret_mat

    def _supMat(self, mat1, mat2):
        ret_mat = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            for j in range(3):
                ret_mat[j][i] = max(mat1[j][i],mat2[j][i])
        
        return ret_mat

    def _drawMat(self, im, mat, x, y):
        # draws a matrix centered in x,y
        for i in range(3):
            for j in range(3):
                im.setPixel(mat[j][i], ((x-1)+i, (y-1)+j))

    def testComputationOneSquare_1(self):
        """Tests supremum by one neighbor computations in square grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[0,0,0],[0,0,0],[0,0,0]]
        
        for wi in range(1,w-1):
            for d in getDirections(SQUARE):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self._drawMat(self.im1_1, mat, wi, 10)
                mat_shi = self._shiftMat(mat, d, fill=1)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im1_2, mat_exp, wi, 10)
                supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self._drawMat(self.im1_1, mat, wi, 13)
                mat_shi = self._shiftMat(mat, d, fill=1)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im1_2, mat_exp, wi, 13)
                supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)

    def testComputationMultiSquare_1(self):
        """Tests supremum by multiple neighbors computations in square grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[0,0,0],[0,0,0],[0,0,0]]

        dirs = getDirections(SQUARE)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im1_1.fill(1)
            self.im1_2.fill(1)
            self._drawMat(self.im1_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=1)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im1_2, mat_exp, wi, 10)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im1_1.fill(1)
            self.im1_2.fill(1)
            self._drawMat(self.im1_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=1)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im1_2, mat_exp, wi, 13)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0)

    def testComputationAllSquare_1(self):
        """Tests supremum by all neighbors computations in square grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[1,1,1],[1,1,1],[1,1,1]]

        dirs = getDirections(SQUARE)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im1_1.reset()
            self.im1_2.reset()
            self.im1_1.setPixel(1, (wi, 10))
            self._drawMat(self.im1_2, mat, wi, 10)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im1_1.reset()
            self.im1_2.reset()
            self.im1_1.setPixel(1, (wi, 13))
            self._drawMat(self.im1_2, mat, wi, 13)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))

    def testComputationOneSquare_8(self):
        """Tests supremum by one neighbor computations in square grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        mat = [[9,2,3],[8,1,4],[7,6,5]]
        
        for wi in range(1,w-1):
            for d in getDirections(SQUARE):
                self.im8_1.fill(255)
                self.im8_2.fill(255)
                self._drawMat(self.im8_1, mat, wi, 10)
                mat_shi = self._shiftMat(mat, d, fill=255)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im8_2, mat_exp, wi, 10)
                supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im8_1.fill(255)
                self.im8_2.fill(255)
                self._drawMat(self.im8_1, mat, wi, 13)
                mat_shi = self._shiftMat(mat, d, fill=255)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im8_2, mat_exp, wi, 13)
                supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)

    def testComputationMultiSquare_8(self):
        """Tests supremum by multiple neighbors computations in square grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        mat = [[9,2,3],[8,1,4],[7,6,5]]

        dirs = getDirections(SQUARE)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im8_1.fill(255)
            self.im8_2.fill(255)
            self._drawMat(self.im8_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=255)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im8_2, mat_exp, wi, 10)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im8_1.fill(255)
            self.im8_2.fill(255)
            self._drawMat(self.im8_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=255)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im8_2, mat_exp, wi, 13)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0)

    def testComputationAllSquare_8(self):
        """Tests supremum by all neighbors computations in square grid on 8-bit images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[255,255,255],[255,255,255],[255,255,255]]

        dirs = getDirections(SQUARE)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im8_1.reset()
            self.im8_2.reset()
            self.im8_1.setPixel(255, (wi, 10))
            self._drawMat(self.im8_2, mat, wi, 10)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im8_1.reset()
            self.im8_2.reset()
            self.im8_1.setPixel(255, (wi, 13))
            self._drawMat(self.im8_2, mat, wi, 13)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))

    def testComputationOneSquare_32(self):
        """Tests supremum by one neighbor computations in square grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        mat = [[9000000,2,30],[800008,10,400],[70000,6666,5000]]
        
        for wi in range(1,w-1):
            for d in getDirections(SQUARE):
                self.im32_1.fill(0xffffffff)
                self.im32_2.fill(0xffffffff)
                self._drawMat(self.im32_1, mat, wi, 10)
                mat_shi = self._shiftMat(mat, d, fill=0xffffffff)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im32_2, mat_exp, wi, 10)
                supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im32_1.fill(0xffffffff)
                self.im32_2.fill(0xffffffff)
                self._drawMat(self.im32_1, mat, wi, 13)
                mat_shi = self._shiftMat(mat, d, fill=0xffffffff)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im32_2, mat_exp, wi, 13)
                supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=FILLED)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)

    def testComputationMultiSquare_32(self):
        """Tests supremum by multiple neighbors computations in square grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        mat = [[9000000,2,30],[800008,10,400],[70000,6666,5000]]
        
        dirs = getDirections(SQUARE)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im32_1.fill(0xffffffff)
            self.im32_2.fill(0xffffffff)
            self._drawMat(self.im32_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=0xffffffff)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im32_2, mat_exp, wi, 10)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im32_1.fill(0xffffffff)
            self.im32_2.fill(0xffffffff)
            self._drawMat(self.im32_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMat(mat, d, fill=0xffffffff)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im32_2, mat_exp, wi, 13)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=SQUARE, edge=FILLED)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0)

    def testComputationAllSquare_32(self):
        """Tests supremum by all neighbors computations in square grid on 32-bit images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[0xffffffff,0xffffffff,0xffffffff],
               [0xffffffff,0xffffffff,0xffffffff],
               [0xffffffff,0xffffffff,0xffffffff]]

        dirs = getDirections(SQUARE)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im32_1.reset()
            self.im32_2.reset()
            self.im32_1.setPixel(0xffffffff, (wi, 10))
            self._drawMat(self.im32_2, mat, wi, 10)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im32_1.reset()
            self.im32_2.reset()
            self.im32_1.setPixel(0xffffffff, (wi, 13))
            self._drawMat(self.im32_2, mat, wi, 13)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=SQUARE, edge=EMPTY)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
                
    def _shiftMatHE(self, mat, d, fill=0):
        if d==0:
            ret_mat = mat[:]
        elif d==1:
            ret_mat = [[fill,fill,fill],mat[0][:], mat[1][1:3]+[fill]]
        elif d==2:
            ret_mat = self._shiftMat(mat, 3, fill)
        elif d==3:
            ret_mat = [mat[1][1:3]+[fill],mat[2][:],[fill,fill,fill]]
        elif d==4:
            ret_mat = [mat[1][:],[fill]+mat[2][0:2],[fill,fill,fill]]
        elif d==5:
            ret_mat = self._shiftMat(mat, 7, fill)
        elif d==6:
            ret_mat = [[fill,fill,fill],[fill]+mat[0][0:2], mat[1][:]]
        else:
            self.assertTrue(False, "Invalid directions in Hexagonal grid")
        
        return ret_mat
                
    def _shiftMatHO(self, mat, d, fill=0):
        if d==0:
            ret_mat = mat[:]
        elif d==1:
            ret_mat = [[fill,fill,fill],mat[0][1:3]+[fill], mat[1][:]]
        elif d==2:
            ret_mat = self._shiftMat(mat, 3, fill)
        elif d==3:
            ret_mat = [mat[1][:],mat[2][1:3]+[fill],[fill,fill,fill]]
        elif d==4:
            ret_mat = [[fill]+mat[1][0:2],mat[2][:],[fill,fill,fill]]
        elif d==5:
            ret_mat = self._shiftMat(mat, 7, fill)
        elif d==6:
            ret_mat = [[fill,fill,fill],mat[0][:], [fill]+mat[1][0:2]]
        else:
            self.assertTrue(False, "Invalid directions in Hexagonal grid")
        
        return ret_mat

    def testComputationOneHexagonal_1(self):
        """Tests supremum by one neighbor computations in hexagonal grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[0,0,0],[0,0,0],[0,0,0]]
        
        for wi in range(1,w-1):
            for d in getDirections(HEXAGONAL):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self._drawMat(self.im1_1, mat, wi, 10)
                mat_shi = self._shiftMatHE(mat, d, fill=1)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im1_2, mat_exp, wi, 10)
                supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
            for d in getDirections(HEXAGONAL):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self._drawMat(self.im1_1, mat, wi, 13)
                mat_shi = self._shiftMatHO(mat, d, fill=1)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im1_2, mat_exp, wi, 13)
                supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0, "(%d,10) in dir %d" %(wi,d))

    def testComputationMultiHexagonal_1(self):
        """Tests supremum by multiple neighbors computations in hexagonal grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat = [[0,0,0],[0,0,0],[0,0,0]]

        dirs = getDirections(HEXAGONAL)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im1_1.fill(1)
            self.im1_2.fill(1)
            self._drawMat(self.im1_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHE(mat, d, fill=1)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im1_2, mat_exp, wi, 10)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im1_1.fill(1)
            self.im1_2.fill(1)
            self._drawMat(self.im1_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHO(mat, d, fill=1)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im1_2, mat_exp, wi, 13)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))

    def testComputationAllHexagonal_1(self):
        """Tests supremum by all neighbors computations in hexagonal grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        mat_odd = [[0,1,1],[1,1,1],[0,1,1]]
        mat_even = [[1,1,0],[1,1,1],[1,1,0]]

        dirs = getDirections(HEXAGONAL)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im1_1.reset()
            self.im1_2.reset()
            self.im1_1.setPixel(1, (wi, 10))
            self._drawMat(self.im1_2, mat_even, wi, 10)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im1_1.reset()
            self.im1_2.reset()
            self.im1_1.setPixel(1, (wi, 13))
            self._drawMat(self.im1_2, mat_odd, wi, 13)
            supNeighbor(self.im1_1, self.im1_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))

    def testComputationOneHexagonal_8(self):
        """Tests supremum by one neighbor computations in hexagonal grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        mat = [[9,2,3],[8,1,4],[7,6,5]]
        
        for wi in range(1,w-1):
            for d in getDirections(HEXAGONAL):
                self.im8_1.fill(255)
                self.im8_2.fill(255)
                self._drawMat(self.im8_1, mat, wi, 10)
                mat_shi = self._shiftMatHE(mat, d, fill=255)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im8_2, mat_exp, wi, 10)
                supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
            for d in getDirections(HEXAGONAL):
                self.im8_1.fill(255)
                self.im8_2.fill(255)
                self._drawMat(self.im8_1, mat, wi, 13)
                mat_shi = self._shiftMatHO(mat, d, fill=255)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im8_2, mat_exp, wi, 13)
                supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)

    def testComputationMultiHexagonal_8(self):
        """Tests supremum by multiple neighbors computations in hexagonal grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        mat = [[9,2,3],[8,1,4],[7,6,5]]

        dirs = getDirections(HEXAGONAL)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im8_1.fill(255)
            self.im8_2.fill(255)
            self._drawMat(self.im8_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHE(mat, d, fill=255)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im8_2, mat_exp, wi, 10)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im8_1.fill(255)
            self.im8_2.fill(255)
            self._drawMat(self.im8_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHO(mat, d, fill=255)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im8_2, mat_exp, wi, 13)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))

    def testComputationAllHexagonal_8(self):
        """Tests supremum by all neighbors computations in hexagonal grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        mat_odd = [[0,255,255],[255,255,255],[0,255,255]]
        mat_even = [[255,255,0],[255,255,255],[255,255,0]]

        dirs = getDirections(HEXAGONAL)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im8_1.reset()
            self.im8_2.reset()
            self.im8_1.setPixel(255, (wi, 10))
            self._drawMat(self.im8_2, mat_even, wi, 10)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im8_1.reset()
            self.im8_2.reset()
            self.im8_1.setPixel(255, (wi, 13))
            self._drawMat(self.im8_2, mat_odd, wi, 13)
            supNeighbor(self.im8_1, self.im8_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))

    def testComputationOneHexagonal_32(self):
        """Tests supremum by one neighbor computations in hexagonal grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        mat = [[9000000,2,30],[800008,10,400],[70000,6666,5000]]
        
        for wi in range(1,w-1):
            for d in getDirections(HEXAGONAL):
                self.im32_1.fill(0xffffffff)
                self.im32_2.fill(0xffffffff)
                self._drawMat(self.im32_1, mat, wi, 10)
                mat_shi = self._shiftMatHE(mat, d, 0xffffffff)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im32_2, mat_exp, wi, 10)
                supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0, "dir : %d %d (%d,%d)" % (d,wi,x,y))
            for d in getDirections(HEXAGONAL):
                self.im32_1.fill(0xffffffff)
                self.im32_2.fill(0xffffffff)
                self._drawMat(self.im32_1, mat, wi, 13)
                mat_shi = self._shiftMatHO(mat, d, 0xffffffff)
                mat_exp = self._supMat(mat, mat_shi)
                self._drawMat(self.im32_2, mat_exp, wi, 13)
                supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)

    def testComputationMultiHexagonal_32(self):
        """Tests supremum by multiple neighbors computations in hexagonal grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        mat = [[9000000,2,30],[800008,10,400],[70000,6666,5000]]

        dirs = getDirections(HEXAGONAL)
        
        for wi in range(1,w-1):
            ds = random.sample(dirs,3)
            dse = functools.reduce(lambda x,y: x|(1<<y), ds, 0)
            self.im32_1.fill(0xffffffff)
            self.im32_2.fill(0xffffffff)
            self._drawMat(self.im32_1, mat, wi, 10)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHE(mat, d, 0xffffffff)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im32_2, mat_exp, wi, 10)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))
            self.im32_1.fill(0xffffffff)
            self.im32_2.fill(0xffffffff)
            self._drawMat(self.im32_1, mat, wi, 13)
            mat_exp = self._copyMat(mat)
            for d in ds:
                mat_shi = self._shiftMatHO(mat, d, 0xffffffff)
                mat_exp = self._supMat(mat_exp, mat_shi)
            self._drawMat(self.im32_2, mat_exp, wi, 13)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=HEXAGONAL, edge=FILLED)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %s %04x" % (wi,x,y,str(ds),dse))

    def testComputationAllHexagonal_32(self):
        """Tests supremum by all neighbors computations in hexagonal grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        mat_odd = [[0         ,0xffffffff,0xffffffff],
                   [0xffffffff,0xffffffff,0xffffffff],
                   [0         ,0xffffffff,0xffffffff]]
        mat_even = [[0xffffffff,0xffffffff,0         ],
                    [0xffffffff,0xffffffff,0xffffffff],
                    [0xffffffff,0xffffffff,0         ]]

        dirs = getDirections(HEXAGONAL)
        for wi in range(1,w-1):
            dse = functools.reduce(lambda x,y: x|(1<<y), dirs, 0)
            self.im32_1.reset()
            self.im32_2.reset()
            self.im32_1.setPixel(0xffffffff, (wi, 10))
            self._drawMat(self.im32_2, mat_even, wi, 10)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
            self.im32_1.reset()
            self.im32_2.reset()
            self.im32_1.setPixel(0xffffffff, (wi, 13))
            self._drawMat(self.im32_2, mat_odd, wi, 13)
            supNeighbor(self.im32_1, self.im32_1, dse, grid=HEXAGONAL, edge=EMPTY)
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0, "%d : (%d,%d) - %04x" % (wi,x,y,dse))
                
    def testEdgeEffect_1(self):
        """Verifies that edge value is correctly taken into account on binary image"""
        (w,h) = self.im1_1.getSize()
        exp_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            self.im1_1.reset()
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d in getDirections(SQUARE):
            self.im1_1.reset()
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_1(self):
        """Verifies edge inocuity when computing binary image"""
        (w,h) = self.im1_1.getSize()
        for d in getDirections(HEXAGONAL):
            self.im1_1.fill(1)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
        for d in getDirections(SQUARE):
            self.im1_1.fill(1)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
        for d in getDirections(HEXAGONAL):
            self.im1_1.fill(0)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, 0)
            self.im1_1.fill(1)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
        for d in getDirections(SQUARE):
            self.im1_1.fill(0)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, 0)
            self.im1_1.fill(1)
            supNeighbor(self.im1_1, self.im1_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
                
    def testEdgeEffect_8(self):
        """Verifies that edge value is correctly taken into account on 8-bit image"""
        (w,h) = self.im8_1.getSize()
        exp_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            self.im8_1.reset()
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol//255, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d in getDirections(SQUARE):
            self.im8_1.reset()
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol//255, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_8(self):
        """Verifies edge inocuity when computing 8-bit image"""
        (w,h) = self.im8_1.getSize()
        for d in getDirections(HEXAGONAL):
            self.im8_1.fill(255)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
        for d in getDirections(SQUARE):
            self.im8_1.fill(255)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
        for d in getDirections(HEXAGONAL):
            self.im8_1.fill(0)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, 0)
            self.im8_1.fill(255)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
        for d in getDirections(SQUARE):
            self.im8_1.fill(0)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, 0)
            self.im8_1.fill(255)
            supNeighbor(self.im8_1, self.im8_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, w*h*255)
                
    def testEdgeEffect_32(self):
        """Verifies that edge value is correctly taken into account on 32-bit image"""
        (w,h) = self.im32_1.getSize()
        exp_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            self.im32_1.fill(0)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol//0xffffffff, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
        exp_volume = [0, w, h+w-1, h, w+h-1, w, w+h-1, h, h+w-1]
        for d in getDirections(SQUARE):
            self.im32_1.fill(0)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol//0xffffffff, exp_volume[d], "%d : %d/%d [%d]" % (d,vol,exp_volume[d],w*h))
                
    def testEdgeInocuity_32(self):
        """Verifies edge inocuity when computing 32-bit image"""
        (w,h) = self.im32_1.getSize()
        for d in getDirections(HEXAGONAL):
            self.im32_1.fill(0xffffffff)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)
        for d in getDirections(SQUARE):
            self.im32_1.fill(0xffffffff)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=FILLED)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)
        for d in getDirections(HEXAGONAL):
            self.im32_1.fill(0)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, 0)
            self.im32_1.fill(0xffffffff)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=HEXAGONAL, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)
        for d in getDirections(SQUARE):
            self.im32_1.fill(0)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, 0)
            self.im32_1.fill(0xffffffff)
            supNeighbor(self.im32_1, self.im32_1, 1<<d, grid=SQUARE, edge=EMPTY)
            vol = computeVolume(self.im32_1)
            self.assertEqual(vol, w*h*0xffffffff)

