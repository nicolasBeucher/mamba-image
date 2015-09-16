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

extern MB_errcode MB3D_Labelb(MB3D_Image *src, MB3D_Image *dest,
                              Uint32 lblow, Uint32 lbhigh,
                              Uint32 *pNbobj,
                              enum MB3D_grid_t grid);
extern MB_errcode MB3D_Label8(MB3D_Image *src, MB3D_Image *dest,
                              Uint32 lblow, Uint32 lbhigh,
                              Uint32 *pNbobj,
                              enum MB3D_grid_t grid);
extern MB_errcode MB3D_Label32(MB3D_Image *src, MB3D_Image *dest,
                               Uint32 lblow, Uint32 lbhigh,
                               Uint32 *pNbobj,
                               enum MB3D_grid_t grid);

/* Table giving the offset for the previous neighbor in cube grid (x, y and z) */ 
const int cubePreDir[13][3] = {
    {0,-1,0},{1,-1,0},{-1,0,0},{-1,-1,0},
    {0,0,-1},{0,-1,-1},{1,-1,-1},{1,0,-1},{1,1,-1},{0,1,-1},{-1,1,-1},{-1,0,-1},{-1,-1,-1},
};

/* Table giving the offset for the neighbor in face-centered cubic grid (x, y and z) */
/* the direction depends on the coordinates of the line y and planes z*/
const int fccPreDir[6][6][3] = {
    /*1        5        6         7        8         9        */
    {{0,-1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{-1,0,-1},{-1,-1,-1}},
    {{1,-1,0},{-1,0,0},{0,-1,0}, {0,0,-1},{-1,0,-1},{0,-1,-1}},
    
    {{0,-1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{0,1,-1}, {-1,1,-1}},
    {{1,-1,0},{-1,0,0},{0,-1,0}, {0,0,-1},{1,1,-1}, {0,1,-1}},
    
    {{0,-1,0},{-1,0,0},{-1,-1,0},{0,0,-1},{0,-1,-1},{1,0,-1}},
    {{1,-1,0},{-1,0,0},{0,-1,0}, {0,0,-1},{1,-1,-1},{1,0,-1}}
};

/*
 * Tidies the label.
 * \param dest the label 3D image to tidy.
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param labels the labels arrays and context
 */
void MB3D_TidyLabel(MB3D_Image *dest,
                    PIX32 lblow, PIX32 lbhigh,
                    MB_Label_struct *labels)
{
    Uint32 x,y,z;
    MB_Image *im;
    PIX32 *pout;
    
    for(z=0; z<dest->length; z++) {
        im = dest->seq[z];
        for(y=0; y<im->height; y++) {
            pout = (PIX32 *) (im->plines[y]);
            for(x=0; x<im->width; x++, pout++) {
                if (*pout!=0) {
                    *pout = MB_find_correct_label(labels, *pout, lblow, lbhigh);
                }
            }
        }
    }
}

/*
 * Labeling the object found in src 3D image.
 *
 * \param src the source 3D image where the object must be labelled
 * \param dest the 32-bit 3D image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object founds
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Label(MB3D_Image *src, MB3D_Image *dest,
                      Uint32 lblow, Uint32 lbhigh,
                      Uint32 *pNbobj,
                      enum MB3D_grid_t grid)
{
    /* Verification over image size compatibility */
    if (!MB3D_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Verification over parameter given in entry*/
    if (lblow>=lbhigh) return MB_ERR_BAD_VALUE;
    if (lbhigh>256) return MB_ERR_BAD_VALUE;
    /* Invalid grid case */
    if (grid==MB3D_INVALID_GRID)
        return MB_ERR_BAD_PARAMETER;
    
    /* The output is necessarly a 32-bit image */
    if ((dest->seq[0]->depth)!=32) return MB_ERR_BAD_DEPTH;
    
    /* Calling the appropriate function */
    switch (src->seq[0]->depth) {
    case 1:
        return MB3D_Labelb(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    case 8:
        return MB3D_Label8(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    case 32:
        return MB3D_Label32(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    default:
        break;
    }

    return MB_ERR_BAD_DEPTH;
}

