/*
 * Copyright (c) <2009>, <Nicolas BEUCHER and ARMINES for the Centre de 
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
 * Labeling the upper line (near the image edge).
 *
 * \param plines_out pointer on the destination image pixel line
 * \param plines_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param labels the labels arrays and context
 */
static INLINE void EDGE_LINE(PLINE plines_out, PLINE plines_in, Uint32 bytes_in, MB_Label_struct *labels)
{
    Uint32 i,j;
    MB_Vector1 pix_reg, previous_pix;

    MB_Vector1 *pin = (MB_Vector1 *) (plines_in);
    PIX32 *pout = (PIX32 *) (plines_out);
    
    /* Previous values initialisation */
    previous_pix = 0;
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++) {
        /* Reading a register of pixels */
        pix_reg = (*pin);
        for(j=0; j<MB_vec1_size; j++,pout++) {
            /* For all the pixels in the register */
            if (pix_reg&1) {
                /* the pixel need to be labelled */
                if (previous_pix&1) {
                    /* with the same label as its neighbor since the */
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
            previous_pix = pix_reg;
            /* Next pixel */
            pix_reg = pix_reg>>1;
        }
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
    Uint32 i,j;
    MB_Vector1 pix_reg_cur, pix_reg_pre, previous_pix;
    MB_Vector1 neighbor_state;

    MB_Vector1 *pin = (MB_Vector1 *) (plines_in[index]);
    MB_Vector1 *pinpre = (MB_Vector1 *) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    previous_pix = 0;
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++) {
        /* Reading a register of pixels in the two sources lines*/
        pix_reg_cur = (*pin);
        pix_reg_pre = (*pinpre);
        for(j=1; j<MB_vec1_size; j++,pout++,poutpre++) {
            /* For all the pixels in the registers */
            /* except the last one */
            if (pix_reg_cur&1) {
                neighbor_state = (previous_pix&1) |
                                 ((pix_reg_pre&3)<<1);
                /* The neighbor state gives the values of the neighbor bit of the currently */
                /* evaluated bit (a&1). It allows to determine which value will take the label */
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
            previous_pix = pix_reg_cur;
            /* Next pixel */
            pix_reg_cur = pix_reg_cur>>1;
            pix_reg_pre = pix_reg_pre>>1;
        }
        /* The last pixel cannot be processed because one of its neighbor is not */
        /* inside the previous line pixel register */
        /* to process it we then need to fetch the neighbor in the next register */
        pinpre++;
        if (i < bytes_in-sizeof(MB_Vector1)) {
            pix_reg_pre = pix_reg_pre|((*pinpre&1)<<1);
        }
        if (pix_reg_cur&1) {
            neighbor_state = (previous_pix&1) |
                             ((pix_reg_pre&3)<<1);
            /* The neighbor state gives the values of the neighbor bit of the currently */
            /* evaluated bit (a&1). It allows to determine which value will take the label */
            /* in the output image (p2).*/
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
        previous_pix = pix_reg_cur;
        /* Next pixel */
        pout++;
        poutpre++;
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
    Uint32 i,j;
    MB_Vector1 pix_reg_cur, pix_reg_pre, previous_pix_cur, previous_pix_pre;
    MB_Vector1 neighbor_state;

    MB_Vector1 *pin = (MB_Vector1 *) (plines_in[index]);
    MB_Vector1 *pinpre = (MB_Vector1 *) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    previous_pix_cur = 0;
    previous_pix_pre = 0;
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++,pinpre++) {
        /* Reading a register of pixels in the two sources lines*/
        pix_reg_cur = (*pin);
        pix_reg_pre = (*pinpre);
        for(j=0; j<MB_vec1_size; j++,pout++,poutpre++) {
            /* For all the pixels in the registers */
            if (pix_reg_cur&1) {
                neighbor_state = (previous_pix_cur&1) |
                                 ((previous_pix_pre&1)<<1) |
                                 ((pix_reg_pre&1)<<2);
                /* The neighbor state gives the values of the neighbor bit of the currently */
                /* evaluated bit (a&1). It allows to determine which value will take the label */
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
                default: /* Case 0 */
                    VAL(pout) = (labels->current);
                    /* No neighbors labelled we take one */
                    labels->EQ[labels->current] = labels->current;
                    labels->current++;
                    break;
                }
            }
            previous_pix_cur = pix_reg_cur;
            previous_pix_pre = pix_reg_pre;
            /* Next pixel */
            pix_reg_cur = pix_reg_cur>>1;
            pix_reg_pre = pix_reg_pre>>1;
        }
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
    Uint32 i,j;
    MB_Vector1 pix_reg_cur, pix_reg_pre, previous_pix_cur, previous_pix_pre;
    MB_Vector1 neighbor_state;

    MB_Vector1 *pin = (MB_Vector1 *) (plines_in[index]);
    MB_Vector1 *pinpre = (MB_Vector1 *) (plines_in[index-1]);
    PIX32 *pout = (PIX32 *) (plines_out[index]);
    PIX32 *poutpre = (PIX32 *) (plines_out[index-1]);
    
    /* Previous values initialisation */
    previous_pix_cur = 0;
    previous_pix_pre = 0;
    
    for(i=0;i<bytes_in;i+=sizeof(MB_Vector1),pin++) {
        /* Reading a register of pixels in the two sources lines*/
        pix_reg_cur = (*pin);
        pix_reg_pre = (*pinpre);
        for(j=1; j<MB_vec1_size; j++,pout++,poutpre++) {
            /* For all the pixels in the registers */
            /* except the last one */
            if (pix_reg_cur&1) {
                neighbor_state = (previous_pix_cur&1) |
                                 ((previous_pix_pre&1)<<1) |
                                 ((pix_reg_pre&3)<<2);
                /* The neighbor state gives the values of the neighbor bit of the currently */
                /* evaluated bit (a&1). It allows to determine which value will take the label */
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
            previous_pix_cur = pix_reg_cur;
            previous_pix_pre = pix_reg_pre;
            /* Next pixel */
            pix_reg_cur = pix_reg_cur>>1;
            pix_reg_pre = pix_reg_pre>>1;
        }
        /* The last pixel cannot be processed because one of its neighbor is not */
        /* inside the previous line pixel register */
        /* to process it we then need to fetch the neighbor in the next register */
        pinpre++;
        if (i < bytes_in-sizeof(MB_Vector1)) {
            pix_reg_pre = pix_reg_pre|((*pinpre&1)<<1);
        }
        if (pix_reg_cur&1) {
            neighbor_state = (previous_pix_cur&1) |
                             ((previous_pix_pre&1)<<1) |
                             ((pix_reg_pre&3)<<2);
            /* The neighbor state gives the values of the neighbor bit of the currently */
            /* evaluated bit (a&1). It allows to determine which value will take the label */
            /* in the output image (p2).*/
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
        previous_pix_cur = pix_reg_cur;
        previous_pix_pre = pix_reg_pre;
        /* Next pixel */
        pout++;
        poutpre++;
    }
}

/******************************************
 * Grid functions                         *
 ******************************************/
#include "MB_Label_neighbors.h"

/*
 * Labeling the object found in src image.
 *
 * \param src the binary source image where the object must be labelled
 * \param dest the 32-bit image where object are labelled
 * \param lblow the lowest value allowed for label on the low byte (must be inferior to lbhigh)
 * \param lbhigh the first high value NOT allowed for label on the low byte (maximum allowed is 256)
 * \param pNbobj the number of object founds
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Labelb(MB_Image *src, MB_Image *dest, Uint32 lblow, Uint32 lbhigh, Uint32 *pNbobj, enum MB_grid_t grid)
{
    Uint32 bytes_in, bytes_out;
    PLINE *plines_in, *plines_out;
    MB_Label_struct labels;
    LABELGRIDFUNC *fn;
    
    /* Initializing the algorithm parameters */
    labels.current = 1;
    labels.ccurrent = 1;
    labels.nbObjs = 0;
    labels.maxEQ = (src->width*src->height)/4;
    labels.EQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if(labels.EQ==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    labels.CEQ = MB_malloc(labels.maxEQ*sizeof(PIX32));
    if(labels.CEQ==NULL){
        /* In case allocation goes wrong */
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

