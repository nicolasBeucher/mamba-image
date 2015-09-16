/*
 * Copyright (c) <2009>, <Nicolas BEUCHER and ARMINES for the Centre de 
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
#include "mambaApi_loc.h"
#include "mambaApi_vector.h"

/*
 * Applies the treshold function to a line of an 8-bits image.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line in im_out
 * \param ublow low value for the threshold
 * \param ubhigh high value for threshold
 */
static INLINE void THRESH_LINE_8_1(PLINE *plines_out, PLINE *plines_in,
                                   Uint32 bytes_in, PIX8 ublow, PIX8 ubhigh)
{
    Uint32 i,j;
    MB_Vector1 pixel2bin;
    MB_Vector1 bin_pixels;

    PLINE pin = (PLINE) (*plines_in);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pout++){
        /* The output binary pixel (bit) are all set to zero first */
        bin_pixels = 0;
        /* Pixel2bin represents the first pixel (LSB) */
        pixel2bin = 1;
        for(j=0; j<MB_vec1_size; j++, pin++) {
            /* If the read value on pin is in range, the pixel bit is set to 1 */
            if (((*pin)>=ublow) && ((*pin)<=ubhigh)) {
                bin_pixels|=pixel2bin;
            }
            /* Shifting so that pixel2bin represent the next pixel */
            pixel2bin=pixel2bin<<1;
        }
        *pout = bin_pixels;
    }
}

/*
 * Applies the treshold function to a line of an 32-bits image.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line in im_out
 * \param low low value for the threshold
 * \param high high value for threshold
 */
static INLINE void THRESH_LINE_32_1(PLINE *plines_out, PLINE *plines_in,
                                    Uint32 bytes_in, PIX32 low, PIX32 high)
{
    Uint32 i,j;
    MB_Vector1 pixel2bin;
    MB_Vector1 bin_pixels;

    PIX32 *pin = (PIX32 *) (*plines_in);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pout++){
        /* The output binary pixels (bit) are all set to zero first */
        bin_pixels = 0;
        /* Pixel2bin represents the first pixel (LSB) */
        pixel2bin = 1;
        for(j=0; j<MB_vec1_size; j++, pin++) {
            /* If the read value on pin is in range, the pixel bit is set to 1 */
            if (((*pin)>=low) && ((*pin)<=high)) {
                bin_pixels|=pixel2bin;
            }
            /* Shifting so that pixel2bin represent the next pixel */
            pixel2bin=pixel2bin<<1;
        }
        *pout = bin_pixels;
    }
}

/*
 * Fills a binary image according to the following rules :
 * if pixel value lower than low or higher than high the binary pixel
 * is set to 0, in other cases the pixel is set to 1.
 * \param src source image
 * \param dest destination image
 * \param low low value for threshold
 * \param high high value for treshold
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Thresh(MB_Image *src, MB_Image *dest, Uint32 low, Uint32 high)
{
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    
    /* Checking input parameters value */
    if (low>high) {
        return MB_ERR_BAD_VALUE;
    }
    
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    /* For this function the number of bytes is the number of */
    /* the binary image */
    bytes_in = MB_LINE_COUNT(dest);

    /* The dest image is a binary */
    switch(MB_PROBE_PAIR(src,dest)) {

    case MB_PAIR_8_1:
        for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
            THRESH_LINE_8_1(plines_out, plines_in, bytes_in, (PIX8) low, (PIX8) high);
        }
        break;

    case MB_PAIR_32_1:
        for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
            THRESH_LINE_32_1(plines_out, plines_in, bytes_in, (PIX32) low, (PIX32) high);
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
}
