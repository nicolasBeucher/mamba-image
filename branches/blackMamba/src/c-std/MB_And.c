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
 * Applies a AND between two pixels lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1 pixel line
 * \param plines_in2 pointer on the source image 2 pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void AND_LINE(PLINE *plines_out,
                            PLINE *plines_in1,
                            PLINE *plines_in2,
                            Uint32 bytes_in)
{
    Uint32 i;

    MB_Vector1 *pin1 = (MB_Vector1 *) (*plines_in1);
    MB_Vector1 *pin2 = (MB_Vector1 *) (*plines_in2);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin1++,pin2++,pout++) {
        *pout = MB_vec1_and((*pin2),(*pin1));
    }
}

/*
 * Performs a bitwise AND between the pixels of two images.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_And(MB_Image *src1, MB_Image *src2, MB_Image *dest) {
    Uint32 i;
    PLINE *plines_in1, *plines_in2, *plines_out;
    Uint32 bytes_in;
    
    /* verification over depth and size */
    if (!MB_CHECK_SIZE_3(src1, src2, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    if(dest->depth != src1->depth) {
        return MB_ERR_BAD_DEPTH;
    }

    /* Setting up line pointers */
    plines_in1 = src1->plines;
    plines_in2 = src2->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src1);

    /* The two source images must have the same */
    /* depth */
    switch (MB_PROBE_PAIR(src1, src2)) {
    case MB_PAIR_1_1:
    case MB_PAIR_8_8:
    case MB_PAIR_32_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }

    /* for all the lines */
    for (i=0; i<src1->height; i++, plines_in1++, plines_in2++, plines_out++) {
        AND_LINE(plines_out,plines_in1,plines_in2,bytes_in);
    }

    return MB_NO_ERR;
}
