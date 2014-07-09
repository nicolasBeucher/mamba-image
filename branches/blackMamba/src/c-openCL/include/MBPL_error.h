/**
 * \file MBPL_error.h
 * \date 17-01-2011
 *
 * This file contains the complete liste of error code 
 * returned by the API functions.
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
#ifndef MBPL_errorH
#define MBPL_errorH

/****************************************/
/* Includes                             */
/****************************************/

/****************************************/
/* Defines                              */
/****************************************/

/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Type definition for error code */
typedef enum {
/** Value returned by function when no error was encountered. */
    NO_ERR,
/** Cannot create (memory allocation) context */
    ERR_CANT_CREATE_CONTEXT,
/** Cannot get the OpenCL platforms */
    ERR_CANT_GET_CL_PLATFORMS,
/** No OpenCL platform available */
    ERR_NO_CL_PLATFORM,
/** Cannot get handle to OpenCL platform 0 */
    ERR_CANT_GET_CL_PLATFORM_0,
/** Cannot get an OpenCL device */
    ERR_CANT_GET_CL_DEVICE,
/** OpenCL context creation failed */
    ERR_CANT_CREATE_CL_CONTEXT,
/** Cannot create the OpenCL command queue */
    ERR_CANT_CREATE_CL_CMDQ,
/** Cannot open the openCL program */
    ERR_CANT_OPEN_CL_PROG,
/** Cannot load the openCL program */
    ERR_CANT_LOAD_CL_PROG,
/** Cannot build the openCL program */
    ERR_CANT_BUILD_CL_PROG,
/** Context is either not properly initialised or closed */
    ERR_INVALID_CONTEXT,
/** Cannot create the OpenCL kernel */
    ERR_CANT_CREATE_CL_KERNEL,
/** Cannot create an OpenCL buffer */
    ERR_CANT_CREATE_CL_BUFFER,
/** Cannot enqueue the OpenCL kernel */
    ERR_CANT_ENQUEUE_CL_KERNEL,
/** Invalid or unsupported image depth */
    ERR_INVALID_IM_DEPTH,
/** Incompatible image sizes */
    ERR_INVALID_IM_SIZE,
/** Invalid direction given as argument */
    ERR_INVALID_DIRECTION,
/** Incorrect image dimension for image creation */
    ERR_BAD_IMAGE_DIMENSIONS,
/** Incorrect load data parameter */
    ERR_INVALID_LOAD_DATA,
/** Cannot load data into image memory on device */
    ERR_CANT_LOAD_DATA,
/** Value returned when the allocation for image memory failed. */
    ERR_CANT_ALLOCATE_MEMORY,
/** Unknown error */
    ERR_UNKNOWN
} MBPL_errcode;

/****************************************/
/* Functions                            */
/****************************************/

char *MBPL_StrErr(MBPL_errcode error_nb);

#endif
