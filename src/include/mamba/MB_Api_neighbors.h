/** \file MB_Api_neighbors.h */
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

#ifndef __MB_Api_neighbors_H
#define __MB_Api_neighbors_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Looks for the minimum between two image pixels (a central pixel
 * and its neighbors in the other image)
 * The neighbor depends on the grid used. Neighbors are
 * described using a pattern. If no neighbor
 * is defined, the function will leave silently doing nothing.
 *
 *\see MB_Neighbors_code_t for encoding neighbors patterns.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param neighbors the neighbors to take into account
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_InfNb(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * Looks for the minimum between two image pixels (a central pixel and its 
 * far neighbor in the other image)
 * The neighbor depends on the grid used.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param nbrnum the neighbor index
 * \param count the amplitude of the shift (in pixels)
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_InfFarNb(MB_Image *src, MB_Image *srcdest, Uint32 nbrnum, Uint32 count, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * Looks for the maximum between two image pixels (a central pixel
 * and its neighbors in the other image)
 * The neighbor depends on the grid used. Neighbors are
 * described using a pattern. If no neighbor
 * is defined, the function will leave silently doing nothing.
 *
 *\see MB_Neighbors_code_t for encoding neighbors patterns.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param neighbors the neighbors to take into account
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_SupNb(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * Looks for the maximum between two image pixels (a central pixel and its 
 * far neighbor in the other image)
 * The neighbor depends on the grid used.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param nbrnum the neighbor index
 * \param count the amplitude of the shift (in pixels)
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_SupFarNb(MB_Image *src, MB_Image *srcdest, Uint32 nbrnum, Uint32 count, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * Computes the set difference between two image pixels
 * (a central pixel and its neighbors in the other image)
 * The neighbor depends on the grid used. Neighbors are
 * described using a pattern. If no neighbor
 * is defined, the function will leave silently doing nothing.
 *
 *\see MB_Neighbors_code_t for encoding neighbors patterns.
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param neighbors the neighbors to take into account
 * \param grid the grid used (either square or hexagonal)
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_DiffNb(MB_Image *src, MB_Image *srcdest, Uint32 neighbors, enum MB_grid_t grid, enum MB_edgemode_t edge);
/**
 * (re)Builds an image according to a direction and a mask image.
 * The direction depends on the grid used.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param dirnum the direction number
 * \param pVolume the computed volume of the output image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_BldNb(MB_Image *mask, MB_Image *srcdest, Uint32 dirnum, Uint64 *pVolume, enum MB_grid_t grid);
/**
 * (re)Builds (dual operation) an image according to a direction and a mask image.
 * The direction depends on the grid used.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param dirnum the direction number
 * \param pVolume the computed volume of the output image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_DualBldNb(MB_Image *mask, MB_Image *srcdest, Uint32 dirnum, Uint64 *pVolume, enum MB_grid_t grid);
/**
 * Shifts the contents of an image in a given direction with a given amplitude
 * The direction depends on the grid used.
 *
 * \param src source image
 * \param dest destination image
 * \param dirnum the direction index
 * \param count the amplitude of the shift
 * \param long_filler_pix the value used to fill the created space
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Shift(MB_Image *src, MB_Image *dest, Uint32 dirnum, Uint32 count, Uint32 long_filler_pix, enum MB_grid_t grid);
/**
 * Shifts the contents of an image by a given vector.
 *
 * \param src source image
 * \param dest destination image
 * \param dx the vector amplitude in x
 * \param dy the vector amplitude in y
 * \param long_filler_pix the value used to fill the created space
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_ShiftVector(MB_Image *src, MB_Image *dest, Sint32 dx, Sint32 dy, Uint32 long_filler_pix);
/**
 * Looks for the minimum between two image pixels (a central pixel
 * and its neighbor in the other image previously shifted by the given vector)
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param dx the vector amplitude in x
 * \param dy the vector amplitude in y
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_InfVector(MB_Image *src, MB_Image *srcdest, Sint32 dx, Sint32 dy, enum MB_edgemode_t edge);
/**
 * Looks for the maximum between two images pixels (a central pixel
 * and its neighbor in the other image previously shifted by the given vector)
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param dx the vector amplitude in x
 * \param dy the vector amplitude in y
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 *
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_SupVector(MB_Image *src, MB_Image *srcdest, Sint32 dx, Sint32 dy, enum MB_edgemode_t edge);
/**
 * Performs a binary Hit-or-Miss operation on src image using the structuring
 * elements es0 and es1. Structuring elements are integer values coding which
 * direction must be taken into account.
 * es0 indicates which neighbor of the current pixel will be checked for 0 value.
 * es1 those which will be evaluated for 1 value.
 *
 * For example, in hexagonal grid, it means that if you want to look for a
 * pattern where the neighbors in direction 6 and 1 are true while the current
 * pixel is false just as neighbors 2 and 5, you will encode this in the
 * elements es0 and es1 like this :
 *
 *      es0 = 1+4+32
 *
 *      es1 = 64+2
 *
 *\see MB_Neighbors_code_t for encoded structuring elements.
 *
 * \param src output image
 * \param dest input image (must be different of src)
 * \param es0 structuring element for 0 value.
 * \param es1 structuring element for 1 value.
 * \param grid grid configuration
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_BinHitOrMiss(MB_Image *src, MB_Image *dest, Uint32 es0, Uint32 es1, enum MB_grid_t grid, enum MB_edgemode_t edge);

#ifdef __cplusplus
}
#endif

#endif /* __MB_Api_neighbors_H */

