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

/*
 * This file redefines some basic OS and memory functions that are used in the 
 * mamba API so that they could be modified or replaced in needed.
 */

/*
 * Allocates memory.
 * \param size size in byte of the allocated memory
 *
 * \return a pointer to the memory space or NULL if unsuccessful
 */
void *MB_malloc(int size) {
    return malloc(size);
}

/*
 * Allocates aligned memory (faster and safer access for SSE2 instructions
 * for example).
 *
 * \param size size in bytes of the allocated memory
 * \param alignment value to which the memory space is aligned
 *
 * \return a pointer to the memory space or NULL if unsuccessful
 */
void *MB_aligned_malloc(int size, int alignment) {
# if defined(__MINGW32__)
    return __mingw_aligned_malloc(size, alignment);
# elif defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
    return _aligned_malloc(size, alignment);
# else
    void *ptr;
    if(posix_memalign((void *) &ptr, alignment, size)!=0) {
        return NULL;
    } else {
        return ptr;
    }
# endif
}

/*
 * Frees memory.
 * \param ptr pointer to the memory space to free
 */
void MB_free(void *ptr) {
    free(ptr);
}

/*
 * Frees aligned memory.
 * \param ptr pointer to the memory space to free
 */
void MB_aligned_free(void *ptr) {
# if defined(__MINGW32__)
    return __mingw_aligned_free(ptr);
# elif defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
    _aligned_free(ptr);
# else
    free(ptr);
# endif
}

/*
 * Sets a memory space to a specific value.
 *
 * \param s pointer to the memory space to set
 * \param c value to use to set
 * \param size the memory space size
 *
 * \return a pointer to the memory space set
 */
void *MB_memset(void *s, int c, int size) {
    return memset(s, c, size);
}

/*
 * Copies a memory space to another. This copy should be protected for safe
 * aliased memory copy.
 *
 * \param dest pointer to the destination memory space
 * \param src pointer to the source memory space
 * \param size the size of the copy
 *
 * \return a pointer to the destination memory space
 */
void *MB_memcpy(void *dest, const void *src, int size) {
    return memmove(dest, src, size);
}

