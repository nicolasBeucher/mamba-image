"""
Test cases for the various functions found in the arithmetic3D
module of mamba3D package.

Python functions:
    add3D
    sub3D
    mul3D
    div3D
    addConst3D
    subConst3D
    divConst3D
    mulConst3D
    mulRealConst3D
    negate3D
    logic3D
    diff3D
    ceilingAddConst3D
    ceilingAdd3D
    floorSubConst3D
    floorSub3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestArithmetic3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(1)
        self.im1_2 = image3DMb(1)
        self.im1_3 = image3DMb(1)
        self.im8_1 = image3DMb(8)
        self.im8_2 = image3DMb(8)
        self.im8_3 = image3DMb(8)
        self.im8_4 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(32)
        self.im32_2 = image3DMb(32)
        self.im32_3 = image3DMb(32)
        self.im32_4 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,add3D,self.im8_4,self.im8_2,self.im8_3)
        self.assertRaises(MambaError,sub3D,self.im8_4,self.im8_2,self.im8_3)
        self.assertRaises(MambaError,mul3D,self.im8_4,self.im8_2,self.im8_3)
        self.assertRaises(MambaError,div3D,self.im8_4,self.im8_2,self.im8_3)
        self.assertRaises(MambaError,addConst3D,self.im8_4,0,self.im8_3)
        self.assertRaises(MambaError,subConst3D,self.im8_4,0,self.im8_3)
        self.assertRaises(MambaError,divConst3D,self.im8_4,1,self.im8_3)
        self.assertRaises(MambaError,mulConst3D,self.im8_4,1,self.im8_3)
        self.assertRaises(MambaError,negate3D,self.im8_4,self.im8_3)
        self.assertRaises(MambaError,logic3D,self.im8_4,self.im8_2,self.im8_3,"and")
        self.assertRaises(MambaError,diff3D,self.im8_4,self.im8_2,self.im8_3)
        self.assertRaises(MambaError,ceilingAddConst3D,self.im32_4,0,self.im32_3)
        self.assertRaises(MambaError,ceilingAdd3D,self.im32_4,self.im32_2,self.im32_3)
        self.assertRaises(MambaError,floorSubConst3D,self.im32_4,0,self.im32_3)
        self.assertRaises(MambaError,floorSub3D,self.im32_4,self.im32_2,self.im32_3)
        self.assertRaises(MambaError,mulRealConst3D,self.im32_1, 1.0, self.im32_4)
    
    def testAdd3D(self):
        """Verifies the 3D addition operator"""
        self.im8_1.fill(23)
        self.im8_2.fill(156)
        self.im8_3.fill(23+156)
        add3D(self.im8_1, self.im8_2,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
    
    def testSub3D(self):
        """Verifies the 3D substraction operator"""
        self.im8_1.fill(23)
        self.im8_2.fill(156)
        self.im8_3.fill(156-23)
        sub3D(self.im8_2, self.im8_1,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
    
    def testMul3D(self):
        """Verifies the 3D multiplication operator"""
        self.im8_1.fill(23)
        self.im8_2.fill(5)
        self.im8_3.fill(5*23)
        mul3D(self.im8_2, self.im8_1,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
    
    def testDiv3D(self):
        """Verifies the 3D division operator"""
        self.im8_1.fill(23)
        self.im8_2.fill(5)
        self.im8_3.fill(23//5)
        div3D(self.im8_1, self.im8_2, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testAddConst3D(self):
        """Verifies the 3D constant addition operator"""
        self.im8_1.fill(23)
        self.im8_3.fill(156+23)
        addConst3D(self.im8_1, 156,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testSubConst3D(self):
        """Verifies the 3D constant addition operator"""
        self.im8_1.fill(156)
        self.im8_3.fill(156-23)
        subConst3D(self.im8_1, 23,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testDivConst3D(self):
        """Verifies the 3D constant addition operator"""
        self.im8_1.fill(156)
        self.im8_3.fill(156//3)
        divConst3D(self.im8_1, 3,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testMulConst3D(self):
        """Verifies the 3D constant addition operator"""
        self.im8_1.fill(41)
        self.im8_3.fill(41*4)
        mulConst3D(self.im8_1, 4,self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testNegate3D(self):
        """Tests the negation operator on 3D images"""
        self.im8_1.fill(41)
        self.im8_3.fill(255-41)
        negate3D(self.im8_1, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testLogic3D(self):
        """Tests the logic operators on 3D images"""
        self.im8_1.fill(41)
        self.im8_2.fill(203)
        logic3D(self.im8_1, self.im8_2, self.im8_3, "sup")
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        logic3D(self.im8_1, self.im8_2, self.im8_3, "inf")
        (x,y,z) = compare3D(self.im8_3, self.im8_1, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testDiff3D(self):
        """Tests the logic operators on 3D images"""
        self.im8_1.fill(41)
        self.im8_2.fill(203)
        self.im8_3.reset()
        diff3D(self.im8_1, self.im8_2, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        self.im8_2.fill(33)
        self.im8_3.fill(41)
        diff3D(self.im8_1, self.im8_2, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testCeilingAddConst3D(self):
        """Verifies the 3D constant saturated addition operator"""
        self.im32_1.fill(0xfffffffe)
        self.im32_3.fill(0xffffffff)
        ceilingAddConst3D(self.im32_1, 10,self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testCeilingAdd3D(self):
        """Verifies the 3D saturated addition operator"""
        self.im32_1.fill(0xfffffffe)
        self.im32_2.fill(10)
        self.im32_3.fill(0xffffffff)
        ceilingAdd3D(self.im32_1, self.im32_2, self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testFloorSubConst3D(self):
        """Verifies the 3D constant saturated substraction operator"""
        self.im32_1.fill(1)
        self.im32_3.fill(0)
        floorSubConst3D(self.im32_1, 10,self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testFloorSub3D(self):
        """Verifies the 3D saturated substraction operator"""
        self.im32_1.fill(1)
        self.im32_2.fill(10)
        self.im32_3.fill(0)
        floorSub3D(self.im32_1, self.im32_2, self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testMulRealConst(self):
        """Tests the real value multiplication"""
        self.im8_1.fill(1)
        
        self.im8_3.fill(1)
        mulRealConst3D(self.im8_1, 1.6, self.im8_2, nearest=False)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_3.fill(2)
        mulRealConst3D(self.im8_1, 1.6, self.im8_2, nearest=True)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(10)
        self.im8_3.fill(15)
        mulRealConst3D(self.im8_1, 1.5, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im32_1.fill(1000)
        self.im32_3.fill(1500)
        mulRealConst3D(self.im32_1, 1.5, self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(200)
        self.im8_3.fill(255)
        self.im32_3.fill(260)
        mulRealConst3D(self.im8_1, 1.3, self.im8_2)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        mulRealConst3D(self.im8_1, 1.3, self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

