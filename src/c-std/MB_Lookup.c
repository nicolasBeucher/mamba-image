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
 * Applies the function in the lookup table to the line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param ptab lookup table pointer
 */
static INLINE void LOOKUP_LINE8(PLINE *plines_out, PLINE *plines_in, Uint32 bytes_in, Uint32 *ptab)
{
    Uint32 j;

    PLINE pin = (PLINE) (*plines_in);
    PLINE pout = (PLINE) (*plines_out);

    for(j=0;j<bytes_in;j++,pin++,pout++){
        *pout = (PIX8) ptab[*pin];
    }
}

/*
 * Applies the function in the lookup table to the pixels of source image.
 * A pixel value is changed to a new value accordingly with its current value
 * \param src source image
 * \param dest destination image
 * \param ptab the lookup table pointer
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Lookup(MB_Image *src, MB_Image *dest, Uint32 *ptab)
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
    
    /* The two images must have 8-bit */
    /* depth */
    switch(MB_PROBE_PAIR( src, dest )) {

    case MB_PAIR_8_8:
        for(i = 0; i < src->height; i++, plines_in++, plines_out++) {
            LOOKUP_LINE8( plines_out, plines_in, bytes_in, ptab );
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
}
