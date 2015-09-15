/*
 * Copyright (c) <2014>, <Nicolas BEUCHER and ARMINES for the Centre de 
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

extern MB_errcode MB_DiffNbb(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);
extern MB_errcode MB_DiffNb8(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);
extern MB_errcode MB_DiffNb32(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);

/****************************************/
/* Main function                        */
/****************************************/

/*
 * Computes the set difference between two image pixels
 * (a central pixel and its neighbors in the other image).
 * The neighbor depends on the grid used (see mambaCommon.h). Neighbors are
 * described using a pattern. If no neighbor
 * is defined, the function will leave silently doing nothing.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param neighbors the neighbors to take into account
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_DiffNb(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge)
{
    switch(srcdest->depth) {
    case 1:
        return MB_DiffNbb(src, srcdest, neighbors, grid, edge);
        break;
    case 8:
        return MB_DiffNb8(src, srcdest, neighbors, grid, edge);
        break;
    case 32:
        return MB_DiffNb32(src, srcdest, neighbors, grid, edge);
        break;
    default:
        break;
    }
    
    return MB_ERR_BAD_DEPTH;
}




