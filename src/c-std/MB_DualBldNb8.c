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
#include "mambaApi_loc.h"
#include "mambaApi_vector.h"

/****************************************/
/* Base functions                       */
/****************************************/
/* The functions described here realised the basic operations */
/* needed to shift pixel in any directions */

/*
 * Used to rebuild the pixels of a line with a line directly above or below.
 * No shifting inside the line.
 */
static INLINE void BLD_LINE(PLINE *plines_germ, PLINE *plines_germ_nbr,
                            PLINE *plines_mask,
                            Uint32 bytes_in, Uint64 *volume)
{
    Uint32 i;
    Uint64 vol=0;
    
#if defined(MB_VECTORIZATION_8) && !defined(__MINGW32__)
    MB_Vector8 vec1, vec2;

    MB_Vector8 *germ = (MB_Vector8 *) (*plines_germ); /* inout image */
    MB_Vector8 *mask = (MB_Vector8 *) (*plines_mask);
    MB_Vector8 *germ_nbr = (MB_Vector8 *) (*plines_germ_nbr); /* inout image shifted */
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),germ++,mask++,germ_nbr++) {
        vec1 = MB_vec8_load(germ);
        vec2 = MB_vec8_load(germ_nbr);
        vec1 = MB_vec8_min(vec1,vec2);
        vec2 = MB_vec8_load(mask);
        vec1 = MB_vec8_max(vec2,vec1);
        MB_vec8_store(germ,vec1);
        MB_vec8_acc(vol, vec1);
    }
#else
    PIX8 a;
    
    PLINE germ = (PLINE) (*plines_germ); /* inout image */
    PLINE mask = (PLINE) (*plines_mask);
    PLINE germ_nbr = (PLINE) (*plines_germ_nbr); /* inout image shifted */
    
    for(i=0;i<bytes_in;i++,germ++,mask++,germ_nbr++) {
        a = (*germ)<(*germ_nbr) ? (*germ) : (*germ_nbr);
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
#endif

    *volume += vol;
}

/*
 * Used to rebuild the pixels of a line when this line is touching the edge.
 */
static INLINE void BLD_EDGE_LINE(PLINE *plines_germ,
                                   PLINE *plines_mask,
                                   Uint32 bytes_in, Uint64 *volume )
{
    Uint32 i;
    Uint64 vol=0;
    PIX8 edge_val = (PIX8) GREY_FILL_VALUE(MB_FILLED_EDGE);
    
#if defined(MB_VECTORIZATION_8) && !defined(__MINGW32__)
    MB_Vector8 vec1,vec2;

    MB_Vector8 edge = MB_vec8_set(edge_val);
    MB_Vector8 *germ = (MB_Vector8 *) (*plines_germ); /* inout image */
    MB_Vector8 *mask = (MB_Vector8 *) (*plines_mask);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),germ++,mask++) {
        vec1 = MB_vec8_load(germ);
        vec1 = MB_vec8_min(edge,vec1);
        vec2 = MB_vec8_load(mask);
        vec1 = MB_vec8_max(vec2,vec1);
        MB_vec8_store(germ,vec1);
        MB_vec8_acc(vol, vec1);
    }
#else
    PIX8 a;

    PLINE germ = (PLINE) (*plines_germ); /* inout image */
    PLINE mask = (PLINE) (*plines_mask);
    
    for(i=0;i<bytes_in;i++,germ++,mask++) {
        a = (*germ)<(edge_val) ? (*germ) : edge_val;
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
#endif
    
    *volume += vol;
}

/*
 * Used to rebuild the pixels of a line using the pixels of an above, below 
 * but shifted in the left direction. In fact, to emulate this, we do
 * not look directly into the above pixel but we look into the above to the right
 * pixel which would have been directly above had the left shifting really
 * happened.
 */
static INLINE void BLD_LINE_LEFT(PLINE *plines_germ, PLINE *plines_germ_nbr,
                                 PLINE *plines_mask,
                                 Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i;
    Uint64 vol=0;
    PIX8 edge_val = (PIX8) GREY_FILL_VALUE(MB_FILLED_EDGE);
    
#if defined(MB_VECTORIZATION_8) && !defined(__MINGW32__)
    MB_Vector8 vec1,vec2,vec3;

    MB_Vector8 edge = MB_vec8_set(edge_val);
    MB_Vector8 *germ = (MB_Vector8 *) (*plines_germ+bytes_in-sizeof(MB_Vector8));
    MB_Vector8 *mask = (MB_Vector8 *) (*plines_mask+bytes_in-sizeof(MB_Vector8));
    MB_Vector8 *germ_nbr = (MB_Vector8 *) (*plines_germ_nbr+bytes_in-sizeof(MB_Vector8));
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),germ--,mask--,germ_nbr--) {
        vec2 = MB_vec8_load(germ_nbr);
        edge = MB_vec8_shlft(edge, MB_vec8_size-1);
        vec1 = MB_vec8_shrgt(vec2, 1);
        vec1 = MB_vec8_or(vec1, edge);
        vec3 = MB_vec8_load(germ);
        vec1 = MB_vec8_min(vec1,vec3);
        vec3 = MB_vec8_load(mask);
        vec1 = MB_vec8_max(vec3,vec1);
        MB_vec8_store(germ,vec1);
        MB_vec8_acc(vol, vec1);
        edge = vec2;
    }
#else
    PIX8 a;

    PLINE germ = (PLINE) (*plines_germ+bytes_in-1);  /* inout image */
    PLINE mask = (PLINE) (*plines_mask+bytes_in-1);
    PLINE germ_nbr = (PLINE) (*plines_germ_nbr+bytes_in); /* inout image shifted */
    
    /* The first pixel is inside the edge */
    a = (*germ)<(edge_val) ? (*germ) : edge_val;
    a = a>(*mask) ? a : (*mask);
    *germ = a;
    vol = a;
    germ--;
    mask--;
    germ_nbr--;
    for(i=0;i<bytes_in-1;i++,germ--,mask--,germ_nbr--) {
        a = (*germ)<(*germ_nbr) ? (*germ) : (*germ_nbr);
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
#endif
    
    *volume += vol;
}

/*
 * Used to rebuild the pixels of a line using the pixels of
 * the same line but shifted in the left direction. 
 */
static INLINE void BLD_LINE_LEFT_HORZ(PLINE *plines_germ,
                                      PLINE *plines_mask,
                                      Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i;
    Uint64 vol=0;
    PIX8 edge_val, a;

    PLINE germ = (PLINE) (*plines_germ+bytes_in-1);  /* inout image */
    PLINE mask = (PLINE) (*plines_mask+bytes_in-1);
    PLINE germ_nbr = (PLINE) (*plines_germ+bytes_in); /* inout image shifted */
    
    edge_val = (PIX8) GREY_FILL_VALUE(MB_FILLED_EDGE);
    
    /* The first pixel is inside the edge */
    a = (*germ)<(edge_val) ? (*germ) : edge_val;
    a = a>(*mask) ? a : (*mask);
    *germ = a;
    vol = a;
    germ--;
    mask--;
    germ_nbr--;
    for(i=0;i<bytes_in-1;i++,germ--,mask--,germ_nbr--) {
        a = (*germ)<(*germ_nbr) ? (*germ) : (*germ_nbr);
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
    
    *volume += vol;
}

/*
 * Used to rebuild the pixels of a line using the pixel of an above, below 
 * but shifted in the right direction. In fact, to emulate this, we do
 * not look directly into the above pixel but we look into the above to the left
 * pixel which would have been directly above had the right shifting really
 * happened.
 */
static INLINE void BLD_LINE_RIGHT(PLINE *plines_germ, PLINE *plines_germ_nbr,
                                  PLINE *plines_mask,
                                  Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i;
    Uint64 vol=0;
    PIX8 edge_val = (PIX8) GREY_FILL_VALUE(MB_FILLED_EDGE);
    
#if defined(MB_VECTORIZATION_8) && !defined(__MINGW32__)
    MB_Vector8 vec1,vec2,vec3;

    MB_Vector8 edge = MB_vec8_set(edge_val);
    MB_Vector8 *germ = (MB_Vector8 *) (*plines_germ);
    MB_Vector8 *mask = (MB_Vector8 *) (*plines_mask);
    MB_Vector8 *germ_nbr = (MB_Vector8 *) (*plines_germ_nbr);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector8),germ++,mask++,germ_nbr++) {
        vec2 = MB_vec8_load(germ_nbr);
        edge = MB_vec8_shrgt(edge, MB_vec8_size-1);
        vec1 = MB_vec8_shlft(vec2, 1);
        vec1 = MB_vec8_or(vec1, edge);
        vec3 = MB_vec8_load(germ);
        vec1 = MB_vec8_min(vec1,vec3);
        vec3 = MB_vec8_load(mask);
        vec1 = MB_vec8_max(vec3,vec1);
        MB_vec8_store(germ,vec1);
        MB_vec8_acc(vol, vec1);
        edge = vec2;
    }
    
#else
    PIX8 a;

    PLINE germ = (PLINE) (*plines_germ); /* inout image */
    PLINE mask = (PLINE) (*plines_mask);
    PLINE germ_nbr = (PLINE) (*plines_germ_nbr-1); /* inout image shifted */
    
    /* The first pixel is inside the edge */
    a = (*germ)<(edge_val) ? (*germ) : edge_val;
    a = a>(*mask) ? a : (*mask);
    *germ = a;
    vol = a;
    germ++;
    mask++;
    germ_nbr++;
    for(i=0;i<bytes_in-1;i++,germ++,mask++,germ_nbr++) {
        a = (*germ)<(*germ_nbr) ? (*germ) : (*germ_nbr);
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
#endif
    
    *volume += vol;
}

/*
 * Used to rebuild the pixels of a line using the pixels of
 * the same line but shifted in the right direction.
 */
static INLINE void BLD_LINE_RIGHT_HORZ(PLINE *plines_germ,
                                       PLINE *plines_mask,
                                       Uint32 bytes_in, Uint64 *volume)
{
    Uint32 i;
    Uint64 vol=0;
    PIX8 edge_val, a;

    PLINE germ = (PLINE) (*plines_germ); /* inout image */
    PLINE mask = (PLINE) (*plines_mask);
    PLINE germ_nbr = (PLINE) (*plines_germ-1); /* inout image shifted */
    
    edge_val = (PIX8) GREY_FILL_VALUE(MB_FILLED_EDGE);
    
    /* The first pixel is inside the edge */
    a = (*germ)<(edge_val) ? (*germ) : edge_val;
    a = a>(*mask) ? a : (*mask);
    *germ = a;
    vol = a;
    germ++;
    mask++;
    germ_nbr++;
    for(i=0;i<bytes_in-1;i++,germ++,mask++,germ_nbr++) {
        a = (*germ)<(*germ_nbr) ? (*germ) : (*germ_nbr);
        a = a>(*mask) ? a : (*mask);
        *germ = a;
        vol += a;
    }
    
    *volume += vol;
}

/****************************************/
/* Direction functions                  */
/****************************************/
/* The functions are described in a separate file to communalize with other */
/* build functions */
#include "MB_BldDirection.h"

/****************************************/
/* Main function                        */
/****************************************/

/*
 * (re)Builds (dual operation) an image according to a direction and a mask image.
 * The direction depends on the grid used (see MB_ngh.h for definitions of directions).
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param dirnum the direction number
 * \param pVolume the computed volume of the output image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_DualBldNb8(MB_Image *mask, MB_Image *srcdest, Uint32 dirnum, Uint64 *pVolume, enum MB_grid_t grid)
{
    Uint32 bytes_in;
    PLINE *plines_mask, *plines_inout;
    NEIBFUNC *fn;

    /* Error management */
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(mask, srcdest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Grid value and possible direction are connected, grid value is the */
    /* maximum number of directions */
    if(dirnum>6 && grid==MB_HEXAGONAL_GRID) {
        return MB_ERR_BAD_DIRECTION;
    }
    if(dirnum>8 && grid==MB_SQUARE_GRID) {
        return MB_ERR_BAD_DIRECTION;
    }
    /* Only binary images can be processed */
    switch (MB_PROBE_PAIR(mask, srcdest)) {
    case MB_PAIR_8_8:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }

    /* Setting up pointers */
    plines_mask = mask->plines;
    plines_inout = srcdest->plines;
    bytes_in = MB_LINE_COUNT(mask);

    /* Initial value of volume*/
    *pVolume = 0;

    /* Calling the corresponding function */
    fn = SwitchTo[grid][dirnum];
    fn(plines_inout, plines_mask, bytes_in, mask->height, pVolume );
    
    return MB_NO_ERR;
}
