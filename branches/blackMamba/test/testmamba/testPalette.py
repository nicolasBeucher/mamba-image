"""
Test cases for the palette functions.

Python functions:
    tagOneColorPalette
    changeColorPalette
"""

from mamba import *
import unittest

class TestPalette(unittest.TestCase):

    def testTagValueAcceptance(self):
        """Verifies that the tag one color palette creator refuses out of bound values"""
        self.assertRaises(ValueError, tagOneColorPalette, -1, (1,1,1))
        self.assertRaises(ValueError, tagOneColorPalette, 256, (1,1,1))
            
    def testTagOneColorPalette(self):
        """Verifies that the tag one color palette creator"""
        pal = tagOneColorPalette(254, (35,87,98))
        self.assertEqual(len(pal),256*3)
        self.assertEqual(pal[0], 0)
        self.assertEqual(pal[3*128], 128)
        self.assertEqual(pal[764], 98)
        self.assertEqual(pal[763], 87)
        self.assertEqual(pal[762], 35)
        
    def testChangeColorPalette(self):
        """Verifies that the color palette modificator"""
        pal = tagOneColorPalette(255, (35,87,98))
        pal = changeColorPalette(pal, 255, (12, 234, 76))
        self.assertEqual(len(pal),256*3)
        self.assertEqual(pal[0], 0)
        self.assertEqual(pal[3*128], 128)
        self.assertEqual(pal[767], 76)
        self.assertEqual(pal[766], 234)
        self.assertEqual(pal[765], 12)
