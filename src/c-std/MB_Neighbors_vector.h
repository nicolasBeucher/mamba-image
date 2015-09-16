/*
 * Copyright (c) <2012>, <Nicolas BEUCHER and ARMINES for the Centre de 
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

/* This file is used to avoid code repetition between the various operators 
 * working on neighbors.
 * This file describe the algorithm in a vectorized form. It applies to
 * greyscale images when using SSE2 instructions and to binary images.
 * It is used by the following files :
 *    MB_DiffNb8.c
 *    MB_SupNb8.c
 *    MB_InfNb8.c
 *    MB_DiffNbb.c
 *    MB_SupNbb.c
 *    MB_InfNbb.c
 *
 * It can be used by including it in your source, like this :
 *    #include "MB_Neighbors_vector.c"
 *
 * You will need to define the following macros :
 * VEC_TYPE
 * VEC_LOAD(pointer)
 * VEC_STORE(pointer, value)
 * COMP_NO_SHIFT(cond,inout,in)
 * COMP_SHIFT_LEFT(cond,inout,inl,inr)
 * COMP_SHIFT_RIGHT(cond,inout,inl,inr)
 */

/***************
 * SQUARE GRID *
 ***************/

static void MB_comp_neighbors_square(
        PLINE *plines_inout, PLINE *plines_in,
        Uint32 bytes_in, Uint32 height, Uint32 neighbors,
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

        COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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

            COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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

        COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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

/******************
 * HEXAGONAL GRID *
 ******************/

static void MB_comp_neighbors_hexagonal(
        PLINE *plines_inout, PLINE *plines_in,
        Uint32 bytes_in, Uint32 height, Uint32 neighbors,
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
    in0 = VEC_LOAD (pinb);
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

        COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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
        /* Odd line */
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

            COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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
        /* Even line */
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

            COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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

        COMP_NO_SHIFT(MB_NEIGHBOR_0,inout,in0);
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

