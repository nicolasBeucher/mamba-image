/** \file MB_Api.h */
/*
 * Copyright (c) <2014>, <Nicolas BEUCHER and ARMINES for the Centre de 
 * Morphologie Mathématique(CMM), common research center to ARMINES and MINES 
 * Paristech>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation files
 * (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish, 
 * distribute, sublicense, and/or sell copies of the Software, and to permit 
 * persons to whom the Software is furnished to do so, subject to the following 
 * conditions: The above copyright notice and this permission notice shall be 
 * included in all copies or substantial portions of the Software.
 *
 * Except as contained in this notice, the names of the above copyright 
 * holders shall not be used in advertising or otherwise to promote the sale, 
 * use or other dealings in this Software without their prior written 
 * authorization.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#ifndef __MB_Api_H
#define __MB_Api_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Performs a bitwise AND between the pixels of two images.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_And(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Applies a bitwise OR on the pixels of two images.
 * All the images must have the same depth for correct work.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Or(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Applies a bitwise XOR on the pixels of two images.
 * All the images must have the same depth for correct work.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Xor(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Inverts the pixels values (logical NOT) of the source image.
 * \param src source image
 * \param dest destination image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Inv(MB_Image *src, MB_Image *dest);
/**
 * Determines the inferior value between the pixels of two images.
 * The result is put in the corresponding pixel position in the destination image.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Inf(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Determines the superior value between the pixels of two images.
 * The result is put in the corresponding pixel position in the destination image.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Sup(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Computes a binary image where pixels are set to 1 when the pixels of
 * image 1 have greater values than pixels of image 2 otherwise 0.
 * \param src1 source image 1
 * \param src2 source image 2
 * \param dest destination image 
 * \param strict flag indicating if the comparison is strict or large
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_SupMask(MB_Image *src1, MB_Image *src2, MB_Image *dest, Uint32 strict);
/**
 * Adds the pixels of two images and puts the result in the third image.
 * Depending on the format of the target image, the result may be saturated or not.
 * You can perform the following additions :
 *      - 1-bit + 1-bit = 1-bit (binary OR)
 *      - 1-bit + 8-bit = 8-bit (saturated)
 *      - 1-bit + 8-bit = 32-bit 
 *      - 1-bit + 32-bit = 32-bit
 *      - 8-bit + 8-bit = 8-bit (saturated)
 *      - 8-bit + 8-bit = 32-bit
 *      - 8-bit + 32-bit = 32-bit
 *      - 32-bit + 32-bit = 32-bit
 *
 * \see MB_Or for the binary OR definition.
 *
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the addition of image 1 and 2 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Add(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Subtracts the values of pixels of the second image to the values of
 * the pixels in the first image
 * You can perform the following substractions :
 *      - 1-bit - 1-bit = 1-bit (binary AND)
 *      - 8-bit - 1-bit = 8-bit (saturated)
 *      - 8-bit - 8-bit = 8-bit (saturated)
 *      - 8-bit - 8-bit = 32-bit
 *      - 8-bit - 32-bit = 32-bit
 *      - 32-bit - 8-bit = 32-bit
 *      - 32-bit - 32-bit = 32-bit
 *
 * \see MB_Diff for the set difference.
 *
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the subtraction 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Sub(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Multiplies the pixels of two images and puts the result in the third image.
 * Depending on the format of the target image, the result may be saturated or not.
 * You can perform the following multiplications :
 *      - 1-bit * 1-bit = 1-bit (binary AND)
 *      - 1-bit * 8-bit = 8-bit
 *      - 1-bit * 8-bit = 32-bit 
 *      - 1-bit * 32-bit = 32-bit
 *      - 8-bit * 8-bit = 8-bit (saturated)
 *      - 8-bit * 8-bit = 32-bit
 *      - 8-bit * 32-bit = 32-bit
 *      - 32-bit * 32-bit = 32-bit
 *
 * \see MB_And for the binary AND.
 *
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the multiplication of image 1 and 2 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Mul(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Divides the pixels of two images and puts the result in the third image.
 * You can perform the following multiplications :
 *      - 8-bit / 8-bit = 8-bit (saturated)
 *      - 8-bit / 8-bit = 32-bit
 *      - 32-bit / 8-bit = 32-bit
 *      - 32-bit / 32-bit = 32-bit
 *
 * Division by zero results in the maximum value possible for the pixels
 * of the destination image depth.
 *
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the division of image 1 and 2 (quotient) 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Div(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Computes the set difference between two images.
 * The result image pixel value is the pixel value of
 * image 1 if this value was greater than value of pixel 2
 * otherwise the minimum possible value is set for the pixel.
 * \param src1 source image 1
 * \param src2 source image 2
 * \param dest destination image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Diff(MB_Image *src1, MB_Image *src2, MB_Image *dest);
/**
 * Adds a constant value to the pixels of an image.
 * \param src the source image
 * \param value the constant value to be added to the pixels
 * \param dest the image resulting of the addition of image 1 and value 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ConAdd(MB_Image *src, Sint64 value, MB_Image *dest);
/**
 * Subtracts a constant value to the pixels of an image.
 * \param src the source image
 * \param value the constant value to be subtracted to the pixels
 * \param dest the image resulting of the subtraction of image 1 and value 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ConSub(MB_Image *src, Sint64 value, MB_Image *dest);
/**
 * Multiplies a constant value to the pixels of an image.
 * \param src the source image
 * \param value the constant value to be multiplied to the pixels
 * \param dest the image resulting of the multiplication of image 1 by the value 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ConMul(MB_Image *src, Uint32 value, MB_Image *dest);
/**
 * Divides (quotient) the pixels of an image by a constant value.
 * \param src the source image
 * \param value the constant value used in the division
 * \param dest the image resulting of the division of image 1 by the value 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ConDiv(MB_Image *src, Uint32 value, MB_Image *dest);
/**
 * Fills an image with a specific value.
 * \param dest the image
 * \param value the value to fill the image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ConSet(MB_Image *dest, Uint32 value);
/**
 * Computes the volume of an image.
 * The volume is the sum of the pixel values (i.e. integration 
 * of the image).
 * \param src source image
 * \param pVolume pointer to the volume variable
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Volume(MB_Image *src, Uint64 *pVolume);
/**
 * Verifies that the image is not empty (all pixels to 0).
 * \param src the source image 
 * \param isEmpty an integer which is set to 1 if empty or 0 if not
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Check(MB_Image *src, Uint32 *isEmpty);
/**
 * Applies the function in the lookup table to the pixels of source image.
 * A pixel value is changed to a new value accordingly with its current value.
 * \param src source image
 * \param dest destination image
 * \param ptab the lookup table pointer
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Lookup(MB_Image *src, MB_Image *dest, Uint32 *ptab);
/**
 * Computes the histogram of an image.
 * The histogram is an array with a minimal size of 256.
 * \param src source image
 * \param phisto pointer to the histogram array
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Histo(MB_Image *src, Uint32 *phisto);
/**
 * Performs a comparaison between a source image and a given base image.
 * \param src the source image 
 * \param cmp the image to which the source image is compared
 * \param dest destination image 
 * \param px position in x of the first different pixel between the two images (-1 if images are similar)
 * \param py position in y of the first different pixel between the two images (-1 if images are similar)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Compare(MB_Image *src, MB_Image *cmp, MB_Image *dest, Sint32 *px, Sint32 *py);
/**
 * Fills a binary image according to the following rules:
 * if pixel value lower than low or higher than high the binary pixel
 * is set to 0, in other cases the pixel is set to 1.
 * \param src source image
 * \param dest destination image
 * \param low low value for threshold
 * \param high high value for treshold
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Thresh(MB_Image *src, MB_Image *dest, Uint32 low, Uint32 high);
/**
 * Converts a binary image in a grey scale image (8-bit) or in a 32-bit image
 * using value maskf to replace 0 and maskt to replace 1.
 * \param src binary source image
 * \param dest destination image 
 * \param maskf for 0 (false) pixel value
 * \param maskt for 1 (true) pixel value
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Mask(MB_Image *src, MB_Image *dest, Uint32 maskf, Uint32 maskt);
/**
 * gives the minimum and maximum values of the image pixels
 * i.e its range.
 * \param src source image
 * \param min the minimum value of the pixels
 * \param max the maximum value of the pixels
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Range(MB_Image *src, Uint32 *min, Uint32 *max);
/**
 * gives the minimum and maximum possible values of the image pixels
 * given the image depth.
 * \param src source image
 * \param min the minimum possible value of the pixels
 * \param max the maximum possible value of the pixels
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_depthRange(MB_Image *src, Uint32 *min, Uint32 *max);
/**
 * Inserts or extracts the bit plane in/out of image src into 
 * dest.
 * \param src source image
 * \param dest destination image
 * \param plane the plane number
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_CopyBitPlane(MB_Image *src, MB_Image *dest, Uint32 plane);
/**
 * Inserts or extracts the byte plane in/out of image src into 
 * dest.
 * \param src source image
 * \param dest destination image
 * \param plane the plane number
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_CopyBytePlane(MB_Image *src, MB_Image *dest, Uint32 plane);
/**
 * Labeling the object found in src image.
 *
 * \param src the source image where the object must be labelled
 * \param dest the 32-bit image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object found
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Label(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid);
/**
 * Computes for each pixel the distance to the edge of the set in which the
 * pixel is found.
 *
 * The algorithm works with a list.
 *
 * \param src the binary source image
 * \param dest the 32-bit image in which the distance for each pixel is stored
 * \param grid the grid used (either hexagonal or square)
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Distanceb(MB_Image *src, MB_Image *dest, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * Returns the smallest frame that contains all the pixels of image that are greater or equal to
 * the given threshold value, using the four last pointers to describe it.
 * \param src source image
 * \param thresval the threshold value used to compute the frame
 * \param ulx the x-coordinate of the upper left corner of the frame
 * \param uly the y-coordinate of the upper left corner of the frame
 * \param brx the x-coordinate of the bottom right corner of the frame
 * \param bry the y-coordinate of the bottom right corner of the frame
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Frame(MB_Image *src, Uint32 thresval, Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry);

#ifdef __cplusplus
}
#endif

#endif /* __MB_Api_H */

