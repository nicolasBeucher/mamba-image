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

/* Image counter */
static Uint32 MB_refcounter = 0;

/*
 * \return the number of image that have been allocated so far.
 */
Uint32 MB_getImageCounter(void)
{
    return MB_refcounter;
}

/*
 * Creates an image (memory allocation) with the correct size and depth given as
 * argument. The size is deduced from the requested size given in argument. 
 * The size must be a multiple of MB_ROUND_W for width and MB_ROUND_H for height.
 * The size cannot be greater than MB_MAX_IMAGE_SIZE.
 * \param image the created image
 * \param width the width of the created image 
 * \param height the height of the created image 
 * \param depth the depth of the created image 
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Create(MB_Image *image, Uint32 width, Uint32 height, Uint32 depth) {
    PLINE *plines = NULL;
    PIX8 *pixarray = NULL;
    Uint32 i;
    Uint32 full_w, full_h;
    Uint64 image_size;
    
    /* Computation of the corrected size */
    width = ((width + MB_ROUND_W-1) / MB_ROUND_W) * MB_ROUND_W;
    height = ((height + MB_ROUND_H-1) / MB_ROUND_H) * MB_ROUND_H;

    /* Verification over the image size */
    image_size = ((Uint64)width) * height;
    if (!(width > 0 && height > 0 &&
        image_size <= MB_MAX_IMAGE_SIZE) ) {
        return MB_ERR_BAD_IMAGE_DIMENSIONS;
    }

    /* Verification over the depth*/
    /* Acceptable values are 1, 8, or 32 bits*/
    if( (depth != 1) && (depth != 8) && (depth != 32) ){
        return MB_ERR_BAD_DEPTH;
    }
    
    /* Full height in pixel with edge*/
    full_h = height;
    /* Full width in bytes with edge*/
    full_w = (width*depth+7)/8;

    /* Memory allocation*/
    plines = (PLINE *) MB_malloc(full_h*sizeof(PLINE));
    /*
     * We need aligned memory allocation to be sure that it works correctly with
     * vectorization instructions enabled. Aligned memory allocation is system dependant.
     */
    pixarray = (PIX8 *) MB_aligned_malloc(full_w*full_h, 16);

    if(pixarray==NULL || plines==NULL){
        /* In case allocation goes wrong */
        MB_aligned_free(pixarray);
        MB_free(plines);
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    
    /* Fills in the MB_Image structure */
    MB_memset(pixarray, 0, full_w*full_h);
    image->plines = plines;
    image->pixels = pixarray;
    image->depth = depth;
    image->width = width;
    image->height = height;

    for (i=0;i<full_h;i++, pixarray += full_w) {
        plines[i] = (PLINE) pixarray;
    }
    
    MB_refcounter++;
    
    return MB_NO_ERR;
}

/*
 * Destroys an image (memory freeing).
 * \param image the image to be destroyed
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Destroy(MB_Image *image) {
    if (image==NULL) return MB_NO_ERR;

    MB_free(image->plines);
    MB_aligned_free(image->pixels);
    MB_free(image);
    if (MB_refcounter>0) {
        MB_refcounter--;
    }
    
    return MB_NO_ERR;
}

