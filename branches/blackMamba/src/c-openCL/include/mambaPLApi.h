/**
 * \file mambaPLApi.h
 * \date 17-01-2011
 *
 * This file contains the various definitions, global variables
 * macro, struct and functions created for the library.
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
#ifndef MBPL_apiH
#define MBPL_apiH

#ifdef __cplusplus
extern "C" {
#endif

/****************************************/
/* Includes                             */
/****************************************/
#include "mambaCommon.h"
#include "MBPL_error.h"

#include <CL/opencl.h>

/****************************************/
/* Defines                              */
/****************************************/

/****************************************/
/* Macros                               */
/****************************************/

/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Images structure with the width, height and depth;
 * the pixels array is stored in an openCL memory buffer
 */
typedef struct {
    /** The width of the image */
    Uint32 width;
    /** The height of the image */
    Uint32 height;
    /** The depth of the image */
    Uint32 depth;
    /** full size of the buffer in device memory */
    Uint32 buf_size;
    /** pixel array */
    cl_mem pixels;
} MBPL_Image;

/****************************************/
/* Global variables                     */
/****************************************/

/** image counter */
extern Uint32 MBPL_refcounter;

/****************************************/
/* Context functions                    */
/****************************************/
MBPL_errcode MBPL_CreateContext(void);
MBPL_errcode MBPL_DestroyContext(void);

/*********************************************/
/* Image Creation and Manipulation Functions */
/*********************************************/
MBPL_errcode MBPL_Create(MBPL_Image *image, Uint32 width, Uint32 height, Uint32 depth);
MBPL_errcode MBPL_Destroy(MBPL_Image *image);
MBPL_errcode MBPL_TransferFromMB(MB_Image *src, MBPL_Image *dest);
MBPL_errcode MBPL_TransferToMB(MBPL_Image *src, MB_Image *dest);
MBPL_errcode MBPL_Load(MBPL_Image *image, PIX8 *indata, Uint32 len);
MBPL_errcode MBPL_Extract(MBPL_Image *image, PIX8 **outdata, Uint32 *len);
MBPL_errcode MBPL_Copy(MBPL_Image *src, MBPL_Image *dest);

/****************************************/
/* Image Processing Functions           */
/****************************************/

/* Logical and */
MBPL_errcode MBPL_And(MBPL_Image *src1, MBPL_Image *src2, MBPL_Image *dest);
/* Adds two images */
MBPL_errcode MBPL_Add(MBPL_Image *src1, MBPL_Image *src2, MBPL_Image *dest);
/* Minimum */
MBPL_errcode MBPL_Inf(MBPL_Image *src1, MBPL_Image *src2, MBPL_Image *dest);
/* Computes the image volume */
MBPL_errcode MBPL_Volume(MBPL_Image *src, Uint64 *pVolume);
/* Constant setting */
MBPL_errcode MBPL_ConSet(MBPL_Image *dest, Uint32 value);
/* Inf neighbor */
MBPL_errcode MBPL_InfNb8(MBPL_Image *src, MBPL_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);


#ifdef __cplusplus
}
#endif

#endif

