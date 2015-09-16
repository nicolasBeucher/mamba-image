/*
 * Copyright (c) <2014>, <Nicolas BEUCHER>
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
 * Converts an 32-bit image to a 8-bit image (downscaling).
 * \param src source image
 * \param dest destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Convert32to8(MB3D_Image *src, MB3D_Image *dest)
{
    Uint32 min, max, allmax, z, j, i;
    MB_errcode err = MB_NO_ERR;
    double value, multiplicator;
    PLINE *plines_in, *plines_out;
    PIX32 *pin;
    PIX8 *pout;
    MB_Image *si;
    
    allmax = 0;
    for(z=0; z<src->length && err==MB_NO_ERR; z++) {
        err = MB_Range(src->seq[z], &min, &max);
        allmax = max>allmax ? max : allmax;
    }

    /* If the max is below the 256 value, simply copy the lower byte */
    /* of the 32-bit image */
    if (allmax<256) {
        for(z=0; z<src->length && err==MB_NO_ERR; z++) {
            err = MB_CopyBytePlane(src->seq[z], dest->seq[z], 0);
        }
    } else {
        /* Computing the multiplicator */
        multiplicator = ((double) 255.0)/allmax;

        for(z=0; z<src->length && err==MB_NO_ERR; z++) {
            /* Setting up line pointers */
            si = src->seq[z];
            plines_in = si->plines;
            plines_out = dest->seq[z]->plines;

            /* Converting the 32-bit values in 8-bit values by downscaling */
            for(j=0; j<si->height; j++, plines_in++, plines_out++) {
                pin = (PIX32 *) (*plines_in);
                pout = (PIX8 *) (*plines_out);
                for(i=0; i<si->width; i++, pin++, pout++) {
                    value = (*pin) * multiplicator;
                    *pout = (PIX8) value;
                }
            }
        }
    }

    return err;
}

/*
 * Converts a 3D image of a given depth into another depth.
 * \param src 3D source image
 * \param dest 3D destination image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Convert(MB3D_Image *src, MB3D_Image *dest)
{
    Uint32 z;
    MB_errcode err = MB_NO_ERR;

    /* Verification over image size compatibility */
    if (!MB3D_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Comparing the depth of the src and the destination */
    switch (MB3D_PROBE_PAIR(src, dest)) {
    case MB_PAIR_32_8:
        err = MB3D_Convert32to8(src,dest);
        break;
    default:
        for(z=0; z<src->length && err==MB_NO_ERR; z++) {
            err = MB_Convert(src->seq[z], dest->seq[z]);
        }
        break;
    }

    return err;
}

