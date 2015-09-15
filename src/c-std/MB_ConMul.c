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
 * Multiplies a constant value to an 8-bit pixels image and places the 
 * result in an 8-bit image. 
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image 1 pixel line
 * \param bytes_in number of bytes inside the line
 * \param ubvalue the constant value
 */
static INLINE void CONMUL_LINE_8_8(PLINE *plines_out,
                                   PLINE *plines_in,
                                   Uint32 bytes_in, Uint32 ubvalue)
{
    Uint32 i;
    Uint32 prov;

    PLINE pin = (PLINE) (*plines_in);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i++,pin++,pout++){
        prov = ((Uint32) *pin)*ubvalue;
        if (prov > 255) {
            *pout = 255;
        } else { 
            if (prov < 0) 
                *pout = 0;
            else 
                *pout = (PIX8) prov;
        }        
    }
}

/*
 * Multiplies a constant value to a 32-bit pixels image and places the 
 * result in a 32-bit image.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image 1 pixel line
 * \param bytes_in number of bytes inside the line
 * \param value the constant value
 */
static INLINE void CONMUL_LINE_32_32(PLINE *plines_out,
                                     PLINE *plines_in,
                                     Uint32 bytes_in, Uint32 value)
{
    Uint32 i;

    PIX32 *pin = (PIX32 *) (*plines_in);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin++,pout++){
        *pout = (*pin)*value;
    }
}

/*
 * Multiplies a constant value to the pixels of an image.
 * \param src the source image
 * \param value the constant value to be multiplied to the pixels
 * \param dest the image resulting of the multiplication of image 1 by the value. 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_ConMul(MB_Image *src, Uint32 value, MB_Image *dest)
{
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* The two images must have the same */
    /* depth */
    switch(MB_PROBE_PAIR(src,dest)) {

    case MB_PAIR_8_8:
        /* Addition with saturation */
        for (i = 0;i < src->height;i++, plines_in++, plines_out++) {
            CONMUL_LINE_8_8( plines_out, plines_in, bytes_in, value );
        }
        break;

    case MB_PAIR_32_32:
        for (i = 0;i < src->height;i++, plines_in++, plines_out++) {
            CONMUL_LINE_32_32( plines_out, plines_in, bytes_in, value );
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
} 


