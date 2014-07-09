/**
 * \file MBPL_error.c
 * \author Nicolas Beucher
 * \date 17-01-2011
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
#include "MBPL_error.h"

/** Error value interpretation*/
char *err_str[] = {
    "No error",
    "Cannot create (memory allocation) context",
    "Cannot get the OpenCL platforms",
    "No OpenCL platform available",
    "Cannot get handle to OpenCL platform 0",
    "Cannot get an OpenCL device",
    "OpenCL context creation failed",
    "Cannot create the OpenCL command queue",
    "Cannot open the openCL program",
    "Cannot load the openCL program",
    "Cannot build the openCL program",
    "Context is either not properly initialised or closed",
    "Cannot create the OpenCL kernel",
    "Cannot create an OpenCL buffer",
    "Cannot enqueue the OpenCL kernel",
    "Invalid or unsupported image depth",
    "Incompatible image sizes",
    "Invalid direction given as argument",
    "Incorrect image dimension for image creation",
    "Incorrect load data parameter",
    "Cannot load data into image memory on device",
    "Image memory allocation failed",
    "Unknown error"
};

/**
 * Returns an explanation of the error code 
 */
char *MBPL_StrErr(MBPL_errcode error_nb) {
    if (error_nb>ERR_UNKNOWN) {
        return err_str[ERR_UNKNOWN];
    } else {
        return err_str[error_nb];
    }
}

