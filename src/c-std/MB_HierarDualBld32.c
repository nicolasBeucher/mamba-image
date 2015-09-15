/*
 * Copyright (c) <2010>, <Nicolas BEUCHER and ARMINES for the Centre de 
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
typedef void (INSERTNB32) (void *ctx, int x, int y);

/* Structure holding the function contextual information 
 * such as the size of the image processed, the pointer to the pixel lines, 
 * the array of tokens and the current flooding level.
 */
typedef struct {
    /* The width of the processed images */
    Uint32 width;
    /* The height of the processed images */
    Uint32 height;
    
    /* The memory used to hold the elements of the hierarchical list */
    MB_Token *TokensArray;
    /* The hierarchical list entries for reconstruction */
    /* lists are splitted in two */
    MB_ListControl HierarchicalList[65536];
    MB_ListControl OverLists[65536];
    /* The memory to hold the status of each pixel */
    Uint32 *pix_status;
    
    /* Pointer to the lines of the mask image */
    PLINE *plines_mask;
    /* Pointer to the line of the source/destination image */
    PLINE *plines_srcdest;
    /* Size in byte of the image lines */
    Uint32 bytes;
    
    /* Variable indicating which level in the hierarchical list
     * the "water" as attained. Only this level and above can be filled with new
     * tokens.
     */
    int current_water_range;
    int max_water_range;
    
    /* Meta function which redirects the neighbor function according to the grid */
    INSERTNB32 *InsertNeighbors;
} MB_Hierardualbld32_Ctx;

/****************************************
 * Hierarchical list functions          *
 ****************************************/

/*
 * Inserts a token in the hierarchical list.
 * This function only uses the tokens of the first half (for initialization).
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param bytes number of bytes inside the line
 */
static INLINE void MB_InsertInHierarchicalList_1(MB_Hierardualbld32_Ctx *local_ctx, int x, int y, PIX32 value)
{
    int position;
    int lx, ly;
    MB_ListControl *list;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    position = x + y*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* Insertion in the over list corresponding */
    list = &(local_ctx->OverLists[value>>16]);
    
    /* The token is inserted after the last value in the list */
    lx = list->lastx;
    ly = list->lasty;
    position = lx+ly*local_ctx->width;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y;
        list->lastx = x;
        list->lasty = y;
    }
    else {
        /* The list is empty, so we create it.*/
        list->firstx = x;
        list->firsty = y;
        list->lastx = x;
        list->lasty = y;
    }
}

/*
 * Inserts a token in the hierarchical list
 * This function only uses the tokens of the second half (for flooding).
 * The function also changes the status of the pixel to QUEUED.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the position in x of the concerned pixel
 * \param y the position in y of the concerned pixel
 * \param bytes number of bytes inside the line
 */
static INLINE void MB_InsertInHierarchicalList_2(MB_Hierardualbld32_Ctx *local_ctx, int x, int y, PIX32 value)
{
    int position;
    PIX32 hvalue;
    int lx, ly;
    MB_ListControl *list;
    
    /* The token corresponding to the pixel process is */
    /* updated/created. */
    /* The y is increased by local_ctx->height to make sure the second half */
    /* of the token is used */
    position = x + (y+local_ctx->height)*local_ctx->width;
    local_ctx->TokensArray[position].nextx = MB_LIST_END;
    local_ctx->TokensArray[position].nexty = MB_LIST_END;
    
    /* Insertion in the hierarchical list */
    /* First if the value is outside the currently supported range */
    /* it will be put in the corresponding overlist */
    if ((value>>16)!=local_ctx->current_water_range) {
        list = &(local_ctx->OverLists[value>>16]);
    } else {
        /* We take the correct list */
        hvalue = value&0xffff;
        list = &(local_ctx->HierarchicalList[hvalue]);
    }
    
    /* The token is inserted after the last value in the list */
    lx = list->lastx;
    ly = list->lasty;
    position = lx+ly*local_ctx->width;
    if (position>=0) {
        /* There is a last value, the list is not empty*/
        local_ctx->TokensArray[position].nextx = x;
        local_ctx->TokensArray[position].nexty = y+local_ctx->height;
        list->lastx = x;
        list->lasty = y+local_ctx->height;
    }
    else {
        /* The list is empty, so we create it.*/
        list->firstx = x;
        list->firsty = y+local_ctx->height;
        list->lastx = x;
        list->lasty = y+local_ctx->height;
    }
    
    /* Change the pixel status */
    local_ctx->pix_status[x+ y*local_ctx->width] = 0x1;
}

/*
 * Initializes the hierarchical list with the marker image.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_HierarchyInit(MB_Hierardualbld32_Ctx *local_ctx)
{

    Uint32 i,j;
    PIX32 *pvalue, *pmask;
    PIX32 max;
    
    /* All the controls are reset */
    for(i=0;i<65536;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
        local_ctx->OverLists[i].firstx = local_ctx->OverLists[i].lastx = MB_LIST_END;
        local_ctx->OverLists[i].firsty = local_ctx->OverLists[i].lasty = MB_LIST_END;
    }
     
    /* All the pixels are inserted inside the hierarchical list */
    max = 0;
    for(i=0; i<local_ctx->height; i++) {
        pvalue = (PIX32 *) (local_ctx->plines_srcdest[i]);
        pmask = (PIX32 *) (local_ctx->plines_mask[i]);
        for(j=0; j<local_ctx->bytes; j+=4, pvalue++, pmask++) {
            *pvalue = *pvalue>*pmask ? *pvalue : *pmask;
            max = max<*pvalue ? *pvalue:max;
            MB_InsertInHierarchicalList_1(local_ctx,j/4,i,*pvalue);
        }
    }
    local_ctx->current_water_range = 0;
    local_ctx->max_water_range = (max>>16)+1;

    /* All pixels status are set to 0 (CANDIDATE) */
    MB_memset(local_ctx->pix_status, 0, local_ctx->width*local_ctx->height*sizeof(Uint32));
}

/****************************************
 * Neighbor functions                   *
 ****************************************/

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reaches their level (SQUARE GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the processed pixel 
 * \param y the x position of the processed pixel 
 */
static void MB_InsertNeighbors_square(void *ctx, int x, int y)
{
    Uint32 i;
    PIX32 value, *p, pmask;
    int nbx,nby;
    MB_Hierardualbld32_Ctx *local_ctx = (MB_Hierardualbld32_Ctx *) ctx;
    
    /* The pixel is processed only if it has not been already processed */
    if (local_ctx->pix_status[x+ y*local_ctx->width] != 0xff) {
        /* The value of the pixel in the rebuild image */
        value = *((PIX32 *)(local_ctx->plines_srcdest[y] + x*4));
        /* Pixel status is now FINAL */
        local_ctx->pix_status[x+ y*local_ctx->width] = 0xff;
        
        /* For the 8 neighbors of the pixel */
        for(i=1; i<9; i++) {
            /* Position */
            nbx = x+sqNbDir[i][0];
            nby = y+sqNbDir[i][1];
            
            /* The neighbor must be in the image */
            if (nbx>=0 && nbx<((int) local_ctx->width) && nby>=0 && nby<((int) local_ctx->height)) {
                if (local_ctx->pix_status[nbx+ nby*local_ctx->width] == 0) {
                    /* If the neighbor status is CANDIDATE */
                    /* we modified its value with the minimum between the value of the */
                    /* mask at its position and the value of the pixel currently processed */
                    pmask = *((PIX32 *)(local_ctx->plines_mask[nby] + nbx*4));
                    p = (PIX32 *)(local_ctx->plines_srcdest[nby] + nbx*4);
                    *p = value>pmask ? value : pmask;
                    MB_InsertInHierarchicalList_2(local_ctx, nbx, nby, *p);
                }
            }
        }
    }
}

/*
 * Inserts the neighbors of pixel (x,y) in the hierarchical list so that they
 * can be flooded when the water reaches their level (HEXAGONAL GRID).
 * \param ctx pointer to the structure holding all the information needed 
 * by the algorithm
 * \param x the x position of the processed pixel 
 * \param y the x position of the processed pixel 
 */
static void MB_InsertNeighbors_hexagonal(void *ctx, int x, int y)
{
    Uint32 i;
    PIX32 value, *p, pmask;
    int nbx,nby;
    MB_Hierardualbld32_Ctx *local_ctx = (MB_Hierardualbld32_Ctx *) ctx;
    
    /* The pixel is processed only if it has not been already processed */
    if (local_ctx->pix_status[x+ y*local_ctx->width] != 0xff) {
        /* The value of the pixel in the rebuild image */
        value = *((PIX32 *)(local_ctx->plines_srcdest[y] + x*4));
        /* Pixel status is now FINAL */
        local_ctx->pix_status[x+ y*local_ctx->width] = 0xff;
        
        /* For the 6 neighbors of the pixel */
        for(i=1; i<7; i++) {
            /* Position */
            nbx = x+hxNbDir[y%2][i][0];
            nby = y+hxNbDir[y%2][i][1];
            
            /* The neighbor must be in the image */
            if (nbx>=0 && nbx<((int) local_ctx->width) && nby>=0 && nby<((int) local_ctx->height)) {
                if (local_ctx->pix_status[nbx+ nby*local_ctx->width] == 0) {
                    /* If the neighbor status is CANDIDATE */
                    /* we modified its value with the minimum between the value of the */
                    /* mask at its position and the value of the pixel currently processed */
                    pmask = *((PIX32 *)(local_ctx->plines_mask[nby] + nbx*4));
                    p = (PIX32 *)(local_ctx->plines_srcdest[nby] + nbx*4);
                    *p = value>pmask ? value : pmask;
                    MB_InsertInHierarchicalList_2(local_ctx, nbx, nby, *p);
                }
            }
        }
    }
}

/****************************************
 * Flooding function                    *
 ****************************************/

/*
 * Handles the OverList and restores the hierarchical lists to process the
 * next batch.
 */
static INLINE void MB_HandlesOverList(MB_Hierardualbld32_Ctx *local_ctx)
{
    Uint32 i;
    PIX32 value;
    int fx,fy,cfx,cfy,lx,ly;
    int position;
    MB_ListControl *list;
    MB_Token *token;
    
    /* Resetting the hierarchical lists */
    for(i=0;i<65536;i++) {
        local_ctx->HierarchicalList[i].firstx = local_ctx->HierarchicalList[i].lastx = MB_LIST_END;
        local_ctx->HierarchicalList[i].firsty = local_ctx->HierarchicalList[i].lasty = MB_LIST_END;
    }
    
    /* Over list handles */
    fx = local_ctx->OverLists[local_ctx->current_water_range].firstx;
    fy = local_ctx->OverLists[local_ctx->current_water_range].firsty;
    while ((fx<0) && (local_ctx->current_water_range<local_ctx->max_water_range-1)) {
        local_ctx->current_water_range++;
        fx = local_ctx->OverLists[local_ctx->current_water_range].firstx;
        fy = local_ctx->OverLists[local_ctx->current_water_range].firsty;
    }
    
    /* Emptying the over list */
    while(fx>=0) {
        position = fx+fy*local_ctx->width;
        token = &local_ctx->TokensArray[position];
        value = *((PIX32 *) (local_ctx->plines_srcdest[fy%(local_ctx->height)] + fx*4));
        
        cfx = fx;
        cfy = fy;
        fx = token->nextx;
        fy = token->nexty;
        token->nextx = MB_LIST_END;
        token->nexty = MB_LIST_END;
        
        list = &(local_ctx->HierarchicalList[value&0xffff]);
        /* The token is inserted after the last value in the list */
        lx = list->lastx;
        ly = list->lasty;
        position = lx+ly*local_ctx->width;
        if (position>=0) {
            /* There is a last value, the list is not empty*/
            local_ctx->TokensArray[position].nextx = cfx;
            local_ctx->TokensArray[position].nexty = cfy;
            list->lastx = cfx;
            list->lasty = cfy;
        }
        else {
            /* The list is empty, so we create it.*/
            list->firstx = cfx;
            list->firsty = cfy;
            list->lastx = cfx;
            list->lasty = cfy;
        }
    }
}

/*
 * Simulates the flooding process using the hierarchical list. Tokens are
 * extracted out of the current water level list and processed. The process consists
 * in inserting in the list all its neighbors that are not already processed.
 * \param local_ctx pointer to the structure holding all the information needed 
 * by the algorithm
 */
static INLINE void MB_Flooding(MB_Hierardualbld32_Ctx *local_ctx)
{

    int fx,fy,pos;
    int i;
    
    while(local_ctx->current_water_range<local_ctx->max_water_range) {
        MB_HandlesOverList(local_ctx);
        
        for(i=0; i<65536; i++) {
            fx = local_ctx->HierarchicalList[i].firstx;
            fy = local_ctx->HierarchicalList[i].firsty;
            while(fx>=0) {
                pos = fx+fy*local_ctx->width;
                local_ctx->InsertNeighbors(local_ctx,fx,fy%(local_ctx->height));
                fx = local_ctx->TokensArray[pos].nextx;
                fy = local_ctx->TokensArray[pos].nexty;
            }
        }
        local_ctx->current_water_range++;
    }
}

/************************************************/
/* High level function and global variables     */
/************************************************/

/*
 * (re)Builds (dual operation) an image according to a mask image and using a 
 * hierarchical list to compute the rebuild.
 *
 * \param mask the mask image
 * \param srcdest the rebuild image
 * \param grid the grid used (either square or hexagonal)
 *
 * \return An error code (MB_NO_ERR if successful)
 */
MB_errcode MB_HierarDualBld32(MB_Image *mask, MB_Image *srcdest, enum MB_grid_t grid)
{
    MB_Hierardualbld32_Ctx *local_ctx;
    
    local_ctx = (MB_Hierardualbld32_Ctx *)MB_malloc(sizeof(MB_Hierardualbld32_Ctx));
    if(local_ctx==NULL){
        /* In case allocation goes wrong */
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    
    /* Local context initialisation */
    local_ctx->width = srcdest->width;
    local_ctx->height = srcdest->height;

    /* Setting up pointers */
    local_ctx->plines_srcdest = srcdest->plines;
    local_ctx->plines_mask = mask->plines;
    local_ctx->bytes = MB_LINE_COUNT(mask);
    
    /* Allocating the token array */
    /* We need two token per pixel for this algorithm */
    /* The init will use the first half and the flooding the other */
    local_ctx->TokensArray = MB_malloc(2*srcdest->width*srcdest->height*sizeof(MB_Token));
    if(local_ctx->TokensArray==NULL){
        /* In case allocation goes wrong */
        MB_free(local_ctx);
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    /* Allocating the pixel status array */
    local_ctx->pix_status = MB_malloc(srcdest->width*srcdest->height*sizeof(Uint32));
    if(local_ctx->pix_status==NULL){
        /* In case allocation goes wrong */
        /* freeing the token array */
        MB_free(local_ctx->TokensArray);
        MB_free(local_ctx);
        return MB_ERR_CANT_ALLOCATE_MEMORY;
    }
    
    /* Grid initialisation */
    if (grid==MB_SQUARE_GRID) {
         local_ctx->InsertNeighbors = MB_InsertNeighbors_square;
     } else {
         local_ctx->InsertNeighbors = MB_InsertNeighbors_hexagonal;
    }

    /* Initialisation */
    MB_HierarchyInit(local_ctx);
    
    /* Actual flooding */
    MB_Flooding(local_ctx);
    
    /* Freeing the token array */
    MB_free(local_ctx->TokensArray);
    /* Freeing the pixel status array */
    MB_free(local_ctx->pix_status);
    /* Freeing the context */
    MB_free(local_ctx);
    
    return MB_NO_ERR;
}
