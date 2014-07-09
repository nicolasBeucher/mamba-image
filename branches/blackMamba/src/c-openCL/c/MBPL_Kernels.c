/**
 * \file MBRT_Kernels.c
 * \author Nicolas Beucher
 * \date 26-01-2011
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

/* list of all the kernels name */
const char *kernels_name[NB_KERNELS] = {
    "logicand",
    "add_8_8_8",
    "add_32_32_32",
    "inf_8_8_8",
    "inf_32_32_32",
    "conset_8",
    "conset_32",
    "infnb_8_s",
    "infnb_8_h"
};

/**
 * Create all the kernels used in the MBPL API
 * /param device the selected device
 */
MBPL_errcode MBPL_CreateKernels(cl_device_id device)
{
    int i;
    cl_int cl_err;
    size_t retSize;
    
    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    /* allocation for all the kernels */
    context->kersCL = MBPL_malloc(NB_KERNELS*sizeof(cl_kernel));
    if (context->kersCL==NULL) {
        return ERR_CANT_CREATE_CL_KERNEL;
    }
    /* allocation of the workgroup maximum size info */
    context->mwgCL = MBPL_malloc(NB_KERNELS*sizeof(size_t));
    if (context->mwgCL==NULL) {
        return ERR_CANT_CREATE_CL_KERNEL;
    }
    
    /* creation of all the kernels */
    for(i=0; i<NB_KERNELS; i++) {
        context->kersCL[i] = clCreateKernel(context->prgCL, kernels_name[i], &cl_err);
        if (cl_err!=CL_SUCCESS) {
            return ERR_CANT_CREATE_CL_KERNEL;
        }
        cl_err = clGetKernelWorkGroupInfo(context->kersCL[i],
                                          device,
                                          CL_KERNEL_WORK_GROUP_SIZE,
                                          sizeof(size_t),
                                          &context->mwgCL[i],
                                          &retSize);
        if (cl_err!=CL_SUCCESS) {
            return ERR_CANT_CREATE_CL_KERNEL;
        }
    }
    
    return NO_ERR;
}

/**
 * Destroy the kernels
 */
MBPL_errcode MBPL_DestroyKernels()
{
    int i;
    
    /* context verification */
    if (context==NULL) {
        return ERR_INVALID_CONTEXT;
    }
    
    /* creation of all the kernels */
    for(i=0; i<NB_KERNELS; i++) {
        clReleaseKernel(context->kersCL[i]);
    }
    
    /* allocation for all the kernels */
    MBPL_free(context->kersCL);

    return NO_ERR;
}
