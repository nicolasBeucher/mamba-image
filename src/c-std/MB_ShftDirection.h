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

/* This file is used to describe the way to perform shift for each 
 * direction and each grid. To work, they must be included inside each file 
 * performing directional shift operations such as :
 *    MB_Shift32.c
 *    MB_Shift8.c
 *    MB_Shift1.c
 *
 * The inclusion must be done like this example for MB_Shift8.c :
 *    #define EDGE_TYPE Uint32
 *    #include "MB_ShftDirection.c"
 *    #undef EDGE_TYPE
 * 
 */

/****************************************
 * Direction functions                  *
 ****************************************
 * The functions described here shift the pixels in a given 
 * direction using base functions.
 */
 
/* SQUARE */

/**
 * Moves and computes the image in direction 1 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir1(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Count cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    
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
 * Moves and computes the image in direction 2 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir2(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    
    p_in = &plines_in[hcount];
    p_out = plines_out;
    
    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,count,edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves and computes the image in direction 3 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir3(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;

    Sint32 i;

    p_in = plines_in;
    p_out = plines_out;
    
    for(i=0; i<nb_lines; i++, p_in++, p_out++) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,count,edge_val);
    }
} 

/**
 * Moves and computes the image in direction 4 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir4(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    
    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];
    
    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,count,edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves and computes the image in direction 5 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir5(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    
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
 * Moves and computes the image in direction 6 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir6(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;

    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];
    
    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,count,edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves and computes the image in direction 7 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir7(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;

    Sint32 i;

    p_in = plines_in;
    p_out = plines_out;
    
    for(i=0; i<nb_lines; i++, p_in++, p_out++) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,count,edge_val);
    }
}

/**
 * Moves and computes the image in direction 8 (SQUARE GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir8(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    
    p_in = &plines_in[hcount];
    p_out = plines_out;

    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,count,edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
} 

/* HEXAGONAL
 * Remark for the hex mode: we suppose that the first line of an image
 * is always of even parity. This means that the line 0 of the image 
 * is of even parity,
 */

/**
 * Moves the image in direction 1 (HEXAGONAL GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_HShiftDir1(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 wcount[2];
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    /* Wcount depends on odd and even lines */
    wcount[0] = (hcount%2)==1 ? hcount/2 + 1 : hcount/2;
    wcount[1] = hcount/2;
    
    p_in = &plines_in[hcount];
    p_out = plines_out;
    
    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,wcount[i%2],edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves the image in direction 3 (HEXAGONAL GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_HShiftDir3(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 wcount[2];
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    /* Wcount depends on odd and even lines */
    wcount[0] = hcount/2;
    wcount[1] = (hcount%2)==1 ? hcount/2 + 1 : hcount/2;
    
    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];

    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_RIGHT(p_out,p_in,bytes_in,wcount[i%2],edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
} 
 
/**
 * Moves and computes the image in direction 4 (HEXAGONAL GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_HShiftDir4(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 wcount[2];
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    /* Wcount depends on odd and even lines */
    wcount[0] = (hcount%2)==1 ? hcount/2 + 1 : hcount/2;
    wcount[1] = hcount/2;
    
    p_in = &plines_in[nb_lines-1-hcount];
    p_out = &plines_out[nb_lines-1];

    for(i=0; i<(nb_lines-hcount); i++, p_in--, p_out--) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,wcount[i%2],edge_val);
    }
    for(i=0; i<hcount; i++, p_out--) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/**
 * Moves and computes the image in direction 6 (HEXAGONAL GRID).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_HShiftDir6(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
{
    PLINE *p_in;
    PLINE *p_out;
    Sint32 wcount[2];
    Sint32 hcount;
    
    Sint32 i;
    
    /* Hcount cannot exceed the number of lines */
    hcount = count>nb_lines ? nb_lines : count;
    /* Wcount depends on odd and even lines */
    wcount[0] = hcount/2;
    wcount[1] = (hcount%2)==1 ? hcount/2 + 1 : hcount/2;
    
    p_in = &plines_in[hcount];
    p_out = plines_out;

    for(i=0; i<(nb_lines-hcount); i++, p_in++, p_out++) {
        SHIFT_LINE_LEFT(p_out,p_in,bytes_in,wcount[i%2],edge_val);
    }
    for(i=0; i<hcount; i++, p_out++) {
        SHIFT_EDGE_LINE(p_out,bytes_in,edge_val);
    }
}

/* SPECIAL */

/**
 * Computes the image in direction 0 (no move).
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_QShiftDir0(PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val)
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
 * \param count the shift amplitude
 * \param edge_val the value used to fill the edge
 */
static void MB_Stub(PLINE *plines_out, PLINE *plines_in,
                    Uint32 bytes_in, Sint32 nb_lines,
                    Sint32 count, EDGE_TYPE edge_val)
{
}

/************************************************/
/* High level function and global variables     */
/************************************************/

/** typedef for the definition of function arguments */
typedef void (SHIFTFUNC) (PLINE *plines_out, PLINE *plines_in,
                          Uint32 bytes_in, Sint32 nb_lines,
                          Sint32 count, EDGE_TYPE edge_val);

/** 
 * Array giving the function to use to go in a given direction with
 * regard to the grid in use (hexagonal or square).
 */
static SHIFTFUNC *SwitchTo[2][9] =
{
  { /* Square directions */
     MB_QShiftDir0, /* No movement, so simple copy */
     MB_QShiftDir1,
     MB_QShiftDir2,
     MB_QShiftDir3,
     MB_QShiftDir4,
     MB_QShiftDir5,
     MB_QShiftDir6,
     MB_QShiftDir7,
     MB_QShiftDir8
  },
  { /* Hexagonal directions */
     MB_QShiftDir0, /* No movement, so simple copy */
     MB_HShiftDir1,
     MB_QShiftDir3, /* Hexagonal direction 2 is similar to square direction 3*/ 
     MB_HShiftDir3,
     MB_HShiftDir4,
     MB_QShiftDir7, /* Hexagonal direction 5 is similar to square direction 7*/ 
     MB_HShiftDir6,
     MB_Stub,
     MB_Stub
  }
};
