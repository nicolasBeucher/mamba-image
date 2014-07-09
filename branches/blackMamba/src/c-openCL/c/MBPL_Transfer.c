/**
 * \file MBPL_Transfer.c
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
 * Transfer the pixels array from a mamba image (MB_Image) into a
 * mambaParallel image (MBPL_Image). The transfer is needed to put the pixel
 * array into device memory (openCL).
 * \param src the source mamba image
 * \param dest the destination mamba parallel image
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_TransferFromMB(MB_Image *src, MBPL_Image *dest)
{
    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }

    /* verification over the depth and size*/
    switch(MBPL_PROBE_PAIR(src,dest)) {
    case MBPL_PAIR_1_1:
    case MBPL_PAIR_8_8:
    case MBPL_PAIR_32_32:
        break;
    default:
        return ERR_INVALID_IM_DEPTH;
        break;
    }
    if (!MBPL_CHECK_SIZE_2(src, dest)) {
        return ERR_INVALID_IM_SIZE;
    }

    /* writing the image data to the device buffer */
    clEnqueueWriteBuffer(context->cmdqCL,
                        dest->pixels,
                        CL_FALSE,
                        0,
                        dest->buf_size,
                        src->pixels,
                        0, NULL, NULL);
    clFinish(context->cmdqCL);
    
    return NO_ERR;
}

/**
 * Transfer the pixels array from a mamba parallel image (MBPL_Image) into a
 * mamba image (MB_Image). The transfer is needed to extract the pixel
 * array from device memory (openCL).
 * \param src the destination mamba parallel image
 * \param dest the source mamba image
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_TransferToMB(MBPL_Image *src, MB_Image *dest)
{
    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }

    /* verification over the depth and size*/
    switch(MBPL_PROBE_PAIR(src,dest)) {
    case MBPL_PAIR_1_1:
    case MBPL_PAIR_8_8:
    case MBPL_PAIR_32_32:
        break;
    default:
        return ERR_INVALID_IM_DEPTH;
        break;
    }
    if (!MBPL_CHECK_SIZE_2(src, dest)) {
        return ERR_INVALID_IM_SIZE;
    }

    /* reading the image data to the device buffer */
    clEnqueueReadBuffer(context->cmdqCL,
                        src->pixels,
                        CL_TRUE,
                        0,
                        src->buf_size,
                        dest->pixels,
                        0, NULL, NULL);
    /* in this direction we must wait for the end of the memory transfer */
    clFinish(context->cmdqCL);
    
    return NO_ERR;
}

