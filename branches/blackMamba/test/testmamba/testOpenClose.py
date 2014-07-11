"""
Test cases for the open and close functions found in the openclose module of 
mamba package.

Python functions and classes:
    opening
    closing
    linearOpen
    linearClose
    buildOpen
    buildClose
    supOpen
    infClose
"""

from mamba import *
import unittest
import random

class TestOpenClose(unittest.TestCase):

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
        
    def testOpening(self):
        """Verifies the correct computation of an opening operation using open"""
        (w,h) = self.im8_1.getSize()
        for n in range(0,10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n)
            for i in range(n+1):
                copy(self.im8_1, self.im8_2)
                opening(self.im8_2, self.im8_2, i)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            copy(self.im8_1, self.im8_2)
            opening(self.im8_2, self.im8_2, n+1)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 0, "%d : vol=%d"%(n,vol))
        
    def testClose(self):
        """Verifies the correct computation of a closing operation using close"""
        (w,h) = self.im8_1.getSize()
        for n in range(0,10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n)
            for i in range(n+1):
                copy(self.im8_1, self.im8_2)
                closing(self.im8_2, self.im8_2, i)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            copy(self.im8_1, self.im8_2)
            closing(self.im8_2, self.im8_2, n+1)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, w*h*255, "%d : vol=%d"%(n,vol))
        
    def testCloseEmptyEdge(self):
        """Verifies the correct computation of a closing operation with an EMPTY edge"""
        (w,h) = self.im8_1.getSize()
        for n in range(0,10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (0,h//2))
            self.im8_1.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n)
            for i in range(n+1):
                copy(self.im8_1, self.im8_2)
                closing(self.im8_2, self.im8_2, i, edge=EMPTY)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            copy(self.im8_1, self.im8_2)
            closing(self.im8_2, self.im8_2, n+1, edge=EMPTY)
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (0,h//2))
            erode(self.im8_1, self.im8_1, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testBuildOpen(self):
        """Verifies the correct computation of an opening by build operation"""
        (w,h) = self.im8_1.getSize()
        for n in range(0,10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n)
            drawLine(self.im8_1, (w//2,h//2,w-2,h//2), 255)
            for i in range(n+1):
                copy(self.im8_1, self.im8_2)
                buildOpen(self.im8_2, self.im8_2, i)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            copy(self.im8_1, self.im8_2)
            buildOpen(self.im8_2, self.im8_2, n+1)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 0, "%d : vol=%d"%(n,vol))
        
    def testBuildClose(self):
        """Verifies the correct computation of a closing by build operation"""
        (w,h) = self.im8_1.getSize()
        for n in range(0,10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n)
            drawLine(self.im8_1, (w//2,h//2,w-2,h//2), 0)
            for i in range(n+1):
                copy(self.im8_1, self.im8_2)
                buildClose(self.im8_2, self.im8_2, i)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            copy(self.im8_1, self.im8_2)
            buildClose(self.im8_2, self.im8_2, n+1)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, w*h*255, "%d : vol=%d"%(n,vol))
        
    def testLinearOpen(self):
        """Verifies the correct computation of a linear opening operation"""
        (w,h) = self.im8_1.getSize()
        for d in getDirections():
            for n in range(0,10):
                self.im8_1.reset()
                self.im8_1.setPixel(255, (w//2,h//2))
                linearDilate(self.im8_1, self.im8_1, d, n)
                for i in range(n+1):
                    copy(self.im8_1, self.im8_2)
                    linearOpen(self.im8_2, self.im8_2, d, i)
                    (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                    self.assertLess(x, 0)
                copy(self.im8_1, self.im8_2)
                linearOpen(self.im8_2, self.im8_2, d, n+1)
                vol = computeVolume(self.im8_2)
                if d==0:
                    self.assertEqual(vol, 255)
                else:
                    self.assertEqual(vol, 0, "dir=%d %d : vol=%d"%(d,n,vol))
        
    def testLinearClose(self):
        """Verifies the correct computation of a linear closing operation"""
        (w,h) = self.im8_1.getSize()
        for d in getDirections():
            for n in range(0,10):
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, (w//2,h//2))
                linearErode(self.im8_1, self.im8_1, d, n)
                for i in range(n+1):
                    copy(self.im8_1, self.im8_2)
                    linearClose(self.im8_2, self.im8_2, d, i)
                    (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                    self.assertLess(x, 0)
                copy(self.im8_1, self.im8_2)
                linearClose(self.im8_2, self.im8_2, d, n+1)
                vol = computeVolume(self.im8_2)
                if d==0:
                    self.assertEqual(vol, (w*h*255-255))
                else:
                    self.assertEqual(vol, w*h*255, "dir=%d %d : vol=%d"%(d,n,vol))
        
    def testLinearCloseEmptyEdge(self):
        """Verifies the correct computation of a linear closing operation with an EMPTY edge"""
        (w,h) = self.im8_1.getSize()
        pos = [(w//2,h//2), (w//2,h-1), (0,h-1), (0,h//2), (0,0), (w//2,0), (w-1,0), (w-1,h//2), (w-1,h-1)]
        for d in getDirections(SQUARE)[1:]:
            for n in range(0,10):
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, (w//2,h//2))
                self.im8_1.setPixel(0, pos[d])
                linearErode(self.im8_1, self.im8_1, transposeDirection(d, SQUARE), n, grid=SQUARE)
                for i in range(n+1):
                    copy(self.im8_1, self.im8_2)
                    linearClose(self.im8_2, self.im8_2, d, i, grid=SQUARE, edge=EMPTY)
                    (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                    self.assertLess(x, 0)
                copy(self.im8_1, self.im8_2)
                linearClose(self.im8_2, self.im8_2, d, n+1, grid=SQUARE, edge=EMPTY)
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, pos[d])
                linearErode(self.im8_1, self.im8_1, transposeDirection(d, SQUARE), n, grid=SQUARE)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
                    
    def _drawSPH(self, imOut, size):
        prov = imageMb(imOut)
        (w,h) = imOut.getSize()
        imOut.reset()
        dirs = getDirections(HEXAGONAL)[1:]
        cd = random.choice(dirs)
        for d in dirs:
            prov.reset()
            prov.setPixel(255, (w//2,h//2))
            if d==cd:
                linearDilate(prov, prov, d, size+1, grid=HEXAGONAL)
            else:
                linearDilate(prov, prov, d, size, grid=HEXAGONAL)
            logic(imOut, prov, imOut, "sup")
        return cd
        
    def testSupOpenHexagonal(self):
        """Tests the supOpen operator in hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        for i in range(10):
            n = random.randint(10,20)
            dc = self._drawSPH(self.im8_1, n)
            for s in range(2*n+1):
                copy(self.im8_1, self.im8_2)
                supOpen(self.im8_2, self.im8_2, s, HEXAGONAL)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            supOpen(self.im8_1, self.im8_2, 2*n+1, HEXAGONAL)
            self.im8_3.reset()
            self.im8_3.setPixel(255, (w//2,h//2))
            linearDilate(self.im8_3, self.im8_3, dc, n+1, HEXAGONAL)
            linearDilate(self.im8_3, self.im8_3, transposeDirection(dc, HEXAGONAL), n, HEXAGONAL)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            supOpen(self.im8_1, self.im8_2, 2*n+2, HEXAGONAL)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 0)
        
    def testInfCloseHexagonal(self):
        """Tests the infClose operator in hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        for i in range(10):
            n = random.randint(10,20)
            dc = self._drawSPH(self.im8_1, n)
            negate(self.im8_1, self.im8_1)
            for s in range(2*n+1):
                copy(self.im8_1, self.im8_2)
                infClose(self.im8_2, self.im8_2, s, HEXAGONAL)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            infClose(self.im8_1, self.im8_2, 2*n+1, HEXAGONAL)
            self.im8_3.fill(255)
            self.im8_3.setPixel(0, (w//2,h//2))
            linearErode(self.im8_3, self.im8_3, dc, n+1, HEXAGONAL)
            linearErode(self.im8_3, self.im8_3, transposeDirection(dc, HEXAGONAL), n, HEXAGONAL)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            infClose(self.im8_1, self.im8_2, 2*n+2, HEXAGONAL)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 255*w*h)
            
    def _obliqueSize(self, n):
        return int((1.4142 * n + 1)//2)
        
    def _drawSPS(self, imOut, size):
        prov = imageMb(imOut)
        (w,h) = imOut.getSize()
        imOut.reset()
        dirs = getDirections(SQUARE)[1:5]
        cd = random.choice(dirs)
        sizes = [self._obliqueSize(size), size]
        asizes = [self._obliqueSize(size+3), size+3]
        for d in dirs:
            prov.reset()
            prov.setPixel(255, (w//2,h//2))
            if d==cd:
                linearDilate(prov, prov, d, asizes[d%2], grid=SQUARE)
            else:
                linearDilate(prov, prov, d, sizes[d%2], grid=SQUARE)
            logic(imOut, prov, imOut, "sup")
        return cd
        
    def testSupOpenSquare(self):
        """Tests the supOpen operator in square grid"""
        (w,h) = self.im8_1.getSize()
        for i in range(10):
            n = random.randint(10,20)
            ns = [self._obliqueSize(n), n]
            ans = [self._obliqueSize(n+3), n+3]
            dc = self._drawSPS(self.im8_1, n)
            for s in range(n+1):
                copy(self.im8_1, self.im8_2)
                supOpen(self.im8_2, self.im8_2, s, SQUARE)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            supOpen(self.im8_1, self.im8_2, n+3, SQUARE)
            self.im8_3.reset()
            self.im8_3.setPixel(255, (w//2,h//2))
            linearDilate(self.im8_3, self.im8_3, dc, ans[dc%2], SQUARE)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            supOpen(self.im8_1, self.im8_2, n+5, SQUARE)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 0, "for %d/%d : %d"%(n,dc,vol))
        
    def testInfCloseSquare(self):
        """Tests the infClose operator in square grid"""
        (w,h) = self.im8_1.getSize()
        for i in range(10):
            n = random.randint(10,20)
            ns = [self._obliqueSize(n), n]
            ans = [self._obliqueSize(n+3), n+3]
            dc = self._drawSPS(self.im8_1, n)
            negate(self.im8_1, self.im8_1)
            for s in range(n+1):
                copy(self.im8_1, self.im8_2)
                infClose(self.im8_2, self.im8_2, s, SQUARE)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            infClose(self.im8_1, self.im8_2, n+3, SQUARE)
            self.im8_3.fill(255)
            self.im8_3.setPixel(0, (w//2,h//2))
            linearErode(self.im8_3, self.im8_3, dc, ans[dc%2], SQUARE)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            infClose(self.im8_1, self.im8_2, n+5, SQUARE)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol, 255*w*h, "for %d/%d : %d"%(n,dc,vol))

