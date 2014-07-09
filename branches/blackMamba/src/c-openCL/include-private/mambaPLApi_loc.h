/**
 * \file mambaPLApi_loc.h
 * \date 17-01-2011
 *
 * This file contains the various definitions, global variables
 * macro, struct and functions that are shared between components
 * of the library but are not meant to be exported to the outside
 * world.
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
#ifndef MBPL_apilocH
#define MBPL_apilocH

/* The local header is the only header called inside each component of
 * the library, The global header is meant for the outside world.
 */
#include "mambaPLApi.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

/****************************************/
/* Defines                              */
/****************************************/
/**@cond */
/* code that must be skipped by Doxygen */

/* Possible image combinations*/
#define MBPL_PAIR_1_1     129 /* 128+1 */
#define MBPL_PAIR_1_8     136 /* 128+8 */
#define MBPL_PAIR_1_32    160 /* 128+32 */

#define MBPL_PAIR_8_1     1025 /* 8*128+1 */
#define MBPL_PAIR_8_8     1032 /* 8*128+8 */
#define MBPL_PAIR_8_32    1056 /* 8*128+32 */

#define MBPL_PAIR_32_1    4097 /* 32*128+1 */
#define MBPL_PAIR_32_8    4104 /* 32*128+8 */
#define MBPL_PAIR_32_32    4128 /* 32*128+32 */

/**@endcond*/

/****************************************/
/* Macros                               */
/****************************************/

/** Returns the value of the images combination MBPL_PAIR_x_x */
#define MBPL_PROBE_PAIR(im_in, im_out) \
    (((im_in->depth)<<7) + (im_out)->depth)
    
/** Returns True if the two images sizes are compatibles */
# define MBPL_CHECK_SIZE_2(im1, im2) \
    (((im1->width)==(im2->width))&&((im1->height)==(im2->height)))
    
/** Returns True if the three images sizes are compatibles */
# define MBPL_CHECK_SIZE_3(im1, im2, im3) \
    (MBPL_CHECK_SIZE_2(im1, im2) && MBPL_CHECK_SIZE_2(im1, im3))
 
/****************************************/
/* Structures and Typedef               */
/****************************************/

/* Parallel library context struct */
typedef struct {
    cl_context ctxCL;
    cl_command_queue cmdqCL;
    cl_program prgCL;
    cl_kernel *kersCL;
    size_t *mwgCL;
} MBPL_Context;

/****************************************/
/* context global pointer               */
/****************************************/

/* General context handler */
extern MBPL_Context *context;

/****************************************/
/* Kernels definition                   */
/****************************************/

typedef enum {
    /** Logic and*/
    KER_AND,
    /** Add 8-bit + 8-bit = 8-bit*/
    KER_ADD_8_8_8,
    /** Add 32-bit + 32-bit = 32-bit*/
    KER_ADD_32_32_32,
    /** Inf 8-bit*/
    KER_INF_8_8_8,
    /** Inf 32-bit*/
    KER_INF_32_32_32,
    /** ConSet for 1-bit and 8-bit*/
    KER_CONSET_8,
    /** ConSet for 32-bit*/
    KER_CONSET_32,
    /** Inferior neighborin square*/
    KER_INFNB_8_S,
    /** Inferior neighbor in hexagonal*/
    KER_INFNB_8_H,
    
    /** total number of kernel defined in the MBPL API */
    NB_KERNELS
} MBPL_kernel_t;

/* creating the kernels */
MBPL_errcode MBPL_CreateKernels(cl_device_id device);
/* deleting the kernels */
MBPL_errcode MBPL_DestroyKernels();

/****************************************/
/* Internal memory management           */
/****************************************/

void *MBPL_malloc(int size);
void *MBPL_aligned_malloc(int size, int alignment);
void MBPL_free(void *ptr);
void MBPL_aligned_free(void *ptr);

void *MBPL_memset(void *s, int c, int size);
void *MBPL_memcpy(void *dest, const void *src, int size);

#endif
