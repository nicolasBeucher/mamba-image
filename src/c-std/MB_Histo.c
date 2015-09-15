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
 * Computes the histogram of a line of an 8-bits image.
 * \param plines pointer on the source image pixel line
 * \param bytes number of bytes inside the line
 * \param phisto pointer to the histogram array
 */
static INLINE void HISTO_LINE8(PLINE *plines, Uint32 bytes, Uint32 *phisto)
{
    Uint32 i;

    PLINE pin = (PLINE) (*plines);

    for(i=0;i<bytes;i++,pin++){
        /* Filling the histogram information with the line data */
        phisto[(*pin)]++;
    }
}

/*
 * Computes the histogram of an image.
 * The histogram is an array with a minimal size of 256.
 * \param src source image
 * \param phisto pointer to the histogram array
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Histo(MB_Image *src, Uint32 *phisto)
{
    Uint32 i;
    PLINE *plines;
    Uint32 bytes;

    /* Setting up line pointers */
    plines = src->plines;
    bytes = MB_LINE_COUNT(src);
    
    /* Reset the histogram value */
    for(i = 0; i<256; i++) {
        phisto[i] = 0;
    }

    /* Only 8-bit images can be processed */
    switch(src->depth) {

    case 8:
        for(i=0; i < src->height; i++, plines++) {
            HISTO_LINE8(plines, bytes, phisto );
        }
        break;
        
    default:
        /* Cannot have histograms for 32-bit or binary images */
        return MB_ERR_BAD_DEPTH;
        break;
      }

      return MB_NO_ERR;
}

