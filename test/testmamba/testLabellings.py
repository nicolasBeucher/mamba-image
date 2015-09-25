"""
Test cases for the labelling functions found in the labellings module of 
mamba package.

Python functions and classes:
    partitionLabel
    measureLabelling
    areaLabelling
    diameterLabelling
    feretdiameterLabelling
    volumeLabelling
"""

from mamba import *
import unittest
import random

class TestLabellings(unittest.TestCase):

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

    def testDepthAcceptation(self):
        """Tests that incorrect direction raises an exception"""
        self.assertRaises(MambaError, feretDiameterLabelling, self.im1_1, self.im32_1, "")
        

    def _genTestImage1(self, imOut):
        # Generates test image in imOut
        imOut.reset()
        (w, h) = imOut.getSize()
        # Draws a first rectangle
        drawSquare(imOut, (0, h//8, w - 1, 7*h//8), 20)
        # Draws a point
        imOut.setPixel(40,(w//8, h//2))
        # Draws 3 other squares
        drawSquare(imOut, (23*w//64, 31*h//64, 25*w//64, 33*h//64), 80)
        drawSquare(imOut, (19*w//32, 15*h//32, 21*w//32, 17*h//32), 120)
        drawSquare(imOut, (13*w//16, 7*h//16, 15*w//16, 9*h//16), 160)
    
    def _genTestImage2(self, imOut):
        # Generates test image in imOut with more then 255 labels
        imWrk = imageMb(imOut, 1)
        imWrk.fill(1)
        imWrk.setPixel(0, (0,0))
        computeDistance(imWrk, imOut, HEXAGONAL, FILLED)
        
    def testPartitionLabel(self):
        """Verifies the general partition labelling"""
        self._genTestImage1(self.im8_1)
        nbLabels = partitionLabel(self.im8_1, self.im32_1)
        self.assertEqual(nbLabels, 7, "wrong number of components %d (instead of 7)" % (nbLabels))
        # Tests the binary case
        threshold(self.im8_1, self.im1_1, 20, 20)
        nbLabels = partitionLabel(self.im1_1, self.im32_1)
        self.assertEqual(nbLabels, 7, "wrong number of black and white labelled regions %d (instead of 7)" % (nbLabels))
        # Testing more than 255 regions in image
        self._genTestImage2(self.im32_1)
        nbLabels = partitionLabel(self.im32_1, self.im32_2)
        (x,y) = computeRange(self.im32_1)
        x = y + 1
        self.assertEqual(nbLabels, x, "%d regions , %d labels" % (x,nbLabels))
                     
    def testAreaLabelling(self):
        """Verifies the labelling of each cell with its area"""
        # Testing 8-bit image
        self._genTestImage1(self.im8_1)
        areaLabelling(self.im8_1, self.im32_1)
        for i in [20, 40, 80, 120, 160]:
            threshold(self.im8_1, self.im1_1, i, i)
            vol = computeVolume(self.im1_1)
            threshold(self.im32_1, self.im1_2, vol, vol)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0)
        # Testing binary image
        threshold(self.im8_1, self.im1_1, 20, 20)
        negate(self.im1_1, self.im1_1)
        nbLabels = label(self.im1_1, self.im32_2)
        areaLabelling(self.im1_1, self.im32_1)      
        for i in range(1, nbLabels +1):
            threshold(self.im32_2, self.im1_1, i, i)
            vol = computeVolume(self.im1_1)
            threshold(self.im32_1, self.im1_2, vol, vol)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0)
            
    def testDiameterLabelling(self):
        """Verifies the labelling of each cell with its diameter"""
        self._genTestImage1(self.im8_1)
        # Grey image
        diameterLabelling(self.im8_1, self.im32_1, 2, HEXAGONAL)
        for i in [20, 40, 80, 120, 160]:
            threshold(self.im8_1, self.im1_1, i, i)
            diam = int(computeDiameter(self.im1_1, 2, grid=HEXAGONAL))
            threshold(self.im32_1, self.im1_2, diam, diam)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0)
        # Binary image
        threshold(self.im8_1, self.im1_1, 20, 20)
        diameterLabelling(self.im1_1, self.im32_2, 1, SQUARE)
        threshold(self.im32_2, self.im1_2, 1, 316)
        (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testFeretDiameterLabelling(self):
        """ Verifies the labelling of each cell with its Feret diameter"""
        self._genTestImage1(self.im8_1)
        # Binary case
        threshold(self.im8_1, self.im1_1, 20, 20)
        negate(self.im1_1, self.im1_1)
        feretDiameterLabelling(self.im1_1, self.im32_1, "horizontal")
        resList = [256, 1, 9, 17, 33]
        j = 0
        for i in [0, 40, 80, 120, 160]:
            threshold(self.im8_1, self.im1_2, i, i)
            threshold(self.im32_1, self.im1_1, resList[j], resList[j])
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0)
            j = j + 1
        # 8-bit case
        feretDiameterLabelling(self.im8_1, self.im32_1, "vertical")
        threshold(self.im8_1, self.im1_1, 20, 20)
        threshold(self.im32_1, self.im1_2, 193, 193)
        (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        # 32-bit case
        self._genTestImage2(self.im32_1)
        feretDiameterLabelling(self.im32_1, self.im32_2, "vertical")
        (x,y) = computeRange(self.im32_2)
        self.assertEqual(y, 256, "Feret diameter : %d" % (y))
   
    def testVolumeLabelling(self):
        """Testing the volume labelling"""
        self._genTestImage1(self.im8_1)
        # 8-bit mask
        volumeLabelling(self.im8_1, self.im8_1, self.im32_1)
        for i in [0, 40, 80, 120, 160]:
            threshold(self.im8_1, self.im1_1, i, i)
            v = computeVolume(self.im1_1)
            s = v * i
            threshold(self.im32_1, self.im1_2, s, s)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0) 
        # 32-bit mask (previous one multiplied by itself)
        mul(self.im8_1, self.im8_1, self.im32_2)
        volumeLabelling(self.im8_1, self.im32_2, self.im32_1)
        for i in [0, 40, 80, 120, 160]:
            threshold(self.im8_1, self.im1_1, i, i)
            v = computeVolume(self.im1_1)
            s = v * i * i
            threshold(self.im32_1, self.im1_2, s, s)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)            
            self.assertLess(x, 0) 

        
        
        
        



    
