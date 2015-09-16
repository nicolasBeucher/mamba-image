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
#include "mambaApi_loc.h"

extern MB_errcode MB3D_HierarBld8(MB3D_Image *mask, MB3D_Image *srcdest, enum MB3D_grid_t grid);
extern MB_errcode MB3D_HierarBld32(MB3D_Image *mask, MB3D_Image *srcdest, enum MB3D_grid_t grid);

/*
 * (re)Builds a 3D image according to a 3D mask image and using a hierarchical
 * list to compute the rebuild.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_HierarBld(MB3D_Image *mask, MB3D_Image *srcdest, enum MB3D_grid_t grid) {
    
    /* Verification over depth and size */
    if (!MB3D_CHECK_SIZE_2(srcdest, mask)) {
        return MB_ERR_BAD_SIZE;
    }
    
    /* Invalid grid case */
    if (grid==MB3D_INVALID_GRID)
        return MB_ERR_BAD_PARAMETER;

    /* Only grey scale can be rebuild */
    switch (MB3D_PROBE_PAIR(srcdest, mask)) {
    case MB_PAIR_8_8:
        return MB3D_HierarBld8(mask,srcdest,grid);
        break;
    case MB_PAIR_32_32:
        return MB3D_HierarBld32(mask,srcdest,grid);
        break;
    default:
        break;
    }
    
    return MB_ERR_BAD_DEPTH;
}
