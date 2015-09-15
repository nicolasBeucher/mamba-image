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
 * Fills an image with a specific value.
 * \param dest the image
 * \param value the value to fill the image
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_ConSet(MB_Image *dest, Uint32 value) {
    Uint8 pattern8;
    Uint32 bytes;
    Uint32 i;
    Uint32 *pix;
    
    /* Pattern depends on the depth of the image */
    switch(dest->depth) {
    case 1:
        /* Pattern computation */
        /* in binary image, value is either one or zero */
        pattern8 = (value) ? 0XFF : 0;
        bytes = (dest->width*dest->height)/8;
        /* Lines fill */
        MB_memset(dest->pixels, pattern8, bytes);
        break;

    case 8:
        /* Pattern computation */
        pattern8 = value & 0xFF;
        bytes = (dest->width*dest->height);
        /* Lines fill */
        MB_memset(dest->pixels, pattern8, bytes);
        break;

    case 32:
        /* Pretending the signed 32-bit is unsigned */
        bytes = (dest->width*dest->height);
        for(i=0, pix=(Uint32 *)dest->pixels;i<bytes;i++,pix++) {
            *pix = value;
        }
        break;
        
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
} 
