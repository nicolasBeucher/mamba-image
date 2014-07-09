/**
 * \file MBPL_Inf.c
 * \author Nicolas Beucher
 * \date 24-02-2014
 *
 */
 
/*
 * Copyright (c) <2014>, <Nicolas BEUCHER>
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
 * Determines the inferior value between the pixels of two images.
 * The result is put in the corresponding pixel position in the destination image.
 * \param src1 image 1
 * \param src2 image 2
 * \param dest destination image 
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_Inf(MBPL_Image *src1, MBPL_Image *src2, MBPL_Image *dest)
{
    size_t workSize[1];

    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    /* verification over image size compatibility */
    if (!MBPL_CHECK_SIZE_3(src1, src2, dest)) {
        return ERR_INVALID_IM_SIZE;
    }
    
    /* destination image should have the depth that source image */
    if(dest->depth != src1->depth) {
        return ERR_INVALID_IM_DEPTH;
    }
    
    /* The two source images must have the same */
    /* depth */
    switch(MBPL_PROBE_PAIR(src1,src2)) {
    /* In case of binary image the inf is the result of a logical AND */
    case MBPL_PAIR_1_1:
        clSetKernelArg(context->kersCL[KER_AND], 0, sizeof(cl_mem), (void*)&(src1->pixels));
        clSetKernelArg(context->kersCL[KER_AND], 1, sizeof(cl_mem), (void*)&(src2->pixels));
        clSetKernelArg(context->kersCL[KER_AND], 2, sizeof(cl_mem), (void*)&(dest->pixels));
        
        workSize[0] = dest->width*dest->height;
        
        clEnqueueNDRangeKernel(context->cmdqCL, 
                               context->kersCL[KER_AND],
                               1, NULL,
                               workSize, NULL,
                               0, NULL, NULL);
        break;
    
    case MBPL_PAIR_8_8:
        clSetKernelArg(context->kersCL[KER_INF_8_8_8], 0, sizeof(cl_mem), (void*)&(src1->pixels));
        clSetKernelArg(context->kersCL[KER_INF_8_8_8], 1, sizeof(cl_mem), (void*)&(src2->pixels));
        clSetKernelArg(context->kersCL[KER_INF_8_8_8], 2, sizeof(cl_mem), (void*)&(dest->pixels));
        
        workSize[0] = dest->width*dest->height/4;
        
        clEnqueueNDRangeKernel(context->cmdqCL, 
                               context->kersCL[KER_INF_8_8_8],
                               1, NULL,
                               workSize, NULL,
                               0, NULL, NULL);
        break;

    case MBPL_PAIR_32_32:
        clSetKernelArg(context->kersCL[KER_INF_32_32_32], 0, sizeof(cl_mem), (void*)&(src1->pixels));
        clSetKernelArg(context->kersCL[KER_INF_32_32_32], 1, sizeof(cl_mem), (void*)&(src2->pixels));
        clSetKernelArg(context->kersCL[KER_INF_32_32_32], 2, sizeof(cl_mem), (void*)&(dest->pixels));
        
        workSize[0] = dest->width*dest->height;

        clEnqueueNDRangeKernel(context->cmdqCL,
                               context->kersCL[KER_INF_32_32_32],
                               1, NULL,
                               workSize, NULL,
                               0, NULL, NULL);
        break;

    default:
        return ERR_INVALID_IM_DEPTH;
        break;
    }

    return NO_ERR;
}
