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
/* The functions described here realise the basic operation */
/* needed to shift pixel in any directions. */

/* Here we used a notion called pixels register. In fact it is a MB_Vector1 value */
/* that is holding binary pixels that we are going to use to perform computation */
/* it is easier to call it pixels registers because the value does not represent */
/* only one pixel but 32 or 64 depending on your computer target. */

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_LINE(PLINE *plines_germ, PLINE *plines_germ_nbr,
                            PLINE *plines_mask,
                            Uint32 bytes_in, Uint64 *volume)
{
    Uint32 i;
    Uint64 vol;
    MB_Vector1 vec1; /* pixel register */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ);
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask);
    MB_Vector1 *germ_nbr = (MB_Vector1 *) (*plines_germ_nbr);
    
    vol = *volume;
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ++,mask++,germ_nbr++) {
        vec1 = ((*germ)&(*germ_nbr))|(*mask);
        *germ = vec1;
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_EDGE_LINE(PLINE *plines_germ,
                                   PLINE *plines_mask,
                                   Uint32 bytes_in, Uint64 *volume )
{
    Uint32 i;
    Uint64 vol;
    MB_Vector1 edge_val;
    MB_Vector1 vec1; /* pixel register */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ);
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask);
    
    vol = *volume;
    edge_val = BIN_FILL_VALUE(MB_FILLED_EDGE);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ++,mask++) {
        vec1 = ((*germ)&edge_val)|(*mask);
        *germ = vec1;
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_LINE_LEFT(PLINE *plines_germ, PLINE *plines_germ_nbr,
                                 PLINE *plines_mask,
                                 Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i;
    Uint64 vol;
    MB_Vector1 edge_val;
    MB_Vector1 vec1,vec2; /* pixel registers */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ+bytes_in-sizeof(MB_Vector1));
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask+bytes_in-sizeof(MB_Vector1));
    MB_Vector1 *germ_nbr = (MB_Vector1 *) (*plines_germ_nbr+bytes_in-sizeof(MB_Vector1));
    
    vol = *volume;
    edge_val = BIN_FILL_VALUE(MB_FILLED_EDGE);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ--,mask--,germ_nbr--) {
        vec2 = (*germ_nbr);
        vec1 = ((*germ)&((vec2>>1) | (edge_val<<(MB_vec1_size-1))))|(*mask);
        *germ = vec1;
        edge_val = vec2; /* now edge_val is used to contains the previous pixel register*/
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_LINE_LEFT_HORZ(PLINE *plines_germ, PLINE *plines_mask,
                                      Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i,j;
    Uint64 vol;
    MB_Vector1 edge_val;
    MB_Vector1 vec1; /* pixel register */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ+bytes_in-sizeof(MB_Vector1));
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask+bytes_in-sizeof(MB_Vector1));
    
    vol = *volume;
    edge_val = BIN_FILL_VALUE(MB_FILLED_EDGE);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ--,mask--) {
        vec1 = (*germ);
        for(j=0; j<MB_vec1_size; j++) {
            vec1 = (vec1&((vec1>>1) | (edge_val<<(MB_vec1_size-1))))|(*mask);
        }
        *germ = vec1;
        edge_val = vec1; /* now edge_val is used to contains the previous pixel register*/
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_LINE_RIGHT(PLINE *plines_germ, PLINE *plines_germ_nbr,
                                  PLINE *plines_mask,
                                  Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i;
    Uint64 vol;
    MB_Vector1 edge_val;
    MB_Vector1 vec1,vec2; /* pixel registers */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ);
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask);
    MB_Vector1 *germ_nbr = (MB_Vector1 *) (*plines_germ_nbr);
    
    vol = *volume;
    edge_val = BIN_FILL_VALUE(MB_FILLED_EDGE);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ++,mask++,germ_nbr++) {
        vec2 = (*germ_nbr);
        vec1 = ((*germ)&((vec2<<1) | (edge_val>>(MB_vec1_size-1))))|(*mask);
        *germ = vec1;
        edge_val = vec2; /* now edge_val is used to contains the previous pixel register*/
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/*
 * Used to rebuild the pixels of a line.
 */
static INLINE void BLD_LINE_RIGHT_HORZ(PLINE *plines_germ,
                                       PLINE *plines_mask,
                                       Uint32 bytes_in, Uint64 *volume ) 
{
    Uint32 i,j;
    Uint64 vol;
    MB_Vector1 edge_val;
    MB_Vector1 vec1; /* pixel register */

    MB_Vector1 *germ = (MB_Vector1 *) (*plines_germ);
    MB_Vector1 *mask = (MB_Vector1 *) (*plines_mask);
    
    vol = *volume;
    edge_val = BIN_FILL_VALUE(MB_FILLED_EDGE);
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),germ++,mask++) {
        vec1 = (*germ);
        for(j=0; j<MB_vec1_size; j++) {
            vec1 = (vec1&((vec1<<1) | (edge_val>>(MB_vec1_size-1))))|(*mask);
        }
        *germ = vec1;
        edge_val = vec1; /* now edge_val is used to contains the previous pixel register*/
        MB_vec1_acc(vol, vec1);
    }
    
    *volume = vol;
}

/****************************************/
/* Direction functions                  */
/****************************************/
/* The functions are described in a separate file to communalize with other */
/* build functions. */
#include "MB_BldDirection.h"

/****************************************/
/* Main function                        */
/****************************************/

/*
 * (re)Builds an image according to a direction and a mask image.
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
MB_errcode MB_DualBldNbb(MB_Image *mask, MB_Image *srcdest, Uint32 dirnum, Uint64 *pVolume, enum MB_grid_t grid)
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
    case MB_PAIR_1_1:
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
    fn(plines_inout, plines_mask, bytes_in, mask->height, pVolume);
    
    return MB_NO_ERR;
}

