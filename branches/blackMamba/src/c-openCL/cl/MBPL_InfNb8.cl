/**
 * \file MBRT_InfNb8.cl
 *
 * This file implemements all the kernel functions for inferior by neighbor
 */
 
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

//This is the kernel function for the INF by NEIGHBOR operator in square grid
__kernel void infnb_8_s(__global uchar8* in,
                        __global uchar8* inout,
                        uint neighbors,
                        uchar border)
{
    uint x = get_global_id(0);
    uint y = get_global_id(1);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    size_t index;
    uchar8 minval;
    uchar8 vec1, vec2;
    
    index = x + y*width;
    minval = inout[index];
    
    if (neighbors&0x106) { // dir 1, 2 and 8
        if (y==0) {
            vec2 = (uchar8) border;
            minval = min(minval, vec2);
        } else {
            vec1 = in[index-width];
            if (neighbors&0x2) { // dir 1
                minval = min(minval, vec1);
            }
            if (neighbors&0x4) { // dir 2
                if (x==(width-1)) {
                    vec2 = (uchar8) (vec1.s1234567, border);
                } else {
                    vec2 = (uchar8) (vec1.s1234567, in[index-width+1].s0);
                }
                minval = min(minval, vec2);
            }
            if (neighbors&0x100) { // dir 8
                if (x==0) {
                    vec2 = (uchar8) (border, vec1.s0123456);
                } else {
                    vec2 = (uchar8) (in[index-width-1].s7, vec1.s0123456);
                }
                minval = min(minval, vec2);
            }
        }
    }
    
    if (neighbors&0x89) { // dir 0, 3 and 7
        vec1 = in[index];
        
        if (neighbors&0x1) minval = (uchar8) min(minval, vec1);

        if (neighbors&0x8) { // dir 3
            if ( (x==(width-1)) ) {
                vec2 = (uchar8) (vec1.s1234567, border);
            } else {
                vec2 = (uchar8) (vec1.s1234567, in[index+1].s0);
            }
            minval = min(minval, vec2);
        }
        if (neighbors&0x80) { // dir 7
            if (x==0) {
                vec2 = (uchar8) (border, vec1.s0123456);
            } else {
                vec2 = (uchar8) (in[index-1].s7, vec1.s0123456);
            }
            minval = min(minval, vec2);
        }
    }
    
    if (neighbors&0x70) { // dir 4, 5 and 6
        if (y==(height-1)) {
            vec2 = (uchar8) border;
            minval = min(minval, vec2);
        } else {
            vec1 = in[index+width];
            if (neighbors&0x10) { // dir 4
                if (x==(width-1)) {
                    vec2 = (uchar8) (vec1.s1234567, border);
                } else {
                    vec2 = (uchar8) (vec1.s1234567, in[index+width+1].s0);
                }
                minval = min(minval, vec2);
            }
            if (neighbors&0x20) { // dir 5
                minval = min(minval, vec1);
            }
            if (neighbors&0x40) { // dir 6
                if (x==0) {
                    vec2 = (uchar8) (border, vec1.s0123456);
                } else {
                    vec2 = (uchar8) (in[index+width-1].s7, vec1.s0123456);
                }
                minval = min(minval, vec2);
            }
        }
    }
    
    inout[index] = minval;
}

//This is the kernel function for the INF by NEIGHBOR operator in hexagonal grid
__kernel void infnb_8_h(__global uchar8* in,
                        __global uchar8* inout,
                        uint neighbors,
                        uchar border)
{
    uint x = get_global_id(0);
    uint y = get_global_id(1);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    size_t index;
    uchar8 minval;
    uchar8 vec1, vec2;
    
    index = x + y*width;
    minval = inout[index];
    
    if (neighbors&0x42) { // dir 1 and 6
        if (y==0) {
            vec2 = (uchar8) border;
            minval = min(minval, vec2);
        } else if (y%2==0) {
            vec1 = in[index-width];
            if (neighbors&0x2) { // dir 1
                minval = min(minval, vec1);
            }
            if (neighbors&0x40) { // dir 6
                if (x==0) {
                    vec2 = (uchar8) (border, vec1.s0123456);
                } else {
                    vec2 = (uchar8) (in[index-width-1].s7, vec1.s0123456);
                }
                minval = min(minval, vec2);
            }
        } else  {
            vec1 = in[index-width];
            if (neighbors&0x40) { // dir 6
                minval = min(minval, vec1);
            }
            if (neighbors&0x2) { // dir 1
                if (x==(width-1)) {
                    vec2 = (uchar8) (vec1.s1234567, border);
                } else {
                    vec2 = (uchar8) (vec1.s1234567, in[index-width+1].s0);
                }
                minval = min(minval, vec2);
            }
        }
    }
    
    if (neighbors&0x25) { // dir 0, 2 and 5
        vec1 = in[index];
        
        if (neighbors&0x1) minval = (uchar8) min(minval, vec1);

        if (neighbors&0x4) { // dir 3
            if ( (x==(width-1)) ) {
                vec2 = (uchar8) (vec1.s1234567, border);
            } else {
                vec2 = (uchar8) (vec1.s1234567, in[index+1].s0);
            }
            minval = min(minval, vec2);
        }
        if (neighbors&0x20) { // dir 7
            if (x==0) {
                vec2 = (uchar8) (border, vec1.s0123456);
            } else {
                vec2 = (uchar8) (in[index-1].s7, vec1.s0123456);
            }
            minval = min(minval, vec2);
        }
    }
    
    if (neighbors&0x18) { // dir 3 and 4
        if (y==(height-1)) {
            vec2 = (uchar8) border;
            minval = min(minval, vec2);
        } else if (y%2==0) {
            vec1 = in[index+width];
            if (neighbors&0x8) { // dir 3
                minval = min(minval, vec1);
            }
            if (neighbors&0x10) { // dir 4
                if (x==0) {
                    vec2 = (uchar8) (border, vec1.s0123456);
                } else {
                    vec2 = (uchar8) (in[index+width-1].s7, vec1.s0123456);
                }
                minval = min(minval, vec2);
            }
        } else {
            vec1 = in[index+width];
            if (neighbors&0x8) { // dir 3
                if (x==(width-1)) {
                    vec2 = (uchar8) (vec1.s1234567, border);
                } else {
                    vec2 = (uchar8) (vec1.s1234567, in[index+width+1].s0);
                }
                minval = min(minval, vec2);
            }
            if (neighbors&0x10) { // dir 4
                minval = min(minval, vec1);
            }
        } 
    }
    
    inout[index] = minval;
}
