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
 * Subtracts the 1-bit pixels of a line to the 8-bit pixels of another. 
 * The results is put in a 8-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_8_1_8(PLINE *plines_out,
                                  PLINE *plines_in1,
                                  PLINE *plines_in2,
                                  Uint32 bytes_in)
{
    Uint32 i,u;
    MB_Vector1 pix_reg;
    Sint16 prov;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    MB_Vector1 *pin2 = (MB_Vector1 *) (*plines_in2);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin2++){
        pix_reg = *pin2;
        for(u=0;u<MB_vec1_size;u++,pin1++,pout++){
            prov = (Sint16) *pin1 - (pix_reg&1);
            if (prov < 0) {
                *pout = 0;
            } else {
                *pout = (PIX8) prov;
            }
            /* Next pixel in the register */
            pix_reg = pix_reg>>1;
        }
    }
}

/*
 * Subtracts the 8-bit pixels of a line to the 8-bit pixels of another. 
 * The results is put in a 8-bits pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_8_8_8(PLINE *plines_out,
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
        vec1 = MB_vec8_subs(vec1,vec2);
        MB_vec8_store(pout, vec1);
    }
#else
    Sint16 prov;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        prov = ((Sint16) *pin1) - *pin2; 
        if (prov < 0) {
            *pout = 0;
        } else {
            *pout = (PIX8) prov;
        }
    }
#endif
} 

/*
 * Subtracts the 8-bit pixels of a line to the 8-bit pixels of another. 
 * The results is put in a 32-bits pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_8_8_32(PLINE *plines_out,
                                   PLINE *plines_in1,
                                   PLINE *plines_in2,
                                   Uint32 bytes_in)
{
    Uint32 i;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        *pout = (PIX32) *pin1 - *pin2;
    }
}

/*
 * Subtracts the 32-bit pixels of a line to the 32-bit pixels of another. 
 * The results is put in a 32-bit pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_32_32_32(PLINE *plines_out,
                                     PLINE *plines_in1,
                                     PLINE *plines_in2,
                                     Uint32 bytes_in) 
{
    Uint32 i;

#ifdef MB_VECTORIZATION_32
    MB_Vector32 vec1, vec2;
    MB_Vector32 *pin1 = (MB_Vector32*) (*plines_in1);
    MB_Vector32 *pin2 = (MB_Vector32*) (*plines_in2);
    MB_Vector32 *pout = (MB_Vector32*) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector32),pin1++,pin2++,pout++) {
        vec1 = MB_vec32_load(pin1);
        vec2 = MB_vec32_load(pin2);
        vec1 = MB_vec32_sub(vec1,vec2);
        MB_vec32_store(pout, vec1);
    }
#else
    PIX32 *pin1 = (PIX32 *) (*plines_in1);
    PIX32 *pin2 = (PIX32 *) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin1++,pin2++,pout++){
        *pout = *pin1 - *pin2;
    }
#endif
}

/*
 * Subtracts the 8-bit pixels of a line to the 32-bit pixels of another. 
 * The results is put in a 32-bits pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_8_32_32(PLINE *plines_out,
                                    PLINE *plines_in1,
                                    PLINE *plines_in2,
                                    Uint32 bytes_in) 
{
    Uint32 i;
    
    PLINE pin1 = (PLINE) (*plines_in1);
    PIX32 *pin2 = (PIX32 *) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin1++,pin2++,pout++){
        *pout = *pin1 - *pin2;
    }
}

/*
 * Subtracts the 32-bit pixels of a line to the 8-bit pixels of another. 
 * The results is put in a 32-bits pixels line.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in1 pointer on the source image 1-bit pixel line
 * \param plines_in2 pointer on the source image 8-bit pixel line
 * \param bytes number of bytes inside the line
 */
static INLINE void SUB_LINE_32_8_32(PLINE *plines_out,
                                    PLINE *plines_in1,
                                    PLINE *plines_in2,
                                    Uint32 bytes_in) 
{
    Uint32 i;
    
    PIX32 *pin1 = (PIX32 *) (*plines_in1);
    PLINE pin2 = (PLINE) (*plines_in2);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i++,pin1++,pin2++,pout++){
        *pout = *pin1 - *pin2;
    }
}

/*
 * Subtracts the values of pixels of the second image to the values of
 * the pixels in the first image
 * \param src1 image 1
 * \param src2 image 2
 * \param dest image resulting of the subtraction 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Sub(MB_Image *src1, MB_Image *src2, MB_Image *dest)
{
    PLINE *plines_in1, *plines_in2, *plines_out;
    Uint32 bytes_in;
    Uint32 i;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_3(src1, src2, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    
    /* Destination image depth must be at least the same or higher */
    /* than image 1 or 2 depth otherwise the function returns with an error. */
    if( (dest->depth < src1->depth) || (dest->depth < src2->depth) )
        return MB_ERR_BAD_DEPTH;
    
    /* Setting up the pointers */
    plines_in1 = src1->plines;
    plines_in2 = src2->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src2);
    
    switch(MB_PROBE_PAIR(src1,src2)) {
    
    /* Subtracting a binary image to binary image amounts to a set difference*/
    case MB_PAIR_1_1:
        return MB_Diff(src1, src2, dest);
        break;
    
    /* Subtracting a binary image to an 8-bit image */
    case MB_PAIR_8_1:
        if(dest->depth !=8)
            return MB_ERR_BAD_DEPTH;
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            SUB_LINE_8_1_8(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    /* subtracting a binary image to an 8-bit image */
    case MB_PAIR_8_8:
        if(dest->depth == 8) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                SUB_LINE_8_8_8(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        if(dest->depth == 32) {
            for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
                SUB_LINE_8_8_32(plines_out, plines_in1, plines_in2, bytes_in);
            }
        }
        break;

    case MB_PAIR_32_32:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            SUB_LINE_32_32_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    case MB_PAIR_8_32:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            SUB_LINE_8_32_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    case MB_PAIR_32_8:
        for (i=0; i<src1->height; i++, plines_out++, plines_in1++, plines_in2++) {
            SUB_LINE_32_8_32(plines_out, plines_in1, plines_in2, bytes_in);
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }
    
    return MB_NO_ERR;
}
