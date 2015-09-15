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
 * Sets the bit plane at the given position.
 * \param value the value in which the bit will be modified
 * \param bitval the bit value we want to set
 * \param pos the position of the bit
 * \return the modified value
 */
Uint8 SET_BIT_PLANE8(Uint8 value, Uint8 bitval, Uint32 pos)
{
    if ((bitval==0) && ((value&(1<<pos))!=0) ) {
        /* Unset the bit if set in value*/
        return value-(1<<pos);
    }
    if ((bitval==1) && ((value&(1<<pos))==0) ) {
        /* Set the bit if not set in value*/
        return value+(1<<pos);
    }
    
    /* Other cases means that value is already */
    /* alright */
    return value;
}

/*
 * Extracts the bit plane at the given position.
 * \param value the value in which the bit will be extracted
 * \param pos the position of the bit
 * \return the value of the bit
 */
MB_Vector1 EXTRACT_BIT_PLANE(MB_Vector1 value, Uint32 pos)
{
    return (value>>pos)&1;
}

/*
 * Extracts the bit plane at the given position out of grey scale lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the bit plane index
 * \return the value of the bit
 */
static INLINE void EXTRACT_BITPLANE_LINE8(PLINE *plines_out,
                                          PLINE *plines_in,
                                          Uint32 bytes_in, Uint32 plane)
{
    Uint32 i,j;
    Sint32 u;
    MB_Vector1 pix_reg;

    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);
    PLINE pin = (PLINE) (*plines_in);
    
    /* Working with MB_vec1_size bit word (MB_Vector1 size) */
    for(i=0,j=0;i<bytes_in;i+=sizeof(MB_Vector1),j+=MB_vec1_size,pout++) {
        /* Building the pixel register */
        pix_reg = 0;
        for(u=MB_vec1_size-1;u>-1;u--){
            pix_reg = (pix_reg<<1) | EXTRACT_BIT_PLANE(pin[j+u], plane);
        }
        *pout = pix_reg;
    }
}


/*
 * Inserts the bit plane at the given position in 32-bit lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the bit plane index
 * \return the value of the bit
 */
static INLINE void INSERT_BITPLANE_LINE8(PLINE *plines_out,
                                        PLINE *plines_in,
                                        Uint32 bytes_in, Uint32 plane)
{
    Uint32 i,u;
    MB_Vector1 pix_reg;
    
    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    PLINE pout = (PLINE) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++) {
        pix_reg = *pin;
        for(u=0;u<MB_vec1_size;u++,pout++){
            /* For all the pixels in the pixel register */
            *pout = SET_BIT_PLANE8(*pout, pix_reg&1, plane);
            pix_reg = pix_reg>>1;
        }    
    }
}

/*
 * Inserts the binary image into the bit plane of the grey scale
 * image.
 * \param src source image
 * \param dest destination image 
 * \param plane the bit plane in which the binary image will be copied
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_InsertBitPlane1to8(MB_Image *src, MB_Image *dest, Uint32 plane) {
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;

    /* The plane index must be between 0 and 7 included */
    if (plane>7) 
        return MB_ERR_BAD_PARAMETER;
        
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);
    
    /* Converting the 1-bit values in 8-bit values */
    for(i=0; i<src->height; i++,plines_in++,plines_out++) {
        INSERT_BITPLANE_LINE8(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Extracts the bit plane of the grey scale image and
 * puts it in the binary image.
 * \param src source image
 * \param dest destination image
 * \param plane the bit plane index 
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_ExtractBitPlane8to1(MB_Image *src, MB_Image *dest, Uint32 plane) {
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;

    /* The plane index must be between 0 and 7 included */
    if (plane>7) 
        return MB_ERR_BAD_PARAMETER;
    
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(dest);
    
    /* Converting the 8-bit values in 1-bit values */
    for(i=0; i<src->height; i++,plines_in++,plines_out++) {
        EXTRACT_BITPLANE_LINE8(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Sets the bit at the given position.
 * \param value the value in which the bit will be modified
 * \param bitval the bit value we want to set
 * \param pos the position of the bit
 * \return the modified value
 */
Uint32 SET_BIT_PLANE32(Uint32 value, Uint32 bitval, Uint32 pos)
{
    if ((bitval==0) && ((value&(1<<pos))!=0) ) {
        /* Unset the bit if set in value*/
        return value-(1<<pos);
    }
    if ((bitval==1) && ((value&(1<<pos))==0) ) {
        /* Set the bit if not set in value*/
        return value+(1<<pos);
    }
    
    /* Other cases means that value is already */
    /* alright */
    return value;
}
/*
 * Extracts the bit plane at the given position out of grey scale lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the bit plane index
 * \return the value of the bit
 */
static INLINE void EXTRACT_BITPLANE_LINE32(PLINE *plines_out,
                                           PLINE *plines_in,
                                           Uint32 bytes_in, Uint32 plane)
{
    Uint32 i,j;
    Sint32 u;
    MB_Vector1 pix_reg;

    MB_Vector1 *pout = (MB_Vector1 *) (*plines_out);
    PIX32 *pin = (PIX32 *) (*plines_in);
    
    /* Working with MB_vec1_size bit word (MB_Vector1 size) */
    for(i=0,j=0;i<bytes_in;i+=sizeof(MB_Vector1),j+=MB_vec1_size,pout++) {
        /* Building the pixel register */
        pix_reg = 0;
        for(u=MB_vec1_size-1;u>-1;u--){
            pix_reg = (pix_reg<<1) | EXTRACT_BIT_PLANE(pin[j+u], plane);
        }
        *pout = pix_reg;
    }
}


/*
 * Inserts the bit plane at the given position in 32-bit lines.
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param plane the bit plane index
 * \return the value of the bit
 */
static INLINE void INSERT_BITPLANE_LINE32(PLINE *plines_out,
                                          PLINE *plines_in,
                                          Uint32 bytes_in, Uint32 plane)
{
    Uint32 i,u;
    MB_Vector1 pix_reg;
    
    MB_Vector1 *pin = (MB_Vector1 *) (*plines_in);
    PIX32 *pout = (PIX32 *) (*plines_out);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++) {
        pix_reg = *pin;
        for(u=0;u<MB_vec1_size;u++,pout++){
            /* For all the pixels in the pixel register */
            *pout = SET_BIT_PLANE32(*pout, pix_reg&1, plane);
            pix_reg = pix_reg>>1;
        }
    }
}

/*
 * Inserts the binary image into the bit plane of the 32-bit image.
 * \param src source image
 * \param dest destination image 
 * \param plane the bit plane in which the binary image will be copied
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_InsertBitPlane1to32(MB_Image *src, MB_Image *dest, Uint32 plane) {
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;

    /* The plane index must be between 0 and 31 included */
    if (plane>31) 
        return MB_ERR_BAD_PARAMETER;
        
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);
    
    /* Converting the 1-bit values in 8-bit values */
    for(i=0; i<src->height; i++,plines_in++,plines_out++) {
        INSERT_BITPLANE_LINE32(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Extracts the bit plane of the 32-bit image and puts it in the binary image.
 * \param src source image
 * \param dest destination image
 * \param plane the bit plane index 
 * \return An error code (MB_NO_ERR if successful)
 */
static MB_errcode MB_ExtractBitPlane32to1(MB_Image *src, MB_Image *dest, Uint32 plane) {    
    Uint32 i;
    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;

    /* The plane index must be between 0 and 31 included */
    if (plane>31) 
        return MB_ERR_BAD_PARAMETER;
    
    /* Setting up line pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(dest);
    
    /* Converting the 8-bit values in 1-bit values */
    for(i=0; i<src->height; i++,plines_in++,plines_out++) {
        EXTRACT_BITPLANE_LINE32(plines_out, plines_in, bytes_in, plane);
    }
    
    return MB_NO_ERR;
}

/*
 * Inserts or extracts the bit plane in/out an image src into 
 * dest.
 * \param src source image
 * \param dest destination image
 * \param plane the plane number
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_CopyBitPlane(MB_Image *src, MB_Image *dest, Uint32 plane) {

    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Comparing the depth of the src and the destination */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_8:
        return MB_InsertBitPlane1to8(src,dest,plane);
        break;
    case MB_PAIR_8_1:
        return MB_ExtractBitPlane8to1(src,dest,plane);
        break;
    case MB_PAIR_1_32:
        return MB_InsertBitPlane1to32(src,dest,plane);
        break;
    case MB_PAIR_32_1:
        return MB_ExtractBitPlane32to1(src,dest,plane);
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }

    /* If this point is reached we can assume there was an error */
    return MB_ERR_BAD_DEPTH;
}

