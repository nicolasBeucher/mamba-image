/** \file MB_Api_hierarchical.h */
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

#ifndef __MB_Api_hierarchical_H
#define __MB_Api_hierarchical_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * (re)Builds an image according to a mask image and using a hierarchical list
 * to compute the rebuild.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_HierarBld(MB_Image *mask, MB_Image *srcdest, enum MB_grid_t grid);
/**
 * (re)Builds (dual operation) an image according to a mask image and using a 
 * hierarchical list to compute the rebuild.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_HierarDualBld(MB_Image *mask, MB_Image *srcdest, enum MB_grid_t grid);
/**
 * Performs a watershed segmentation of the image using the marker image
 * as a starting point for the flooding. The function builds the actual 
 * watershed line (idempotent) plus catchment basins (not idempotent). 
 *
 * The result is put into the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32-bit values.
 *
 * | 0     | 1     | 2     | 3      |
 * |-------|-------|-------|--------|
 * |  <--- | label | --->  | isLine |
 *
 * isLine is a value indicating if the pixel belongs to the watershed
 * (255 if this is the case, undefined otherwise).
 *
 * \see MB_CopyBytePlane to access each byte individually.
 *
 * \param src the greyscale or 32-bit image to segment
 * \param marker the marker image in which the result of segmentation will be put
 * \param max_level the maximum level reach by the water
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Watershed(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid);
/**
 * Performs a watershed segmentation of the image using the marker image
 * as a starting point for the flooding. The function returns the catchment 
 * basins of the watershed but no actual watershed line. It is recommended
 * to use this functions rather than MB_Watershed if you are only interested
 * in catchment basins (faster).
 *
 * The result is put into a the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32-bit values.
 *
 * | 0     | 1     | 2     | 3      |
 * |-------|-------|-------|--------|
 * |  <--- | label | --->  | unused |
 *
 * \see MB_CopyBytePlane to access each byte individually.
 *
 * \param src the greyscale or 32-bit image to be segmented
 * \param marker the marker image in which the result of segmentation will be put
 * \param max_level the maximum level reached by the water
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Basins(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid);

#ifdef __cplusplus
}
#endif

#endif /* __MB_Api_H */

