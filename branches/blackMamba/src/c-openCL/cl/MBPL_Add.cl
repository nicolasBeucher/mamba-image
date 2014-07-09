/**
 * \file MBRT_Add.cl
 * \date 23-01-2011
 *
 * This file implemements all the kernel functions for Add
 */
 
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

//This is the kernel function for the ADD operator
// depth support is : 8 + 8 = 8
__kernel void add_8_8_8(__global uchar4* in1, __global uchar4* in2, __global uchar4* out)
{
    int i;
    int index = get_global_id(0);

    out[index] = add_sat(in1[index],in2[index]);
}

//This is the kernel function for the ADD operator
// depth support is : 32 + 32 = 32
__kernel void add_32_32_32(__global const uint* in1, __global const uint* in2, __global uint* out)
{
    int index = get_global_id(0);
    
    out[index] = in1[index] + in2[index];
}
