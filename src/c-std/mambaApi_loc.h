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
#ifndef MB_apilocH
#define MB_apilocH

/* The local header is the only header called inside each component of
 * the library, The global header is meant for the outside world.
 */
#include "mamba/mamba.h"

/* standard headers */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>

/****************************************/
/* Defines                              */
/****************************************/
/**@cond */
/* code that must be skipped by Doxygen */

/* Compiler specific */
#ifdef _MSC_VER
    #define INLINE __inline
#else
    #define INLINE inline
#endif

/* Possible image combinations*/
#define MB_PAIR_1_1     129 /* 128+1 */
#define MB_PAIR_1_8     136 /* 128+8 */
#define MB_PAIR_1_32    160 /* 128+32 */

#define MB_PAIR_8_1     1025 /* 8*128+1 */
#define MB_PAIR_8_8     1032 /* 8*128+8 */
#define MB_PAIR_8_32    1056 /* 8*128+32 */

#define MB_PAIR_32_1    4097 /* 32*128+1 */
#define MB_PAIR_32_8    4104 /* 32*128+8 */
#define MB_PAIR_32_32    4128 /* 32*128+32 */
/**@endcond*/

/** Value used to specify the end of a hierarchical list */
#define MB_LIST_END -1

/****************************************/
/* Macros                               */
/****************************************/

/** Returns the value of the image combination MB_PAIR_x_x */
#define MB_PROBE_PAIR(im_in, im_out) \
    (((im_in->depth)<<7) + (im_out)->depth)
    
/** Returns True if the two images sizes are compatible */
# define MB_CHECK_SIZE_2(im1, im2) \
    (((im1->width)==(im2->width))&&((im1->height)==(im2->height)))
    
/** Returns True if the three image sizes are compatible */
# define MB_CHECK_SIZE_3(im1, im2, im3) \
    (MB_CHECK_SIZE_2(im1, im2) && MB_CHECK_SIZE_2(im1, im3))
    
/** Returns the value of the image combination MB3D_PAIR_x_x */
#define MB3D_PROBE_PAIR(im_in, im_out) \
    (((im_in->seq[0]->depth)<<7) + im_out->seq[0]->depth)

/** Returns True if the two images sizes are compatible */
# define MB3D_CHECK_SIZE_2(im1, im2) \
    (((im1->seq[0]->width)  == (im2->seq[0]->width) ) && \
     ((im1->seq[0]->height) == (im2->seq[0]->height)) && \
     ((im1->length) == (im2->length)) )
     
/** Returns the size in bytes of an image line */
#define MB_LINE_COUNT(im) ((im->width*im->depth)/8)

/** How to fill the edge (1-bit images) */
#define BIN_FILL_VALUE(edge) ((edge==MB_FILLED_EDGE) ? UINT64_MAX:0)
/** How to fill the edge (8-bit images) */
#define GREY_FILL_VALUE(edge) ((edge==MB_FILLED_EDGE) ? UINT32_MAX:0)
/** How to fill the edge (32-bit images) */
#define I32_FILL_VALUE(edge) ((edge==MB_FILLED_EDGE) ? UINT32_MAX:0)

/* Neighbor pixel reading and accessing */
/* Macros work with the pointer to the pixel */
/* Macro returning the value of a pixel */
#define VAL(p_pix) (*p_pix)
/* Macro returning the value of the left neighbor pixel */
#define LEFT(p_pix) (*(p_pix-1))
/* Macro returning the value of the right neighbor pixel */
#define RIGHT(p_pix) (*(p_pix+1))

/****************************************/
/* Structures and Typedef               */
/****************************************/

/**
 * Label structure holding all the information needed to handle
 * labels attribution and creation.
 */
typedef struct {
    /* Equivalence between labels in an image */
    PIX32 *EQ;
    /* Equivalence between corrected labels in an image */
    PIX32 *CEQ;
    /* The greatest number of labels possible according to current image size */
    Uint32 maxEQ;
    /* Current label index (value given to the next label) */
    PIX32 current;
    /* Current corrected label index (value given to the next label) */
    PIX32 ccurrent;
    /* Number of objects found */
    PIX32 nbObjs;
} MB_Label_struct;

/* Label handling */
PIX32 MB_find_correct_label(MB_Label_struct *labels, PIX32 inlabel, PIX32 lblow, PIX32 lbhigh);
PIX32 MB_find_above_label(MB_Label_struct *labels, PIX32 inlabel);
void MB_TidyLabel(PLINE *plines_out,
                  Uint32 bytes, Uint32 nb_lines,
                  PIX32 lblow, PIX32 lbhigh,
                  MB_Label_struct *labels);
void MB3D_TidyLabel(MB3D_Image *dest,
                    PIX32 lblow, PIX32 lbhigh,
                    MB_Label_struct *labels);

/* typedef for the definition of function arguments */
typedef void (LABELGRIDFUNC) (PLINE *plines_out, PLINE *plines_in,
                              Uint32 bytes_in, Uint32 nb_lines,
                              MB_Label_struct *labels);


/* Definitions for the hierarchical queues :
 * Each pixel is tagged with one of these values in the MSByte of the 
 * marker image to represent their status
 */

/* Candidates : pixels not yet introduced in the HQ */
#define CANDIDATE 0x01000000
/* Queued : pixels in the HQ not yet sorted out */
#define QUEUED 0x02000000
/* RG_Labelled : pixels that were processed and do not belong to the watershed */
#define RG_LAB 0x00000000
/* WTS_Labelled : pixels that were processed and do belong to the watershed */
#define WTS_LAB 0xFF000000

/* Macro to extract the label of the pixel */
#define READ_LABEL(pixel) ((*pixel)&0x00FFFFFF)
/* Macro to set the status of the pixel */
#define SET_STATUS(pixel, status) (((*pixel)&0x00FFFFFF)|status)
/* Macro to check the status of a pixel */
#define IS_PIXEL(pixel, status) (((*pixel)&0xFF000000)==status)

/** 
 * Token used in hierarchical list.
 * A token gives its next (by position nextx, nexty in image) 
 * token in the list (-1 if the list ends).
 */
typedef struct {
    /** next token (x) */
    int nextx;
    /** next token (y) */
    int nexty;
} MB_Token;

/** 
 * List control structure that gives you the index
 * of the first and last elements of list.
 */
typedef struct {
    /** first token of the list (x) */
    int firstx;
    /** first token of the list (y) */
    int firsty;
    /** last token of the list (x) */
    int lastx;
    /** last token of the list (y) */
    int lasty;
} MB_ListControl;

/** 
 * Token used in hierarchical list.
 * A token gives its next (by position nextx, nexty in image) 
 * token in the list (-1 if the list ends).
 */
typedef struct {
    /** next token (x) */
    int nextx;
    /** next token (y) */
    int nexty;
    /** next token (z) */
    int nextz;
} MB3D_Token;

/** 
 * List control structure that gives you the index
 * of the first and last elements of list.
 */
typedef struct {
    /** first token of the list (x) */
    int firstx;
    /** first token of the list (y) */
    int firsty;
    /** first token of the list (z) */
    int firstz;
    /** last token of the list (x) */
    int lastx;
    /** last token of the list (y) */
    int lasty;
    /** last token of the list (z) */
    int lastz;
} MB3D_ListControl;

/****************************************/
/* Neighbors access                     */
/****************************************/

/** Table giving the offset for the neighbor in square grid (x and y) */ 
extern const int sqNbDir[9][2];

/** Table giving the offset for the neighbor in hexagonal grid (x and y) */
/* the direction depends on the oddness/evenness of the line */
extern const int hxNbDir[2][7][2];

/** Table giving the offset for the neighbor in cubic grid (x, y and z) */ 
extern const int cubeNbDir[27][3];

/** Table giving the offset for the neighbor in face-centered cubic grid (x, y and z) */
/* the direction depends on the coordinates of the line y and planes z*/
extern const int fccNbDir[6][13][3];

/* Table giving the offset for the previous neighbor in cubic grid (x, y and z) */ 
extern const int cubePreDir[13][3];

/* Table giving the offset for the neighbor in face-centered cubic grid (x, y and z) */
/* the direction depends on the coordinates of the line y and planes z*/
extern const int fccPreDir[6][6][3];

/****************************************/
/* Volume arrays                        */
/****************************************/

/** Volume arrays*/
extern const Uint64 MB_VolumePerByte[256];

/****************************************/
/* Internal memory management           */
/****************************************/

void *MB_malloc(int size);
void *MB_aligned_malloc(int size, int alignment);
void MB_free(void *ptr);
void MB_aligned_free(void *ptr);

void *MB_memset(void *s, int c, int size);
void *MB_memcpy(void *dest, const void *src, int size);

#endif
