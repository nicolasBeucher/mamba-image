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
 * Compares the pixels of two 32-bit image lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param plines_cmp pointer on the comparaison image pixel line
 * \param bytes_in number of bytes inside the line
 * \param x position of the first discordant pixel in x
 */
static INLINE void COMP_LINE_32(PLINE *plines_out,
                                PLINE *plines_in,
                                PLINE *plines_cmp,
                                Uint32 bytes_in, Sint32 *x )
{
    Uint32 i;

    PIX32 *pin = (PIX32 *) (*plines_in);
    PIX32 *pcmp = (PIX32 *) (*plines_cmp);
    PIX32 *pout = (PIX32 *) (*plines_out);

    for(i=0;i<bytes_in;i+=4,pin++,pout++,pcmp++){
        if((*pin)!=(*pcmp)){
            *x = (Sint32) (i>>2);
            *pout = *pin;
            break;
        }
    }
}

/*
 * Compares the pixels of two 8-bit image lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param plines_cmp pointer on the comparaison image pixel line
 * \param bytes_in number of bytes inside the line
 * \param x position of the first discordant pixel in x
 */
static INLINE void COMP_LINE_8(PLINE *plines_out,
                               PLINE *plines_in,
                               PLINE *plines_cmp,
                               Uint32 bytes_in, Sint32 *x )
{
    Uint32 j;

    PLINE pin = (PLINE) (*plines_in);
    PLINE pcmp = (PLINE) (*plines_cmp);
    PLINE pout = (PLINE) (*plines_out);

    for(j=0;j<bytes_in;j++,pin++,pout++,pcmp++){
        if((*pin)!=(*pcmp)){
            *x = (Sint32) j;
            *pout = *pin;
            break;
        }
    }
}


/*
 * Compares the pixels of two binary image lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param plines_cmp pointer on the comparaison image pixel line
 * \param bytes_in number of bytes inside the line
 * \param x position of the first discordant pixel in x
 */
static INLINE void COMP_LINE_1(PLINE *plines_out,
                               PLINE *plines_in,
                               PLINE *plines_cmp,
                               Uint32 bytes_in, Sint32 *x )
{
    Uint32 i;
    MB_Vector1 vec_in,vec_cmp;
    
    MB_Vector1 value2shift = 0;

    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    MB_Vector1 *pcmp = (MB_Vector1 *) (*plines_cmp);
    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);

    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++,pout++,pcmp++){
        vec_in = *pin;
        vec_cmp = *pcmp;
        if(vec_in!=vec_cmp){
            /* The two pixels vectors are differents */
            /* We will look for the first pixel in it that is */
            /* different */
            while(vec_in!=vec_cmp) {
                /* shifting to access pixel by pixel */
                vec_in = vec_in>>1;
                vec_cmp = vec_cmp>>1;
                value2shift++;
            }
            /* We put the pixel to 1 in the out image */
            (*pout) = (*pout) | (((MB_Vector1) 1L)<<(value2shift-1));
            *x = (Sint32) (i*8 + (value2shift-1));
            break;
        }
        
    }
}
 
/*
 * Performs a comparaison between a source image and a given base image.
 * \param src the source image 
 * \param cmp the image to which the source image is compared
 * \param dest destination image 
 * \param px position in x of the first different pixel between the two images (-1 if images are similar)
 * \param py position in y of the first different pixel between the two images (-1 if images are similar)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Compare(MB_Image *src, MB_Image *cmp, MB_Image *dest, Sint32 *px, Sint32 *py) 
{
    Uint32 i;
    Sint32 x,y;
    PLINE *plines_in, *plines_cmp, *plines_out;
    Uint32 bytes_in;
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_3(src, cmp, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Verification over depth */
    if(src->depth != dest->depth) {
        return MB_ERR_BAD_DEPTH;
    }

    /* Setting up line pointers */
    plines_in = src->plines;
    plines_cmp = cmp->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);
    
    /* Position of the first pixel which is different in the two images */
    /* the value is -1 when the two images are similar */
    x = -1;
    y = -1;

    switch(MB_PROBE_PAIR(src,cmp)) {

    case MB_PAIR_1_1:
        for(i = 0; i < src->height; i++, plines_in++, plines_out++, plines_cmp++) {
            COMP_LINE_1(plines_out, plines_in, plines_cmp, bytes_in, &x);
            /* As soon as a difference has been found the function ends */
            if (x != -1) {
                y = i;
                break;
            }
        }
        break;

    case MB_PAIR_8_8:
        for(i = 0; i < src->height; i++, plines_in++, plines_out++, plines_cmp++) {
            COMP_LINE_8(plines_out, plines_in, plines_cmp, bytes_in, &x);
            /* As soon as a difference has been found the function ends */
            if (x != -1) {
                y = i;
                break;
            }
        }
        break;
        
    case MB_PAIR_32_32:
        for(i = 0; i < src->height; i++, plines_in++, plines_out++, plines_cmp++) {
            COMP_LINE_32(plines_out, plines_in, plines_cmp, bytes_in, &x);
            /* As soon as a difference has been found the function ends */
            if (x != -1) {
                y = i;
                break;
            }
        }
        break;

    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    /* Value output */
    *px = x;
    *py = y;

    return MB_NO_ERR;
}

