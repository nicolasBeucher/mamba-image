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

/* Array containing the number of pixel set to True in a byte*/
const Uint64 MB_VolumePerByte[256] = {
    00,01,01,02,01,02,02,03,01,02,02,03,02,03,03,04,
    01,02,02,03,02,03,03,04,02,03,03,04,03,04,04,05,
    01,02,02,03,02,03,03,04,02,03,03,04,03,04,04,05,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    01,02,02,03,02,03,03,04,02,03,03,04,03,04,04,05,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    03,04,04,05,04,05,05,06,04,05,05,06,05,06,06,07,
    01,02,02,03,02,03,03,04,02,03,03,04,03,04,04,05,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    03,04,04,05,04,05,05,06,04,05,05,06,05,06,06,07,
    02,03,03,04,03,04,04,05,03,04,04,05,04,05,05,06,
    03,04,04,05,04,05,05,06,04,05,05,06,05,06,06,07,
    03,04,04,05,04,05,05,06,04,05,05,06,05,06,06,07,
    04,05,05,06,05,06,06,07,05,06,06,07,06,07,07,8
};

/*
 * Computes the volume of a line of an 1-bit image.
 * \param plines pointer on the source image pixel line
 * \param bytes number of bytes inside the line
 * \param volume pointer to the variable holding the computed volume of the image
 */
static INLINE void VOLUME_LINE_1(PLINE *plines, Uint32 bytes, Uint64 *volume)
{
    Uint32 i;
    
    PLINE pin = (PLINE) (*plines);
    
    for(i=0;i<bytes;i++,pin++){
        *volume += MB_VolumePerByte[*pin];
    }
} 

/*
 * Computes the volume of a line of an 8-bit image.
 * \param plines pointer on the source image pixel line
 * \param bytes number of bytes inside the line
 * \param volume pointer to the variable holding the computed volume of the image
 */
static INLINE void VOLUME_LINE_8(PLINE *plines, Uint32 bytes, Uint64 *volume)
{
    Uint32 i;

    PIX8 *pin = (PIX8 *) (*plines);

    for(i=0;i<bytes;i++,pin++){
        *volume += *pin;
    }
} 

/*
 * Computes the volume of a line of an 32-bit image.
 * \param plines pointer on the source image pixel line
 * \param bytes number of bytes inside the line
 * \param volume pointer to the variable holding the computed volume of the image
 */
static INLINE void VOLUME_LINE_32(PLINE *plines, Uint32 bytes, Uint64 *volume)
{
    Uint32 i;

    PIX32 *pin = (PIX32 *) (*plines);

    for(i=0;i<bytes;i+=4,pin++){
        *volume += (Uint64) *pin;
    }
} 

/*
 * Computes the volume of an image.
 * The volume is the sum of the pixel values (i.e. integration 
 * of the image)
 * \param src source image
 * \param pVolume pointer to the volume variable
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Volume(MB_Image *src, Uint64 *pVolume) {
    PLINE *plines;
    Uint32 bytes;
    Uint64 volume;
    Uint32 i;

    /* Setting up line pointers */
    plines = src->plines;
    bytes = MB_LINE_COUNT(src);

    /* Init volume variable */
    volume = 0;

    /* Volume computation depends on the depth of the image */
    switch(src->depth) {
    case 1:
        for(i=0; i<src->height; i++, plines++) {
            VOLUME_LINE_1(plines, bytes, &volume );
        }
        break;

    case 8:
        for(i=0; i<src->height; i++, plines++) {
            VOLUME_LINE_8(plines, bytes, &volume );
        }
        break;

    case 32:
        for(i=0; i<src->height; i++, plines++) {
            VOLUME_LINE_32(plines, bytes, &volume );
        }
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    /* Returns of volume */
    *pVolume = volume;

    return MB_NO_ERR;
}

