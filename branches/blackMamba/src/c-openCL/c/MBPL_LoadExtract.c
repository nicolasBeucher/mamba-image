/**
 * \file MBPL_LoadExtract.c
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

/**
 * Loads a grey scale image data with data given in argument
 * \param image the image to fill
 * \param indata the data to fill the image with (complete pixels values)
 * \param len the length of data given
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Load8(MBPL_Image *image, PIX8 *indata, Uint32 len) {
    /* Only 8 bit image can be loaded */
    if (image->depth!=8) {
        return ERR_INVALID_IM_DEPTH;
    }
    /* the data given must be sufficient to fill the image */
    if (len!=(image->height*image->width)) {
        return ERR_INVALID_LOAD_DATA;
    }

    /* writing the image data to the device buffer */
    clEnqueueWriteBuffer(context->cmdqCL,
                         image->pixels,
                         CL_FALSE,
                         0,
                         len,
                         indata,
                         0, NULL, NULL);
    clFlush(context->cmdqCL);

    return NO_ERR;
}

/**
 * Loads a 32-bits image data with data given in argument
 * \param image the image to fill
 * \param indata the data to fill the image with (complete pixels values)
 * \param len the length of data given
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Load32(MBPL_Image *image, PIX8 *indata, Uint32 len) {
    /* Only 32 bit image can be loaded */
    if (image->depth!=32) {
        return ERR_INVALID_IM_DEPTH;
    }
    /* the data given must be sufficient to fill the image */
    if (len!=(image->height*image->width*4)) {
        return ERR_INVALID_LOAD_DATA;
    }

    /* writing the image data to the device buffer */
    clEnqueueWriteBuffer(context->cmdqCL,
                         image->pixels,
                         CL_FALSE,
                         0,
                         len,
                         indata,
                         0, NULL, NULL);
    clFlush(context->cmdqCL);

    return NO_ERR;
}

/**
 * Loads an image data with data given in argument
 * \param image the image to fill
 * \param indata the data to fill the image with (complete pixels values)
 * \param len the length of data given
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Load(MBPL_Image *image, PIX8 *indata, Uint32 len) {
    MBPL_errcode err = NO_ERR;

    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    switch(image->depth) {
        case 8:
            err = MBPL_Load8(image, indata, len);
            break;
        case 32:
            err = MBPL_Load32(image, indata, len);
            break;
        default:
            err = ERR_INVALID_IM_DEPTH;
            break;
    }
    
    return err;
}


/**
 * Reads a grey scale image data contents and put it in an array
 * \param image the image to read
 * \param outdata pointer to the array created (malloc) and filled with the 
 * pixel data of the image
 * \param len the length in bytes of data extracted
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Extract8(MBPL_Image *image, PIX8 **outdata, Uint32 *len) {
    /* only for 8 bit images */
    if (image->depth!=8) {
        return ERR_INVALID_IM_DEPTH;
    }

    /* allocating the memory */
    *len = image->height*image->width;
    *outdata = MBPL_malloc((*len)*sizeof(PIX8));
    
    /* reading the image data to the device buffer */
    clEnqueueReadBuffer(context->cmdqCL,
                        image->pixels,
                        CL_TRUE,
                        0,
                        *len,
                        *outdata,
                        0, NULL, NULL);
    /* in this direction we must wait for the end of the memory transfer */
    clFinish(context->cmdqCL);

    return NO_ERR;
}

/**
 * Reads a 32-bits image data contents and put it in an array
 * \param image the image to read
 * \param outdata pointer to the array created (malloc) and filled with the 
 * pixel data of the image
 * \param len the length in bytes of data extracted
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Extract32(MBPL_Image *image, PIX8 **outdata, Uint32 *len) {
    /* only for 32 bit images */
    if (image->depth!=32) {
        return ERR_INVALID_IM_DEPTH;
    }

    /* allocating the memory */
    *len = image->height*image->width*4;
    *outdata = MBPL_malloc((*len)*sizeof(PIX8));
    
    /* reading the image data to the device buffer */
    clEnqueueReadBuffer(context->cmdqCL,
                        image->pixels,
                        CL_TRUE,
                        0,
                        *len,
                        *outdata,
                        0, NULL, NULL);
    /* in this direction we must wait for the end of the memory transfer */
    clFinish(context->cmdqCL);

    return NO_ERR;
}

/**
 * Reads an image data contents and put it in an array
 * \param image the image to read
 * \param outdata pointer to the array created (malloc) and filled with the 
 * pixel data of the image
 * \param len the length in bytes of data extracted
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Extract(MBPL_Image *image, PIX8 **outdata, Uint32 *len) {
    MBPL_errcode err = NO_ERR;

    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    switch(image->depth) {
        case 8:
            err = MBPL_Extract8(image, outdata, len);
            break;
        case 32:
            err = MBPL_Extract32(image, outdata, len);
            break;
        default:
            err = ERR_INVALID_IM_DEPTH;
            break;
    }
    
    return err;
}
