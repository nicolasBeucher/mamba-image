/*
 * Copyright (c) <2014>, <Nicolas BEUCHER>
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

/*
 * Creates a 3D image container. 3D images are just a list of 2D images
 * stacked together.
 * \param image the created image
 * \param length the length of the 3D image (number of images stacked)
 * \return an error code (MB_NO_ERR if everything went OK).
 */
MB_errcode MB3D_Create(MB3D_Image *image, Uint32 length)
{
    image->length = length;
    image->seq = (MB_Image **) MB_malloc(length*sizeof(MB_Image *));
    if (image->seq==NULL) {
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    
    return MB_NO_ERR;
}

/*
 * Stack the 2D image at the given position.
 * \param image the 3D image
 * \param stacked the 2D image stacked in the 3D image
 * \param position the position in the 3D image of the 2D image
 * \return an error code (MB_NO_ERR if everything went OK).
 */
MB_errcode MB3D_Stack(MB3D_Image *image, MB_Image *stacked, Uint32 position)
{
    
    if (position>=image->length)
    {
        return MB_ERR_BAD_SIZE;
    }
    image->seq[position] = stacked;
    
    return MB_NO_ERR;
}

/*
 * Destroys the 3D image (free memory).
 * \param image the image to destroy
 * \return an error code.
 */
MB_errcode MB3D_Destroy(MB3D_Image *image)
{
    if (image==NULL) return MB_NO_ERR;
    
    MB_free(image->seq);
    return MB_NO_ERR;
}
