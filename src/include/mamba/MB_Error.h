/** \file MB_Error.h */
/*
 * Copyright (c) <2009>, <Nicolas BEUCHER and ARMINES for the Centre de 
 * Morphologie Mathématique(CMM), common research center to ARMINES and MINES 
 * Paristech>
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
#ifndef __MB_Error_H
#define __MB_Error_H

#ifdef __cplusplus
extern "C" {
#endif

/** Type definition for error code. */
typedef enum {
/** Value returned by function when no error was encountered. */
    MB_NO_ERR,
/** Value returned by function when an error of size inside the image was encountered.
 * For example, if the width of a first image was not corresponding with the width of a
 * second image when both are used in the same computations.
 */
    MB_ERR_BAD_SIZE,
/** Value returned by function when an error of depth inside the image was encountered.
 * For example, the function expected 8-bit pixels and got 1-bit pixels.
 */
    MB_ERR_BAD_DEPTH,
/** Value returned by function when a given parameter was incorrect. */
    MB_ERR_BAD_PARAMETER,
/** Value returned by function when a given value (as argument) was
 * incorrect.
 */
    MB_ERR_BAD_VALUE,
/** Value returned when a function requiring a direction (shift, neighbor)
 * is given an incorrect argument for direction (allowed value depends on the grid).
 */
    MB_ERR_BAD_DIRECTION,
/** Value returned when the allocation for image memory failed. */
    MB_ERR_CANT_ALLOCATE_MEMORY,
/** Value returned when the dimension of the image given in argument of a
 * function is incorrect.
 */
    MB_ERR_BAD_IMAGE_DIMENSIONS,
/** Value returned when the data given to a load function is incorrect 
 * (size or type).
 */
    MB_ERR_LOAD_DATA,
/** Value never returned (reserved for the error function). */
    MB_ERR_UNKNOWN
} MB_errcode;

/**
 * Returns an explanation of the error code. 
 * \param error_nb the error code number
 */
extern MB_API_ENTRY char * MB_API_CALL
MB_StrErr(MB_errcode error_nb);

#ifdef __cplusplus
}
#endif

#endif
