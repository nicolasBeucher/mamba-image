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

/* This file is used to describe the way to perform build/dualbuild for each 
 * direction and each grid. To work, they must be included inside each file 
 * performing directionnal build or dualbuild operations such as :
 *    MB_BldNb32.c
 *    MB_BldNb8.c
 *    MB_BldNbb.c
 *    MB_DualBldNb32.c
 *    MB_DualBldNb8.c
 *    MB_DualBldNbb.c
 *
 * The inclusion must be done like this :
 *    #include "MB_BldDirection.h"
 * 
 */

/****************************************/
/* Direction functions                  */
/****************************************/
/* The functions described here shift the pixel in a given */
/* direction using base functions */    
 
/* SQUARE */

/**
 * Moves the image in the direction 1 (SQUARE GRID)
 * This means the pixels are shifted towards the top of the image.
 * We then rebuild the image part above
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir1(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )

{
    PLINE *plines_germ_nbr;
    Uint32 i;

    plines_mask = &plines_mask[nb_lines-1];
    plines_germ_nbr = &plines_inout[nb_lines];
    plines_inout = &plines_inout[nb_lines-1];

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask--, plines_inout--, plines_germ_nbr--;
        BLD_LINE(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 2 (SQUARE GRID)
 * This means the pixels are shifted towards the top right of the image.
 * We then rebuild the image part above and to the right
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir2(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr;
    Uint32 i;

    plines_mask = &plines_mask[nb_lines-1];
    plines_germ_nbr = &plines_inout[nb_lines];
    plines_inout = &plines_inout[nb_lines-1];

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask--, plines_inout--, plines_germ_nbr--;
        BLD_LINE_RIGHT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 3 (SQUARE GRID)
 * This means the pixels are shifted towards the right of the image.
 * We then rebuild the image part to the right
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir3(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    Uint32 i;
    for(i = 0; i < nb_lines; i++) {
        BLD_LINE_RIGHT_HORZ(plines_inout,plines_mask,bytes_in,p_volume);
        plines_inout++, plines_mask++;
    }
}

/**
 * Moves the image in the direction 4 (SQUARE GRID)
 * This means the pixels are shifted towards the bottom right of the image.
 * We then rebuild the image part below and to the right
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir4(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    Uint32 i;
    PLINE *plines_germ_nbr = &plines_inout[-1];

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE_RIGHT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 5 (SQUARE GRID)
 * This means the pixels are shifted towards the bottom of the image.
 * We then rebuild the image part below
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir5(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr = &plines_inout[-1];
    Uint32 i;

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 6 (SQUARE GRID)
 * This means the pixels are shifted towards the bottom left of the image.
 * We then rebuild the image part below and to the left
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir6(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr = &plines_inout[-1];
    Uint32 i;

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE_LEFT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 7 (SQUARE GRID)
 * This means the pixels are shifted towards the left of the image.
 * We then rebuild the image part to the left
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir7(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    Uint32 i;
  
    for(i = 0; i < nb_lines; i++) {
        BLD_LINE_LEFT_HORZ(plines_inout,plines_mask,bytes_in,p_volume);
        plines_inout++, plines_mask++;
    }
}

/**
 * Moves the image in the direction 8 (SQUARE GRID)
 * This means the pixels are shifted towards the top left of the image.
 * We then rebuild the image part above and to the left
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir8(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr;
    Uint32 i;

    plines_mask = &plines_mask[nb_lines-1];
    plines_germ_nbr = &plines_inout[nb_lines];
    plines_inout = &plines_inout[nb_lines-1];

    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    for(i = 1; i < nb_lines; i++) {
        plines_mask--, plines_inout--, plines_germ_nbr--;
        BLD_LINE_LEFT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/* HEXAGONAL
 * Remark for the hex mode: we suppose that the first line of AOI
 * is always of even parity. This means that the line 0 of the image 
 * is of even parity,
 */

/**
 * Moves the image in the direction 1 (HEXAGONAL GRID)
 * This means the pixels are shifted towards the top right of the image.
 * We then rebuild the image part above and to the right
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_HBldDir1(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *p_germ_nbr, *p_mask, *p_inout;
    Uint32 i;

    p_inout = &plines_inout[nb_lines-1];
    p_mask = &plines_mask[nb_lines-1];
    p_germ_nbr = &plines_inout[nb_lines];

    /* do the last -- odd -- line */
    BLD_EDGE_LINE(p_inout,p_mask,bytes_in,p_volume);

    /* do the second-to-last line -- even */
    p_inout--, p_mask--, p_germ_nbr--;
    BLD_LINE_RIGHT(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);

    for(i = 2; i < nb_lines; i+=2) {
        /* do odd line */
        p_mask--, p_inout--, p_germ_nbr--;
        BLD_LINE(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);
        /* do even line */
        p_mask--, p_inout--, p_germ_nbr--;
        BLD_LINE_RIGHT(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 3 (HEXAGONAL GRID)
 * This means the pixels are shifted towards the bottom right of the image.
 * We then rebuild the image part below and to the right
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_HBldDir3(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr = &plines_inout[-1];
    Uint32 i;

    /* do the first -- even -- line */
    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    /* do the second -- odd -- line */
    plines_mask++, plines_inout++, plines_germ_nbr++;
    BLD_LINE(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);

    for(i = 2; i < nb_lines; i+=2) {
        /* do even line */
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE_RIGHT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
        /* do odd line */
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 4 (HEXAGONAL GRID)
 * This means the pixels are shifted towards the bottom left of the image.
 * We then rebuild the image part below and to the left
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_HBldDir4(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *plines_germ_nbr = &plines_inout[-1];
    Uint32 i;

    /* do the first -- even -- line */
    BLD_EDGE_LINE(plines_inout,plines_mask,bytes_in,p_volume);

    /* do the second -- odd -- line */
    plines_mask++, plines_inout++, plines_germ_nbr++;
    BLD_LINE_LEFT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);

    for(i = 2; i < nb_lines; i+=2) {
        /* do even line */
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
        /* do odd line */
        plines_mask++, plines_inout++, plines_germ_nbr++;
        BLD_LINE_LEFT(plines_inout,plines_germ_nbr,plines_mask,bytes_in,p_volume);
    }
}

/**
 * Moves the image in the direction 6 (HEXAGONAL GRID)
 * This means the pixels are shifted towards the top left of the image.
 * We then rebuild the image part above and to the left
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_HBldDir6(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{
    PLINE *p_germ_nbr, *p_mask, *p_inout;
    Uint32 i;

    /* do the last -- odd -- line */
    p_inout = &plines_inout[nb_lines-1];
    p_mask = &plines_mask[nb_lines-1];
    p_germ_nbr = &plines_inout[nb_lines];

    BLD_EDGE_LINE(p_inout,p_mask,bytes_in,p_volume);

    /* do the second -- odd -- line */
    p_mask--, p_inout--, p_germ_nbr--;
    BLD_LINE(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);

    for(i = 2; i < nb_lines; i += 2) {
        /* do even line */
        p_mask--, p_inout--, p_germ_nbr--;
        BLD_LINE_LEFT(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);
        /* do odd line */
        p_mask--, p_inout--, p_germ_nbr--;
        BLD_LINE(p_inout,p_germ_nbr,p_mask,bytes_in,p_volume);
    }
}

/* SPECIAL */

/**
 * Moves the image in the direction 0 (SQUARE GRID)
 * This amounts to no movement and a simple mask between the two images.
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_QBldDir0(PLINE *plines_inout,
                        PLINE *plines_mask,
                        Uint32 bytes_in, Uint32 nb_lines,
                        Uint64 *p_volume )
{ 
    Uint32 i;

    for(i = 0; i < nb_lines; i++,plines_inout++,plines_mask++) {
        BLD_LINE(plines_inout, plines_inout,plines_mask,bytes_in,p_volume);
    }
}


/**
 * Does nothing.
 * This function exists to handle impossible movement cases in hexagonal grid.
 * \param plines_inout pointer on the destination image lines
 * \param plines_mask pointer on the source image that is shifted pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines in the image processed
 * \param p_volume volume of the generated image
 */
static void MB_Stub(PLINE *plines_inout,
                    PLINE *plines_mask,
                    Uint32 bytes_in, Uint32 nb_lines,
                    Uint64 *p_volume )
{
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/** typedef for the definition of function arguments */
typedef void (NEIBFUNC) (PLINE *plines_inout,
                         PLINE *plines_mask,
                         Uint32 bytes_in, Uint32 nb_lines,
                         Uint64 *p_volume);

/** 
 * Array giving the function to use to go in a given direction with
 * regards to the grid in use (hexagonal or square).
 */
static NEIBFUNC *SwitchTo[2][9] =
{
  { /* Square directions */
     MB_QBldDir0,
     MB_QBldDir1,
     MB_QBldDir2,
     MB_QBldDir3,
     MB_QBldDir4,
     MB_QBldDir5,
     MB_QBldDir6,
     MB_QBldDir7,
     MB_QBldDir8
  },
  { /* Hexagonal directions */
     MB_QBldDir0,
     MB_HBldDir1,
     MB_QBldDir3,
     MB_HBldDir3,
     MB_HBldDir4,
     MB_QBldDir7,
     MB_HBldDir6,
     MB_Stub,
     MB_Stub
  }
};
