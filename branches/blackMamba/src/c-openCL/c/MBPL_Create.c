/**
 * \file MBPL_Create.c
 * \author Nicolas Beucher
 * \date 22-01-2011
 *
 */
 
/*
 * Copyright (c) <2011>, <Nicolas BEUCHER>
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
#include "mambaPLApi_loc.h"

/* image counter */
Uint32 MBPL_refcounter = 0;

/** Making sure the image size is multiple of 64 for the width */
#define MBPL_ROUND_W    64
/** Making sure the image size is multiple of 2 for the heigth */
#define MBPL_ROUND_H    2

/* When considering the limits on the image size, remember that
 * the function computing the volume which returns Uint64
 * should not overflow on the 32-bit images. (that is, max volume
 * for the 32-bit image is 2^64-1) which yields approx 4.3 billions pixels
 * so roughly 65536*65536 images size.
 * However, if we compute a watershed transform, the number of allowed
 * labels is 2^24 (3 lower bytes of the label image). Therefore, if, in
 * a large image, the number of labels exceeds this value, some basins of
 * the watershed transform will share the same label. You must be aware of
 * this possibility.
 */
/** Image limit size in total number of pixels*/
#define MBPL_MAX_IMAGE_SIZE    ((Uint64)4294967296)

/**
 * Creates an image (memory allocation) with the correct size and depth given as
 * argument. The size is deduced from the requested size given in argument. 
 * The size must be a multiple of MB_ROUND_W for width and MB_ROUND_H for height.
 * The size cannot be greater than MB_MAX_IMAGE_W_SIZExMB_MAX_IMAGE_H_SIZE.
 * The memory is allocated inside the openCL device selected in context.
 * \param image the created image
 * \param width the width of the created image 
 * \param height the height of the created image 
 * \param depth the depth of the created image 
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Create(MBPL_Image *image, Uint32 width, Uint32 height, Uint32 depth) {
    Uint32 full_w, full_h;
    cl_int cl_err;
    Uint64 image_size;

    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    /* computation of the corrected size */
    width = ((width + MBPL_ROUND_W-1) / MBPL_ROUND_W) * MBPL_ROUND_W;
    height = ((height + MBPL_ROUND_H-1) / MBPL_ROUND_H) * MBPL_ROUND_H;

    /* verification over the image size */
    image_size = ((Uint64)width) * height;
    if (!(width > 0 && height > 0 &&
        image_size <= MBPL_MAX_IMAGE_SIZE) ) {
        return ERR_BAD_IMAGE_DIMENSIONS;
    }

    /* verification over the depth*/
    /*acceptable values are 1, 8, or 32 bits*/
    if( (depth != 1) && (depth != 8) && (depth != 32) ){
        return ERR_INVALID_IM_DEPTH;
    }
    
    /* full height in pixel with edge*/
    full_h = height;
    /* full width in bytes with edge*/
    full_w = (width*depth+CHARBIT-1)/CHARBIT;

    /*memory allocation*/
    image->pixels = clCreateBuffer(context->ctxCL, CL_MEM_READ_WRITE, full_w*full_h, NULL, &cl_err);
    if (cl_err!=CL_SUCCESS) {
        return ERR_CANT_CREATE_CL_BUFFER;
    }
    
    /* Fills in the MB_Image structure */
    image->depth = depth;
    image->width = width;
    image->height = height;
    image->buf_size = full_w*full_h;
    
    MBPL_refcounter++;
    
    return NO_ERR;
}

/**
 * Destroys an image (memory freeing)
 * \param image the image to be destroyed
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Destroy(MBPL_Image *image) {
    if (image==NULL) return NO_ERR;
    
    clReleaseMemObject(image->pixels);
    MBPL_free(image);
    if (MBPL_refcounter>0) {
        MBPL_refcounter--;
    }
    
    return NO_ERR;
}

