/**
 * \file MBPL_Copy.c
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
 * Copies an image data contents into another image
 * This copy works with same size images.
 * \param src the source image
 * \param dest the destination image
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Copy(MBPL_Image *src, MBPL_Image *dest)
{
    /* verification over src and dest to know */
    /* if the copy is really needed */
    if (src==dest) {
        /* pointing to the same image data */
        /* then nothing to do */
        return NO_ERR;
    }
    
    /* verification over image size compatibility */
    if (!MBPL_CHECK_SIZE_2(src, dest)) {
        return ERR_INVALID_IM_SIZE;
    }

    /* The two images must have the same depth */
    switch (MBPL_PROBE_PAIR(src, dest)) {
    case MBPL_PAIR_1_1:
        break;
    case MBPL_PAIR_8_8:
        break;
    case MBPL_PAIR_32_32:
        break;
    default:
        return ERR_INVALID_IM_DEPTH;
        break;
    }

    clEnqueueCopyBuffer(context->cmdqCL, src->pixels, dest->pixels, 0, 0, src->buf_size, 0, NULL, NULL);
    
    return NO_ERR;
}
