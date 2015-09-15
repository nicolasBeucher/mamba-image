/*
 * Copyright (c) <2012>, <Nicolas BEUCHER>
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

/* typedef for the definition of neighbor function arguments */
typedef void (INSERTNB) (void *ctx, int x, int y);

/* Structure holding the function contextual information 
 * such as the size of the processed image, the pointer to the pixel lines
 * the array of tokens and the current flooding level
 */
typedef struct {
    /* The width of the processed images */
    Uint32 width;
    /* The height of the processed images */
    Uint32 height;
    
    /* The memory used to hold the elements of the hierarchical list */
    MB_Token *TokensArray;
    /* The list entries for computation */
    MB_ListControl List;
    
    /* Pointer to the lines of the dest image */
    PLINE *plines_dest;
    /* Pointer to the lines of the src image */
    PLINE *plines_src;
    
    /* The edge configuration */
    enum MB_edgemode_t edge;
    
    /* Meta function which redirects the neighbor function according to the grid */
    INSERTNB *InsertNeighbors;
} MB_Distanceb_Ctx;

/****************************************
 * list functions                       *
 ****************************************/

/*
 * Inserts a token in the list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 */
static INLINE void MB_InsertInList(MB_Distanceb_Ctx *local_ctx, int x, int y)
{
    int position;
    int lposition;
    int lx, ly;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->List.lastx;
    ly = local_ctx->List.lasty;
    lposition = lx+ly*local_ctx->width;
    if (lposition>=0) {
        /*There is a last value, the list is not empty*/
        local_ctx->TokensArray[lposition].nextx = x;
        local_ctx->TokensArray[lposition].nexty = y;
        local_ctx->List.lastx = x;
        local_ctx->List.lasty = y;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->List.firstx = x;
        local_ctx->List.firsty = y;
        local_ctx->List.lastx = x;
        local_ctx->List.lasty = y;
    }
}

/*
 * Gets the pixel value at a given position.
 * \param im pointer on the source image pixel
 * \param x the position in the line
 * \param y the position in the line
 */
static INLINE PIX8 GET_PIX_1(PLINE line, Uint32 x)
{
    PIX8 mask, offset;
   
    PIX8 *px = (PIX8 *) (line + (x/8));
    offset = (PIX8) (x&7);

    mask = (1<<offset);
   
    return (PIX8) (((*px)&mask) != 0);
}

/*
 * Initializes the list with the pixel inside the set border (SQUARE GRID).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_ListInit_square(MB_Distanceb_Ctx *local_ctx)
{
    Uint32 x,y;
    PIX32 *p;
    Uint32 neighbor;
    int nbx,nby;

    /*All the controls are reset */
    local_ctx->List.firstx = local_ctx->List.lastx = MB_LIST_END;
    local_ctx->List.firsty = local_ctx->List.lasty = MB_LIST_END;
    
    /* The pixel in the set border are inserted inside the list */
    for(y=0; y<local_ctx->height; y++) {
        p = (PIX32 *) (local_ctx->plines_dest[y]);
        for(x=0; x<local_ctx->width; x++, p++) {
            /* The pixel in the result image is put to 0 by default */
            *p = 0;
            /* If the pixel is not black */
            if (GET_PIX_1(local_ctx->plines_src[y], x))
            {
                /* Looking for black neighbors */
                /* For the 8 neighbors of the pixel */
                for(neighbor=1; neighbor<9; neighbor++) {
                    /* Position and value in the marker image */
                    nbx = x+sqNbDir[neighbor][0];
                    nby = y+sqNbDir[neighbor][1];
                    
                    if (nbx>=0 && nbx<((int) local_ctx->width) && 
                        nby>=0 && nby<((int) local_ctx->height) ) {
                        /* If the neighbor is inside the image we look */
                        /* for its value. If the neighbor if False (black) */
                        /* then it means our pixel is in the set border */
                        if (!GET_PIX_1(local_ctx->plines_src[nby], nbx)) {
                            *p = 1;
                            MB_InsertInList(local_ctx, x, y);
                            /* We can stop here for this pixel */
                            break;
                        }
                    } else {
                        /* For a pixel at the edge of an image we take */
                        /* the value of the edge configuration to */
                        /* decide if it must be put inside the set border */
                        if (local_ctx->edge==MB_EMPTY_EDGE) {
                            *p = 1;
                            MB_InsertInList(local_ctx, x, y);
                            /* We can stop here for this pixel */
                            break;
                        }
                    }
                }
            }
        }
    }
}

/*
 * Initializes the list with the pixel inside the set border (HEXAGONAL GRID).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_ListInit_hexagonal(MB_Distanceb_Ctx *local_ctx)
{
    Uint32 x,y;
    PIX32 *p;
    Uint32 neighbor;
    int nbx,nby,dirSelect;
    
    /*All the controls are reset */
    local_ctx->List.firstx = local_ctx->List.lastx = MB_LIST_END;
    local_ctx->List.firsty = local_ctx->List.lasty = MB_LIST_END;
    
    /* The pixel in the set border are inserted inside the list */
    for(y=0; y<local_ctx->height; y++) {
        p = (PIX32 *) (local_ctx->plines_dest[y]);
        /* Computing the directions to use depending on the y of the */
        /* pixel */
        dirSelect = (y%2);
        for(x=0; x<local_ctx->width; x++, p++) {
            /* The pixel in the result image is put to 0 by default */
            *p = 0;
            /* If the pixel is not black */
            if (GET_PIX_1(local_ctx->plines_src[y], x))
            {
                /* Looking for black neighbors */
                /* For the 6 neighbors of the pixel */
                for(neighbor=1; neighbor<7; neighbor++) {
                    /*position and value in the marker image */
                    nbx = x+hxNbDir[dirSelect][neighbor][0];
                    nby = y+hxNbDir[dirSelect][neighbor][1];
                    
                    if (nbx>=0 && nbx<((int) local_ctx->width) && 
                        nby>=0 && nby<((int) local_ctx->height) ) {
                        /* If the neighbor is inside the image we look */
                        /* for its value. If the neighbor if False (black) */
                        /* then it means our pixel is in the set border */
                        if (!GET_PIX_1(local_ctx->plines_src[nby], nbx)) {
                            *p = 1;
                            MB_InsertInList(local_ctx, x, y);
                            /* We can stop here for this pixel */
                            break;
                        }
                    } else {
                        /* For a pixel at the edge of an image we take */
                        /* the value of the edge configuration to */
                        /* decide if it must be put inside the set border */
                        if (local_ctx->edge==MB_EMPTY_EDGE) {
                            *p = 1;
                            MB_InsertInList(local_ctx, x, y);
                            /* We can stop here for this pixel */
                            break;
                        }
                    }
                }
            }
        }
    }
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y) in the list if they are
 * set to True (SQUARE GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the y position of the pixel processed
 */
static void MB_InsertNeighbors_square(void *ctx, int x, int y)
{
    Uint32 neighbor;
    PIX32 *p, *pix;
    int nbx,nby;
    MB_Distanceb_Ctx *local_ctx = (MB_Distanceb_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_dest[y] + x*4);
    
    /* For the 8 neighbors of the pixel */
    for(neighbor=1; neighbor<9; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+sqNbDir[neighbor][0];
        nby = y+sqNbDir[neighbor][1];
        
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) ) {
            
            p = (PIX32 *) (local_ctx->plines_dest[nby] + nbx*4);
            /* If the neighbor is inside the image we look */
            /* for its value and if it has already been processed */
            /* a True pixel not process is then added */
            if (GET_PIX_1(local_ctx->plines_src[nby], nbx) && (*p==0) ) {
                *p = *pix+1;
                MB_InsertInList(local_ctx, nbx, nby);
            }
        }
    }
}

/*
 * Inserts the neighbors of pixel (x,y) in the list if they are
 * set to True (HEXAGONAL GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the y position of the pixel processed
 */
static void MB_InsertNeighbors_hexagonal(void *ctx, int x, int y)
{
    Uint32 neighbor;
    PIX32 *p, *pix;
    int nbx,nby,dirSelect;
    MB_Distanceb_Ctx *local_ctx = (MB_Distanceb_Ctx *) ctx;
    
    /* Computing the directions to use depending on the y of the */
    /* pixel */
    dirSelect = (y%2);
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_dest[y] + x*4);
    
    /* For the 6 neighbors of the pixel */
    for(neighbor=1; neighbor<7; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+hxNbDir[dirSelect][neighbor][0];
        nby = y+hxNbDir[dirSelect][neighbor][1];
        
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) ) {
            
            p = (PIX32 *) (local_ctx->plines_dest[nby] + nbx*4);
            /* If the neighbor is inside the image we look */
            /* for its value and if it has already been processed */
            /* a True pixel not process is then added */
            if (GET_PIX_1(local_ctx->plines_src[nby], nbx) && (*p==0) ) {
                *p = *pix+1;
                MB_InsertInList(local_ctx, nbx, nby);
            }
        }
    }
}

/****************************************
 * Process function                     *
 ****************************************/
 
/*
 * Start the distance computation using the initialized list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_Process(MB_Distanceb_Ctx *local_ctx)
{
    int fx,fy,pos;
    
    fx = local_ctx->List.firstx;
    fy = local_ctx->List.firsty;
    while(fx>=0) {
        pos = fx+fy*local_ctx->width;
        local_ctx->InsertNeighbors(local_ctx,fx,fy);
        fx = local_ctx->TokensArray[pos].nextx;
        fy = local_ctx->TokensArray[pos].nexty;
    }
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Computes for each pixel the distance to the edge of the set in which the
 * pixel is found.
 *
 * The algorithm works with a list.
 *
 * \param src the binary source image
 * \param dest the 32-bits image in which the distance for each pixel is stored
 * \param grid the grid used (either hexagonal or square)
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Distanceb(MB_Image *src, MB_Image *dest, enum MB_grid_t grid, enum MB_edgemode_t edge)
{
    MB_Distanceb_Ctx local_ctx;
    
    /* Verification over depth and size */
    if (!MB_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Only grey scale images can be segmented */
    /* the marker image is 32-bit */
    switch (MB_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }
    
    /* Local context initialisation */
    local_ctx.width = src->width;
    local_ctx.height = src->height;
    local_ctx.edge = edge;

    /* Setting up pointers */
    local_ctx.plines_src = src->plines;
    local_ctx.plines_dest = dest->plines;
    
    /* Allocating the token array */
    local_ctx.TokensArray = malloc(local_ctx.width*local_ctx.height*sizeof(MB_Token));
    if(local_ctx.TokensArray==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }

    /* Grid initialisation */
    if (grid==MB_SQUARE_GRID) {
         local_ctx.InsertNeighbors = MB_InsertNeighbors_square;
        /* List initialisation */
        MB_ListInit_square(&local_ctx);
     } else {
         local_ctx.InsertNeighbors = MB_InsertNeighbors_hexagonal;
        /* List initialisation */
        MB_ListInit_hexagonal(&local_ctx);
    }

    /* Actual Process */
    MB_Process(&local_ctx);
    
    /* Freeing the token array */
    free(local_ctx.TokensArray);
    
    return MB_NO_ERR;
}
