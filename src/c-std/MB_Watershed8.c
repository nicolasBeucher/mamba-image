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
typedef MB_Token (INSERTNB8) (void *ctx, int x, int y);

/* Structure holding the function contextual information 
 * such as the size of the processed image, the pointer to the pixel lines,
 * the array of tokens and the current flooding level.
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
    /*
     * List of pixels that will be inserted into the hierarchical list if the
     * the parent pixel (their neighbor which is currently processed) is
     * tagged 
     */
    MB_ListControl toreinsertList;
    
    /* Pointer to the lines of the marker image */
    PLINE *plines_marker;
    /* pointer to the line of the source image */
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
} MB_Watershed8_Ctx;

/****************************************
 * Hierarchical list functions          *
 ****************************************/

/*
 * Inserts a token in the hierarchical list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param value the value determines in which list to insert it
 */
static INLINE void MB_InsertInHierarchicalList(MB_Watershed8_Ctx *local_ctx, int x, int y, PIX8 value)
{
    int position;
    PIX32 *p;
    int lx, ly;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* Insertion in the hierarchical list */
    /* the value is normed as we do not want to process */
    /* already flooded level */
    value = (value < (local_ctx->current_water_level)) ? (local_ctx->current_water_level) : value;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->HierarchicalList[value].lastx;
    ly = local_ctx->HierarchicalList[value].lasty;
    position = lx+ly*local_ctx->width;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
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
    
    /* The marker image is updated with the tag value in the pixel position */
    p = (PIX32 *) (local_ctx->plines_marker[y] + x*4);
    *p = SET_STATUS(p,QUEUED);
}

/*
 * Initializes the hierarchical list with the marker image.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_HierarchyInit(MB_Watershed8_Ctx *local_ctx)
{
    Uint32 i,j;
    PIX32 *p;
    
    /* All the control are reset */
    for(i=0;i<256;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
    }
     
    /* The first marker are inserted inside the hierarchical list */
    local_ctx->current_water_level = 0;
    for(i=0; i<local_ctx->height; i++) {
        for(j=0; j<local_ctx->bytes_marker; j+=4) {
            p = (PIX32 *) (local_ctx->plines_marker[i] + j);
            if (READ_LABEL(p)!=0) {
                MB_InsertInHierarchicalList(local_ctx,j/4,i,0);
            } else {
                *p = CANDIDATE;
            }
        }
    }
}

/****************************************
 * Reinsert list functions              *
 ****************************************/
 
/*
 * Clears the reinsert list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_ClearReinsertList(MB_Watershed8_Ctx *local_ctx)
{
    local_ctx->toreinsertList.firstx = local_ctx->toreinsertList.lastx = MB_LIST_END;
    local_ctx->toreinsertList.firsty = local_ctx->toreinsertList.lasty = MB_LIST_END;
}

/*
 * Inserts in the reinsert list the pixel.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 */
static INLINE void MB_InsertInReinsertList(MB_Watershed8_Ctx *local_ctx, int x, int y)
{
    int position;
    int lx, ly;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->toreinsertList.lastx;
    ly = local_ctx->toreinsertList.lasty;
    position = lx+ly*local_ctx->width;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y;
        local_ctx->toreinsertList.lastx = x;
        local_ctx->toreinsertList.lasty = y;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->toreinsertList.firstx = x;
        local_ctx->toreinsertList.firsty = y;
        local_ctx->toreinsertList.lastx = x;
        local_ctx->toreinsertList.lasty = y;
    }
}

/*
 * Reinserts the pixels in the reinsert list (called only if the pixel which puts
 * them there is tagged).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_ReinsertFromList(MB_Watershed8_Ctx *local_ctx)
{
    int x,y,pos;
    MB_Token next_token;
    PIX8 value;

    x = local_ctx->toreinsertList.firstx;
    y = local_ctx->toreinsertList.firsty;
    while(x>=0) {
        /* The next token is evaluated first since reinsertion will destroy the info */
        pos = x+y*local_ctx->width;
        next_token = local_ctx->TokensArray[pos];
        /* The pixel is inserted into the hierarchical list */
        value = *(local_ctx->plines_src[y] + x);
        MB_InsertInHierarchicalList(local_ctx, x, y, value);
        /* The next pixel is extracted */
        x = next_token.nextx;
        y = next_token.nexty;
    }
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reaches their level (SQUARE GRID). Also
 * evaluates to which basin the pixel belongs or if it is a point of the 
 * watershed.
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 *
 * \return the function return the next token (pixel) that must be process
 */
static MB_Token MB_InsertNeighbors_square(void *ctx, int x, int y)
{
    Uint32 neighbor;
    PIX32 *p, *pix, tag;
    int nbx,nby,pos;
    MB_Watershed8_Ctx *local_ctx = (MB_Watershed8_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_marker[y] + x*4);
    *pix = SET_STATUS(pix,RG_LAB);
    
    /* We will then look at its neighbors and it will help us decide to which */
    /* marker the pixel belongs and also evaluate if the pixel might be in */
    /* the watershed. The neighbors not yet processed or inserted will be put */
    /* in the reinsert list to insert them later if the pixel is taggued at the */
    /* end. */
    
    /* The reinsert list is emptied */
    MB_ClearReinsertList(local_ctx);
    
    /* For the 8 neighbors of the pixel */
    for(neighbor=1; neighbor<9; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+sqNbDir[neighbor][0];
        nby = y+sqNbDir[neighbor][1];
        
        /* The neighbor must be in the image*/
        if (nbx>=0 && nbx<((int) local_ctx->width) &&
            nby>=0 && nby<((int) local_ctx->height) ) {
            p = (PIX32 *) (local_ctx->plines_marker[nby] + nbx*4);
            
            if( IS_PIXEL(p, CANDIDATE) ) {
                /* The neighbor is not inserted into the list yet */
                /* For the time being it is only put into the reinsert list */
                MB_InsertInReinsertList(local_ctx, nbx, nby);
            } else if ( IS_PIXEL(p, RG_LAB) ) {
                /* The neighbor has already been processed and tagged */
                tag = READ_LABEL(pix);
                if (tag==0) {
                    /* First neighbor we met with a tag, we take it */
                    /* for our pixel */
                    *pix |= READ_LABEL(p);
                } else if ( tag!=READ_LABEL(p) ) {
                    /* The tag of the neighbor is different that ours */
                    /* and the neighbor is not on the watershed */
                    /* the pixel belongs to the watershed */
                    *pix = SET_STATUS(pix,WTS_LAB);
                } 
            }
            /* Other case means that the neighbor is in the list but not processed */
        }
    }
    
    /* At this point if the pixel does not belong to the watershed */
    /* we insert its unprocessed and unlisted neighbor into the */
    /* hierarchical list. */
    if( !IS_PIXEL(pix, WTS_LAB) ) {
        MB_ReinsertFromList(local_ctx);
    }

    /* What is the next token to process */
    pos = x+y*local_ctx->width;
    return local_ctx->TokensArray[pos];
}

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reach their level (HEXAGONAL GRID). Also
 * evaluates to which basin the pixel belongs or if it is a point of the 
 * watershed.
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 */
static MB_Token MB_InsertNeighbors_hexagonal(void *ctx, int x, int y)
{
    Uint32 neighbor;
    PIX32 *p, *pix, tag;
    int nbx,nby,pos;
    MB_Watershed8_Ctx *local_ctx = (MB_Watershed8_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y */
    pix = (PIX32 *) (local_ctx->plines_marker[y] + x*4);
    *pix = SET_STATUS(pix,RG_LAB);
    
    /* We will then look at its neighbors and it will help us decide to which */
    /* marker the pixel belongs and also evaluate if the pixel might be in */
    /* the watershed. The neighbors not yet processed or inserted will be put */
    /* in the reinsert list to insert them later if the pixel is taggued at the */
    /* end. */
    
    /* The reinsert list is emptied */
    MB_ClearReinsertList(local_ctx);
    
    /* For the 6 neighbors of the pixel */
    for(neighbor=1; neighbor<7; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+hxNbDir[y%2][neighbor][0];
        nby = y+hxNbDir[y%2][neighbor][1];
        
        /* The neighbor must be in the image*/
        if (nbx>=0 && nbx<((int) local_ctx->width) &&
            nby>=0 && nby<((int) local_ctx->height) ) {
            p = (PIX32 *) (local_ctx->plines_marker[nby] + nbx*4);
            
            if( IS_PIXEL(p, CANDIDATE) ) {
                /* The neighbor is not inserted into the list yet */
                /* For the time being it is only put into the reinsert list */
                MB_InsertInReinsertList(local_ctx, nbx, nby);
            } else if ( IS_PIXEL(p, RG_LAB) ) {
                /* The neighbor has already been processed and tagged */
                tag = READ_LABEL(pix);
                if (tag==0) {
                    /* First neighbor we met with a tag, we take it */
                    /* for our pixel */
                    *pix = READ_LABEL(p);
                } else if ( tag!=READ_LABEL(p) ) {
                    /* The tag of the neighbor is different that ours */
                    /* and the neighbor is not on the watershed */
                    /* the pixel belongs to the watershed */
                    *pix = SET_STATUS(pix,WTS_LAB);
                } 
            }
            /* Other case means that the neighbor is in the list but not processed */
        }
    }
    
    /* At this point if the pixel does not belong to the watershed */
    /* we insert its unprocessed and unlisted neighbor into the */
    /* hierarchical list. */
    if( !IS_PIXEL(pix, WTS_LAB) ) {
        MB_ReinsertFromList(local_ctx);
    }

    /* What is the next token to process */
    pos = x+y*local_ctx->width;
    return local_ctx->TokensArray[pos];
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
 * \param max_level the maximum level reach by the water
 */
static INLINE void MB_Flooding(MB_Watershed8_Ctx *local_ctx, Uint32 max_level)
{
    Uint32 i;
    int fx,fy;
    MB_Token next_token;
    
    for(i=0; i<max_level; i++, local_ctx->current_water_level++) {
        fx = local_ctx->HierarchicalList[local_ctx->current_water_level].firstx;
        fy = local_ctx->HierarchicalList[local_ctx->current_water_level].firsty;
        while(fx>=0) {
            next_token = local_ctx->InsertNeighbors(local_ctx,fx,fy);
            fx = next_token.nextx;
            fy = next_token.nexty;
        }
    }
}

/*
 * Controls that all the pixels are tagged and if not tags them as being part of 
 * the watershed (at this point, untagged pixels are pixels completely surrounded
 * by watershed pixels).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_ControlPass(MB_Watershed8_Ctx *local_ctx)
{
    Uint32 i,j;
    PIX32 *p;
    
    /* All the pixels are checked */
    for(i=0; i<local_ctx->height; i++) {
        for(j=0; j<local_ctx->bytes_marker; j+=4) {
            p = (PIX32 *) (local_ctx->plines_marker[i] + j);
            switch ((*p)&0xFF000000) {
            case CANDIDATE:
                /* Untagged pixel */
                *p = SET_STATUS(p,WTS_LAB);
                break;
            default:
                break;
            }
        }
    }
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Performs a watershed segmentation of the image using the marker image
 * as a starting point for the flooding. The function builds the actual 
 * watershed line (idempotent) plus catchment basins (not idempotent). 
 * The result is put into the 32-bit marker image.
 *
 * The segmentation is coded as follows into the 32-bits values.
 * | 0      | 1      | 2      | 3      |
 * |--------|--------|--------|--------|
 * | Segment label            | isLine |
 * Each byte can be accessed using the function MB_CopyBytePlane. isLine is a value
 * indicating if the pixel belongs to the watershed (255 if this is the case, 
 * undefined otherwise).
 *
 * \param src the greyscale image to segment
 * \param marker the marker image in which the result of segmentation will be put
 * \param max_level the maximum level reach by the water.
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_Watershed8(MB_Image *src, MB_Image *marker, Uint32 max_level, enum MB_grid_t grid) {
    MB_Watershed8_Ctx local_ctx;
    
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
        /* In case allocation goes wrong */
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
    
    /* Control pass (only if all levels where flooded) */
    if (max_level==256) 
        MB_ControlPass(&local_ctx);
    
    /* Freeing the token array */
    MB_free(local_ctx.TokensArray);
    
    return MB_NO_ERR;
}
