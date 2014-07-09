/**
 * \file MBPL_InfNb8.c
 * \author Nicolas Beucher
 * \date 26-01-2010
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
 * Looks for the minimum between two greyscale image pixels (a central pixel
 * and its neighbors in the other image)
 * The neighbor depends on the grid used (see mambaCommon.h). Neighbors are
 * described using a pattern (see enum MB_Neighbors_code_t). If no neighbor
 * is defined, the function will leave silently doing nothing.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param neighbors the neighbors to take into account
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
MBPL_errcode MBPL_InfNb8(MBPL_Image *src, MBPL_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge)
{
    MBPL_errcode err;
    cl_int cl_err;
    MBPL_kernel_t oper;
    size_t workSize[2];
    cl_uchar border;
    MBPL_Image *intern_src; /* this is needed in case src and srcdest are the same images */

    /* error management */
    /* verification over image size compatibility */
    if (!MBPL_CHECK_SIZE_2(src, srcdest)) {
        return ERR_INVALID_IM_SIZE;
    }
    /* Only greyscale images can be processed */
    switch (MBPL_PROBE_PAIR(src, srcdest)) {
    case MBPL_PAIR_8_8:
        break;
    default:
        return ERR_INVALID_IM_DEPTH;
    }
    
    /* identifying the operation to do */
    if (grid==MB_HEXAGONAL_GRID) {
        if ((neighbors&MB_NEIGHBOR_ALL_HEXAGONAL)==0) {
            /* No neighbors to take into account */
            return NO_ERR;
        }
        oper = KER_INFNB_8_H;
    } else {
        if ((neighbors&MB_NEIGHBOR_ALL_SQUARE)==0) {
            /* No neighbors to take into account */
            return NO_ERR;
        }
        oper = KER_INFNB_8_S;
    }
    
    /* border value */
    border = (cl_uchar) GREY_FILL_VALUE(edge);
    
    /* verification over src and srcdest to know */
    /* if count should be taken into account or not */
    if (src!=srcdest) {
        /* not pointing to the same image data */
        /* then count is set to 1. Even if this is not */
        /* done this would have no impact on the image */
        /* produced if the two images are different but */
        /* this is important for performance sake */
        intern_src = src; /* in this case intern_src is just an alias */
    } else {
        /* when pointing to the same image data the src image is copied to */
        /* prevent data access race conflict */
        intern_src = MBPL_malloc(sizeof(MBPL_Image));
        if (intern_src==NULL) {
            return ERR_CANT_ALLOCATE_MEMORY;
        }
        err = MBPL_Create(intern_src, src->width, src->height, src->depth);
        if (err!=NO_ERR) {
            return err;
        }
        err = MBPL_Copy(src, intern_src);
        if (err!=NO_ERR) {
            return err;
        }
    }
    
    workSize[0] = src->width/8;
    workSize[1] = src->height;
    
    clSetKernelArg(context->kersCL[oper], 0, sizeof(cl_mem), (void*)&(intern_src->pixels));
    clSetKernelArg(context->kersCL[oper], 1, sizeof(cl_mem), (void*)&(srcdest->pixels));
    clSetKernelArg(context->kersCL[oper], 2, sizeof(cl_uint), (void*)&(neighbors));
    clSetKernelArg(context->kersCL[oper], 3, sizeof(cl_uchar), (void*)&(border));

    cl_err = clEnqueueNDRangeKernel(context->cmdqCL,
                                    context->kersCL[oper],
                                    2, NULL,
                                    workSize, NULL,
                                    0, NULL, NULL);
    if (cl_err!=CL_SUCCESS) {
        return ERR_CANT_ENQUEUE_CL_KERNEL;
    }
    
    clFinish(context->cmdqCL);
    
    return NO_ERR;
}




