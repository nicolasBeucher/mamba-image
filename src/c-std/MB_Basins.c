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

extern MB_errcode MB_Basins8(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid);
extern MB_errcode MB_Basins32(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid);

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Performs a watershed segmentation of the image using the marker image
 * as a starting point for the flooding. The function returns the catchment 
 * basins of the watershed but no actual watershed line. It is recommended
 * to use this function rather than MB_Watershed if you are only interested
 * in catchment basins (faster).
 * The result is put into a the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32-bit values.
 * | 0      | 1      | 2      | 3      |
 * |--------|--------|--------|--------|
 * | Segment label            | Unused |
 * Each byte can be accessed using the function MB_CopyBytePlane.
 *
 * \param src the image to be segmented
 * \param marker the marker image in which the result of segmentation will be put
 * \param max_level the maximum level reached by the water
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Basins(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid) {
    
    /* Verification over depth and size */
    if (!MB_CHECK_SIZE_2(src, marker)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Only grey scale or 32-bit images can be segmented */
    /* the marker image is 32-bit */
    switch (MB_PROBE_PAIR(src, marker)) {
    case MB_PAIR_8_32:
        return MB_Basins8(src, marker, max_level, grid);
        break;
    case MB_PAIR_32_32:
        return MB_Basins32(src, marker, max_level, grid);
        break;
    default:
        break;
    }
    
    return MB_ERR_BAD_DEPTH;
}
