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
#include "mambaApi_loc.h"

/****************************************/
/* Base functions                       */
/****************************************/
/* The functions described here realise the basic operations */
/* needed to shift pixel in any directions. */

/*
 * Used to displace a complete line in an y direction.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void SHIFT_LINE(PLINE *p_out, PLINE *p_in, Uint32 bytes_in)
{
    Uint32 i;

    PIX32 *pin = (PIX32 *) (*p_in);
    PIX32 *pout = (PIX32 *) (*p_out);
    
    for(i=0;i<bytes_in;i+=4,pin++,pout++) {
        (*pout) = (*pout)>(*pin) ? (*pout) : (*pin);
    }
}

/*
 * Used to fill a complete line with a given value (used to fill voided line following
 * a displacement in y).
 * \param p_out pointer on the destination image pixel line
 * \param bytes_in number of bytes inside the line
 * \param fill_val the value used to fill the line
 */
static INLINE void SHIFT_EDGE_LINE(PLINE *p_out, Uint32 bytes_in, PIX32 fill_val)
{
    Uint32 i;

    PIX32 *pout = (PIX32 *) (*p_out);
    
    for(i=0;i<bytes_in;i+=4,pout++) {
        (*pout) = (*pout)>(fill_val) ? (*pout) : (fill_val);
    }
}

/*
 * Used to displace a complete line in the left direction.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param count the shift amplitude
 * \param fill_val the value used to fill created space
 */
static INLINE void SHIFT_LINE_LEFT(PLINE *p_out, PLINE *p_in, Uint32 bytes_in,
                                   Sint32 count, PIX32 fill_val)
{
    Sint32 i;

    PIX32 *pin = (PIX32 *) (*p_in + 4*count);
    PIX32 *pout = (PIX32 *) (*p_out);
    
    /* Count cannot exceed the number of pixel in a line */
    count = count<((Sint32) (bytes_in/4)) ? count : bytes_in/4;
    
    for(i=0; i<((Sint32) bytes_in)-(4*count); i+=4,pin++,pout++) {
        (*pout) = (*pout)>(*pin) ? (*pout) : (*pin);
    }
    for(i=0; i<count; i++,pout++) {
        (*pout) = (*pout)>(fill_val) ? (*pout) : (fill_val);
    }
}

/*
 * Used to displace a complete line in the right direction.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param count the shift amplitude
 * \param fill_val the value used to fill created space
 */
static INLINE void SHIFT_LINE_RIGHT(PLINE *p_out, PLINE *p_in, Uint32 bytes_in, 
                                    Sint32 count, PIX32 fill_val)
{
    Sint32 i;

    PIX32 *pin = (PIX32 *) (*p_in + bytes_in -4*(count+1));
    PIX32 *pout = (PIX32 *) (*p_out + bytes_in -4);
    
    /* Count cannot exceed the number of pixel in a line */
    count = count<((Sint32) (bytes_in/4)) ? count : bytes_in/4;
    
    for(i=0;i<((Sint32) bytes_in)-(4*count);i+=4,pin--,pout--) {
        (*pout) = (*pout)>(*pin) ? (*pout) : (*pin);
    }
    for(i=0; i<count; i++,pout--) {
        (*pout) = (*pout)>(fill_val) ? (*pout) : (fill_val);
    }
}

/****************************************/
/* Direction functions                  */
/****************************************/
/* The functions are described in a separate file to communalize with other */
/* shift functions. */
/* Data type of the value used to represent the edge. */
#define EDGE_TYPE PIX32
#include "MB_ShftVector.h"
#undef EDGE_TYPE

/****************************************/
/* Main function                        */
/****************************************/

/*
 * Looks for the maximum between two 32-bits image pixels (a central pixel
 * and its neighbor in the other image previously shifted by the given vector).
 *
 * \param src source image in which the neighbor are taken
 * \param srcdest source of the central pixel and destination image
 * \param dx the vector amplitude in x
 * \param dy the vector amplitude in y
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_SupVector32(MB_Image *src, MB_Image *srcdest, Sint32 dx, Sint32 dy, enum MB_edgemode_t edge)
{
    Uint32 bytes_in;
    PLINE *plines_in, *plines_out;
    VECFUNC *fn;

    /* Error management */
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, srcdest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Only binary and greyscale images can be processed */
    switch (MB_PROBE_PAIR(src, srcdest)) {
    case MB_PAIR_32_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }

    /* Setting up pointers */
    plines_in = src->plines;
    plines_out = srcdest->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Calling the corresponding function which depends on the orientation */
    /* of the vector */
    fn = orientationFunc[CODE_ORIENTATION(dx,dy)];
    fn(plines_out, plines_in, bytes_in, (Sint32) src->height, dx, dy, I32_FILL_VALUE(edge));

    return MB_NO_ERR;
}
