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

/****************************************
 * Neighbor functions                   *
 ****************************************/

#define VEC_TYPE MB_Vector1
#define VEC_LOAD(pointer) MB_vec1_load(pointer)
#define VEC_STORE(pointer, value) MB_vec1_store(pointer,value)

#define COMP_NO_SHIFT(cond,inout,in)                                        \
{                                                                           \
    if (all_es&(cond)) {                                                    \
        inout &= (es1&(cond)) ? in : ~(in);                                 \
    }                                                                       \
}                                                                           \

#define COMP_SHIFT_LEFT(cond,inout,inl,inr)                                 \
{                                                                           \
    if (all_es&(cond)) {                                                    \
        MB_Vector1 temp1, temp2;                                            \
        temp1 = (inr<<(MB_vec1_size-1));                                    \
        temp2 = (inl>>1);                                                   \
        temp1 = temp1 | temp2;                                              \
        inout &= (es1&(cond)) ? temp1 : ~(temp1);                           \
    }                                                                       \
}                                                                           \

#define COMP_SHIFT_RIGHT(cond,inout,inl,inr)                                \
{                                                                           \
    if (all_es&(cond)) {                                                    \
        MB_Vector1 temp1, temp2;                                            \
        temp1 = (inl>>(MB_vec1_size-1));                                    \
        temp2 = (inr<<1);                                                   \
        temp1 = temp1 | temp2;                                              \
        inout &= (es1&(cond)) ? temp1 : ~(temp1);                           \
    }                                                                       \
}                                                                           \

/* SQUARE GRID */
static void MB_comp_neighbors_square(
        PLINE *plines_inout, PLINE *plines_in,
        Uint32 bytes_in, Uint32 height, Uint32 all_es, Uint32 es1,
        VEC_TYPE edge)
{
    Uint32 x,y;
    VEC_TYPE in8, in1, in2;
    VEC_TYPE in7, in0, in3;
    VEC_TYPE in6, in5, in4;
    VEC_TYPE *pinout;
    VEC_TYPE *pina,*pinb,*pinc;
    VEC_TYPE inout;

    /* FIRST LINE */
    in7 = edge;
    in6 = edge;
    pinb = (VEC_TYPE*) (plines_in[0]);
    pinc = (VEC_TYPE*) (plines_in[1]);
    in0 = VEC_LOAD(pinb);
    in5 = VEC_LOAD(pinc);
    pinb++;
    pinc++;
    pinout = (VEC_TYPE*) (plines_inout[0]);
    for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pinb++,pinc++,pinout++) {
        inout = VEC_LOAD(pinout);
        if (x==(bytes_in-sizeof(VEC_TYPE))) {
            in3 = edge;
            in4 = edge;
        } else {
            in3 = VEC_LOAD(pinb);
            in4 = VEC_LOAD(pinc);
        }

        COMP_SHIFT_LEFT(MB_NEIGHBOR_3,inout,in0,in3);
        COMP_SHIFT_LEFT(MB_NEIGHBOR_4,inout,in5,in4);
        COMP_NO_SHIFT(MB_NEIGHBOR_5,inout,in5);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_6,inout,in6,in5);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_7,inout,in7,in0);
        COMP_NO_SHIFT(MB_NEIGHBOR_8|MB_NEIGHBOR_1|MB_NEIGHBOR_2,inout,edge);
        
        VEC_STORE(pinout, inout);
        in7 = in0;
        in0 = in3;
        in6 = in5;
        in5 = in4;
    }

    /* MIDDLE LINES */
    for(y=1; y<height-1; y++) {
        in8 = edge;
        in6 = edge;
        in7 = edge;
        pina = (VEC_TYPE*) (plines_in[y-1]);
        pinb = (VEC_TYPE*) (plines_in[y]);
        pinc = (VEC_TYPE*) (plines_in[y+1]);
        in1 = VEC_LOAD (pina);
        in0 = VEC_LOAD (pinb);
        in5 = VEC_LOAD (pinc);
        pina++;
        pinb++;
        pinc++;
        pinout = (VEC_TYPE*) (plines_inout[y]);
        for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = VEC_LOAD(pinout);
            if (x==(bytes_in-sizeof(VEC_TYPE))) {
                in2 = edge;
                in3 = edge;
                in4 = edge;
            } else {
                in2 = VEC_LOAD(pina);
                in3 = VEC_LOAD(pinb);
                in4 = VEC_LOAD(pinc);
            }

            COMP_NO_SHIFT(MB_NEIGHBOR_1,inout,in1);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in1,in2);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_3,inout,in0,in3);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_4,inout,in5,in4);
            COMP_NO_SHIFT(MB_NEIGHBOR_5,inout,in5);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_6,inout,in6,in5);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_7,inout,in7,in0);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_8,inout,in8,in1);
            
            VEC_STORE(pinout, inout);
            in8 = in1;
            in1 = in2;
            in7 = in0;
            in0 = in3;
            in6 = in5;
            in5 = in4;
        }
    }

    /* END LINE */
    in8 = edge;
    in7 = edge;
    pina = (VEC_TYPE*) (plines_in[y-1]);
    pinb = (VEC_TYPE*) (plines_in[y]);
    in1 = VEC_LOAD (pina);
    in0 = VEC_LOAD (pinb);
    pina++;
    pinb++;
    pinout = (VEC_TYPE*) (plines_inout[y]);
    for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pina++,pinb++,pinout++) {
        inout = VEC_LOAD(pinout);
        if (x==(bytes_in-sizeof(VEC_TYPE))) {
            in2 = edge;
            in3 = edge;
        } else {
            in2 = VEC_LOAD(pina);
            in3 = VEC_LOAD(pinb);
        }

        COMP_NO_SHIFT(MB_NEIGHBOR_1,inout,in1);
        COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in1,in2);
        COMP_SHIFT_LEFT(MB_NEIGHBOR_3,inout,in0,in3);
        COMP_NO_SHIFT(MB_NEIGHBOR_4|MB_NEIGHBOR_5|MB_NEIGHBOR_6,inout,edge);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_7,inout,in7,in0);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_8,inout,in8,in1);
        
        VEC_STORE(pinout, inout);
        in8 = in1;
        in1 = in2;
        in7 = in0;
        in0 = in3;
    }
}

/* HEXAGONAL GRID */
static void MB_comp_neighbors_hexagonal(
        PLINE *plines_inout, PLINE *plines_in,
        Uint32 bytes_in, Uint32 height, Uint32 all_es, Uint32 es1,
        VEC_TYPE edge)
{
    Uint32 x,y;
    VEC_TYPE in8, in1, in2;
    VEC_TYPE in7, in0, in3;
    VEC_TYPE in6, in5, in4;
    VEC_TYPE *pinout;
    VEC_TYPE *pina,*pinb,*pinc;
    VEC_TYPE inout;

    /* FIRST LINE (even) */
    in7 = edge;
    in6 = edge;
    pinb = (VEC_TYPE*) (plines_in[0]);
    pinc = (VEC_TYPE*) (plines_in[1]);
    in0 = VEC_LOAD(pinb);
    pinb++;
    pinout = (VEC_TYPE*) (plines_inout[0]);
    for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pinb++,pinc++,pinout++) {
        inout = VEC_LOAD(pinout);
        in5 = VEC_LOAD(pinc);
        if (x==(bytes_in-sizeof(VEC_TYPE))) {
            in3 = edge;
        } else {
            in3 = VEC_LOAD(pinb);
        }

        COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in0,in3);
        COMP_NO_SHIFT(MB_NEIGHBOR_3,inout,in5);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_4,inout,in6,in5);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_5,inout,in7,in0);
        COMP_NO_SHIFT(MB_NEIGHBOR_1|MB_NEIGHBOR_6,inout,edge);
        
        VEC_STORE(pinout, inout);
        in7 = in0;
        in0 = in3;
        in6 = in5;
    }

    /* MIDDLE LINES */
    for(y=1; y<height-1; y+=2) {
        /* odd line */
        in7 = edge;
        pina = (VEC_TYPE*) (plines_in[y-1]);
        pinb = (VEC_TYPE*) (plines_in[y]);
        pinc = (VEC_TYPE*) (plines_in[y+1]);
        in1 = VEC_LOAD (pina);
        in0 = VEC_LOAD (pinb);
        in5 = VEC_LOAD (pinc);
        pina++;
        pinb++;
        pinc++;
        pinout = (VEC_TYPE*) (plines_inout[y]);
        for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = VEC_LOAD(pinout);
            if (x==(bytes_in-sizeof(VEC_TYPE))) {
                in2 = edge;
                in3 = edge;
                in4 = edge;
            } else {
                in2 = VEC_LOAD(pina);
                in3 = VEC_LOAD(pinb);
                in4 = VEC_LOAD(pinc);
            }

            COMP_SHIFT_LEFT(MB_NEIGHBOR_1,inout,in1,in2);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in0,in3);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_3,inout,in5,in4);
            COMP_NO_SHIFT(MB_NEIGHBOR_4,inout,in5);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_5,inout,in7,in0);
            COMP_NO_SHIFT(MB_NEIGHBOR_6,inout,in1);
            
            VEC_STORE(pinout, inout);
            in1 = in2;
            in7 = in0;
            in0 = in3;
            in5 = in4;
        }
        /* even line */
        in8 = edge;
        in6 = edge;
        in7 = edge;
        pina = (VEC_TYPE*) (plines_in[y]);
        pinb = (VEC_TYPE*) (plines_in[y+1]);
        pinc = (VEC_TYPE*) (plines_in[y+2]);
        in0 = VEC_LOAD (pinb);
        pinb++;
        for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = VEC_LOAD(pinout);
            in1 = VEC_LOAD(pina);
            in5 = VEC_LOAD(pinc);
            if (x==(bytes_in-sizeof(VEC_TYPE))) {
                in3 = edge;
            } else {
                in3 = VEC_LOAD(pinb);
            }

            COMP_NO_SHIFT(MB_NEIGHBOR_1,inout,in1);
            COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in0,in3);
            COMP_NO_SHIFT(MB_NEIGHBOR_3,inout,in5);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_4,inout,in6,in5);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_5,inout,in7,in0);
            COMP_SHIFT_RIGHT(MB_NEIGHBOR_6,inout,in8,in1);
            
            VEC_STORE(pinout, inout);
            in8 = in1;
            in7 = in0;
            in0 = in3;
            in6 = in5;
        }
    }

    /* END LINE (odd) */
    in7 = edge;
    pina = (VEC_TYPE*) (plines_in[y-1]);
    pinb = (VEC_TYPE*) (plines_in[y]);
    in1 = VEC_LOAD (pina);
    in0 = VEC_LOAD (pinb);
    pina++;
    pinb++;
    pinout = (VEC_TYPE*) (plines_inout[y]);
    for(x=0; x<bytes_in; x+=sizeof(VEC_TYPE),pina++,pinb++,pinout++) {
        inout = VEC_LOAD(pinout);
        if (x==(bytes_in-sizeof(VEC_TYPE))) {
            in2 = edge;
            in3 = edge;
        } else {
            in2 = VEC_LOAD(pina);
            in3 = VEC_LOAD(pinb);
        }

        COMP_SHIFT_LEFT(MB_NEIGHBOR_1,inout,in1,in2);
        COMP_SHIFT_LEFT(MB_NEIGHBOR_2,inout,in0,in3);
        COMP_NO_SHIFT(MB_NEIGHBOR_3|MB_NEIGHBOR_4,inout,edge);
        COMP_SHIFT_RIGHT(MB_NEIGHBOR_5,inout,in7,in0);
        COMP_NO_SHIFT(MB_NEIGHBOR_6,inout,in1);
        
        VEC_STORE(pinout, inout);
        in1 = in2;
        in7 = in0;
        in0 = in3;
    }
}

#undef VEC_TYPE
#undef VEC_LOAD
#undef VEC_STORE
#undef COMP_NO_SHIFT
#undef COMP_SHIFT_LEFT
#undef COMP_SHIFT_RIGHT

/****************************************/
/* Main function                        */
/****************************************/

/*
 * Performs a binary Hit-or-Miss operation on src image using the structuring elements es0 and es1.
 * Structuring elements are integer values coding which direction must be taken into account.
 * es0 indicating which neighbor of the current pixel will be checked for 0 value.
 * es1 those which will be evaluated for 1 value.
 *
 * For example, in hexagonal grid, it means that if you want to look for a pattern where the neighbors in
 * direction 6 and 1 are true while the current pixel is false just as neighbors 2 and 5, 
 * you will encode this in the elements es0 and es1 like this :
 *   1 1
 *  0 0 0
 *   X X
 * es0 = 1+4+32
 * es1 = 64+2
 *
 * \param src output image
 * \param dest input image (must be different of src)
 * \param es0 structuring element for 0 value.
 * \param es1 structuring element for 1 value.
 * \param grid grid configuration
 * \param edge the kind of edge to use (behavior for pixel near edge depends on it)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_BinHitOrMiss(MB_Image *src, MB_Image *dest, Uint32 es0, Uint32 es1, enum MB_grid_t grid, enum MB_edgemode_t edge)
{
    Uint32 bytes_in;
    PLINE *plines_in, *plines_inout;
    MB_errcode err;
    MB_Vector1 edge_val = BIN_FILL_VALUE(edge);
    
    /* Verification over depth and size */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Images must be binary */
    if (MB_PROBE_PAIR(src, dest)!=MB_PAIR_1_1) {
        return MB_ERR_BAD_DEPTH;
    }
    
    /* Verification over src and dest to know */
    /* if they point to the same image which is forbidden */
    if (src==dest) {
        return MB_ERR_BAD_PARAMETER;
    }
    /* A neighbor cannot be both true and false so requesting this will */
    /* provoke an error */
    if ((es0&es1)!=0) {
        return MB_ERR_BAD_PARAMETER;
    }

    /* Central point, mask == 1 */
    if (es1 & 1)
        err = MB_Copy(src, dest);
    else
        if (es0 & 1)
            err = MB_Inv(src, dest);
        else
            err = MB_ConSet(dest, 1);

    if (err == MB_NO_ERR) {

        /* Setting up pointers */
        plines_in = src->plines;
        plines_inout = dest->plines;
        bytes_in = MB_LINE_COUNT(src);

        /* Calling the corresponding function */
        if (grid==MB_SQUARE_GRID) {
            MB_comp_neighbors_square(plines_inout, plines_in, bytes_in, src->height,
                                     es0|es1, es1, edge_val);
        } else {
            MB_comp_neighbors_hexagonal(plines_inout, plines_in, bytes_in, src->height,
                                        es0|es1, es1, edge_val);
        }
    }

    return err;
}
