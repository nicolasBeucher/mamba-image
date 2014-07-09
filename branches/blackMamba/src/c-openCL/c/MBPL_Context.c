/**
 * \file MBRT_Context.c
 * \author Nicolas Beucher
 * \date 17-01-2011
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

/* General context handler */
MBPL_Context *context = NULL;

/* program source is extracted from the cl source file */
#include "cl_srcs.c"

/**
 * Create the context used throughout the library.
 * The context contains every pointer to data structure used globally in the
 * API.
 */
MBPL_errcode MBPL_CreateContext()
{
    MBPL_errcode err;
    cl_int cl_err;
    cl_uint num_platforms;
    cl_platform_id platform;
    cl_device_id* devices;
    cl_uint num_devices;

    context = MBPL_malloc(sizeof(MBPL_Context));
    if (context==NULL) {
        return ERR_CANT_CREATE_CONTEXT;
    }
    
    /* blanking the structure */
    MBPL_memset(context, 0, sizeof(MBPL_Context));
    
    /* get openCL platforms available */
    cl_err = clGetPlatformIDs (0, NULL, &num_platforms);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_GET_CL_PLATFORMS;
        goto error_fallback;
    }
    if (num_platforms==0) {
        err = ERR_NO_CL_PLATFORM;
        goto error_fallback;
    }
    cl_err = clGetPlatformIDs (1, &platform, NULL);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_GET_CL_PLATFORM_0;
        goto error_fallback;
    }

    /* Getting the devices */
    cl_err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices);
    if ((cl_err!=CL_SUCCESS) || (num_devices==0)) {
        err = ERR_CANT_GET_CL_DEVICE;
        goto error_fallback;
    }
    devices = MBPL_malloc(num_devices* sizeof(cl_device_id));
    cl_err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, num_devices, devices, NULL);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_GET_CL_DEVICE;
        goto error_fallback;
    }

    /* creating the openCL context */
    context->ctxCL = clCreateContext(0, num_devices, devices, NULL, NULL, &cl_err);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_CREATE_CL_CONTEXT;
        goto error_fallback;
    }

    /* creating the openCL command queue */
    context->cmdqCL = clCreateCommandQueue(context->ctxCL, devices[0], 0, &cl_err);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_CREATE_CL_CMDQ;
        goto error_fallback;
    }
    
    /* Opening and loading the CL program */
    context->prgCL = clCreateProgramWithSource(context->ctxCL,
                                               1,
                                               (const char **) &progSrc,
                                               NULL,
                                               &cl_err);
    if (cl_err!=CL_SUCCESS) {
        err = ERR_CANT_LOAD_CL_PROG;
        goto error_fallback;
    }
    cl_err = clBuildProgram(context->prgCL, num_devices, devices, NULL, NULL, NULL);
    if (cl_err!=CL_SUCCESS) {
        char *build_log;
        size_t ret_val_size;
        cl_err = clGetProgramBuildInfo(context->prgCL,
                                       devices[0],
                                       CL_PROGRAM_BUILD_LOG,
                                       0, NULL,
                                       &ret_val_size);
        build_log = MBPL_malloc((ret_val_size+1)*sizeof(char));
        cl_err = clGetProgramBuildInfo(context->prgCL,
                                       devices[0],
                                       CL_PROGRAM_BUILD_LOG,
                                       ret_val_size,
                                       build_log,
                                       NULL);
        build_log[ret_val_size] = '\0';
        printf("%s\n", build_log);
        err = ERR_CANT_BUILD_CL_PROG;
        goto error_fallback;
    }
    
    /* Creating kernels and work group maximum size */
    err = MBPL_CreateKernels(devices[0]);
    if (err!=NO_ERR) {
        goto error_fallback;
    }
    MBPL_free(devices);

    return err;
    
/* This is the error fallback to tidy things up after errors */
error_fallback:
    if (context->prgCL) {
        clReleaseProgram(context->prgCL);
    }
    if (context->cmdqCL) {
        clReleaseCommandQueue(context->cmdqCL);
    }
    if (context->ctxCL) {
        clReleaseContext(context->ctxCL);
    }
    
    MBPL_free(context);
    context = NULL;
    
    return err;
}

/**
 * Destroy the context and all the data associated to it
 */
MBPL_errcode MBPL_DestroyContext()
{
    if (context!=NULL) {

        MBPL_DestroyKernels();

        clReleaseProgram(context->prgCL);
        clReleaseCommandQueue(context->cmdqCL);
        clReleaseContext(context->ctxCL);

        MBPL_free(context);
        context = NULL;
    }

    return NO_ERR;
}
