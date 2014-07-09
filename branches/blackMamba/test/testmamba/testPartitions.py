"""
Test cases for the partitions image functions found in the partitions module of 
mamba package.

Python functions and classes:
    cellsErode
    cellsOpen
    cellsComputeDistance
    equalNeighbors
    nonEqualNeighbors
    cellsHMT
    cellsThin
    cellsFullThin
    cellsBuild
    cellsExtract
    cellsOpenByBuild
    partitionErode
    partitionDilate
"""

from mamba import *
import unittest
import random

class TestPartitions(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)

    def testCellsErode(self):
        """Verifies the cell erode function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1), 10)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 20)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 30)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 40)
        cellsErode(self.im8_1, self.im8_2, se=SQUARE3X3)
        drawSquare(self.im8_3, (0,0,w//2-2,h//2-2), 10)
        drawSquare(self.im8_3, (w//2+1,0,w-1,h//2-2), 20)
        drawSquare(self.im8_3, (0,h//2+1,w//2-2,h-1), 30)
        drawSquare(self.im8_3, (w//2+1,h//2+1,w-1,h-1), 40)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testCellsOpen(self):
        """Verifies the cell open function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1), 10)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 20)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 30)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 40)
        drawSquare(self.im8_1, (w//2,h//2,w//2+1,h//2+1), 50)
        cellsOpen(self.im8_1, self.im8_2, se=SQUARE3X3)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1), 10)
        drawSquare(self.im8_3, (w//2,0,w-1,h//2-1), 20)
        drawSquare(self.im8_3, (0,h//2,w//2-1,h-1), 30)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 40)
        drawSquare(self.im8_3, (w//2,h//2,w//2+1,h//2+1), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testCellsComputeDistance(self):
        """Verifies the cell distance function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1), 10)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 20)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 30)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 40)
        cellsComputeDistance(self.im8_1, self.im32_2, grid=SQUARE)
        for i in range(w//4):
            drawBox(self.im32_3, (i,i,w//2-1-i,h//2-1-i), i+1)
            drawBox(self.im32_3, (w//2+i,i,w-1-i,h//2-1-i), i+1)
            drawBox(self.im32_3, (i,h//2+i,w//2-1-i,h-1-i), i+1)
            drawBox(self.im32_3, (w//2+i,h//2+i,w-1-i,h-1-i), i+1)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

    def testEqualNeighbors(self):
        """Verifies the equal neighbor function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        equalNeighbors(self.im8_1, self.im8_2, 0x2, grid=SQUARE)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_3, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_3, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 200)
        drawLine(self.im8_3, (0,0,w-1,0), 0)
        drawLine(self.im8_3, (0,h//2,w-1,h//2), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testNonEqualNeighbors(self):
        """Verifies the non equal neighbor function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        nonEqualNeighbors(self.im8_1, self.im8_2, 0x2, grid=SQUARE)
        self.im8_3.reset()
        drawLine(self.im8_3, (0,0,w//2-1,0), 50)
        drawLine(self.im8_3, (w//2,0,w-1,0), 100)
        drawLine(self.im8_3, (0,h//2,w//2-1,h//2), 150)
        drawLine(self.im8_3, (w//2,h//2,w-1,h//2), 200)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsHMT(self):
        """Verifies the hit or miss on cell operator"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        dse = doubleStructuringElement([3,4,5],[1,7,8],SQUARE)
        cellsHMT(self.im8_1, self.im8_2, dse, EMPTY)
        self.im8_3.setPixel( 50, (w//2-1,h//2-1))
        self.im8_3.setPixel(100, (w-1,h//2-1))
        self.im8_3.setPixel(150, (w//2-1,h-1))
        self.im8_3.setPixel(200, (w-1,h-1))
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsThin(self):
        """Verifies the cell thinning operator"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        dse = doubleStructuringElement([],[0,3],SQUARE)
        cellsThin(self.im8_1, self.im8_2, dse, EMPTY)
        drawLine(self.im8_3, (w//2-1,0,w//2-1,h//2-1), 50)
        drawLine(self.im8_3, (w-1,0,w-1,h//2-1), 100)
        drawLine(self.im8_3, (w//2-1,h//2,w//2-1,h-1), 150)
        drawLine(self.im8_3, (w-1,h//2,w-1,h-1), 200)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsFullThin(self):
        """Verifies the cell full thinning operator"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        dse = doubleStructuringElement([],[2,3,4],SQUARE)
        cellsFullThin(self.im8_1, self.im8_2, dse, EMPTY)
        drawLine(self.im8_3, (0,0,w//2-1,0), 50)
        drawLine(self.im8_3, (w//2-1,0,w//2-1,h//2-1), 50)
        drawLine(self.im8_3, (0,h//2-1,w//2-1,h//2-1), 50)
        drawLine(self.im8_3, (w//2,0,w-1,0), 100)
        drawLine(self.im8_3, (w-1,0,w-1,h//2-1), 100)
        drawLine(self.im8_3, (w//2,h//2-1,w-1,h//2-1), 100)
        drawLine(self.im8_3, (0,h//2,w//2-1,h//2), 150)
        drawLine(self.im8_3, (w//2-1,h//2,w//2-1,h-1), 150)
        drawLine(self.im8_3, (0,h-1,w//2-1,h-1), 150)
        drawLine(self.im8_3, (w//2,h//2,w-1,h//2), 200)
        drawLine(self.im8_3, (w-1,h//2,w-1,h-1), 200)
        drawLine(self.im8_3, (w//2,h-1,w-1,h-1), 200)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsBuild(self):
        """Verifies the cell geodesic reconstruction operator"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        drawSquare(self.im8_2, (w//4,h//4,w//4+1,h//4+1), 60)
        drawSquare(self.im8_2, (3*w//4,3*h//4,3*w//4+1,3*h//4+1), 210)
        cellsBuild(self.im8_1, self.im8_2, SQUARE)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1),  60)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 210)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsExtract(self):
        """Verifies the cell extraction function"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        drawLine(self.im1_1, (w//4,0,w//4,h-1), 1)
        cellsExtract(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_3, (0,h//2,w//2-1,h-1), 150)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testCellsOpenByBuild(self):
        """Tests the open by build cell operator"""
        (w,h) = self.im8_1.getSize()
        drawSquare(self.im8_1, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_1, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_1, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_1, (w//2,h//2,w-1,h-1), 200)
        drawSquare(self.im8_1, (w//2-2,h//2-2,w//2+2,h//2+2), 250)
        cellsOpenByBuild(self.im8_1, self.im8_2, n=1, se=SQUARE3X3)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_3, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_3, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 200)
        drawSquare(self.im8_3, (w//2-2,h//2-2,w//2+2,h//2+2), 250)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        cellsOpenByBuild(self.im8_1, self.im8_2, n=3, se=SQUARE3X3)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1),  50)
        drawSquare(self.im8_3, (w//2,0,w-1,h//2-1), 100)
        drawSquare(self.im8_3, (0,h//2,w//2-1,h-1), 150)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 200)
        drawSquare(self.im8_3, (w//2-2,h//2-2,w//2+2,h//2+2), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def drawChessBoard(self, imOut, n=4):
        (w,h) = imOut.getSize()
        cw = w//n
        ch = h//n
        bval = 256//(n*n)
        val = bval
        for j in range(0,h,ch):
            for i in range(0,w,cw):
                drawSquare(imOut, (i,j,i+cw-1,j+ch-1), val-1)
                val += bval
        return bval
                
    def testPartitionErode(self):
        """Verifies the partitions (graph) erode operator"""
        (w,h) = self.im8_1.getSize()
        bval = self.drawChessBoard(self.im8_1)
        partitionErode(self.im8_1, self.im8_2, n=1, grid=SQUARE)
        drawSquare(self.im8_3, (0,0,w//2-1,h//2-1), bval)
        drawSquare(self.im8_3, (w//2,0,3*w//4-1,h//2-1), 2*bval)
        drawSquare(self.im8_3, (3*w//4,0,w-1,h//2-1), 3*bval)
        drawSquare(self.im8_3, (0,h//2,w//2-1,3*h//4-1), 5*bval)
        drawSquare(self.im8_3, (w//2,h//2,3*w//4-1,3*h//4-1), 6*bval)
        drawSquare(self.im8_3, (3*w//4,h//2,w-1,3*h//4-1), 7*bval)
        drawSquare(self.im8_3, (0,3*h//4,w//2-1,h-1), 9*bval)
        drawSquare(self.im8_3, (w//2,3*h//4,3*w//4-1,h-1), 10*bval)
        drawSquare(self.im8_3, (3*w//4,3*h//4,w-1,h-1), 11*bval)
        subConst(self.im8_3, 1, self.im8_3)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
                
    def testPartitionDilate(self):
        """Verifies the partitions (graph) dilate operator"""
        (w,h) = self.im8_1.getSize()
        bval = self.drawChessBoard(self.im8_1)
        partitionDilate(self.im8_1, self.im8_2, n=1, grid=SQUARE)
        drawSquare(self.im8_3, (0,0,w//4-1,h//4-1), 6*bval)
        drawSquare(self.im8_3, (w//4,0,w//2-1,h//4-1), 7*bval)
        drawSquare(self.im8_3, (w//2,0,w-1,h//4-1), 8*bval)
        drawSquare(self.im8_3, (0,h//4,w//4-1,h//2-1), 10*bval)
        drawSquare(self.im8_3, (w//4,h//4,w//2-1,h//2-1), 11*bval)
        drawSquare(self.im8_3, (w//2,h//4,w-1,h//2-1), 12*bval)
        drawSquare(self.im8_3, (0,h//2,w//4-1,h-1), 14*bval)
        drawSquare(self.im8_3, (w//4,h//2,w//2-1,h-1), 15*bval)
        subConst(self.im8_3, 1, self.im8_3)
        drawSquare(self.im8_3, (w//2,h//2,w-1,h-1), 16*bval-1)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

