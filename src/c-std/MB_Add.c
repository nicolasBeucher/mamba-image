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
 * Adds the 1-bit pixels of a line to the 8-bit pixels of another. 
 * The result is put in a 8-bit pixels line (with saturation).
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_1_8_8(PLINE *plines_out,
                                  PLINE *plines_in1,
                                  PLINE *plines_in2,
                                  Uint32 bytes_in)
{
    Uint32 i,j;
    MB_Vector1 bin_pixels;
    Sint16 prov;
    
    MB_Vector1 *pin1 = (MB_Vector1 *) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin1++){
        /* we first extract the binary pixels (bit) in binaryT format */
        bin_pixels = MB_vec1_load(pin1);
        for(j=0;j<MB_vec1_size;j++,pin2++,pout++){
            /* for each binary pixel (i.e. bit), we add it to pin2 to */
            /* produce pout */
            prov = (Sint16) *pin2 + (bin_pixels&1);
            /* saturation operation */
            *pout = (prov > 255) ? 255 : (PIX8) prov;
            /* shifting the pixels to access the next one */
            bin_pixels = MB_vec1_shrgt(bin_pixels,1);
        }
    }
} 

/*
 * Adds the 1-bit pixels of a line to the 8-bit pixels of another. 
 * The result is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_1_8_32(PLINE *plines_out,
                                   PLINE *plines_in1,
                                   PLINE *plines_in2,
                                   Uint32 bytes_in)
{
    Uint32 i,j;
    MB_Vector1 bin_pixels;
    
    MB_Vector1 *pin1 = (MB_Vector1 *) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin1++){
        /* we first extract the binary pixels (bit) in binaryT format */
        bin_pixels = MB_vec1_load(pin1);
        for(j=0;j<MB_vec1_size;j++,pin2++,pout++){
            *pout = (PIX32) *pin2 + (bin_pixels&1);
            /* shifting the pixels to access the next one */
            bin_pixels = MB_vec1_shrgt(bin_pixels,1);
        }
    }
}

/*
 * Add the 8-bit pixels of a line to the 8-bit pixels of another. 
 * The result is put in a 8-bit pixels line (with saturation).
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_8_8_8(PLINE *plines_out,
                                  PLINE *plines_in1,
                                  PLINE *plines_in2,
                                  Uint32 bytes_in) 
{
    Uint32 i;

#ifdef MB_VECTORIZATION_8
    MB_Vector8 vec1, vec2;
    MB_Vector8 *pin1 = (MB_Vector8*) (*plines_in1);
    MB_Vector8 *pin2 = (MB_Vector8*) (*plines_in2);
    MB_Vector8 *pout = (MB_Vector8*) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),pin1++,pin2++,pout++) {
        vec1 = MB_vec8_load(pin1);
        vec2 = MB_vec8_load(pin2);
        vec1 = MB_vec8_adds(vec2,vec1);
        MB_vec8_store(pout, vec1);
    }
#else
    Uint16 prov;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        prov = (Uint16) *pin2 + *pin1;
        /* saturation operation */
        *pout = (prov > 255) ? 255 : (PIX8) prov;
    }
#endif
}
 
/*
 * Add the 8-bit pixels of a line to the 8-bit pixels of another. 
 * The result is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_8_8_32(PLINE *plines_out,
                                   PLINE *plines_in1,
                                   PLINE *plines_in2,
                                   Uint32 bytes_in) 
{
    Uint32 i;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        *pout = (PIX32) *pin2 + *pin1;
    }
}

/*
 * Add the 32-bit pixels of a line to the 32-bit pixels of another. 
 * The result is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_32_32_32(PLINE *plines_out,
                                     PLINE *plines_in1,
                                     PLINE *plines_in2,
                                     Uint32 bytes_in) 
{
    Uint32 i;

#ifdef MB_VECTORIZATION_32
    MB_Vector32 vec1,vec2;
    MB_Vector32 *pin1 = (MB_Vector32*) (*plines_in1);
    MB_Vector32 *pin2 = (MB_Vector32*) (*plines_in2);
    MB_Vector32 *pout = (MB_Vector32*) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector32),pin1++,pin2++,pout++) {
        vec1 = MB_vec32_load(pin1);
        vec2 = MB_vec32_load(pin2);
        vec1 = MB_vec32_add(vec2,vec1);
        MB_vec32_store(pout, vec1);
    }
#else
    PIX32 *pin1 = (PIX32 *) (*plines_in1);
    PIX32 *pin2 = (PIX32 *) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin1++,pin2++,pout++){
        *pout = *pin2 + *pin1;
    }
#endif
}

/*
 * Add the 1-bit pixels of a line to the 32-bit pixels of another. 
 * The result is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_1_32_32(PLINE *plines_out,
                                    PLINE *plines_in1,
                                    PLINE *plines_in2,
                                    Uint32 bytes_in) 
{
    Uint32 i,j;
    MB_Vector1 bin_pixels;
    
    MB_Vector1 *pin1 = (MB_Vector1 *) (*plines_in1);
    PIX32 *pin2 = (PIX32 *) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin1++){
        /* we first extract the binary pixels (bit) in binaryT format */
        bin_pixels = MB_vec1_load(pin1);
        for(j=0;j<MB_vec1_size;j++,pin2++,pout++){
            *pout = *pin2 + (bin_pixels&1);
            /* shifting the pixels to access the next one */
            bin_pixels = MB_vec1_shrgt(bin_pixels,1);
        }
    }
}

/*
 * Add the 8-bit pixels of a line to the 32-bit pixels of another. 
 * The result is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line of im1
 */
static INLINE void ADD_LINE_8_32_32(PLINE *plines_out,
                                    PLINE *plines_in1,
                                    PLINE *plines_in2,
                                    Uint32 bytes_in) 
{
    Uint32 i;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PIX32 *pin2 = (PIX32 *) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        *pout = *pin2 + (PIX32) *pin1;
    }
}

/*
 * Adds the pixels of two images and put the result in the third image.
 * Depending on the format of the target image, the result may be saturated or not.
 * You can perform the following additions :
 *      1-bit + 1-bit = 1-bit (call the MB_Or function)
 *      1-bit + 8-bit = 8-bit (saturated)
 *      1-bit + 8-bit = 32-bit 
 *      1-bit + 32-bit = 32-bit
 *      8-bit + 8-bit = 8-bit (saturated)
 *      8-bit + 8-bit = 32-bit
 *      8-bit + 32-bit = 32-bit
 *      32-bit + 32-bit = 32-bit
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the addition of image 1 and 2 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Add(MB_Image *src1, MB_Image *src2, MB_Image *dest) {

    PLINE *plines_in1, *plines_in2, *plines_out;
    Uint32 bytes_in;
    Uint32 i;
    
    /* verification over image size compatibility */
    if (!MB_CHECK_SIZE_3(src1, src2, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    
    /* image 2 becomes the deeper one */
    if (src1->depth > src2->depth) {
        MB_Image *tmp = src1; src1 = src2; src2 = tmp;
    }
    
    /* Destination image depth must be at least the same or higher */
    /* than image 2 depth otherwise the function returns with an error. */
    if(dest->depth < src2->depth) {
        return MB_ERR_BAD_DEPTH;
    }

    /* Setting up the pointers */
    plines_in1 = src1->plines;
    plines_in2 = src2->plines;
    plines_out = dest->plines;
    
    /* Setting up offset */
    bytes_in = MB_LINE_COUNT(src1);
    
    /* Evaluating the addition case : 
     * 9 cases can happen depending of the two input images depth
     * Only the "legal" ones are being considered. Other cases make
     * The function returns with an error.
      */
    switch(MB_PROBE_PAIR(src1,src2)) {

    /* Two binary images */
    case MB_PAIR_1_1:
        return MB_Or(src1, src2, dest);
        break;
    
    /* binary + 8-bit images */
    case MB_PAIR_1_8:
        if (dest->depth == 8) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                ADD_LINE_1_8_8(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        if (dest->depth == 32) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                ADD_LINE_1_8_32(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        break;

    /* two 8-bit images */
    case MB_PAIR_8_8:
        if(dest->depth == 8) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                ADD_LINE_8_8_8(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        if(dest->depth == 32) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                ADD_LINE_8_8_32(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        break;

    /* two 32-bit images */
    case MB_PAIR_32_32:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            ADD_LINE_32_32_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    /* binary image + 32-bit image */
    case MB_PAIR_1_32:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            ADD_LINE_1_32_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    /*8-bit image + 32-bit image*/
    case MB_PAIR_8_32:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            ADD_LINE_8_32_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    /* Other cases are impossible and provoke an error */
    default:
        /* Incompatible depths */
        return MB_ERR_BAD_DEPTH;
        break;
    }
    
    return MB_NO_ERR;
}
