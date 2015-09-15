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
 * Copies an image data contents into another image.
 * This copy works with same size images.
 * \param src the source image
 * \param dest the destination image
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Copy(MB_Image *src, MB_Image *dest) {

    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    Uint32 i;
    
    /* Verification over src and dest to know */
    /* if the copy is really needed */
    if (src==dest) {
        /* Pointing to the same image data */
        /* then nothing to do */
        return MB_NO_ERR;
    }
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* The two images must have the same */
    /* depth */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_1:
    case MB_PAIR_8_8:
    case MB_PAIR_32_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }
    
    /* Setting up the pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    
    /* Setting up offset */
    bytes_in = MB_LINE_COUNT(src);
    
    for (i = 0; i < src->height;i++, plines_out++, plines_in++) {
        MB_memcpy(*plines_out,*plines_in,bytes_in);
    }
    
    return MB_NO_ERR;
}

/*
 * Copies an image line contents into another image line.
 * \param src the source image
 * \param dest the destination image
 * \param insrc_pos the position of the line copied from src
 * \param indest_pos the position in dest in which the line is copied
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_CopyLine(MB_Image *src, MB_Image *dest, Uint32 insrc_pos, Uint32 indest_pos) {

    PLINE *plines_in, *plines_out;
    Uint32 bytes_in;
    
    /* Verification over the line indexes that need to be copied */
    if ( (insrc_pos>=(src->height))   ||
         (insrc_pos<0)                ||
         (indest_pos>=(dest->height)) ||
         (indest_pos<0) ) {
        /* Either the source line or the destination line is out of range*/
        return MB_ERR_BAD_VALUE;
    }
    
    /* Verification over src and dest to know */
    /* if the copy is really needed */
    if (src==dest && insrc_pos==indest_pos) {
        /* Pointing to the same image data */
        /* then nothing to do */
        return MB_NO_ERR;
    }
    
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* The two images must have the same */
    /* depth */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_1:
    case MB_PAIR_8_8:
    case MB_PAIR_32_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }
    
    /* Setting up the pointers */
    plines_in = &src->plines[insrc_pos];
    plines_out = &dest->plines[indest_pos];
    
    /* Setting up offset */
    bytes_in = MB_LINE_COUNT(src);
    
    MB_memcpy(*plines_out,*plines_in,bytes_in);

    return MB_NO_ERR;
}

/*
 * Copies an image data contents into another image.
 * This copy can work with image of different sizes. As the size can be different,
 * the position where the copy occurs must be specified for both images as well
 * as the size of the copy. 
 * The function will compute the actual crop inside the source and destination 
 * images. 
 * Works only with non binary images.
 * \param src the source image
 * \param x_src the x position in the source image where the copy should begin
 * \param y_src the y position in the source image where the copy should begin
 * \param dest the destination image
 * \param x_dest the x position in the destination image where the copy should happen
 * \param y_dest the y position in the destination image where the copy should happen
 * \param w the width of the copy
 * \param h the height of the copy
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_CropCopy(MB_Image *src, Uint32 x_src, Uint32 y_src,
                       MB_Image *dest, Uint32 x_dest, Uint32 y_dest,
                       Uint32 w, Uint32 h)
{

    PLINE *plines_in, *plines_out;
    Uint32 linoff_in, linoff_out, bytes_in;
    Uint32 i;
    Uint32 w_src, w_dest;
    Uint32 h_src, h_dest;

    /* The two images must have the same */
    /* depth */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_8_8:
    case MB_PAIR_32_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
        break;
    }
   
    /* Given size should be at least greater than 0 */
    if (w==0 || h==0) {
        return MB_ERR_BAD_VALUE;
    }

    /* Verification the given position and the images sizes*/
    if (x_dest>=dest->width || y_dest>=dest->height) {
        return MB_ERR_BAD_SIZE;
    }
    if (x_src>=src->width || y_src>=src->height) {
        return MB_ERR_BAD_SIZE;
    }

    /* Computing the size of the copy, its the minimum of all the available */
    /* spaces */
    w_dest = dest->width-x_dest;
    h_dest = dest->height-y_dest;
    w_src = src->width-x_src;
    h_src = src->height-y_src;
    w = w<w_dest ? w : w_dest;
    w = w<w_src ? w : w_src;
    h = h<h_dest ? h : h_dest;
    h = h<h_src ? h : h_src;

    /* Setting up the pointers */
    plines_in = &src->plines[y_src];
    plines_out = &dest->plines[y_dest];
    
    /* Setting up offset */
    linoff_in = ((x_src*src->depth)/8);
    linoff_out = ((x_dest*src->depth)/8);
    bytes_in = ((w*src->depth)/8);
    
    for (i = 0; i < h;i++, plines_out++, plines_in++) {
        MB_memcpy(*plines_out+linoff_out,*plines_in+linoff_in,bytes_in);
    }
    
    return MB_NO_ERR;
}
