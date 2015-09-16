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
typedef void (INSERTNB8) (void *ctx, int x, int y, int z);

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
    /* The memory to hold the status of each pixel */
    Uint32 *pix_status;
    
    /* Image sequence for the marker */
    MB_Image **seq_mask;
    /* Image sequence for the source/destination */
    MB_Image **seq_srcdest;
    /* Size in byte of the image lines */
    Uint32 bytes;
    
    /* Variable indicating which level in the hierarchical list
     * the "water" as attained. Only this level and above can be filled with new
     * tokens.
     */
    PIX8 current_water_level;
    
    /* Meta function which redirects the neighbor function according to the grid */
    INSERTNB8 *InsertNeighbors;
} MB3D_Hierardualbld8_Ctx;

/****************************************
 * Hierarchical list functions          *
 ****************************************/

/*
 * Inserts a token in the hierarchical list.
 * This function only uses the tokens of the first half (for initialization)
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm.
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param z the position in z of the concerned pixel
 * \param bytes number of bytes inside the line
 */
static INLINE void MB3D_InsertInHierarchicalList_1(
    MB3D_Hierardualbld8_Ctx *local_ctx,
    int x, int y, int z,
    PIX8 value)
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
    
    /* Insertion in the hierarchical list */
    /* The token is inserted after the last value in the list */
    lx = local_ctx->HierarchicalList[value].lastx;
    ly = local_ctx->HierarchicalList[value].lasty;
    lz = local_ctx->HierarchicalList[value].lastz;
    lposition = lx+ly*local_ctx->width+lz*local_ctx->width*local_ctx->height;
    if (lposition>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[lposition].nextx = x;
        local_ctx->TokensArray[lposition].nexty = y;
        local_ctx->TokensArray[lposition].nextz = z;
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
}

/*
 * Inserts a token in the hierarchical list.
 * This function only uses the tokens of the second half (for flooding).
 * The function also changes the status of the pixel to QUEUED.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param z the position in z of the concerned pixel
 * \param bytes number of bytes inside the line
 */
static INLINE void MB3D_InsertInHierarchicalList_2(
    MB3D_Hierardualbld8_Ctx *local_ctx, 
    int x, int y, int z,
    PIX8 value)
{
    int position;
    int lposition;
    int lx, ly, lz;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    /* The y is increased by local_ctx->height to make sure the second half */
    /* of the token is used */
    position = x + y*local_ctx->width + (z+local_ctx->length)*local_ctx->width*local_ctx->height;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    local_ctx->TokensArray[position].nextz = MB_LIST_END;
    
    /* Insertion in the hierarchical list */
    /* The token is inserted after the last value in the list */
    lx = local_ctx->HierarchicalList[value].lastx;
    ly = local_ctx->HierarchicalList[value].lasty;
    lz = local_ctx->HierarchicalList[value].lastz;
    lposition = lx+ly*local_ctx->width+lz*local_ctx->width*local_ctx->height;
    if (lposition>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[lposition].nextx = x;
        local_ctx->TokensArray[lposition].nexty = y;
        local_ctx->TokensArray[lposition].nextz = z+local_ctx->length;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
        local_ctx->HierarchicalList[value].lastz = z+local_ctx->length;
    }
    else {
        /* The list is empty, so we create it.*/
        local_ctx->HierarchicalList[value].firstx = x;
        local_ctx->HierarchicalList[value].firsty = y;
        local_ctx->HierarchicalList[value].firstz = z+local_ctx->length;
        local_ctx->HierarchicalList[value].lastx = x;
        local_ctx->HierarchicalList[value].lasty = y;
        local_ctx->HierarchicalList[value].lastz = z+local_ctx->length;
    }
    
    /* Change the pixel status */
    local_ctx->pix_status[x+y*local_ctx->width+z*local_ctx->width*local_ctx->height] = 0x1;
}

/*
 * Initializes the hierarchical list with the marker image.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB3D_HierarchyInit(MB3D_Hierardualbld8_Ctx *local_ctx)
{
    Uint32 i,x,y,z;
    MB_Image *srcdest, *mask;
    PLINE pvalue, pmask;
    
    /* All the control are reset */
    for(i=0;i<256;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
        local_ctx->HierarchicalList[i].firstz = local_ctx->HierarchicalList[i].lastz = MB_LIST_END;
    }
     
    /* All the pixels are inserted inside the hierarchical list */
    local_ctx->current_water_level = 0;
    for(z=0; z<local_ctx->length; z++) {
        mask = local_ctx->seq_mask[z];
        srcdest = local_ctx->seq_srcdest[z];
        for(y=0; y<local_ctx->height; y++) {
            pvalue = (PLINE) (srcdest->plines[y]);
            pmask = (PLINE) (mask->plines[y]);
            for(x=0; x<local_ctx->bytes; x++, pvalue++, pmask++) {
                *pvalue = *pvalue>*pmask ? *pvalue : *pmask;
                MB3D_InsertInHierarchicalList_1(local_ctx,x,y,z,*pvalue);
            }
        }
    }

    /* All pixels status are set to 0 (CANDIDATE) */
    MB_memset(local_ctx->pix_status, 0, local_ctx->width*local_ctx->height*local_ctx->length*sizeof(Uint32));
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y,z) in the hierarchical list so that they
 * can be flooded when the water reaches their level (CUBE GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the processed pixel 
 * \param y the y position of the processed pixel 
 * \param y the z position of the processed pixel 
 */
static void MB3D_InsertNeighbors_cube(void *ctx, int x, int y, int z)
{
    Uint32 i;
    PIX8 value, *p, pmask;
    MB_Image *srcdest, *mask;
    int nbx,nby,nbz;
    MB3D_Hierardualbld8_Ctx *local_ctx = (MB3D_Hierardualbld8_Ctx *) ctx;
    
    /* The pixel is processed only if it has not been already processed */
    if (local_ctx->pix_status[x+y*local_ctx->width+z*local_ctx->width*local_ctx->height] != 0xff) {
        /* The value of the pixel in the rebuild image */
        srcdest = local_ctx->seq_srcdest[z];
        value = *(srcdest->plines[y] + x);
        /* Pixel status is now FINAL */
        local_ctx->pix_status[x+y*local_ctx->width+z*local_ctx->width*local_ctx->height] = 0xff;
        
        /* For the 26 neighbors of the pixel */
        for(i=1; i<27; i++) {
            /* Position */
            nbx = x+cubeNbDir[i][0];
            nby = y+cubeNbDir[i][1];
            nbz = z+cubeNbDir[i][2];
            
            /* The neighbor must be in the image */
            if (nbx>=0 && nbx<((int) local_ctx->width) && 
                nby>=0 && nby<((int) local_ctx->height) &&
                nbz>=0 && nbz<((int) local_ctx->length) ) {
                if (local_ctx->pix_status[nbx+nby*local_ctx->width+nbz*local_ctx->width*local_ctx->height] == 0) {
                    /* If the neighbor status is CANDIDATE */
                    /* we modified its value with the minimum between the value of the */
                    /* mask at its position and the value of the pixel currently processed */
                    mask = local_ctx->seq_mask[nbz];
                    srcdest = local_ctx->seq_srcdest[nbz];
                    pmask = *(mask->plines[nby] + nbx);
                    p = (srcdest->plines[nby] + nbx);
                    *p = value>pmask ? value : pmask;
                    MB3D_InsertInHierarchicalList_2(local_ctx, nbx, nby, nbz, *p);
                }
            }
        }
    }
}

/*
 * Inserts the neighbors of pixel (x,y,z) in the hierarchical list so that they
 * can be flooded when the water reaches their level (FACE CENTERED CUBIC GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm.
 * \param x the x position of the processed pixel 
 * \param y the y position of the processed pixel 
 * \param y the z position of the processed pixel 
 */
static void MB3D_InsertNeighbors_fcc(void *ctx, int x, int y, int z)
{
    Uint32 i;
    PIX8 value, *p, pmask;
    MB_Image *srcdest, *mask;
    int nbx,nby,nbz,dirSelect;
    MB3D_Hierardualbld8_Ctx *local_ctx = (MB3D_Hierardualbld8_Ctx *) ctx;
    
    /* The pixel is processed only if it has not been already processed */
    if (local_ctx->pix_status[x+y*local_ctx->width+z*local_ctx->width*local_ctx->height] != 0xff) {
        /* The value of the pixel in the rebuild image */
        srcdest = local_ctx->seq_srcdest[z];
        value = *(srcdest->plines[y] + x);
        /* Pixel status is now FINAL */
        local_ctx->pix_status[x+y*local_ctx->width+z*local_ctx->width*local_ctx->height] = 0xff;
    
        /* Computing the directions to use depending on the y and z of the */
        /* pixel */
        dirSelect = ((z%3)<<1)+(y%2);
        
        /* For the 12 neighbors of the pixel */
        for(i=1; i<13; i++) {
            /* Position */
            nbx = x+fccNbDir[dirSelect][i][0];
            nby = y+fccNbDir[dirSelect][i][1];
            nbz = z+fccNbDir[dirSelect][i][2];
            
            /* The neighbor must be in the image */
            if (nbx>=0 && nbx<((int) local_ctx->width) && 
                nby>=0 && nby<((int) local_ctx->height) &&
                nbz>=0 && nbz<((int) local_ctx->length) ) {
                if (local_ctx->pix_status[nbx+nby*local_ctx->width+nbz*local_ctx->width*local_ctx->height] == 0) {
                    /* If the neighbor status is CANDIDATE */
                    /* we modified its value with the minimum between the value of the */
                    /* mask at its position and the value of the pixel currently processed */
                    mask = local_ctx->seq_mask[nbz];
                    srcdest = local_ctx->seq_srcdest[nbz];
                    pmask = *(mask->plines[nby] + nbx);
                    p = (srcdest->plines[nby] + nbx);
                    *p = value>pmask ? value : pmask;
                    MB3D_InsertInHierarchicalList_2(local_ctx, nbx, nby, nbz, *p);
                }
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
 * in inserting in the list all its neighbor that are not already processed.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm.
 */
static INLINE void MB3D_Flooding(MB3D_Hierardualbld8_Ctx *local_ctx)
{
    int fx,fy,fz,pos;
    Uint32 i;
    
    for(i=0; i<256; i++, local_ctx->current_water_level++) {
        fx = local_ctx->HierarchicalList[local_ctx->current_water_level].firstx;
        fy = local_ctx->HierarchicalList[local_ctx->current_water_level].firsty;
        fz = local_ctx->HierarchicalList[local_ctx->current_water_level].firstz;
        while(fx>=0) {
            pos = fx+fy*local_ctx->width+fz*local_ctx->width*local_ctx->height;
            local_ctx->InsertNeighbors(local_ctx,fx,fy,fz%(local_ctx->length));
            fx = local_ctx->TokensArray[pos].nextx;
            fy = local_ctx->TokensArray[pos].nexty;
            fz = local_ctx->TokensArray[pos].nextz;
        }
    }
}

/************************************************/
/*High level function and global variables      */
/************************************************/

/*
 * (re)Builds (dual operation) a 3D image according to a 3D mask image and
 * using a hierarchical list to compute the rebuild.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB3D_HierarDualBld8(MB3D_Image *mask, MB3D_Image *srcdest, enum MB3D_grid_t grid) {
    MB3D_Hierardualbld8_Ctx local_ctx;
    
    /* Local context initialisation */
    local_ctx.width = srcdest->seq[0]->width;
    local_ctx.height = srcdest->seq[0]->height;
    local_ctx.length = srcdest->length;

    /* Setting up pointers */
    local_ctx.seq_srcdest = &srcdest->seq[0];
    local_ctx.seq_mask = &mask->seq[0];
    local_ctx.bytes = MB_LINE_COUNT(mask->seq[0]);
    
    /* Allocating the token array */
    /* We need two token per pixel for this algorithm */
    /* the init will use the first half and the flooding the other */
    local_ctx.TokensArray = MB_malloc(2*local_ctx.width*local_ctx.height*local_ctx.length*sizeof(MB3D_Token));
    if(local_ctx.TokensArray==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    /* Allocating the pixel status array */
    local_ctx.pix_status = MB_malloc(local_ctx.width*local_ctx.height*local_ctx.length*sizeof(Uint32));
    if(local_ctx.pix_status==NULL){
        /* In case allocation goes wrong */
        MB_free(local_ctx.TokensArray);
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
    MB3D_Flooding(&local_ctx);
    
    /* Freeing the token array */
    MB_free(local_ctx.TokensArray);
    /* Freeing the pixel status array */
    MB_free(local_ctx.pix_status);
    
    return MB_NO_ERR;
}
