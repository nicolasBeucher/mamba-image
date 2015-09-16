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

/* typedef for the definition of neighbor function arguments */
typedef MB3D_Token (INSERTNB8) (void *ctx, int x, int y, int z);

/* Structure holding the function contextual information 
 * such as the size of the processed image, the pointer to the pixel lines,
 * the array of tokens and the current flooding level.
 */
typedef struct {
    /* The width of the processed images */
    Uint32 width;
    /* The height of the processed images */
    Uint32 height;
    /* The length of the processed images */
    Uint32 length;
    
    /* The memory used to hold the elements of the hierarchical list */
    MB3D_Token *TokensArray;
    /* The hierarchical list entries for watershed segmentation */
    MB3D_ListControl HierarchicalList[256];
    /*
     * List of pixels that will be inserted into the hierarchical list if the
     * the parent pixel (their neighbor which is currently processed) is
     * tagged 
     */
    MB3D_ListControl toreinsertList;
    
    /* Image sequence for the marker */
    MB_Image **seq_marker;
    /* Image sequence for the src */
    MB_Image **seq_src;
    /* Size in byte of the marker image lines */
    Uint32 bytes_marker;
    
    /* Variable indicating which level in the hierarchical list
     * the "water" as attained. Only this level and above can be filled with new
     * tokens.
     */
    PIX8 current_water_level;
    
    /* Meta function which redirects the neighbor function according to the grid */
    INSERTNB8 *InsertNeighbors;
} MB3D_Watershed8_Ctx;

/****************************************
 * Hierarchical list functions          *
 ****************************************/

/*
 * Inserts a token in the hierarchical list.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param z the position in y of the concerned pixel
 * \param value the value determines in which list to insert it
 */
static INLINE void MB3D_InsertInHierarchicalList(
    MB3D_Watershed8_Ctx *local_ctx,
    int x, int y, int z,
    PIX8 value)
{
    int position;
    PIX32 *p;
    int lx, ly, lz;
    MB_Image *im;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width + z*local_ctx->width*local_ctx->height;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    local_ctx->TokensArray[position].nextz = MB_LIST_END;
    
    /* Insertion in the hierarchical list */
    /* The value is normed as we do not want to process */
    /* already flooded level */
    value = (value < (local_ctx->current_water_level)) ? (local_ctx->current_water_level) : value;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->HierarchicalList[value].lastx;
    ly = local_ctx->HierarchicalList[value].lasty;
    lz = local_ctx->HierarchicalList[value].lastz;
    position = lx+ly*local_ctx->width+lz*local_ctx->width*local_ctx->height;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y;
        local_ctx->TokensArray[position].nextz = z;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
        local_ctx->HierarchicalList[value].lastz = z;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->HierarchicalList[value].firstx = x;
        local_ctx->HierarchicalList[value].firsty = y;
        local_ctx->HierarchicalList[value].firstz = z;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
        local_ctx->HierarchicalList[value].lastz = z;
    }
    
    /* The marker image is updated with the tag value in the pixel position */
    im = local_ctx->seq_marker[z];
    p = (PIX32 *) (im->plines[y] + x*4);
    *p = SET_STATUS(p,QUEUED);
}

/*
 * Initializes the hierarchical list with the marker image.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_HierarchyInit(MB3D_Watershed8_Ctx *local_ctx)
{
    Uint32 x,y,z,i;
    PIX32 *p;
    MB_Image *im;
    
    /* All the control are reset */
    for(i=0;i<256;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
        local_ctx->HierarchicalList[i].firstz = local_ctx->HierarchicalList[i].lastz = MB_LIST_END;
    }
    
    /* The first marker are inserted inside the hierarchical list */
    local_ctx->current_water_level = 0;
    for(z=0; z<local_ctx->length; z++) {
        im = local_ctx->seq_marker[z];
        for(y=0; y<local_ctx->height; y++) {
            for(x=0; x<local_ctx->bytes_marker; x+=4) {
                p = (PIX32 *) (im->plines[y] + x);
                if (READ_LABEL(p)!=0) {
                    MB3D_InsertInHierarchicalList(local_ctx,x/4,y,z,0);
                } else {
                    *p = CANDIDATE;
                }
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
static INLINE void MB3D_ClearReinsertList(MB3D_Watershed8_Ctx *local_ctx)
{
    local_ctx->toreinsertList.firstx = local_ctx->toreinsertList.lastx = MB_LIST_END;
    local_ctx->toreinsertList.firsty = local_ctx->toreinsertList.lasty = MB_LIST_END;
    local_ctx->toreinsertList.firstz = local_ctx->toreinsertList.lastz = MB_LIST_END;
}

/*
 * Inserts in the reinsert list the pixel.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 */
static INLINE void MB3D_InsertInReinsertList(
    MB3D_Watershed8_Ctx *local_ctx,
    int x, int y, int z)
{
    int position;
    int lx, ly, lz;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width + z*local_ctx->width*local_ctx->height;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    local_ctx->TokensArray[position].nextz = MB_LIST_END;
    
    /* The token is inserted after the last value in the list */
    lx = local_ctx->toreinsertList.lastx;
    ly = local_ctx->toreinsertList.lasty;
    lz = local_ctx->toreinsertList.lastz;
    position = lx+ly*local_ctx->width+lz*local_ctx->width*local_ctx->height;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y;
        local_ctx->TokensArray[position].nextz = z;
        local_ctx->toreinsertList.lastx = x;
        local_ctx->toreinsertList.lasty = y;
        local_ctx->toreinsertList.lastz = z;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->toreinsertList.firstx = x;
        local_ctx->toreinsertList.firsty = y;
        local_ctx->toreinsertList.firstz = z;
        local_ctx->toreinsertList.lastx = x;
        local_ctx->toreinsertList.lasty = y;
        local_ctx->toreinsertList.lastz = z;
    }
}

/*
 * Reinserts the pixels in the reinsert list (called only if the pixel which puts
 * them there is taggued).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_ReinsertFromList(MB3D_Watershed8_Ctx *local_ctx)
{
    int x,y,z,pos;
    MB3D_Token next_token;
    PIX8 value;
    MB_Image *im;

    x = local_ctx->toreinsertList.firstx;
    y = local_ctx->toreinsertList.firsty;
    z = local_ctx->toreinsertList.firstz;
    while(x>=0) {
        /* The next token is evaluated first since reinsertion will destroy the info */
        pos = x+y*local_ctx->width+z*local_ctx->width*local_ctx->height;
        next_token = local_ctx->TokensArray[pos];
        /* The pixel is inserted into the hierarchical list */
        im = local_ctx->seq_src[z];
        value = *(im->plines[y] + x);
        MB3D_InsertInHierarchicalList(local_ctx, x, y, z, value);
        /* The next pixel is extracted */
        x = next_token.nextx;
        y = next_token.nexty;
        z = next_token.nextz;
    }
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y,z) in the hierarchical list so that they
 * can be flooded when the water reaches their level (CUBE GRID). Also
 * evaluates to which basin the pixel belongs or if it is a point of the 
 * watershed.
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 * \param z the z position of the pixel processed
 *
 * \return the function return the next token (pixel) that must be process
 */
static MB3D_Token MB3D_InsertNeighbors_cube(void *ctx, int x, int y, int z)
{
    Uint32 neighbor;
    PIX32 *p, *pix, tag;
    int nbx,nby,nbz,pos;
    MB_Image *im;
    MB3D_Watershed8_Ctx *local_ctx = (MB3D_Watershed8_Ctx *) ctx;
    
    /* The tag value is the value of the marker image in x,y,z */
    im = local_ctx->seq_marker[z];
    pix = (PIX32 *) (im->plines[y] + x*4);
    *pix = SET_STATUS(pix,RG_LAB);
    
    /* We will then look at its neighbors and it will help us decide to which */
    /* marker the pixel belongs and also evaluates if the pixel might be in */
    /* the watershed. The neighbors not yet processed or inserted will be put */
    /* in the reinsert list to insert them later if the pixel is taggued at the */
    /* end. */
    
    /* The reinsert list is emptied */
    MB3D_ClearReinsertList(local_ctx);
    
    /* For the 26 neighbors of the pixel */
    for(neighbor=1; neighbor<27; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+cubeNbDir[neighbor][0];
        nby = y+cubeNbDir[neighbor][1];
        nbz = z+cubeNbDir[neighbor][2];
        
        /* The neighbor must be in the image*/
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) &&
            nbz>=0 && nbz<((int) local_ctx->length) ) {
            im = local_ctx->seq_marker[nbz];
            p = (PIX32 *) (im->plines[nby] + nbx*4);
            
            if( IS_PIXEL(p, CANDIDATE) ) {
                /* The neighbor is not inserted into the list yet */
                /* For the time being it is only put into the reinsert list */
                MB3D_InsertInReinsertList(local_ctx, nbx, nby, nbz);
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
    
    /* At this point, if the pixel does not belong to the watershed */
    /* we insert its unprocessed and unlisted neighbor into the */
    /* hierarchical list */
    if( !IS_PIXEL(pix, WTS_LAB) ) {
        MB3D_ReinsertFromList(local_ctx);
    }

    /* wWat is the next token to process */
    pos = x+y*local_ctx->width+z*local_ctx->width*local_ctx->height;
    return local_ctx->TokensArray[pos];
}

/*
 * Inserts the neighbors of pixel (x,y,z) in the hierarchical list so that they
 * can be flooded when the water reaches their level (FACE CENTERED CUBIC 
 * GRID). Also evaluates to which basin the pixel belongs or if it is a point
 * of the watershed.
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the pixel processed
 * \param y the x position of the pixel processed
 * \param z the z position of the pixel processed
 *
 * \return the function return the next token (pixel) that must be process
 */
static MB3D_Token MB3D_InsertNeighbors_fcc(void *ctx, int x, int y, int z)
{
    Uint32 neighbor;
    PIX32 *p, *pix, tag;
    int nbx,nby,nbz,pos,dirSelect;
    MB_Image *im;
    MB3D_Watershed8_Ctx *local_ctx = (MB3D_Watershed8_Ctx *) ctx;
    
    /* Computing the directions to use depending on the y and z of the */
    /* pixel */
    dirSelect = ((z%3)<<1)+(y%2);
    
    /* The tag value is the value of the marker image in x,y */
    im = local_ctx->seq_marker[z];
    pix = (PIX32 *) (im->plines[y] + x*4);
    *pix = SET_STATUS(pix,RG_LAB);
    
    /* We will then look at its neighbors and it will help us decide to which */
    /* marker the pixel belongs and also evaluates if the pixel might be in */
    /* the watershed. The neighbors not yet processed or inserted will be put */
    /* in the reinsert list to insert them later if the pixel is taggued at the */
    /* end. */
    
    /* The reinsert list is emptied */
    MB3D_ClearReinsertList(local_ctx);
    
    /* For the 12 neighbors of the pixel */
    for(neighbor=1; neighbor<13; neighbor++) {
        /* Position and value in the marker image */
        nbx = x+fccNbDir[dirSelect][neighbor][0];
        nby = y+fccNbDir[dirSelect][neighbor][1];
        nbz = z+fccNbDir[dirSelect][neighbor][2];
        
        /* The neighbor must be in the image*/
        if (nbx>=0 && nbx<((int) local_ctx->width) && 
            nby>=0 && nby<((int) local_ctx->height) &&
            nbz>=0 && nbz<((int) local_ctx->length) ) {
            im = local_ctx->seq_marker[nbz];
            p = (PIX32 *) (im->plines[nby] + nbx*4);
            
            if( IS_PIXEL(p, CANDIDATE) ) {
                /* The neighbor is not inserted into the list yet */
                /* For the time being it is only put into the reinsert list */
                MB3D_InsertInReinsertList(local_ctx, nbx, nby, nbz);
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
    
    /* At this point, if the pixel does not belong to the watershed */
    /* we insert its unprocessed and unlisted neighbor into the */
    /* hierarchical list */
    if( !IS_PIXEL(pix, WTS_LAB) ) {
        MB3D_ReinsertFromList(local_ctx);
    }

    /* What is the next token to process */
    pos = x+y*local_ctx->width+z*local_ctx->width*local_ctx->height;
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
static INLINE void MB3D_Flooding(MB3D_Watershed8_Ctx *local_ctx, Uint32 max_level)
{
    Uint32 i;
    int fx,fy,fz;
    MB3D_Token next_token;
    
    for(i=0; i<max_level; i++, local_ctx->current_water_level++) {
        fx = local_ctx->HierarchicalList[local_ctx->current_water_level].firstx;
        fy = local_ctx->HierarchicalList[local_ctx->current_water_level].firsty;
        fz = local_ctx->HierarchicalList[local_ctx->current_water_level].firstz;
        while(fx>=0) {
            next_token = local_ctx->InsertNeighbors(local_ctx,fx,fy,fz);
            fx = next_token.nextx;
            fy = next_token.nexty;
            fz = next_token.nextz;
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
static INLINE void MB3D_ControlPass(MB3D_Watershed8_Ctx *local_ctx)
{
    Uint32 x,y,z;
    PIX32 *p;
    MB_Image *im;
    
    /* All the pixels are checked */
    for(z=0; z<local_ctx->length; z++) {
        for(y=0; y<local_ctx->height; y++) {
            for(x=0; x<local_ctx->bytes_marker; x+=4) {
                im = local_ctx->seq_marker[z];
                p = (PIX32 *) (im->plines[y] + x);
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
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * Performs a watershed segmentation of the 3D image using the marker image
 * as a starting point for the flooding. The function builds the actual 
 * watershed line (idempotent) plus catchment basins (not idempotent). 
 * The result is put into the 32-bits marker image.
 *
 * The segmentation is coded as follows into the 32-bits values.
 * | 0      | 1      | 2      | 3      |
 * |--------|--------|--------|--------|
 * | Segment label            | isLine |
 * Each byte can be accessed using the function MB_CopyBytePlane. isLine is a value
 * indicating if the pixel belongs to the watershed (255 if this is the case, 
 * undefined otherwise).
 *
 * \param src the greyscale 3D image to segment
 * \param marker the marker 3D image in which the result of segmentation will be put
 * \param max_level the maximum level reach by the water.
 * \param grid the grid used (either square or hexagonal)
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_Watershed8(MB3D_Image *src, MB3D_Image *marker, Uint32 max_level, enum MB3D_grid_t grid) {
    MB3D_Watershed8_Ctx local_ctx;
    
    /* Maximum level for flood cannot be greater than 256 */
    if (max_level>256)
        return MB_ERR_BAD_VALUE;
    if (max_level==0) max_level=256;
        
    /* Local context initialisation */
    local_ctx.width = src->seq[0]->width;
    local_ctx.height = src->seq[0]->height;
    local_ctx.length = src->length;

    /* Setting up pointers */
    local_ctx.seq_src = &src->seq[0];
    local_ctx.seq_marker = &marker->seq[0];
    local_ctx.bytes_marker = MB_LINE_COUNT(marker->seq[0]);
    
    /* Allocating the token array */
    local_ctx.TokensArray = MB_malloc(local_ctx.width*local_ctx.height*local_ctx.length*sizeof(MB3D_Token));
    if(local_ctx.TokensArray==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    } 
    
    /* Grid initialisation */
    if (grid==MB3D_CUBIC_GRID) {
        local_ctx.InsertNeighbors = MB3D_InsertNeighbors_cube;
    } else {
        local_ctx.InsertNeighbors = MB3D_InsertNeighbors_fcc;
    }

    /* Initialisation */
    MB3D_HierarchyInit(&local_ctx);
    
    /* Actual flooding */
    MB3D_Flooding(&local_ctx, max_level);
    
    /* Control pass (only if all levels where flooded) */
    if (max_level==256) 
        MB3D_ControlPass(&local_ctx);
    
    /* Freeing the token array */
    MB_free(local_ctx.TokensArray);
    
    return MB_NO_ERR;
}
