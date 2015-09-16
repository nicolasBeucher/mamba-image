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
typedef void (TSWITCHEP) (void *ctx, int x, int y, int z);

/* Structure holding the function contextual information 
 * such as the size of the image processed, the pointer to the pixel lines
 * the array of tokens and the current flooding level.
 */
typedef struct {
    /* The width of the images processed */
    Uint32 width;
    /* The height of the images processed */
    Uint32 height;
    /* The length of the processed images */
    Uint32 length;
    
    /* The memory used to hold the elements of the hierarchical list */
    MB3D_Token *TokensArray;
    /* The hierarchical list entries for watershed segmentation */
    MB3D_ListControl List;
    
    /* Image sequence for the dest */
    MB_Image **seq_dest;
    /* Image sequence for the src */
    MB_Image **seq_src;
    
    /* The edge configuration */
    enum MB_edgemode_t edge;
    
    /* Meta function which redirects the neighbor function according to the grid */
    TSWITCHEP *InsertNeighbors;
} MB3D_Distanceb_Ctx;

/***************************************
 * list functions                       *
 ****************************************/

/*
 * Inserts a token in the list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param z the position in z of the concerned pixel
 */
static INLINE void MB3D_InsertInList(MB3D_Distanceb_Ctx *local_ctx, int x, int y, int z)
{
    int position;
    int lposition;
    int lx, ly, lz;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width + z*local_ctx->width*local_ctx->height;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    local_ctx->TokensArray[position].nextz = MB_LIST_END;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->List.lastx;
    ly = local_ctx->List.lasty;
    lz = local_ctx->List.lastz;
    lposition = lx+ly*local_ctx->width + lz*local_ctx->width*local_ctx->height;
    if (lposition>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[lposition].nextx = x;
        local_ctx->TokensArray[lposition].nexty = y;
        local_ctx->TokensArray[lposition].nextz = z;
        local_ctx->List.lastx = x;
        local_ctx->List.lasty = y;
        local_ctx->List.lastz = z;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->List.firstx = x;
        local_ctx->List.firsty = y;
        local_ctx->List.firstz = z;
        local_ctx->List.lastx = x;
        local_ctx->List.lasty = y;
        local_ctx->List.lastz = z;
    }
}

/*
 * Gets the pixel value at a given position.
 * \param im pointer on the source image pixel
 * \param x the position in the line
 * \param y the position in the line
 */
static INLINE PIX8 GET_PIX_1(MB_Image *im, Uint32 x, Uint32 y)
{
    PIX8 mask, offset;
   
    PIX8 *px = (PIX8 *) (im->plines[y] + (x/8));
    offset = (PIX8) (x&7);

    mask = (1<<offset);
   
    return (PIX8) (((*px)&mask) != 0);
}

/*
 * Initializes the list with the pixel inside the set border (CUBIC GRID).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_ListInit_cube(MB3D_Distanceb_Ctx *local_ctx)
{
    Uint32 x,y,z;
    PIX32 *p;
    Uint32 neighbor;
    int nbx,nby,nbz;
    MB_Image *imd, *ims;
    
    /* All the controls are reset */
    local_ctx->List.firstx = local_ctx->List.lastx = MB_LIST_END;
    local_ctx->List.firsty = local_ctx->List.lasty = MB_LIST_END;
    local_ctx->List.firstz = local_ctx->List.lastz = MB_LIST_END;
    
    /* The pixel in the set border are inserted inside the list */
    for(z=0; z<local_ctx->length; z++) {
        imd = local_ctx->seq_dest[z];
        ims = local_ctx->seq_src[z];
        for(y=0; y<local_ctx->height; y++) {
            p = (PIX32 *) (imd->plines[y]);
            for(x=0; x<local_ctx->width; x++, p++) {
                /* The pixel in the result image is put to 0 by default */
                *p = 0;
                /* If the pixel is not black */
                if (GET_PIX_1(ims, x, y))
                {
                    /* Looking for black neighbors */
                    /* For the 26 neighbors of the pixel */
                    for(neighbor=1; neighbor<27; neighbor++) {
                        /* Position and value in the marker image */
                        nbx = x+cubeNbDir[neighbor][0];
                        nby = y+cubeNbDir[neighbor][1];
                        nbz = z+cubeNbDir[neighbor][2];
                        
                        if (nbx>=0 && nbx<((int) local_ctx->width) && 
                            nby>=0 && nby<((int) local_ctx->height) &&
                            nbz>=0 && nbz<((int) local_ctx->length) ) {
                            /* If the neighbor is inside the image we look */
                            /* for its value. If the neighbor if False (black) */
                            /* then it means our pixel is in the set border */
                            if (!GET_PIX_1(local_ctx->seq_src[nbz], nbx, nby)) {
                                *p = 1;
                                MB3D_InsertInList(local_ctx, x, y, z);
                                /* We can stop here for this pixel */
                                break;
                            }
                        } else {
                            /* For a pixel at the edge of an image we take */
                            /* the value of the edge configuration to */
                            /* decide if it must be put inside the set border */
                            if (local_ctx->edge==MB_EMPTY_EDGE) {
                                *p = 1;
                                MB3D_InsertInList(local_ctx, x, y, z);
                                /* We can stop here for this pixel */
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}

/*
 * Initializes the list with the pixel inside the set border (FACE CENTERED CUBIC GRID).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_ListInit_fcc(MB3D_Distanceb_Ctx *local_ctx)
{
    Uint32 x,y,z;
    PIX32 *p;
    Uint32 neighbor;
    int nbx,nby,nbz,dirSelect;
    MB_Image *imd, *ims;
    
    /* All the controls are reset */
    local_ctx->List.firstx = local_ctx->List.lastx = MB_LIST_END;
    local_ctx->List.firsty = local_ctx->List.lasty = MB_LIST_END;
    local_ctx->List.firstz = local_ctx->List.lastz = MB_LIST_END;
    
    /* The pixel in the set border are inserted inside the list */
    for(z=0; z<local_ctx->length; z++) {
        imd = local_ctx->seq_dest[z];
        ims = local_ctx->seq_src[z];
        for(y=0; y<local_ctx->height; y++) {
            p = (PIX32 *) (imd->plines[y]);
            /* Computing the directions to use depending on the y and z of the */
            /* pixel */
            dirSelect = ((z%3)<<1)+(y%2);
            for(x=0; x<local_ctx->width; x++, p++) {
                /* The pixel in the result image is put to 0 by default */
                *p = 0;
                /* If the pixel is not black */
                if (GET_PIX_1(ims, x, y))
                {
                    /* Looking for black neighbors */
                    /* For the 26 neighbors of the pixel */
                    for(neighbor=1; neighbor<13; neighbor++) {
                        /* Position and value in the marker image */
                        nbx = x+fccNbDir[dirSelect][neighbor][0];
                        nby = y+fccNbDir[dirSelect][neighbor][1];
                        nbz = z+fccNbDir[dirSelect][neighbor][2];
                        
                        if (nbx>=0 && nbx<((int) local_ctx->width) && 
                            nby>=0 && nby<((int) local_ctx->height) &&
                            nbz>=0 && nbz<((int) local_ctx->length) ) {
                            /* If the neighbor is inside the image we look */
                            /* for its value. If the neighbor if False (black) */
                            /* then it means our pixel is in the set border */
                            if (!GET_PIX_1(local_ctx->seq_src[nbz], nbx, nby)) {
                                *p = 1;
                                MB3D_InsertInList(local_ctx, x, y, z);
                                /* We can stop here for this pixel */
                                break;
                            }
                        } else {
                            /* For a pixel at the edge of an image we take */
                            /* the value of the edge configuration to */
                            /* decide if it must be put inside the set border */
                            if (local_ctx->edge==MB_EMPTY_EDGE) {
                                *p = 1;
                                MB3D_InsertInList(local_ctx, x, y, z);
                                /* We can stop here for this pixel */
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}

/***************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y,z) in the list if they are
 * set to True (CUBE GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the y position of the pixel processed
 * \param z the z position of the pixel processed
 */
static void MB3D_InsertNeighbors_cube(void *ctx, int x, int y, int z)
{
    Uint32 neighbor;
    PIX32 *p, *pix;
    int nbx,nby,nbz;
    MB_Image *im;
    MB3D_Distanceb_Ctx *local_ctx = (MB3D_Distanceb_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    im = local_ctx->seq_dest[z];
    pix = (PIX32 *) (im->plines[y] + x*4);
    
    /* For the 26 neighbors of the pixel */
    for(neighbor=1; neighbor<27; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+cubeNbDir[neighbor][0];
        nby = y+cubeNbDir[neighbor][1];
        nbz = z+cubeNbDir[neighbor][2];
        
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) &&
            nbz>=0 && nbz<((int) local_ctx->length) ) {
            
            im = local_ctx->seq_dest[nbz];
            p = (PIX32 *) (im->plines[nby] + nbx*4);
            /* If the neighbor is inside the image we look */
            /* for its value and if it has already been processed */
            /* a True pixel not process is then added */
            if (GET_PIX_1(local_ctx->seq_src[nbz], nbx, nby) &&
                (*p==0) ) {
                *p = *pix+1;
                MB3D_InsertInList(local_ctx, nbx, nby, nbz);
            }
        }
    }
}

/*
 * Inserts the neighbors of pixel (x,y,z) in the list if they are
 * set to True (FACE CENTERED CUBIC GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the y position of the pixel processed
 * \param z the z position of the pixel processed
 */
static void MB3D_InsertNeighbors_fcc(void *ctx, int x, int y, int z)
{
    Uint32 neighbor;
    PIX32 *p, *pix;
    int nbx,nby,nbz,dirSelect;
    MB_Image *im;
    MB3D_Distanceb_Ctx *local_ctx = (MB3D_Distanceb_Ctx *) ctx;
    
    /* Computing the directions to use depending on the y and z of the */
    /* pixel */
    dirSelect = ((z%3)<<1)+(y%2);
    
    /* The tag value is the value of the marker image in x,y */
    im = local_ctx->seq_dest[z];
    pix = (PIX32 *) (im->plines[y] + x*4);
    
    /* For the 12 neighbors of the pixel */
    for(neighbor=1; neighbor<13; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+fccNbDir[dirSelect][neighbor][0];
        nby = y+fccNbDir[dirSelect][neighbor][1];
        nbz = z+fccNbDir[dirSelect][neighbor][2];
        
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) &&
            nbz>=0 && nbz<((int) local_ctx->length) ) {
            
            im = local_ctx->seq_dest[nbz];
            p = (PIX32 *) (im->plines[nby] + nbx*4);
            /* If the neighbor is inside the image we look */
            /* for its value and if it has already been processed */
            /* a True pixel not process is then added */
            if (GET_PIX_1(local_ctx->seq_src[nbz], nbx, nby) &&
                (*p==0) ) {
                *p = *pix+1;
                MB3D_InsertInList(local_ctx, nbx, nby, nbz);
            }
        }
    }
}

/***************************************
 * Process function                     *
 ****************************************/
 
/*
 * Start the distance computation using the initialized list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_Process(MB3D_Distanceb_Ctx *local_ctx)
{
    int fx,fy,fz,pos;
    
    fx = local_ctx->List.firstx;
    fy = local_ctx->List.firsty;
    fz = local_ctx->List.firstz;
    while(fx>=0) {
        pos = fx+fy*local_ctx->width+fz*local_ctx->width*local_ctx->height;
        local_ctx->InsertNeighbors(local_ctx,fx,fy,fz);
        fx = local_ctx->TokensArray[pos].nextx;
        fy = local_ctx->TokensArray[pos].nexty;
        fz = local_ctx->TokensArray[pos].nextz;
    }
}

/***********************************************/
/*High level function and global variables      */
/***********************************************/

/*
 * Computes for each pixel the distance to the edge of the set in which the
 * pixel is found.
 *
 * The algorithm works with a list.
 *
 * \param src the binary source 3D image
 * \param dest the 32-bits 3D image in which the distance for each pixel is stored
 * \param grid the grid used (either cubic or face_center_cubic)
 * \param edge the kind of edge to use (behavior for pixels near edge depends on it)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Distanceb(MB3D_Image *src, MB3D_Image *dest, enum MB3D_grid_t grid, enum MB_edgemode_t edge) {
    MB3D_Distanceb_Ctx local_ctx;
    
    /* Verification over depth and size */
    if (!MB3D_CHECK_SIZE_2(src, dest)) {
        return MB_ERR_BAD_SIZE;
    }

    /* Only grey scale images can be segmented */
    /* the marker image is 32-bit */
    switch (MB3D_PROBE_PAIR(src, dest)) {
    case MB_PAIR_1_32:
        break;
    default:
        return MB_ERR_BAD_DEPTH;
    }
    /* Invalid grid case */
    if (grid==MB3D_INVALID_GRID)
        return MB_ERR_BAD_PARAMETER;
        
    /* Local context initialisation */
    local_ctx.width = src->seq[0]->width;
    local_ctx.height = src->seq[0]->height;
    local_ctx.length = src->length;
    local_ctx.edge = edge;

    /* Setting up pointers */
    local_ctx.seq_src = &src->seq[0];
    local_ctx.seq_dest = &dest->seq[0];
    
    /* Allocating the token array */
    local_ctx.TokensArray = MB_malloc(local_ctx.width*local_ctx.height*local_ctx.length*sizeof(MB3D_Token));
    if(local_ctx.TokensArray==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    
    /* Grid initialisation */
    if (grid==MB3D_CUBIC_GRID) {
        local_ctx.InsertNeighbors = MB3D_InsertNeighbors_cube;
        /* List initialisation */
        MB3D_ListInit_cube(&local_ctx);
    } else {
        local_ctx.InsertNeighbors = MB3D_InsertNeighbors_fcc;
        /* List initialisation */
        MB3D_ListInit_fcc(&local_ctx);
    }

    /* Actual Process */
    MB3D_Process(&local_ctx);
    
    /* Freeing the token array */
    MB_free(local_ctx.TokensArray);
    
    return MB_NO_ERR;
}
