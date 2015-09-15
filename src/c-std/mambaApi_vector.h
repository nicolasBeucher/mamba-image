/**
 * \file mambaApi_vector.h
 * \date 18-11-2012
 *
 * This file contains all the macros and definitions used to vectorize in the
 * Mamba library. Modify this file to add support for other vectorization
 * instruction-set.
 */
 
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
#ifndef MB_apivecH
#define MB_apivecH

/**@cond */
/* code that must be skipped by Doxygen */
/*******************************************************************************
 * BINARY PIXELS VECTORIZATION
 ******************************************************************************/
/* Computations on binary image are always vectorized */

/* binary computations are performed on a complete 64-bit integer */
#ifdef VECTOR_32BIT
    typedef uint32_t MB_Vector1;
    #define MB_vec1_size 32
#else
    typedef uint64_t MB_Vector1;
    #define MB_vec1_size 64
#endif

/* Loading/Storing instructions */
#define MB_vec1_load(pointer) (*pointer)
#define MB_vec1_store(pointer, value) {*pointer =  value;}
#define MB_vec1_set(value) (value)
#define MB_vec1_setzero 0

/* Arithmetic operations */
#define MB_vec1_and(vec1, vec2) ((vec1)&(vec2))
#define MB_vec1_or(vec1, vec2) ((vec1)|(vec2))
#define MB_vec1_xor(vec1, vec2) ((vec1)^(vec2))
#define MB_vec1_adds(vec1, vec2) ((vec1)|(vec2))
#define MB_vec1_subs(vec1, vec2) ((vec1)&(~(vec2)))

/* Shifting */
# define MB_vec1_shlft(vec, dec) ((vec)<<(dec))
# define MB_vec1_shrgt(vec, dec) ((vec)>>(dec))

/* Extrema */
#define MB_vec1_min(vec1, vec2) ((vec1)&(vec2))
#define MB_vec1_max(vec1, vec2) ((vec1)|(vec2))

/* Accumulation */
#define MB_vec1_acc(result,vec) \
{ \
MB_Vector1 vc; \
for(vc=vec; vc!=0; vc = vc>>8) \
    result += MB_VolumePerByte[vc&255]; \
}

/*******************************************************************************
 * 8-BIT PIXELS VECTORIZATION
 ******************************************************************************/
#ifdef __SSE2__
/* SSE2 instruction set *******************************************************/
/* if SSE2 is available use it ! it's faster*/
/* Vectorization is enabled */
#define MB_VECTORIZATION_8 1
#include <xmmintrin.h>
#include <emmintrin.h>

typedef __m128i MB_Vector8;
#define MB_vec8_size sizeof(MB_Vector8) /* Vector size must not exceed 16 */

/* Loading/Storing instructions */
#define MB_vec8_load(pointer) _mm_load_si128(pointer)
#define MB_vec8_store(pointer, value) _mm_store_si128(pointer,value)
#define MB_vec8_set(value) _mm_set1_epi8((char) value)
#define MB_vec8_set32(value) _mm_set1_epi32((int) value)
#define MB_vec8_setzero _mm_setzero_si128()

/* Comparison */
#define MB_vec8_cmpeq(vec1, vec2) _mm_cmpeq_epi8(vec1,vec2)

/* Arithmetic operations */
#define MB_vec8_and(vec1, vec2) _mm_and_si128(vec1,vec2)
#define MB_vec8_andnot(vec1, vec2) _mm_andnot_si128(vec1,vec2)
#define MB_vec8_or(vec1, vec2) _mm_or_si128(vec1,vec2)
#define MB_vec8_adds(vec1, vec2) _mm_adds_epu8(vec1,vec2)
#define MB_vec8_subs(vec1, vec2) _mm_subs_epu8(vec1,vec2)
#define MB_vec8_sub(vec1, vec2) _mm_sub_epi8(vec1, vec2)

/* Shifting */
# define MB_vec8_shlft(vec, dec) _mm_slli_si128(vec,dec)
# define MB_vec8_shrgt(vec, dec) _mm_srli_si128(vec,dec)

/* Extrema */
#define MB_vec8_min(vec1, vec2) _mm_min_epu8(vec1, vec2)
#define MB_vec8_max(vec1, vec2) _mm_max_epu8(vec1, vec2)

/* Accumulation */
#define MB_vec8_acc(result,vec) \
{ \
    __m128i acc_vec; \
    __m128i zero = _mm_setzero_si128(); \
    acc_vec = _mm_sad_epu8(vec,zero); \
    result += ((Uint16 *) &acc_vec)[0]+((Uint16 *) &acc_vec)[4]; \
}

#else
/* No vectorization ***********************************************************/

#endif

/*******************************************************************************
 * 32-BIT PIXELS VECTORIZATION
 ******************************************************************************/
#ifdef __SSE2__

#define MB_VECTORIZATION_32 1
typedef __m128i MB_Vector32;
#define MB_vec32_size 4

/* Loading/Storing instructions */
#define MB_vec32_load(pointer) _mm_load_si128(pointer)
#define MB_vec32_store(pointer, value) _mm_store_si128(pointer,value)
#define MB_vec32_set(value) _mm_set1_epi32((int) value)
#define MB_vec32_setzero _mm_setzero_si128()

/* Comparison */
#define MB_vec32_cmpgt(vec1, vec2) _mm_cmpgt_epi32(vec1,vec2)

/* Arithmetic operations */
#define MB_vec32_and(vec1, vec2) _mm_and_si128(vec1,vec2)
#define MB_vec32_or(vec1, vec2) _mm_or_si128(vec1,vec2)
#define MB_vec32_sub(vec1, vec2) _mm_sub_epi32(vec1, vec2)
#define MB_vec32_add(vec1, vec2) _mm_add_epi32(vec1, vec2)

#endif

/**@endcond*/
#endif
