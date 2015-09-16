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

/**********************************/
/* Base functions                 */
/**********************************/
/* The functions described here realised the basic operation */
/* needed to shift pixel in any directions. */

/*
 * Used to displace a complete line in an y direction.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 */
static INLINE void SHIFT_LINE(PLINE *p_out, PLINE *p_in, Uint32 bytes_in )
{
    MB_memcpy((*p_out),(*p_in),bytes_in);
}

/*
 * Used to fill a complete line in a given value (used to fill voided line following
 * a displacement in y).
 * \param p_out pointer on the destination image pixel line
 * \param bytes_in number of bytes inside the line
 * \param fill_val the value used to fill the line
 */
static INLINE void SHIFT_EDGE_LINE(PLINE *p_out, Uint32 bytes_in, MB_Vector1 fill_val )
{
    MB_memset((*p_out),(int) fill_val, bytes_in);
}

/*
 * Used to displace a complete line in the right direction.
 * The shift is done to the left as the byte order is Little Endian.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param count the shift amplitude
 * \param fill_val the value used to fill the line
 */
static INLINE void SHIFT_LINE_RIGHT(PLINE *p_out, PLINE *p_in, Uint32 bytes_in,
                                    Sint32 count, MB_Vector1 fill_val)
{
    Uint32 i;
    Uint32 reg_dec;
    MB_Vector1 reg1, reg2, ins_reg_dec;
    MB_Vector1 *pin, *pout;

    reg_dec = count / MB_vec1_size;
    ins_reg_dec = (MB_Vector1) count % MB_vec1_size;
    
    /* Count cannot exceed the number of pixel in a line */
    reg_dec = reg_dec<(bytes_in/sizeof(MB_Vector1)) ? reg_dec : (bytes_in/sizeof(MB_Vector1));

    pin = (MB_Vector1 *) (*p_in + bytes_in - (reg_dec+1)*sizeof(MB_Vector1));
    pout = (MB_Vector1 *) (*p_out + bytes_in - sizeof(MB_Vector1));
    
    if (ins_reg_dec==0) {
        /* No intra register shifting */
        for(i=0;i<(bytes_in-reg_dec*sizeof(MB_Vector1));i+=sizeof(MB_Vector1),pin--,pout--) {
            (*pout) = (*pin);
        }
    } else {
        /* Intra register shiffting */
        for(i=0;i<(bytes_in-reg_dec*sizeof(MB_Vector1));i+=sizeof(MB_Vector1),pin--,pout--) {
            reg1 = (*pin);
            reg2 = (i==(bytes_in-(reg_dec+1)*sizeof(MB_Vector1))) ? fill_val : (*(pin-1));
            (*pout) = (reg1<<ins_reg_dec) | (reg2>>(MB_vec1_size-ins_reg_dec));
        }
    }
    
    /* The created space is filled with the fill value */
    for(i=0;i<reg_dec;i++,pout--) {
        (*pout) = fill_val;
    }
}

/*
 * Used to displace a complete line in the left direction.
 * The shift is done to the right as the byte order is Little Endian.
 * \param p_out pointer on the destination image pixel line
 * \param p_in pointer on the source image pixel line
 * \param bytes_in number of bytes inside the line
 * \param count the shift amplitude
 * \param fill_val the value used to fill the line
 */
static INLINE void SHIFT_LINE_LEFT(PLINE *p_out, PLINE *p_in, Uint32 bytes_in,
                                   Sint32 count, MB_Vector1 fill_val)
{
    Uint32 i;
    Uint32 reg_dec;
    MB_Vector1 reg1, reg2, ins_reg_dec;
    MB_Vector1 *pin, *pout;

    reg_dec = count / MB_vec1_size;
    ins_reg_dec = (MB_Vector1) count % MB_vec1_size;
    
    /* Count cannot exceed the number of pixel in a line */
    reg_dec = reg_dec<(bytes_in/sizeof(MB_Vector1)) ? reg_dec : (bytes_in/sizeof(MB_Vector1));

    pin = (MB_Vector1 *) (*p_in + reg_dec*sizeof(MB_Vector1));
    pout = (MB_Vector1 *) (*p_out);
    
    if (ins_reg_dec==0) {
        /* No intra register shifting */
        for(i=0;i<(bytes_in-reg_dec*sizeof(MB_Vector1));i+=sizeof(MB_Vector1),pin++,pout++) {
            (*pout) = (*pin);
        }
    } else {
        /* Intra register shiffting */
        for(i=0;i<(bytes_in-reg_dec*sizeof(MB_Vector1));i+=sizeof(MB_Vector1),pin++,pout++) {
            reg1 = (*pin);
            reg2 = (i==(bytes_in-(reg_dec+1)*sizeof(MB_Vector1))) ? fill_val : (*(pin+1));
            (*pout) = (reg1>>ins_reg_dec) | (reg2<<(MB_vec1_size-ins_reg_dec));
        }
    }
    
    /* The created space is filled with the fill value */
    for(i=0;i<reg_dec;i++,pout++) {
        (*pout) = fill_val;
    }
}

/****************************************/
/* Direction functions                  */
/****************************************/
/* The functions are described in a separate file to communalize with other */
/* shift functions. */
/* Data type of the value used to represent the edge. */
#define EDGE_TYPE MB_Vector1
#include "MB_ShftDirection.h"
#undef EDGE_TYPE

/****************************************/
/* Main function                        */
/****************************************/

/*
 * Shifts the source image in the given direction.
 * The direction depends on the grid used.
 *
 * \param src source image
 * \param dest destination image
 * \param dirnum the direction(from 0 to 8)
 * \param count the amplitude of the shift (in pixels)
 * \param long_filler_pix the value used to fill the created space
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Shiftb(MB_Image *src, MB_Image *dest, Uint32 dirnum, Uint32 count, Uint32 long_filler_pix, enum MB_grid_t grid)
{
    Uint32 long_filler[2];
    Uint32 lf_value, bytes_in;
    MB_Vector1 fill_val;
    PLINE *plines_in, *plines_out;
    SHIFTFUNC *fn;

    /* Error management */
    /* Verification over image size compatibility */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }
    /* Grid value and possible direction are connected, grid value is the */
    /* maximum number of directions */
    if(dirnum>6 && grid==MB_HEXAGONAL_GRID) {
        return MB_ERR_BAD_DIRECTION;
    }
    if(dirnum>8 && grid==MB_SQUARE_GRID) {
        return MB_ERR_BAD_DIRECTION;
    }
    /* Only binary and greyscale images can be processed */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_1:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }
    
    /* If count is to zero, it amounts to a simple copy of src into dest */
    /* otherwise its a shift */
    if (count==0) {
        return MB_Copy(src, dest);
    }

    /* Setting up pointers */
    plines_in = src->plines;
    plines_out = dest->plines;
    bytes_in = MB_LINE_COUNT(src);

    /* Creating the fill_value (a MB_Vector1 element) which size can vary from */
    /* 32-bit to 64-bit depending on the machine on which the code is executed. */
    /* We create an array of two 32-bit values filled with the fill pattern */
    /* the array pointer is cast into a MB_Vector1 to make sure the correct */
    /* value is used. */
    lf_value = (long_filler_pix==0) ? 0 : 0xffffffff;
    long_filler[0] = lf_value;
    long_filler[1] = lf_value;
    fill_val = *((MB_Vector1 *) &long_filler[0]);

    /* Calling the corresponding function */
    fn = SwitchTo[grid][dirnum];
    fn(plines_out, plines_in, bytes_in, (Sint32) src->height, count, fill_val);

    return MB_NO_ERR;
}
