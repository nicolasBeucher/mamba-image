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
 * Extracts the byte plane at the given position out of 32-bit lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the byte plane index
 * \return the value of the bit
 */
static INLINE void EXTRACT_BYTEPLANE_LINE(PLINE *plines_out,
                                          PLINE *plines_in,
                                          Uint32 bytes_in, Uint32 plane)
{
    Uint32 i;
    
    Uint32 *pin = (Uint32 *) (*plines_in);
    PLINE pout = (PLINE) (*plines_out);
    
    for(i=0;i<bytes_in;i+=4,pin++,pout++) {
        *pout = (PIX8) (((*pin)>>(plane*8))&0xFF);
    }
}


/*
 * Inserts the byte plane at the given position in 32-bit lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the byte plane index
 * \return the value of the bit
 */
static INLINE void INSERT_BYTEPLANE_LINE(PLINE *plines_out,
                                          PLINE *plines_in,
                                          Uint32 bytes_in, Uint32 plane)
{
    Uint32 i;
    Uint32 plane_mask[4] = {0xFFFFFF00, 0xFFFF00FF, 0xFF00FFFF, 0x00FFFFFF};
    
    PLINE pin = (PLINE) (*plines_in);
    Uint32 *pout = (Uint32 *) (*plines_out);
    
    for(i=0;i<bytes_in;i++,pin++,pout++) {
        *pout = (*pout & plane_mask[plane]) | (((Uint32) *pin)<<(8*plane));
    }
}

/*
 * Inserts the grey scale into the byte plane of the 32-bit
 * image.
 * \param src source image
 * \param dest destination image 
 * \param plane the byte plane in which the grey scale image will be copied
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_InsertBytePlane8to32(MB_Image *src, MB_Image *dest, Uint32 plane)
{
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
        
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);

    for (i=0; i<src->height; i++, plines_in++, plines_out++) {
        INSERT_BYTEPLANE_LINE(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Extracts the byte plane of the 32-bit image and
 * puts it in the grey scale image.
 * \param src source image
 * \param dest destination image
 * \param plane the byte plane index 
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_ExtractBytePlane32to8(MB_Image *src, MB_Image *dest, Uint32 plane)
{
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);
    
    for (i = 0; i < src->height; i++, plines_in++, plines_out++) {
        EXTRACT_BYTEPLANE_LINE(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Inserts or extracts the byte plane in/out an image src into/from 
 * dest.
 * \param src source image
 * \param dest destination image
 * \param plane the plane number
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_CopyBytePlane(MB_Image *src, MB_Image *dest, Uint32 plane) {
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* The plane index must be between 0 and 3 included */
    if (plane>3) 
        return MB_ERR_BAD_PARAMETER;

    /* Comparing the depth of the src and the destination */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_8_32:
        return MB_InsertBytePlane8to32(src,dest,plane);
        break;
    case MB_PAIR_32_8:
        return MB_ExtractBytePlane32to8(src,dest,plane);
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    /* If this point is reached we can assume there was an error*/
    return MB_ERR_BAD_DEPTH;
}
