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
 * Inverts (NOT operation) the binary pixels of the source line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void INVERT_LINE1(PLINE *plines_out, PLINE *plines_in, Uint32 bytes_in)
{
    Uint32 i;

    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++,pout++){
        *pout = ~(*pin);
    }
}

/*
 * Inverts (NOT operation) the pixels of the source line (8-bits pixels).
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void INVERT_LINE8(PLINE *plines_out, PLINE *plines_in, Uint32 bytes_in)
{
    Uint32 i;

#ifdef MB_VECTORIZATION_8
    MB_Vector8 vec1;
    MB_Vector8 v = MB_vec8_set(255);

    MB_Vector8 *pin = (MB_Vector8 *) (*plines_in);
    MB_Vector8 *pout = (MB_Vector8 *) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),pout++,pin++) {
        vec1 = MB_vec8_load(pin);
        vec1 = MB_vec8_sub(v,vec1);
        MB_vec8_store(pout, vec1);
    }
#else
    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++,pout++){
        *pout = ~(*pin);
    }
#endif
}

/*
 * Inverts (two-complement operation) the 32-bits pixels of the source line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void INVERT_LINE32(PLINE *plines_out, PLINE *plines_in, Uint32 bytes_in)
{
    Uint32 i;

    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++,pout++){
        *pout = ~(*pin);
    }
}

/*
 * Inverts the pixels values (negation) of the source image.
 * \param src source image
 * \param dest destination image
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Inv(MB_Image *src, MB_Image *dest)
{
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    Uint32 i;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    
    /* Setting up line pointers */
    plines_in  = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Source and dest must have the same depth */
    switch(MB_PROBE_PAIR(src,dest)) {
    case MB_PAIR_1_1:
        for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
            INVERT_LINE1( plines_out, plines_in, bytes_in);
        }
        break;
        
    case MB_PAIR_8_8:
        for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
            INVERT_LINE8( plines_out, plines_in, bytes_in);
        }
        break;

    case MB_PAIR_32_32:
        for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
            INVERT_LINE32( plines_out, plines_in, bytes_in);
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
} 
