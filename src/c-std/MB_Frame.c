
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

/* Functions for each depth */

static INLINE MB_errcode MB_Frame1(MB_Image *src, Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry) {
    Uint32 bytes_in;
    Uint32 i,j,u;
    Uint32 x,y;
    PLINE *plines;
    MB_Vector1 *pin, pixel_register;
    
    /* Default value */
    /* This way, the first comparison will always be in */
    /* favor of the pixel */

    *brx = 0;
    *bry = 0;
    *ulx = src->width-1;
    *uly = src->height-1;

    /* Setting up line pointers */
    /* and offset to avoid edge of the image */
    plines = src->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Proceeding line by line */
    for(i=0, y=0; i<src->height; y++, i++, plines++) {
        pin = (MB_Vector1 *) (*plines);
        for(j=0,x=0; j<bytes_in; j+=sizeof(MB_Vector1), pin++) {
            pixel_register = *pin;
            for(u=0; u<MB_vec1_size; u++, x++) {
                if(pixel_register&1) {
                    *brx = *brx>x ? *brx : x;
                    *bry = *bry>y ? *bry : y;
                    *ulx = *ulx>x ? x : *ulx;
                    *uly = *uly>y ? y : *uly;
                }
                /* next pixel */
                pixel_register = pixel_register>>1;
            }
        }
    }

    return MB_NO_ERR;
}

static INLINE MB_errcode MB_Frame8(MB_Image *src, PIX8 thresval, Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry) {
    Uint32 bytes_in;
    Uint32 i,j;
    Uint32 x,y;
    PLINE *plines;
    PLINE pin;
    
    /* Default value */
    /* This way, the first comparison will always be in */
    /* favor of the pixel */

    *brx = 0;
    *bry = 0;
    *ulx = src->width-1;
    *uly = src->height-1;

    /* Setting up line pointers */
    /* and offset to avoid edge of the image */
    plines = src->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Proceeding line by line */
    for(i=0, y=0; i < src->height; i++, y++, plines++) {
        pin = (PLINE) (*plines);
        for(j=0, x=0; j<bytes_in; j++, x++, pin++) {
            if(*pin>=thresval) {
                *brx = *brx>x ? *brx : x;
                *bry = *bry>y ? *bry : y;
                *ulx = *ulx>x ? x : *ulx;
                *uly = *uly>y ? y : *uly;
            }
        }
    }

    return MB_NO_ERR;
}

static INLINE MB_errcode MB_Frame32(MB_Image *src, PIX32 thresval, Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry) {
    Uint32 bytes_in;
    Uint32 i,j;
    Uint32 x,y;
    PLINE *plines;
    PIX32 *pin;
    
    /* Default value */
    /* This way, the first comparison will always be in */
    /* favor of the pixel */

    *brx = 0;
    *bry = 0;
    *ulx = src->width-1;
    *uly = src->height-1;

    /* Setting up line pointers */
    /* and offset to avoid edge of the image */
    plines = src->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Proceeding line by line */
    for(i=0, y=0; i < src->height; i++, y++, plines++) {
        pin = (PIX32 *) (*plines);
        for(j=0, x=0; j<bytes_in/4; j++, x++, pin++) {
            if(*pin>=thresval) {
                *brx = *brx>x ? *brx : x;
                *bry = *bry>y ? *bry : y;
                *ulx = *ulx>x ? x : *ulx;
                *uly = *uly>y ? y : *uly;
            }
        }
    }

    return MB_NO_ERR;
}

/*
 * Returns the smallest frame that contains all the pixels of image that are greater or equal to
 * the given threshold value, using the four last pointers to describe it.
 * \param src source image
 * \param thresval the threshold value used to compute the frame
 * \param ulx the x-coordinate of the upper left corner of the frame
 * \param uly the y-coordinate of the upper left corner of the frame
 * \param brx the x-coordinate of the bottom right corner of the frame
 * \param bry the y-coordinate of the bottom right corner of the frame
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Frame(MB_Image *src, Uint32 thresval, Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry) {

    /* Comparing the depth of the src and the destination */
    switch (src->depth) {
    case 1:
        /* For binary image the threshold value is always 1*/
        return MB_Frame1(src, ulx, uly, brx, bry);
        break;
    case 8:
        return MB_Frame8(src, (PIX8) thresval, ulx, uly, brx, bry);
        break;
    case 32:
        return MB_Frame32(src, (PIX32) thresval, ulx, uly, brx, bry);
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    /* If this point is reached, we can assume there was an error*/
    return MB_ERR_BAD_VALUE;
}

