/**
 * \file MBPL_ConSet.c
 * \author Nicolas Beucher
 * \date 23-01-2011
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
 * Fills an image with a specific value
 * \param dest the image
 * \param value the value to fill the image
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_ConSet(MBPL_Image *dest, Uint32 value)
{
    cl_uint pattern32;
    cl_uchar pattern8;
    size_t workSize[1];

    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    /* pattern depends on the depth of the image */
    switch(dest->depth) {
    case 1:
        /* pattern computation */
        /* in binary image, value is eitheir one or zero */
        pattern8 = (value) ? 0XFF : 0;

        clSetKernelArg(context->kersCL[KER_CONSET_8], 0, sizeof(cl_mem), (void*)&(dest->pixels));
        clSetKernelArg(context->kersCL[KER_CONSET_8], 1, sizeof(cl_uchar), (void*)&(pattern8));
        
        workSize[0] = dest->width*dest->height;
        
        clEnqueueNDRangeKernel(context->cmdqCL,
                               context->kersCL[KER_CONSET_8],
                               1, NULL,
                               workSize, NULL,
                               0, NULL, NULL);
        break;

    case 8:
        /* pattern computation */
        /* the pattern is set by a concatenation of value to */
        /* reach the size of an Uint32 */
        pattern8 = value<0xFF ? value : 0xFF;

        clSetKernelArg(context->kersCL[KER_CONSET_8], 0, sizeof(cl_mem), (void*)&(dest->pixels));
        clSetKernelArg(context->kersCL[KER_CONSET_8], 1, sizeof(cl_uchar), (void*)&(pattern8));
        
        workSize[0] = dest->width*dest->height;
        clEnqueueNDRangeKernel(context->cmdqCL, context->kersCL[KER_CONSET_8], 2, NULL, workSize, NULL, 0, NULL, NULL);
        clFlush(context->cmdqCL);
        break;

    case 32:
        /* pretending the signed 32 bit is unsigned */
        pattern32 = value;
        
        clSetKernelArg(context->kersCL[KER_CONSET_32], 0, sizeof(cl_mem), (void*)&(dest->pixels));
        clSetKernelArg(context->kersCL[KER_CONSET_32], 1, sizeof(cl_uint), (void*)&(pattern32));
        
        workSize[0] = dest->width*dest->height;
        
        clEnqueueNDRangeKernel(context->cmdqCL,
                               context->kersCL[KER_CONSET_32],
                               1, NULL,
                               workSize, NULL,
                               0, NULL, NULL);
        break;
        
    default:
        return ERR_INVALID_IM_SIZE;
        break;
    }

    return NO_ERR;
} 
