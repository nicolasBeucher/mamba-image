/** \file MB_Image.h */
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

#ifndef __MB_Image_H
#define __MB_Image_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Creates an image (memory allocation) with the correct size and depth given as
 * argument. The size is deduced from the requested size given in argument. 
 * The size must be a multiple of MB_ROUND_W for width and MB_ROUND_H for height.
 * The size cannot be greater than MB_MAX_IMAGE_SIZE.
 * \param image the created image
 * \param width the width of the created image 
 * \param height the height of the created image 
 * \param depth the depth of the created image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Create(MB_Image *image, Uint32 width, Uint32 height, Uint32 depth);
/**
 * Destroys an image (memory freeing).
 * \param image the image to be destroyed
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Destroy(MB_Image *image);
/**
 * \return the number of image that have been allocated so far
 */
extern MB_API_ENTRY Uint32 MB_API_CALL
MB_getImageCounter(void);
/**
 * Loads an image data with data given in argument.
 * \param image the image to fill
 * \param indata the data to fill the image with (complete pixels values)
 * \param len the length of data given
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Load(MB_Image *image, PIX8 *indata, Uint32 len);
/**
 * Reads an image data contents and put it in an array.
 * \param image the image to read
 * \param outdata pointer to the array created (malloc) and filled with the 
 * pixel data of the image
 * \param len the length in bytes of data extracted (0 if an error occured)
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Extract(MB_Image *image, PIX8 **outdata, Uint32 *len);
/**
 * Converts an image of a given depth into another depth.
 * All possible conversions are supported.
 * \param src source image
 * \param dest destination image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Convert(MB_Image *src, MB_Image *dest);
/**
 * Copies an image data contents into another image.
 * This copy works with same size images.
 * \param src the source image
 * \param dest the destination image
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_Copy(MB_Image *src, MB_Image *dest);
/**
 * Copies an image line contents into another image line.
 * \param src the source image
 * \param dest the destination image
 * \param insrc_pos the position of the line copied from src
 * \param indest_pos the position in dest in which the line is copied
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_CopyLine(MB_Image *src, MB_Image *dest, Uint32 insrc_pos, Uint32 indest_pos);
/**
 * Copies an image data contents into another image.
 * This copy can work with image of different sizes. As the size can be different
 * the position where the copy occurs must be specified for both images as well
 * as the size of the copy. 
 * The function will compute the actual crop inside the source and destination 
 * images. 
 * Works only with non binary images.
 * \param src the source image
 * \param x_src the x position in the source image where the copy should begin
 * \param y_src the y position in the source image where the copy should begin
 * \param dest the destination image
 * \param x_dest the x position in the destination image where the copy should happen
 * \param y_dest the y position in the destination image where the copy should happen
 * \param w the width of the copy
 * \param h the height of the copy
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_CropCopy(MB_Image *src, Uint32 x_src, Uint32 y_src,
                                        MB_Image *dest, Uint32 x_dest, Uint32 y_dest,
                       Uint32 w, Uint32 h);
/**
 * Puts the pixel value inside the image at the given position.
 * \param dest the image 
 * \param pixVal the pixel value
 * \param x position in x of the pixel targeted
 * \param y position in y of the pixel targeted
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_PutPixel(MB_Image *dest, Uint32 pixVal, Uint32 x, Uint32 y);
/**
 * Gets the pixel value inside the image at the given position.
 * \param src the image 
 * \param pixVal the returned pixel value
 * \param x position in x of the pixel targeted
 * \param y position in y of the pixel targeted
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB_GetPixel(MB_Image *src, Uint32 *pixVal, Uint32 x, Uint32 y);

/**
 * Creates a 3D image container. 3D images are just a list of 2D images
 * stacked together.
 * \param image the created image
 * \param length the length of the 3D image (number of images stacked)
 * \return an error code (NO_ERR if everything went OK).
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB3D_Create(MB3D_Image *image, Uint32 length);
/**
 * Stack the 2D image at the given position.
 * \param image the 3D image
 * \param stacked the 2D image stacked in the 3D image
 * \param position the position in the 3D image of the 2D image
 * \return an error code (NO_ERR if everything went OK).
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB3D_Stack(MB3D_Image *image, MB_Image *stacked, Uint32 position);
/**
 * Destroys the 3D image (free memory).
 * \param image the image to destroy
 * \return an error code.
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB3D_Destroy(MB3D_Image *image);
/**
 * Converts a 3D image of a given depth into another depth.
 * Supported conversions are: 1->8, 8->1 and 32->8 (downscaling).
 * \param src 3D source image
 * \param dest 3D destination image 
 * \return An error code (NO_ERR if successful)
 */
extern MB_API_ENTRY MB_errcode MB_API_CALL
MB3D_Convert(MB3D_Image *src, MB3D_Image *dest);

#ifdef __cplusplus
}
#endif

#endif /* __MB_Image_H */

