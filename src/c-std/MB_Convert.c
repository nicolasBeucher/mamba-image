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

/*
 * Converts a binary image to an 8-bit image.
 * Pixels to True are set to 255 and to 0 otherwise.
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert1to8(MB_Image *src, MB_Image *dest)
{
    Uint32 i,j,u,pix_reg;
    PLINE *plines_in, *plines_out;
    Uint32 *pin;
    Uint8 *pout;
        
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    
    /* Converting the 1-bit values in 8-bit values */
    for(j=0; j<src->height; j++,plines_in++,plines_out++) {
        pin = (Uint32 *) (*plines_in);
        pout = (Uint8 *) (*plines_out);
        for(i=0; i<src->width; i+=32,pin++) {
            pix_reg = *pin;
            for(u=0;u<32;u++,pout++){
                /* for all the pixels inside the pixel register */
                *pout = (pix_reg&1) ? 0xFF : 0;
                pix_reg = pix_reg>>1;
            }    
        }
    }
    
    return MB_NO_ERR;
}

/*
 * Converts an 8-bit image to a binary image.
 * Pixels at 255 are set to True and to False otherwise.
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert8to1(MB_Image *src, MB_Image *dest)
{
    Uint32 i,j;
    Sint32 u;
    PLINE *plines_in, *plines_out;
    Uint32 *pout, pix_reg;

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    
    /* Converting the 8-bit values in 1-bit values */
    /* If 8-bit value is equal to 255 (white) the bit is set to 1 */
    /* and 0 in all other cases */
    for(j=0; j<src->height; j++,plines_in++,plines_out++) {
        pout = (Uint32 *) (*plines_out);
        for(i=0; i<src->width; i+=32,pout++) {
            /* Building the pixel register */
            pix_reg = 0;
            for(u=31;u>-1;u--){
                pix_reg = (pix_reg<<1) | (*(*plines_in+i+u)==0xFF);
            }
            *pout = pix_reg;
        }
    }    
    
    return MB_NO_ERR;
}

/*
 * Converts a binary image to an 32-bit image.
 * Pixels to True are set to 0xffffffff and to 0 otherwise.
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert1to32(MB_Image *src, MB_Image *dest)
{
    Uint32 i,j,u,pix_reg;
    PLINE *plines_in, *plines_out;
    Uint32 *pin;
    PIX32 *pout;
        
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    
    /* Converting the 1-bit values in 8-bit values */
    for(j=0; j<src->height; j++,plines_in++,plines_out++) {
        pin = (Uint32 *) (*plines_in);
        pout = (PIX32 *) (*plines_out);
        for(i=0; i<src->width; i+=32,pin++) {
            pix_reg = *pin;
            for(u=0;u<32;u++,pout++){
                /* For all the pixels inside the pixel register */
                *pout = (pix_reg&1) ? 0xFFFFFFFF : 0;
                pix_reg = pix_reg>>1;
            }    
        }
    }
    
    return MB_NO_ERR;
}

/*
 * Converts an 32-bit image to a binary image.
 * Pixels at 0xffffffff are set to True and to False otherwise.
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert32to1(MB_Image *src, MB_Image *dest)
{
    Uint32 i,j;
    Sint32 u;
    PLINE *plines_in, *plines_out;
    Uint32 *pout, pix_reg;
    PIX32 *pin;

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    
    /* Converting the 32-bit values in 1-bit values */
    /* If 32-bit value is equal to 0xffffffff (white) the bit is set to 1 */
    /* and 0 in all other cases */
    for(j=0; j<src->height; j++,plines_in++,plines_out++) {
        pout = (Uint32 *) (*plines_out);
        pin = (PIX32 *) (*plines_in);
        for(i=0; i<src->width; i+=32,pout++) {
            /* Building the pixel register */
            pix_reg = 0;
            for(u=31;u>-1;u--){
                pix_reg = (pix_reg<<1) | (pin[i+u]==0xFFFFFFFF);
            }
            *pout = pix_reg;
        }
    }    
    
    return MB_NO_ERR;
}

/*
 * Converts an 32-bit image to a 8-bit image (downscaling).
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert32to8(MB_Image *src, MB_Image *dest)
{
    Uint32 min, max, j, i;
    MB_errcode err;
    double value, multiplicator;
    PLINE *plines_in, *plines_out;
    PIX32 *pin;
    PIX8 *pout;
    
    err = MB_Range(src, &min, &max);
    if (err != MB_NO_ERR) {
        return err;
    }

    /* If the max is below the 256 value, simply copy the lower byte */
    /* of the 32-bit image */
    if (max<256) {
        return MB_CopyBytePlane(src, dest, 0);
    }

    /* Computing the multiplicator */
    multiplicator = ((double) 255.0)/max;

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;

    /* Converting the 32-bit values in 8-bit values by downscaling */
    for(j=0; j<src->height; j++, plines_in++, plines_out++) {
        pin = (PIX32 *) (*plines_in);
        pout = (PIX8 *) (*plines_out);
        for(i=0; i<src->width; i++, pin++, pout++) {
            value = (*pin) * multiplicator;
            *pout = (PIX8) value;
        }
    }

    return MB_NO_ERR;
}

/*
 * Converts an image of a given depth into another depth.
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Convert(MB_Image *src, MB_Image *dest)
{
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Comparing the depth of the src and the destination */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_1:;
    case MB_PAIR_8_8:
    case MB_PAIR_32_32:
        return MB_Copy(src,dest);
        break;
    case MB_PAIR_1_8:
        return MB_Convert1to8(src,dest);
        break;
    case MB_PAIR_8_1:
        return MB_Convert8to1(src,dest);
        break;
    case MB_PAIR_32_8:
        return MB_Convert32to8(src,dest);
        break;
    case MB_PAIR_8_32:
        return MB_CopyBytePlane(src,dest,0);
        break;
    case MB_PAIR_1_32:
        return MB_Convert1to32(src,dest);
        break;
    case MB_PAIR_32_1:
        return MB_Convert32to1(src,dest);
        break;
    default:
        break;
    }

    /* If this point is reached we can assume there was an error*/
    return MB_ERR_BAD_DEPTH;
}

