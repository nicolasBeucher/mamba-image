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

extern MB_errcode MB3D_Watershed8(MB3D_Image *src, MB3D_Image *marker, Uint32 max_level, enum MB3D_grid_t grid);
extern MB_errcode MB3D_Watershed32(MB3D_Image *src, MB3D_Image *marker, Uint32 max_level, enum MB3D_grid_t grid);

/* Table giving the offset for the neighbor in cube grid (x, y and z) */ 
const int cubeNbDir[27][3] = {
    {0,0,0},{0,-1,0},{1,-1,0},{1,0,0},{1,1,0},{0,1,0},{-1,1,0},{-1,0,0},{-1,-1,0},
    {0,0,-1},{0,-1,-1},{1,-1,-1},{1,0,-1},{1,1,-1},{0,1,-1},{-1,1,-1},{-1,0,-1},{-1,-1,-1},
    {0,0,1},{0,-1,1},{1,-1,1},{1,0,1},{1,1,1},{0,1,1},{-1,1,1},{-1,0,1},{-1,-1,1}
};

/* Table giving the offset for the neighbor in face-centered cubic grid (x, y and z) */
/* the direction depends on the coordinates of the line y and planes z*/
const int fccNbDir[6][13][3] = {
    /*0       1        2       3       4        5        6         7        8         9          10      11       12      */
    {{0,0,0},{0,-1,0},{1,0,0},{0,1,0},{-1,1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{-1,0,-1},{-1,-1,-1},{0,0,1},{0,-1,1},{-1,-1,1}},
    {{0,0,0},{1,-1,0},{1,0,0},{1,1,0},{0,1,0}, {-1,0,0},{0,-1,0}, {0,0,-1},{-1,0,-1},{0,-1,-1}, {0,0,1},{1,-1,1},{0,-1,1}},
    
    {{0,0,0},{0,-1,0},{1,0,0},{0,1,0},{-1,1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{0,1,-1}, {-1,1,-1}, {0,0,1},{-1,1,1},{-1,0,1}},
    {{0,0,0},{1,-1,0},{1,0,0},{1,1,0},{0,1,0}, {-1,0,0},{0,-1,0}, {0,0,-1},{1,1,-1}, {0,1,-1},  {0,0,1},{0,1,1}, {-1,0,1}},
    
    {{0,0,0},{0,-1,0},{1,0,0},{0,1,0},{-1,1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{0,-1,-1},{1,0,-1},  {0,0,1},{1,0,1}, {0,1,1}},
    {{0,0,0},{1,-1,0},{1,0,0},{1,1,0},{0,1,0}, {-1,0,0},{0,-1,0}, {0,0,-1},{1,-1,-1},{1,0,-1},  {0,0,1},{1,0,1}, {1,1,1}}
};

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Performs a watershed segmentation of the 3D image using the marker image
 * as a starting point for the flooding. The function builds the actual 
 * watershed line (idempotent) plus catchment basins (not idempotent). 
 * The result is put into the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32-bits values.
 * | 0      | 1      | 2      | 3      |
 * |--------|--------|--------|--------|
 * | Segment label            | isLine |
 * Each byte can be accessed using the function MB_CopyBytePlane. isLine is a value
 * indicating if the pixel belongs to the watershed (255 if this is the case, 
 * undefined otherwise).
 *
 * \param src the greyscale 3D image to segment
 * \param marker the marker 3D image in which the result of segmentation will be put
 * \param max_level the maximum level reach by the water.
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Watershed(MB3D_Image *src, MB3D_Image *marker, Uint32 max_level, enum MB3D_grid_t grid) {

    /* Verification over depth and size */
    if (!MB3D_CHECK_SIZE_2(src, marker)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Invalid grid case */
    if (grid==MB3D_INVALID_GRID)
        return MB_ERR_BAD_PARAMETER;
    
    /* Only grey scale or 32-bit images can be segmented */
    /* the marker image is 32-bit */
    switch (MB3D_PROBE_PAIR(src, marker)) {
    case MB_PAIR_8_32:
        return MB3D_Watershed8(src,marker,max_level,grid);
        break;
    case MB_PAIR_32_32:
        return MB3D_Watershed32(src,marker,max_level,grid);
        break;
    default:
        break;
    }
    
    return MB_ERR_BAD_DEPTH;
}
