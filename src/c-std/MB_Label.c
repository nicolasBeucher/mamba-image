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

extern MB_errcode MB_Labelb(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid);
extern MB_errcode MB_Label8(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid);
extern MB_errcode MB_Label32(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid);

/* Function returning the corrected label to use.*/
/* The corrected label have values that follow each other */
/* along a specific rule to allow lblow and lbhml values */
/* to exclude some value in the first byte. */
PIX32 MB_find_correct_label(MB_Label_struct *labels, PIX32 inlabel, PIX32 lblow, PIX32 lbhigh)
{
    PIX32 lbvalue;
    inlabel = MB_find_above_label(labels, inlabel);

    if (labels->CEQ[inlabel]==0) {
        lbvalue = labels->ccurrent & 0xff;
        if (lbvalue<lblow) {
            labels->ccurrent += (lblow-lbvalue);
        } else if (lbvalue>=lbhigh) {
            labels->ccurrent += (0x100+lblow-lbvalue);
        }
        labels->CEQ[inlabel] = labels->ccurrent;
        labels->ccurrent++;
        labels->nbObjs++;
    }
    
    return labels->CEQ[inlabel];
}

/* Recursive function to find the root label*/
PIX32 MB_find_above_label(MB_Label_struct *labels, PIX32 inlabel)
{
    if (labels->EQ[inlabel]==inlabel) {
        return inlabel;
    } else {
        labels->EQ[inlabel] = MB_find_above_label(labels, labels->EQ[inlabel]);
        return labels->EQ[inlabel];
    }
}

/****************************************
 * Tidying function                     *
 ****************************************
 * The functions tidy the label.
 */

/*
 * Tidies the label.
 * \param plines_out pointer on the destination image lines
 * \param bytes number of bytes inside the line
 * \param nb_lines number of lines inside the image processed
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param labels the labels arrays and context
 */
void MB_TidyLabel(PLINE *plines_out,
                  Uint32 bytes, Uint32 nb_lines,
                  PIX32 lblow, PIX32 lbhigh,
                  MB_Label_struct *labels)
{
    Uint32 u,v;
    PIX32 *p1;
    
    for(u=0; u<nb_lines; u++, plines_out++) {
        p1 = (PIX32 *) (*plines_out);
        for(v=0; v<bytes; v+=4, p1++) {
            if (*p1!=0) {
                *p1 = MB_find_correct_label(labels, *p1, lblow, lbhigh);
            }
        }            
    }
}

/*
 * Labeling the object found in src image.
 *
 * \param src the source image where the object must be labelled
 * \param dest the 32-bit image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object founds
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Label(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid)
{
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Verification over parameter given in entry*/
    if (lblow>=lbhigh) return MB_ERR_BAD_VALUE;
    if (lbhigh>256) return MB_ERR_BAD_VALUE;
    
    /* The output is necessarly a 32-bit image */
    if (dest->depth!=32) return MB_ERR_BAD_DEPTH;
    
    /* Calling the appropriate function */
    switch (src->depth) {
    case 1:
        return MB_Labelb(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    case 8:
        return MB_Label8(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    case 32:
        return MB_Label32(src, dest, lblow, lbhigh, pNbobj, grid);
        break;
    default:
        break;
    }

    return MB_ERR_BAD_DEPTH;
}

