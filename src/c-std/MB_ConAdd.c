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
 * Adds a constant value to an 8-bits pixels image and places the 
 * result in an 8-bit image. 
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image 1 pixel line
 * \param bytes_in number of bytes inside the line
 * \param ubvalue the constant value
 */
static INLINE void CONADD_LINE_8_8(PLINE *plines_out,
                                   PLINE *plines_in,
                                   Uint32 bytes_in, Sint16 ubvalue)
{
    Uint32 i;

#ifdef MB_VECTORIZATION_8
    MB_Vector8 vec1;
    MB_Vector8 *pin, *pout, constv;
    PIX8 satvalue;
    
    pin = (MB_Vector8*) (*plines_in);
    pout = (MB_Vector8*) (*plines_out);
    
    /* Computing the saturated value to add */
    /* or substract if the value is negative */
    if (ubvalue<0) {
        /* The value is negative */
        /* We subtract its absolute value to the pixels */
        if (ubvalue<-255) {
            satvalue = 255;
        } else {
            satvalue = (PIX8) abs(ubvalue);
        }
        
        constv = MB_vec8_set(satvalue);
        
        for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),pin++,pout++) {
            vec1 = MB_vec8_load(pin);
            vec1 = MB_vec8_subs(vec1,constv);
            MB_vec8_store(pout, vec1);
        }
        
    } else {
        /* The value is positive */
        /* We add it to the pixels */
        if (ubvalue>255) {
            satvalue = 255;
        } else {
            satvalue = (PIX8) ubvalue;
        }
        constv = MB_vec8_set(satvalue);
        
        for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),pin++,pout++) {
            vec1 = MB_vec8_load(pin);
            vec1 = MB_vec8_adds(vec1,constv);
            MB_vec8_store(pout, vec1);
        }
    }
    
#else
    Sint16 prov;

    PLINE pin = (PLINE) (*plines_in);
    PLINE pout = (PLINE) (*plines_out);

    for(i=0;i<bytes_in;i++,pin++,pout++){
        prov = *pin+ubvalue;
        if (prov > 255) {
            *pout = 255;
        } else { 
            if (prov < 0) 
                *pout = 0;
            else 
                *pout = (PIX8) prov;
        }        
    }
#endif
}

/*
 * Adds a constant value to a 32-bits pixels image and places the 
 * result in a 32-bit image.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image 1 pixel line
 * \param bytes_in number of bytes inside the line
 * \param value the constant value
 */
static INLINE void CONADD_LINE_32_32(PLINE *plines_out,
                                     PLINE *plines_in,
                                     Uint32 bytes_in, Sint64 value)
{
    Uint32 i;

    PIX32 *pin = (PIX32 *) (*plines_in);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin++,pout++){
        *pout = (PIX32) (*pin+value);
    }
}

/*
 * Adds a constant value to an 8-bits pixels image and places the 
 * result in a 32-bit image.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image 1 pixel line
 * \param bytes_in number of bytes inside the line
 * \param value the constant value
 */
static INLINE void CONADD_LINE_8_32(PLINE *plines_out,
                                    PLINE *plines_in,
                                    Uint32 bytes_in, Sint64 value)
{
    Uint32 i;

    PLINE pin = (PLINE) (*plines_in);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i++,pin++,pout++){
        *pout = (PIX32) (*pin+value);
    }
}


/*
 * Adds a constant value to the pixels of an image.
 * \param src the source image
 * \param value the constant value to be added to the pixels
 * \param dest the image resulting of the addition of image 1 and value. 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_ConAdd(MB_Image *src, Sint64 value, MB_Image *dest)
{
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* The two images must have the same */
    /* depth */
    switch(MB_PROBE_PAIR(src,dest)) {

    case MB_PAIR_8_8:
            /* Addition with saturation */
            for (i = 0;i < src->height;i++, plines_in++, plines_out++) {
            CONADD_LINE_8_8( plines_out, plines_in, bytes_in, (Sint16) value );
        }
            break;

    case MB_PAIR_32_32:
            for (i = 0;i < src->height;i++, plines_in++, plines_out++) {
            CONADD_LINE_32_32( plines_out, plines_in, bytes_in, value );
        }
            break;

    case MB_PAIR_8_32:
            for (i = 0;i < src->height;i++, plines_in++, plines_out++) {
            CONADD_LINE_8_32( plines_out, plines_in, bytes_in, value );
        }
            break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    return MB_NO_ERR;
} 


