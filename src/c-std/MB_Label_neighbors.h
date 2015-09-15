/*
 * Copyright (c) <2014>, <Nicolas BEUCHER and ARMINES for the Centre de 
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
 
/******************************************
 * Grid functions                         *
 ******************************************
 * The functions described here perform labeling depending on the grid.
 */

/* SQUARE */

/*
 * Labelizes the object found in src image over a square grid.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines inside the image processed
 * \param labels the labels arrays and context
 */
static void MB_QLabel(PLINE *plines_out, PLINE *plines_in,
                      Uint32 bytes_in, Uint32 nb_lines,
                      MB_Label_struct *labels)
{
    Uint32 i;
   
    /* Do the first line */
    EDGE_LINE(plines_out[0],plines_in[0],bytes_in,labels);

    for(i=1; i<nb_lines; i++) {
        QLAB_LINE(plines_out,plines_in,i,bytes_in,labels);
    }
}

/* HEXAGONAL */

/*
 * Labelizes the object found in src image over an hexagonal grid.
 * \param plines_out pointer on the destination image lines
 * \param plines_in pointer on the source image pixel lines
 * \param bytes_in number of bytes inside the line
 * \param nb_lines number of lines inside the image processed
 * \param labels the labels arrays and context
 */
static void MB_HLabel(PLINE *plines_out, PLINE *plines_in,
                      Uint32 bytes_in, Uint32 nb_lines,
                      MB_Label_struct *labels)
{
    Uint32 i;
   
    /* Do the first -- even -- line */
    EDGE_LINE(plines_out[0],plines_in[0],bytes_in,labels);

    /* Do the second -- odd -- line */
    HLAB_LINE_ODD(plines_out,plines_in,1,bytes_in,labels);

    for(i=2; i<nb_lines; i+=2) {
        /* Do even line */
        HLAB_LINE_EVEN(plines_out,plines_in,i,bytes_in,labels);
        /* Do odd line */
        HLAB_LINE_ODD(plines_out,plines_in,i+1,bytes_in,labels);
    }
}

/***********************************************/
/* High level function and global variables    */
/***********************************************/

/* 
 * Array giving the function to use to go in a given direction with
 * regard to the grid in use (hexagonal or square).
 */
static LABELGRIDFUNC *SwitchTo[2] =
{ /* Square grid */
     MB_QLabel,
  /* Hexagonal grid*/
     MB_HLabel
};
