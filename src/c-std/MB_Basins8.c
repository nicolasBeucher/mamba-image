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

/* typedef for the definition of neighbor function arguments */
typedef void (INSERTNB8) (void *ctx, int x, int y);

/* Structure holding the function contextual information 
 * such as the size of the processed image, the pointer to the pixel lines,
 * the array of tokens and the current flooding level
 */
typedef struct {
    /* The width of the processed images */
    Uint32 width;
    /* The height of the processed images */
    Uint32 height;
    
    /* The memory used to hold the elements of the hierarchical list */
    MB_Token *TokensArray;
    /* The hierarchical list entries for watershed segmentation */
    MB_ListControl HierarchicalList[256];
    
    /* Pointer to the lines of the marker image */
    PLINE *plines_marker;
    /* Pointer to the lines of the source image */
    PLINE *plines_src;
    /* Size in byte of the marker image lines */
    Uint32 bytes_marker;
    
    /* Variable indicating which level in the hierarchical list
     * the "water" has attained. Only this level and above can be filled with new
     * tokens.
     */
    PIX8 current_water_level;
    
    /* Meta function which redirects the neighbor function according to the grid */
    INSERTNB8 *InsertNeighbors;
} MB_Basins8_Ctx;


/****************************************
 * Hierarchical list functions          *
 ****************************************/

/*
 * Inserts a token in the hierarchical list
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param bytes number of bytes inside the line
 */
static INLINE void MB_InsertInHierarchicalList(MB_Basins8_Ctx *local_ctx, int x, int y, PIX8 value)
{
    int position;
    int lx, ly;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* Insertion in the hierarchical list */
    /* the value is normed as we do not want to process */
    /* already flooded levels */
    value = (value < (local_ctx->current_water_level)) ? (local_ctx->current_water_level) : value;
    /* The token is inserted after the last value in the list */
    lx = local_ctx->HierarchicalList[value].lastx;
    ly = local_ctx->HierarchicalList[value].lasty;
    position = lx+ly*local_ctx->width;
    if (position>=0) {
        /*There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->HierarchicalList[value].firstx = x;
        local_ctx->HierarchicalList[value].firsty = y;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
    }
}

/*
 * Initializes the hierarchical list with the marker image
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_HierarchyInit(MB_Basins8_Ctx *local_ctx)
{
    Uint32 i,j;
    PIX32 *p;

    /*All the controls are reset */
    for(i=0;i<256;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
    }

    /* The first markers are inserted inside the hierarchical list */
    /* all the other pixels are tagged as not processed */
    local_ctx->current_water_level = 0;
    for(i=0; i<local_ctx->height; i++) {
        for(j=0; j<local_ctx->bytes_marker; j+=4) {
            p = (PIX32 *) (local_ctx->plines_marker[i] + j);
            if (((*p)&0x00ffffff)!=0)
                MB_InsertInHierarchicalList(local_ctx,j/4,i,0);
            else
                *p = 0x01000000;
        }
    }
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reaches their level (SQUARE GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 */
static void MB_InsertNeighbors_square(void *ctx, int x, int y)
{
    Uint32 i;
    PIX32 *p, *pix;
    PIX8 value;
    int nbx,nby;
    MB_Basins8_Ctx *local_ctx = (MB_Basins8_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_marker[y] + x*4);
    *pix &= 0x00FFFFFF;
    
    /* For the 8 neighbors of the pixel */
    for(i=1; i<9; i++) {
        /* Position and value in the marker image */
        nbx = x+sqNbDir[i][0];
        nby = y+sqNbDir[i][1];
        
        /* The neighbor must be in the image and not yet tagged in the marker image */
        if (nbx>=0 && nbx<((int) local_ctx->width) && nby>=0 && nby<((int) local_ctx->height)) {
            p = (PIX32 *) (local_ctx->plines_marker[nby] + nbx*4);
            
            if ((*p)==0x01000000) {
                /* The neighbor is not tagged yet */
                value = *(local_ctx->plines_src[nby] + nbx);
                MB_InsertInHierarchicalList(local_ctx, nbx, nby, value);
                /* The neighbor is updated with the pixel tag value*/
                *p |= *pix;
            }
        }
    }
}

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reaches their level (HEXAGONAL GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 */
static void MB_InsertNeighbors_hexagonal(void *ctx, int x, int y)
{
    Uint32 i;
    PIX32 *p, *pix;
    PIX8 value;
    int nbx,nby;
    MB_Basins8_Ctx *local_ctx = (MB_Basins8_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_marker[y] + x*4);
    *pix = *pix & 0x00FFFFFF;
    
    /* For the 6 neighbors of the pixel */
    for(i=1; i<7; i++) {
        /* Position and value in the marker image */
        nbx = x+hxNbDir[y%2][i][0];
        nby = y+hxNbDir[y%2][i][1];
        
        /* The neighbor must be in the image and not yet tagged in the marker image */
        if (nbx>=0 && nbx<((int) local_ctx->width) && nby>=0 && nby<((int) local_ctx->height)) {
            p = (PIX32 *) (local_ctx->plines_marker[nby] + nbx*4);
            
            if ((*p)==0x01000000) {
                /* The neighbor is not tagged yet */
                value = *(local_ctx->plines_src[nby] + nbx);
                MB_InsertInHierarchicalList(local_ctx, nbx, nby, value);
                /* The neighbor is updated with the pixel tag value*/
                *p |= *pix;
            }
        }
    }
}

/****************************************
 * Flooding function                    *
 ****************************************/
 
/*
 * Simulates the flooding process using the hierarchical list. Tokens are
 * extracted out of the current water level list and processed. The process consists
 * in inserting in the list all its neighbors that are not already processed.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param max_level the maximum level reached by the water
 */
static INLINE void MB_Flooding(MB_Basins8_Ctx *local_ctx, Uint32 max_level)
{
    int fx,fy,pos;
    Uint32 i;
    
    for(i=0; i<max_level; i++, local_ctx->current_water_level++) {
        fx = local_ctx->HierarchicalList[local_ctx->current_water_level].firstx;
        fy = local_ctx->HierarchicalList[local_ctx->current_water_level].firsty;
        while(fx>=0) {
            pos = fx+fy*local_ctx->width;
            local_ctx->InsertNeighbors(local_ctx,fx,fy);
            fx = local_ctx->TokensArray[pos].nextx;
            fy = local_ctx->TokensArray[pos].nexty;
        }
    }
}

/************************************************/
/* High level function and global variables     */
/************************************************/

/*
 * Performs a watershed segmentation of the image using the marker image
 * as a starting point for the flooding. The function returns the catchment 
 * basins of the watershed but no actual watershed line. It is recommended
 * to use this functions rather than MB_Watershed if you are only interested
 * in catchment basins (faster).
 * The result is put into a the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32 bit values.
 * | 0      | 1      | 2      | 3      |
 * |--------|--------|--------|--------|
 * | Segment label            | Unused |
 * Each byte can be accessed using the function MB_CopyBytePlane.
 *
 * \param src the greyscale image to be segmented
 * \param marker the marker image in which the result of segmentation will be put
 * \param max_level the maximum level reached by the water.
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Basins8(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid) {
    MB_Basins8_Ctx local_ctx;
    
    /* Maximum level for flood cannot be greater than 256 */
    if (max_level>256)
        return MB_ERR_BAD_VALUE;
    if (max_level==0) max_level=256;
    
    /* Local context initialisation */
    local_ctx.width = src->width;
    local_ctx.height = src->height;

    /* Setting up pointers */
    local_ctx.plines_src = src->plines;
    local_ctx.plines_marker = marker->plines;
    local_ctx.bytes_marker = MB_LINE_COUNT(marker);
    
    /* Allocating the token array */
    local_ctx.TokensArray = MB_malloc(src->width*src->height*sizeof(MB_Token));
    if(local_ctx.TokensArray==NULL){
        /* in case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    
    /* Grid initialisation */
    if (grid==MB_SQUARE_GRID) {
         local_ctx.InsertNeighbors = MB_InsertNeighbors_square;
     } else {
         local_ctx.InsertNeighbors = MB_InsertNeighbors_hexagonal;
    }

    /* Initialisation */
    MB_HierarchyInit(&local_ctx);
    
    /* Actual flooding */
    MB_Flooding(&local_ctx, max_level);
    
    /* Freeing the token array */
    MB_free(local_ctx.TokensArray);
    
    return MB_NO_ERR;
}
