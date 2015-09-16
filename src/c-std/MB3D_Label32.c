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

/****************************************/
/* Base functions                       */
/****************************************/
/* The functions described here realise the basic operations */
/* needed to label pixels */

/* This function gives the value of the pixel inside the image */
/* with its position */
static PIX32 GET_VAL(MB3D_Image *im, int x, int y, int z)
{
    PIX32 *p, value;
    
    if( (z >= (int)(im->length)) || 
        (z <  0) ||
        (y >= (int)(im->seq[0]->height)) ||
        (y <  0) ||
        (x >= (int)(im->seq[0]->width)) ||
        (x <  0) ) {
        value = 0;
    } else {
        p = (PIX32 *) (im->seq[z]->plines[y] + x*4);
        value = *p;
    }

    return value;
}

/* This function verifies if the neighbor pixel is of the same value */
/* as the current pixel */
static int IS_SAME_VALUE(MB3D_Image *im,
                         int x, int y, int z,
                         int nx, int ny, int nz)
{
    int value;
    PIX32 *p, v, nv;
    
    if( (nz >= (int)(im->length)) || 
        (nz <  0) ||
        (ny >= (int)(im->seq[0]->height)) ||
        (ny <  0) ||
        (nx >= (int)(im->seq[0]->width)) ||
        (nx <  0) ) {
        value = 0;
    } else {
        p = (PIX32 *) (im->seq[z]->plines[y] + x*4);
        v = *p;
        p = (PIX32 *) (im->seq[nz]->plines[ny] + nx*4);
        nv = *p;
        value = (v==nv);
    }
    
    return value;
}

/* Function returning the corrected label for a pixel at a given position */
/* in cubic grid */
static PIX32 GET_CUBIC_LABEL(MB3D_Image *dest, MB3D_Image *src, MB_Label_struct *labels, int x, int y, int z)
{
    PIX32 value, label, rlab;
    int i;
    int nx, ny, nz;
    
    label = 0;
    for(i=0; i<13; i++) {
        nx = x+cubePreDir[i][0];
        ny = y+cubePreDir[i][1];
        nz = z+cubePreDir[i][2];
        if (IS_SAME_VALUE(src, x, y, z, nx, ny, nz)) {
            value = GET_VAL(dest, nx, ny, nz);
            rlab = MB_find_above_label(labels, value);
            if (rlab!=0) {
                /* When the neighbor pixel has a label we take it */
                if (label==0) {
                    /* No label yet for the position x,y,z */
                    label = rlab;
                } else {
                    /* Our pixel already has a label */
                    /* we must then put a correspondance between those two */
                    labels->EQ[rlab] = label;
                }
            }
        }
    }
    
    if (label==0) {
        /* No neighbors labelled we take one */
        label = (labels->current);
        labels->EQ[label] = label;
        labels->current++;
    }
    
    return label;
}

/* Function returning the corrected label for a pixel at a given position */
/* in cubic grid */
static PIX32 GET_FCC_LABEL(MB3D_Image *dest, MB3D_Image *src, MB_Label_struct *labels, int x, int y, int z)
{
    PIX32 value, label, rlab;
    int i,dirSelect;
    int nx, ny, nz;
    
    /* Computing the directions to use depending on the y and z of the */
    /* pixel */
    dirSelect = ((z%3)<<1)+(y%2);
    
    label = 0;
    for(i=0; i<6; i++) {
        nx = x+fccPreDir[dirSelect][i][0];
        ny = y+fccPreDir[dirSelect][i][1];
        nz = z+fccPreDir[dirSelect][i][2];
        if (IS_SAME_VALUE(src, x, y, z, nx, ny, nz)) {
            value = GET_VAL(dest, nx, ny, nz);
            rlab = MB_find_above_label(labels, value);
            if (rlab!=0) {
                /* When the neighbor pixel has a label we take it */
                if (label==0) {
                    /* No label yet for the position x,y,z */
                    label = rlab;
                } else {
                    /* Our pixel already has a label */
                    /* we must then put a correspondance between those two */
                    labels->EQ[rlab] = label;
                }
            }
        }
    }
    
    if (label==0) {
        /* No neighbors labelled we take one */
        label = (labels->current);
        labels->EQ[label] = label;
        labels->current++;
    }
    
    return label;
}

/****************************************
 * Grid functions                       *
 ****************************************
 * The functions described here perform labeling depending on the grid
 */

/* CUBIC */

/*
 * Labelizes the object found in src image over a cubic grid.
 * \param dest the 32-bit 3D image where object are labelled
 * \param src the binary source 3D image where the object must be labelled
 * \param labels the labels arrays and context
 */
static void MB3D_cubeLabel32(MB3D_Image *dest, MB3D_Image *src, MB_Label_struct *labels)
{
    Uint32 x,y,z;
    MB_Image *imSrc, *imDest;
    PIX32 *pout, *pin;
    
    for(z=0; z<dest->length; z++) {
        imDest = dest->seq[z];
        imSrc = src->seq[z];
        for(y=0; y<(int) (imDest->height); y++) {
            pout = (PIX32 *) (imDest->plines[y]);
            pin = (PIX32 *) (imSrc->plines[y]);
            for(x=0; x<(int) (imDest->width); x++, pin++, pout++) {
                if (*pin>0) {
                    /* If the pixel in the src binary register is not */
                    /* empty then we label it in the dest image */
                    *pout = GET_CUBIC_LABEL(dest,src,labels,x,y,z);
                }
            }
        }
    }
}

/* FACE CENTERED CUBIC */

/*
 * Labelizes the object found in src image over a face centered cubic grid.
 * \param dest the 32-bit 3D image where object are labelled
 * \param src the binary source 3D image where the object must be labelled
 * \param labels the labels arrays and context
 */
static void MB3D_fccLabel32(MB3D_Image *dest, MB3D_Image *src, MB_Label_struct *labels)
{
    Uint32 x,y,z;
    MB_Image *imSrc, *imDest;
    PIX32 *pout, *pin;
    
    for(z=0; z<dest->length; z++) {
        imDest = dest->seq[z];
        imSrc = src->seq[z];
        for(y=0; y<(int) (imDest->height); y++) {
            pout = (PIX32 *) (imDest->plines[y]);
            pin = (PIX32 *) (imSrc->plines[y]);
            for(x=0; x<(int) (imDest->width); x++, pin++, pout++) {
                if (*pin>0) {
                    /* If the pixel in the src binary register is not */
                    /* empty then we label it in the dest image */
                    *pout = GET_FCC_LABEL(dest,src,labels,x,y,z);
                }
            }
        }
    }
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Labeling the object found in src 3D image.
 *
 * \param src the 32-bit source 3D image where the object must be labelled
 * \param dest the 32-bit 3D image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object founds
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Label32(MB3D_Image *src, MB3D_Image *dest,
                         Uint32 lblow, Uint32 lbhigh,
                         Uint32 *pNbobj,
                         enum MB3D_grid_t grid)
{
    MB_Label_struct labels;
    Uint32 z;
    
    /* Initializing the algorithm parameters */
    labels.current = 1;
    labels.ccurrent = 1;
    labels.nbObjs = 0;
    labels.maxEQ = (src->seq[0]->width * src->seq[0]->height * src->length);
    labels.EQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    labels.CEQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if (labels.EQ==NULL) {
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    labels.CEQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if (labels.CEQ==NULL){
        /* In case allocation goes wrong */
        MB_free(labels.EQ);
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    MB_memset(labels.EQ, 0, labels.maxEQ*sizeof(PIX32));
    MB_memset(labels.CEQ, 0, labels.maxEQ*sizeof(PIX32));
    
    /* The label image is reset */
    for(z=0; z<dest->length; z++) {
        MB_ConSet(dest->seq[z], 0);
    }
    
    /* Calling the corresponding function */
    switch(grid) {
        case MB3D_CUBIC_GRID:
            MB3D_cubeLabel32(dest, src, &labels);
            break;
        case MB3D_FCC_GRID:
            MB3D_fccLabel32(dest, src, &labels);
            break;
        default:
            MB_free(labels.EQ);
            MB_free(labels.CEQ);
            return MB_ERR_BAD_PARAMETER;
            break;
    }
    MB3D_TidyLabel(dest, (PIX32) lblow, (PIX32) lbhigh, &labels);
    
    *pNbobj = (Uint32) (labels.nbObjs);
    
    /* Freeing the labels arrays */
    MB_free(labels.EQ);
    MB_free(labels.CEQ);

    return MB_NO_ERR;
}

