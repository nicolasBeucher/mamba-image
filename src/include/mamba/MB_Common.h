/** \file MB_Common.h */
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
#ifndef __MB_Common_H
#define __MB_Common_H

#ifdef __cplusplus
extern "C" {
#endif

/****************************************/
/* Includes                             */
/****************************************/
#include <stdint.h>

/****************************************/
/* Defines                              */
/****************************************/

#if defined(WIN32) || defined(_WIN32)
#undef __WIN32__
#define __WIN32__ 1
#endif

#ifndef MB_API_ENTRY
#  if defined(__WIN32__) && defined(MB_BUILD)
#    define MB_API_ENTRY __declspec(dllexport)
#  else
#    define MB_API_ENTRY
#  endif
#endif

#ifndef MB_API_CALL
# if defined(__WIN32__) && !defined(__GNUC__)
#  define MB_API_CALL __cdecl
# else
#  define MB_API_CALL
# endif
#endif

/** Making sure the image size is multiple of 64 for the width. */
#define MB_ROUND_W    64
/** Making sure the image size is multiple of 2 for the height. */
#define MB_ROUND_H    2
/** Image limit size in total number of pixels.
 * When considering the limits on the image size, remember that
 * the function computing the volume which returns Uint64
 * should not overflow on the 32-bit images. (that is, max volume
 * for the 32-bit image is 2^64-1) which yields approx 4.3 billions pixels
 * so roughly 65536*65536 images size.
 * However, if we compute a watershed transform, the number of allowed
 * labels is 2^24 (3 lower bytes of the label image). Therefore, if, in
 * a large image, the number of labels exceeds this value, some basins of
 * the watershed transform will share the same label. You must be aware of
 * this possibility.
 */
#define MB_MAX_IMAGE_SIZE    ((Uint64)4294967296)

/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Unsigned 8-bit value type */
typedef uint8_t Uint8;
/** Unsigned 16-bit value type */
typedef uint16_t Uint16;
/** Unsigned 32-bit value type*/
typedef uint32_t Uint32;
/** Unsigned 64-bit value type */
typedef uint64_t Uint64;
/** Signed 8-bit value type */
typedef int8_t Sint8;
/** Signed 16-bit value type */
typedef int16_t Sint16;
/** Signed 32-bit value type */
typedef int32_t Sint32;
/** Signed 64-bit value type */
typedef int64_t Sint64;

/** grey-scale pixels value type */
typedef uint8_t PIX8;
/** Pixels line pointers type */
typedef PIX8 *PLINE;

/** Signed 32-bit pixels value type */
typedef uint32_t PIX32;
/** 32-bit pixels line pointers type */
typedef PIX32 *PLINE32;

/** 2D image */
typedef struct {
    /** The width of the image */
    Uint32 width;
    /** The height of the image */
    Uint32 height;
    /** The depth of the image */
    Uint32 depth;
    /** access to pixel lines */
    PLINE *plines;
    /** pixel array */
    PIX8 *pixels;
} MB_Image;

/** 3D image */
typedef struct {
    /** The images sequence composing the 3D data */
    MB_Image **seq;
    /** the length of the sequence */
    Uint32 length;
} MB3D_Image;

/** Possible grid values: */
enum MB_grid_t {
    /** Hexagonal grid */
    MB_HEXAGONAL_GRID = 1,
    /** Square grid */
    MB_SQUARE_GRID = 0
};

/** Possible edge modes: */
enum MB_edgemode_t {
    /** Empty edge (zero) */
    MB_EMPTY_EDGE = 0,
    /** Filled edge (maximum value for a given depth) */
    MB_FILLED_EDGE = 1
};

/** Possible 3D grid values:
 * Values are specificly chosen not to match 2D grid values.
 */
enum MB3D_grid_t {
    /** Invalid grid */
    MB3D_INVALID_GRID = -1,
    /** Cubic grid */
    MB3D_CUBIC_GRID = 1024,
    /** Face centered cubic grid (fcc, also known as cubic close-packed or ccp) */
    MB3D_FCC_GRID = 1025
};

/** Neighbors encoding: */
enum MB_Neighbors_code_t {
    MB_NEIGHBOR_0 = 0x0001,
    MB_NEIGHBOR_1 = 0x0002,
    MB_NEIGHBOR_2 = 0x0004,
    MB_NEIGHBOR_3 = 0x0008,
    MB_NEIGHBOR_4 = 0x0010,
    MB_NEIGHBOR_5 = 0x0020,
    MB_NEIGHBOR_6 = 0x0040,
    MB_NEIGHBOR_7 = 0x0080,
    MB_NEIGHBOR_8 = 0x0100,
    MB_NEIGHBOR_ALL_HEXAGONAL = 0x07f,
    MB_NEIGHBOR_ALL_SQUARE = 0x01ff
};

#ifdef __cplusplus
}
#endif

#endif /* __MB_Common_H */

