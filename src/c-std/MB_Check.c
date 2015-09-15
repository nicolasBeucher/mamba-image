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
 * Checks if the line is empty.
 * \param plines_in pointer on the source image pixel line
 * \param linoff_in offset inside the source image line
 * \param bytes_in number of bytes inside the line
 * \param isEmpty integer value indicating emptyness
 */
static INLINE void CHECK_LINE(PLINE *plines_in, Uint32 bytes_in, Uint32 * isEmpty)
{
    Uint32 i;

    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);

    for(i=0;(i<bytes_in) && (*isEmpty==1);i+=sizeof(MB_Vector1),pin++){
        if((*pin)!=0){
           *isEmpty = 0;
        }
    }
}
 
/*
 * Verifies that the image is not empty (all pixels to 0).
 * \param src the source image 
 * \param isEmpty an integer which is set to 1 if empty or 0 if not
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Check(MB_Image *src, Uint32 *isEmpty) 
{
    Uint32 i;
    PLINE *plines_in;
    Uint32 bytes_in;

    /* Setting up line pointers */
    plines_in = src->plines;
    bytes_in = MB_LINE_COUNT(src);
    
    /* Emptiness is assumed false at the begining */
    *isEmpty = 1;

    for(i = 0; (i < src->height) && (*isEmpty==1); i++, plines_in++) {
        CHECK_LINE(plines_in, bytes_in, isEmpty);
        /* As soon as a difference has been found the function ends */
    }

    return MB_NO_ERR;
}

