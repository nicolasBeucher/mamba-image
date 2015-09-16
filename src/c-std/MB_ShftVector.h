/**
 * \file MB_ShftVector.c
 * \author Nicolas Beucher
 * \date 31-05-2011
 *
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

/* This file is used to describes the way to perform vector shift. 
 * To work they must be included inside each file 
 * performing vector shift operations.
 *
 * The inclusion must be done like this :
 *    #define EDGE_TYPE Uint32
 *    #include "MB_ShftVector.c"
 *    #undef EDGE_TYPE
 * 
 */

/****************************************
 * Vector functions                     *
 ****************************************
 * The functions described here shift the pixels by a given 
 * vector using base functions.
 */
 

/**
 * Moves Up and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (0)
 * \param dy the vector y amplitude (negative)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectUp(PLINE *plines_out, PLINE *plines_in,
                           Uint32 bytes_in, Sint32 nb_lines,
                           Sint32 dx, Sint32 dy, EDGE_TYPE edge_val )
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Count cannot exceed the number of lines */
    hcount = (-dy)>nb_lines ? nb_lines : (-dy);
    
    p_in = &plines_in[hcount];
    p_out = plines_out;
    
    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE(p_out,p_in,bytes_in);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
} 

/**
 * Moves Up and Right and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (positive)
 * \param dy the vector y amplitude (negative)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectUpRight(PLINE *plines_out, PLINE *plines_in,
                                Uint32 bytes_in, Sint32 nb_lines,
                                Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = (-dy)>nb_lines ? nb_lines : (-dy);
    
    p_in = &plines_in[hcount];
    p_out = plines_out;
    
    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,dx,edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves Right and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (positive)
 * \param dy the vector y amplitude (0)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectRight(PLINE *plines_out, PLINE *plines_in,
                              Uint32 bytes_in, Sint32 nb_lines,
                              Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;

    Sint32 i;

    p_in = plines_in;
    p_out = plines_out;
    
    for(i=0; i<nb_lines; i++, p_in++, p_out++) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,dx,edge_val);
    }
} 

/**
 * Moves Down and right computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (positive)
 * \param dy the vector y amplitude (positive)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectDownRight(PLINE *plines_out, PLINE *plines_in,
                                  Uint32 bytes_in, Sint32 nb_lines,
                                  Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = dy>nb_lines ? nb_lines : dy;
    
    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];
    
    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,dx,edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves Down and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (0)
 * \param dy the vector y amplitude (positive)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectDown(PLINE *plines_out, PLINE *plines_in,
                             Uint32 bytes_in, Sint32 nb_lines,
                             Sint32 dx, Sint32 dy, EDGE_TYPE edge_val )
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = dy>nb_lines ? nb_lines : dy;
    
    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];

    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE(p_out,p_in,bytes_in);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves Down and Left and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (negative)
 * \param dy the vector y amplitude (positive)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectDownLeft(PLINE *plines_out, PLINE *plines_in,
                                 Uint32 bytes_in, Sint32 nb_lines,
                                 Sint32 dx, Sint32 dy, EDGE_TYPE edge_val )
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = dy>nb_lines ? nb_lines : dy;

    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];
    
    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,(-dx),edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves Left and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (negative)
 * \param dy the vector y amplitude (0)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectLeft(PLINE *plines_out, PLINE *plines_in,
                             Uint32 bytes_in, Sint32 nb_lines,
                             Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;

    Sint32 i;

    p_in = plines_in;
    p_out = plines_out;
    
    for(i=0; i<nb_lines; i++, p_in++, p_out++) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,(-dx),edge_val);
    }
}

/**
 * Moves Up and Left and computes the image.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (negative)
 * \param dy the vector y amplitude (negative)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectUpLeft(PLINE *plines_out, PLINE *plines_in,
                               Uint32 bytes_in, Sint32 nb_lines,
                               Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = (-dy)>nb_lines ? nb_lines : (-dy);
    
    p_in = &plines_in[hcount];
    p_out = plines_out;

    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,(-dx),edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Computes the image (no move).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (0)
 * \param dy the vector y amplitude (0)
 * \param edge_val the value used to fill the edge
 */
static void MB_ShiftVectNull(PLINE *plines_out, PLINE *plines_in,
                             Uint32 bytes_in, Sint32 nb_lines,
                             Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
    Sint32 i;

    for(i = 0; i < nb_lines; i++, plines_in++, plines_out++) {
        SHIFT_LINE( plines_out, plines_in, bytes_in);
    }
}

/**
 * Does nothing.
 * This function exists to handle impossible movement cases in hexagonal grid.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param dx the vector x amplitude (0)
 * \param dy the vector y amplitude (0)
 * \param edge_val the value used to fill the edge
 */
static void MB_Stub(PLINE *plines_out, PLINE *plines_in,
                    Uint32 bytes_in, Sint32 nb_lines,
                    Sint32 dx, Sint32 dy, EDGE_TYPE edge_val)
{
}

/************************************************/
/* High level function and global variables     */
/************************************************/

/** typedef for the definition of function arguments */
typedef void (VECFUNC) (PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 dx, Sint32 dy, EDGE_TYPE edge_val);

/** Encode the vector orientation */
#define CODE_ORIENTATION(dx,dy) \
    (((dx>0)<<3)|((dx<0)<<2)|((dy>0)<<1)|(dy<0))

/** 
 * Array giving the function to use depending on the vector orientation
 */
static VECFUNC *orientationFunc[16] =
{
    MB_ShiftVectNull,
    MB_ShiftVectUp,
    MB_ShiftVectDown,
    MB_Stub,
    MB_ShiftVectLeft,
    MB_ShiftVectUpLeft,
    MB_ShiftVectDownLeft,
    MB_Stub,
    MB_ShiftVectRight,
    MB_ShiftVectUpRight,
    MB_ShiftVectDownRight,
    MB_Stub,
    MB_Stub,
    MB_Stub,
    MB_Stub,
    MB_Stub
};
