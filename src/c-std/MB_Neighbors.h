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
 * This file applies to 8-bit and 32-bit images. Computations are performed
 * pixel by pixel (no vectorization).
 * It is used by the following files :
 *    MB_DiffNb8.c
 *    MB_SupNb8.c
 *    MB_InfNb8.c
 *    MB_DiffNb32.c
 *    MB_SupNb32.c
 *    MB_InfNb32.c
 *
 * It can be used by including it in your source, like this :
 *    #include "MB_Neighbors.c"
 *
 * You will need to define the following macros :
 * DATA_TYPE
 * COMP(cond,inout,in)
 */

/***************
 * SQUARE GRID *
 ***************/

static void MB_comp_neighbors_square(
        PLINE *plines_inout, PLINE *plines_in,
        Uint32 bytes_in, Uint32 height, Uint32 neighbors,
        DATA_TYPE edge)
{
    Uint32 x,y;
    DATA_TYPE in8, in1, in2;
    DATA_TYPE in7, in0, in3;
    DATA_TYPE in6, in5, in4;
    DATA_TYPE *pinout;
    DATA_TYPE *pina,*pinb,*pinc;
    DATA_TYPE inout;

    /* FIRST LINE */
    in7 = edge;
    in6 = edge;
    pinb = (DATA_TYPE*) (plines_in[0]);
    pinc = (DATA_TYPE*) (plines_in[1]);
    in0 = *pinb;
    in5 = *pinc;
    pinb++;
    pinc++;
    pinout = (DATA_TYPE*) (plines_inout[0]);
    for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pinb++,pinc++,pinout++) {
        inout = *pinout;
        if (x==(bytes_in-sizeof(DATA_TYPE))) {
            in3 = edge;
            in4 = edge;
        } else {
            in3 = *pinb;
            in4 = *pinc;
        }

        COMP(MB_NEIGHBOR_0,inout,in0);
        COMP(MB_NEIGHBOR_3,inout,in3);
        COMP(MB_NEIGHBOR_4,inout,in4);
        COMP(MB_NEIGHBOR_5,inout,in5);
        COMP(MB_NEIGHBOR_6,inout,in6);
        COMP(MB_NEIGHBOR_7,inout,in7);
        COMP(MB_NEIGHBOR_8|MB_NEIGHBOR_1|MB_NEIGHBOR_2,inout,edge);
        
        *pinout = inout;
        in7 = in0;
        in0 = in3;
        in6 = in5;
        in5 = in4;
    }

    /* MIDDLE LINES */
    for(y=1; y<height-1; y++) {
        in8 = edge;
        in7 = edge;
        in6 = edge;
        pina = (DATA_TYPE*) (plines_in[y-1]);
        pinb = (DATA_TYPE*) (plines_in[y]);
        pinc = (DATA_TYPE*) (plines_in[y+1]);
        in1 = *pina;
        in0 = *pinb;
        in5 = *pinc;
        pina++;
        pinb++;
        pinc++;
        pinout = (DATA_TYPE*) (plines_inout[y]);
        for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = *pinout;
            if (x==(bytes_in-sizeof(DATA_TYPE))) {
                in2 = edge;
                in3 = edge;
                in4 = edge;
            } else {
                in2 = *pina;
                in3 = *pinb;
                in4 = *pinc;
            }

            COMP(MB_NEIGHBOR_0,inout,in0);
            COMP(MB_NEIGHBOR_1,inout,in1);
            COMP(MB_NEIGHBOR_2,inout,in2);
            COMP(MB_NEIGHBOR_3,inout,in3);
            COMP(MB_NEIGHBOR_4,inout,in4);
            COMP(MB_NEIGHBOR_5,inout,in5);
            COMP(MB_NEIGHBOR_6,inout,in6);
            COMP(MB_NEIGHBOR_7,inout,in7);
            COMP(MB_NEIGHBOR_8,inout,in8);
            
            *pinout = inout;
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
    pina = (DATA_TYPE*) (plines_in[y-1]);
    pinb = (DATA_TYPE*) (plines_in[y]);
    in1 = *pina;
    in0 = *pinb;
    pina++;
    pinb++;
    pinout = (DATA_TYPE*) (plines_inout[y]);
    for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pina++,pinb++,pinout++) {
        inout = *pinout;
        if (x==(bytes_in-sizeof(DATA_TYPE))) {
            in2 = edge;
            in3 = edge;
        } else {
            in2 = *pina;
            in3 = *pinb;
        }

        COMP(MB_NEIGHBOR_0,inout,in0);
        COMP(MB_NEIGHBOR_1,inout,in1);
        COMP(MB_NEIGHBOR_2,inout,in2);
        COMP(MB_NEIGHBOR_3,inout,in3);
        COMP(MB_NEIGHBOR_4|MB_NEIGHBOR_5|MB_NEIGHBOR_6,inout,edge);
        COMP(MB_NEIGHBOR_7,inout,in7);
        COMP(MB_NEIGHBOR_8,inout,in8);
        
        *pinout = inout;
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
        DATA_TYPE edge)
{
    Uint32 x,y;
    DATA_TYPE in8, in1, in2;
    DATA_TYPE in7, in0, in3;
    DATA_TYPE in6, in5, in4;
    DATA_TYPE *pinout;
    DATA_TYPE *pina,*pinb,*pinc;
    DATA_TYPE inout;

    /* FIRST LINE (even) */
    in7 = edge;
    in6 = edge;
    pinb = (DATA_TYPE*) (plines_in[0]);
    pinc = (DATA_TYPE*) (plines_in[1]);
    in0 = *pinb;
    pinb++;
    pinout = (DATA_TYPE*) (plines_inout[0]);
    for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pinb++,pinc++,pinout++) {
        inout = *pinout;
        in5 = *pinc;
        if (x==(bytes_in-sizeof(DATA_TYPE))) {
            in3 = edge;
        } else {
            in3 = *pinb;
        }

        COMP(MB_NEIGHBOR_0,inout,in0);
        COMP(MB_NEIGHBOR_2,inout,in3);
        COMP(MB_NEIGHBOR_3,inout,in5);
        COMP(MB_NEIGHBOR_4,inout,in6);
        COMP(MB_NEIGHBOR_5,inout,in7);
        COMP(MB_NEIGHBOR_6|MB_NEIGHBOR_1,inout,edge);
        
        *pinout = inout;
        in7 = in0;
        in0 = in3;
        in6 = in5;
    }

    /* MIDDLE LINES */
    for(y=1; y<height-1; y+=2) {
        /* Odd line */
        in7 = edge;
        pina = (DATA_TYPE*) (plines_in[y-1]);
        pinb = (DATA_TYPE*) (plines_in[y]);
        pinc = (DATA_TYPE*) (plines_in[y+1]);
        in1 = *pina;
        in0 = *pinb;
        in5 = *pinc;
        pina++;
        pinb++;
        pinc++;
        pinout = (DATA_TYPE*) (plines_inout[y]);
        for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = *pinout;
            if (x==(bytes_in-sizeof(DATA_TYPE))) {
                in2 = edge;
                in3 = edge;
                in4 = edge;
            } else {
                in2 = *pina;
                in3 = *pinb;
                in4 = *pinc;
            }

            COMP(MB_NEIGHBOR_0,inout,in0);
            COMP(MB_NEIGHBOR_1,inout,in2);
            COMP(MB_NEIGHBOR_2,inout,in3);
            COMP(MB_NEIGHBOR_3,inout,in4);
            COMP(MB_NEIGHBOR_4,inout,in5);
            COMP(MB_NEIGHBOR_5,inout,in7);
            COMP(MB_NEIGHBOR_6,inout,in1);
            
            *pinout = inout;
            in1 = in2;
            in7 = in0;
            in0 = in3;
            in5 = in4;
        }

        /* Even line */
        in8 = edge;
        in7 = edge;
        in6 = edge;
        pina = (DATA_TYPE*) (plines_in[y]);
        pinb = (DATA_TYPE*) (plines_in[y+1]);
        pinc = (DATA_TYPE*) (plines_in[y+2]);
        in0 = *pinb;
        pinb++;
        for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pina++,pinb++,pinc++,pinout++) {
            inout = *pinout;
            in1 = *pina;
            in5 = *pinc;
            if (x==(bytes_in-sizeof(DATA_TYPE))) {
                in3 = edge;
            } else {
                in3 = *pinb;
            }

            COMP(MB_NEIGHBOR_0,inout,in0);
            COMP(MB_NEIGHBOR_1,inout,in1);
            COMP(MB_NEIGHBOR_2,inout,in3);
            COMP(MB_NEIGHBOR_3,inout,in5);
            COMP(MB_NEIGHBOR_4,inout,in6);
            COMP(MB_NEIGHBOR_5,inout,in7);
            COMP(MB_NEIGHBOR_6,inout,in8);
            
            *pinout = inout;
            in8 = in1;
            in7 = in0;
            in0 = in3;
            in6 = in5;
        }
    }

    /* END LINE (odd) */
    in7 = edge;
    pina = (DATA_TYPE*) (plines_in[y-1]);
    pinb = (DATA_TYPE*) (plines_in[y]);
    in1 = *pina;
    in0 = *pinb;
    pina++;
    pinb++;
    pinc++;
    pinout = (DATA_TYPE*) (plines_inout[y]);
    for(x=0; x<bytes_in; x+=sizeof(DATA_TYPE),pina++,pinb++,pinout++) {
        inout = *pinout;
        if (x==(bytes_in-sizeof(DATA_TYPE))) {
            in2 = edge;
            in3 = edge;
        } else {
            in2 = *pina;
            in3 = *pinb;
        }

        COMP(MB_NEIGHBOR_0,inout,in0);
        COMP(MB_NEIGHBOR_1,inout,in2);
        COMP(MB_NEIGHBOR_2,inout,in3);
        COMP(MB_NEIGHBOR_3|MB_NEIGHBOR_4,inout,edge);
        COMP(MB_NEIGHBOR_5,inout,in7);
        COMP(MB_NEIGHBOR_6,inout,in1);
        
        *pinout = inout;
        in1 = in2;
        in7 = in0;
        in0 = in3;
    }
}

