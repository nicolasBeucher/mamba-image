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
#include "mambaApi_vector.h"

/****************************************/
/* Base functions                       */
/****************************************/
/* The functions described here realise the basic operations */
/* needed to label pixels. */

/*
 * labeling the upper line (near the image edge).
 *
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param labels the labels arrays and context
 */
static INLINE void EDGE_LINE(PLINE plines_out, PLINE plines_in, Uint32 bytes_in, MB_Label_struct *labels)
{
    Uint32 i;
    PIX8 pix, previous_pix;

    PLINE pin = (PLINE) (plines_in);
    PIX32 *pout = (PIX32 *) (plines_out);
    
    /* Previous values initialisation */
    previous_pix = 0;
    
    for(i=0;i<bytes_in;i++,pin++,pout++) {
        /* Reading a register of pixels */
        pix = (*pin);
        if (pix>0) {
            if (pix==previous_pix) {
                /* With the same label as its neighbor since the */
                /* neighbor is set (and thus already labelled) */
                /* (only one neighbor since the other are in the */
                /* edge) */
                VAL(pout) = LEFT(pout);
            } else {
                /* or with a new label value */
                VAL(pout) = (labels->current);
                /* which mark the label as being used */
                labels->EQ[labels->current] = labels->current;
                labels->current++;
            }
        }
        previous_pix = pix;
    }
}

/*
 * labeling the odd lines for hexagonal grid.
 * 
 * \param plines_out pointer on the current line in the destination image
 * \param plines_in pointer on the current line in the source image
 * \param index line being processed
 * \param bytes_in number of bytes inside the line
 * \param labels the labels arrays and context
 */
static INLINE void HLAB_LINE_ODD(PLINE *plines_out, PLINE *plines_in, Uint32 index,
                                 Uint32 bytes_in, MB_Label_struct *labels)
{
    Uint32 i;
    PIX8 pix, prev_pix, pix_up, next_pix_up;
    Uint32 neighbor_state;

    PLINE pin = (PLINE) (plines_in[index]);
    PLINE pinpre = (PLINE) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    prev_pix = 0;
    pix_up = (*pinpre);
    pinpre++;
    next_pix_up = (*pinpre);
    for(i=0;i<bytes_in;i++,pin++,pout++,poutpre++) {
        /* Reading a register of pixels in the two sources lines*/
        pix = (*pin);
        if (pix>0) {
            neighbor_state = (pix==prev_pix) |
                             ((pix==pix_up)<<1) |
                             ((pix==next_pix_up)<<2);
            /* The neighbor state gives the values of the neighbors of the currently */
            /* evaluated pixel. It allows to determine which value will take the label */
            /* in the output image (pout).*/
            /* We always take the label of the last labelled neighbor */
            /* in case more than one neighbor is labelled, the equivalence */
            /* table is updated */
            switch(neighbor_state) {
            case 1:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                break;
            case 2:
                VAL(pout) = MB_find_above_label(labels, VAL(poutpre));
                break;
            case 3:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (VAL(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, VAL(poutpre));
                break;
            case 4:
            case 6:
                VAL(pout) = MB_find_above_label(labels, RIGHT(poutpre));
                break;
            case 5:
            case 7:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (RIGHT(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, RIGHT(poutpre));
                break;
            default: /* Case 0 */
                VAL(pout) = (labels->current);
                /* No neighbors labelled we take one */
                labels->EQ[labels->current] = labels->current;
                labels->current++;
                break;
            }
        }
        /* Next pixel */
        prev_pix = pix;
        pix_up = next_pix_up;
        pinpre++;
        if (i < bytes_in-2) {
            next_pix_up = (*pinpre);
        } else {
            next_pix_up = 0;
        }
    }
}

/*
 * Labeling the even lines for hexagonal grid.
 * 
 * \param plines_out pointer on the current line in the destination image
 * \param plines_in pointer on the current line in the source image
 * \param index line being processed
 * \param bytes_in number of bytes inside the line
 * \param labels the labels arrays and context
 */
static INLINE void HLAB_LINE_EVEN(PLINE *plines_out, PLINE *plines_in, Uint32 index,
                                  Uint32 bytes_in, MB_Label_struct *labels)
{
    Uint32 i;
    PIX8 pix, prev_pix, pix_up, prev_pix_up;
    Uint32 neighbor_state;

    PLINE pin = (PLINE) (plines_in[index]);
    PLINE pinpre = (PLINE) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    prev_pix = 0;
    prev_pix_up = 0;
    
    for(i=0;i<bytes_in;i++,pin++,pinpre++,pout++,poutpre++) {
        /* Reading a register of pixels in the two sources lines*/
        pix = (*pin);
        pix_up = (*pinpre);
        if (pix>0) {
            neighbor_state = (pix==prev_pix) |
                             ((pix==prev_pix_up)<<1) |
                             ((pix==pix_up)<<2);
            /* The neighbor state gives the values of the neighbors of the currently */
            /* evaluated pixel. It allows to determine which value will take the label */
            /* in the output image (pout).*/
            /* We always take the label of the last labelled neighbor */
            /* in case more than one neighbor is labelled, the equivalence */
            /* table is updated */
            switch(neighbor_state) {
            case 1:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                break;
            case 2:
                VAL(pout) = MB_find_above_label(labels, LEFT(poutpre));
                break;
            case 3:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (LEFT(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, LEFT(poutpre));
                break;
            case 4:
            case 6:
                VAL(pout) = MB_find_above_label(labels, VAL(poutpre));
                break;
            case 5:
            case 7:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (VAL(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, VAL(poutpre));
                break;
            default: /* case 0 */
                VAL(pout) = (labels->current);
                /* no neighbors labelled we take one */
                labels->EQ[labels->current] = labels->current;
                labels->current++;
                break;
            }
        }
        /* Next pixel */
        prev_pix = pix;
        prev_pix_up = pix_up;
    }
}

/*
 * Labeling the lines for square grid.
 * 
 * \param plines_out pointer on the lines in the destination image
 * \param plines_in pointer on the lines in the source image
 * \param index line being processed
 * \param bytes_in number of bytes inside the line
 * \param labels the labels arrays and context
 */
static INLINE void QLAB_LINE(PLINE *plines_out, PLINE *plines_in, Uint32 index,
                             Uint32 bytes_in, MB_Label_struct *labels)
{
    Uint32 i;
    PIX8 pix, prev_pix, pix_up, prev_pix_up, next_pix_up;
    Uint32 neighbor_state;

    PLINE pin = (PLINE) (plines_in[index]);
    PLINE pinpre = (PLINE) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    prev_pix = 0;
    prev_pix_up = 0;
    pix_up = (*pinpre);
    pinpre++;
    next_pix_up = (*pinpre);
    
    for(i=0;i<bytes_in;i++,pin++,pout++,poutpre++) {
        /* Reading a register of pixels in the two sources lines*/
        pix = (*pin);
        if (pix>0) {
            neighbor_state = ((pix==prev_pix)&1) |
                             ((pix==prev_pix_up)<<1) |
                             ((pix==pix_up)<<2) |
                             ((pix==next_pix_up)<<3);
            /* The neighbor state gives the values of the neighbors of the currently */
            /* evaluated pixel. It allows to determine which value will take the label */
            /* in the output image (pout).*/
            /* We always take the label of the last labelled neighbor */
            /* in case more than one neighbor is labelled, the equivalence */
            /* table is updated */
            switch(neighbor_state) {
            case 1:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                break;
            case 2:
                VAL(pout) = MB_find_above_label(labels, LEFT(poutpre));
                break;
            case 3:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (LEFT(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, LEFT(poutpre));
                break;
            case 4:
            case 6:
                VAL(pout) = MB_find_above_label(labels, VAL(poutpre));
                break;
            case 5:
            case 7:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (VAL(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, VAL(poutpre));
                break;
            case 10:
                VAL(pout) = MB_find_above_label(labels, RIGHT(poutpre));
                if (LEFT(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, LEFT(poutpre));
                break;
            case 8:
            case 12:
            case 14:
                VAL(pout) = MB_find_above_label(labels, RIGHT(poutpre));
                break;
            case 9:
            case 11:
            case 13:
            case 15:
                VAL(pout) = MB_find_above_label(labels, LEFT(pout));
                if (RIGHT(poutpre) != VAL(pout))
                    labels->EQ[VAL(pout)] = MB_find_above_label(labels, RIGHT(poutpre));
                break;
            default: /* Case 0 */
                VAL(pout) = (labels->current);
                /* No neighbors labelled we take one */
                labels->EQ[labels->current] = labels->current;
                labels->current++;
                break;
            }
        }
        /* Next pixel */
        prev_pix = pix;
        prev_pix_up = pix_up;
        pix_up = next_pix_up;
        pinpre++;
        if (i < bytes_in-2) {
            next_pix_up = (*pinpre);
        } else {
            next_pix_up = 0;
        }
    }
}

/******************************************
 * Grid functions                         *
 ******************************************/
#include "MB_Label_neighbors.h"

/*
 * Labeling the object found in src image.
 *
 * \param src the greyscale source image where the object must be labelled
 * \param dest the 32-bit image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object founds
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Label8(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid)
{
    Uint32 bytes_in, bytes_out;
    PLINE *plines_in, *plines_out;
    MB_Label_struct labels;
    LABELGRIDFUNC *fn;
    
    /* Initializing the algorithm parameters */
    labels.current = 1;
    labels.ccurrent = 1;
    labels.nbObjs = 0;
    labels.maxEQ = (src->width*src->height);
    labels.EQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if(labels.EQ==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    labels.CEQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if(labels.CEQ==NULL){
        /* in case allocation goes wrong */
        MB_free(labels.EQ);
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    MB_memset(labels.EQ, 0, labels.maxEQ*sizeof(PIX32));
    MB_memset(labels.CEQ, 0, labels.maxEQ*sizeof(PIX32));
    
    /* The label image is reset */
    MB_ConSet(dest, 0);
    
    /* Setting up pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);
    bytes_out = MB_LINE_COUNT(dest);
    
    /* Calling the corresponding function */
    fn = SwitchTo[grid];
    fn(plines_out, plines_in, bytes_in, src->height, &labels);

    MB_TidyLabel(plines_out, bytes_out, src->height, (PIX32) lblow, (PIX32) lbhigh, &labels);
    
    *pNbobj = (Uint32) (labels.nbObjs);
    
    /* Freeing the labels arrays */
    MB_free(labels.EQ);
    MB_free(labels.CEQ);

    return MB_NO_ERR;
}

