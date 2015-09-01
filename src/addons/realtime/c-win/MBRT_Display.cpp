/**
 * \file MBRT_Display.cpp
 * \author Nicolas Beucher
 * \date 03-29-2009
 *
 */
 
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
#include "mambaRTApi_loc.h"

/** Extracts the red pixel */
#define RED(pix)  (*(pix+2))
/** Extracts the green pixel */
#define GREEN(pix)  (*(pix+1))
/** Extracts the blue pixel */
#define BLUE(pix)  (*pix)

/**
 * When requested, the framerate is drawn into the screen by calling this function
 * \param wfps the desired framerate
 * \param ofps the obtained framerate
 */
static INLINE void DRAW_FPS_RATE(double ofps, double wfps)
{
    PIX8 *bufp,*pixels;
    int val;
    Uint32 i,j,w;

    /* blackening the background */
    pixels = ((PIX8 *)context->pixels);
    for(j=(context->sz_y-12-FPS_THICKNESS); j<context->sz_y; j++) {
        for(i=0; i<context->sz_x; i++) {
            bufp = pixels + j*context->sz_x*4 + i*4;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
            bufp++;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
            bufp++;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
        }
    }
    
    /* drawing the FPS bar */
    for (i=0; i<context->sz_x/2+4; i++) {
        context->pixels[(context->sz_y-7)*context->sz_x+i+7] = FRAME_COLOR;
        context->pixels[(context->sz_y-10-FPS_THICKNESS)*context->sz_x+i+7] = FRAME_COLOR;
    }
    for (i=0; i<FPS_THICKNESS+4; i++) {
        context->pixels[(context->sz_y-7-i)*context->sz_x+7] = FRAME_COLOR;
        context->pixels[(context->sz_y-7-i)*context->sz_x+10+context->sz_x/2] = FRAME_COLOR;
    }
    w = (Uint32) ((context->sz_x/2*(ofps))/wfps);
    w = w>(Uint32)context->sz_x/2 ? context->sz_x/2:w;
    for (i=0; i<w; i++) {
        for (j=0; j<FPS_THICKNESS; j++) {
            context->pixels[(context->sz_y-9-j)*context->sz_x+i+9] = FRAME_COLOR;
        }
    }
}

/**
 * When resquested, this function draws the image histogram on display
 */
static INLINE void DRAW_HISTO()
{
    PIX8 * bufp,*pixels;
    int val;
    int i,j,h;
    int ybegin;
    Uint32 max_histo = 0;
    
    /* looking for histo max */
    for(i=0; i<256; i++) {
        if (context->histo[i]>max_histo)
            max_histo = context->histo[i];
    }
    
    /* blackening the background */
    ybegin = context->sz_y-13-FPS_THICKNESS;
    h = (context->sz_y/2);
    
    pixels = ((PIX8 *)context->pixels);
    for(j=0; j<(h+2); j++) {
        for(i=0; i<258; i++) {
            bufp = pixels + (ybegin-1-j)*context->sz_x*4 + (i + 8)*4;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
            bufp++;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
            bufp++;
            val = ((int) *bufp) - HISTO_BLACKENING;
            *bufp = val<0 ? 0 :(PIX8) val;
        }
    }
    
    /* drawing the frame */
    for (i=0; i<h+4; i++) {
        context->pixels[(ybegin-i)*context->sz_x+7] = FRAME_COLOR;
        context->pixels[(ybegin-i)*context->sz_x+266] = FRAME_COLOR;
    }
    for (i=0; i<260; i++) {
        context->pixels[(ybegin-h-3)*context->sz_x+7+i] = FRAME_COLOR;
        context->pixels[(ybegin)*context->sz_x+7+i] = FRAME_COLOR;
    }
    
    /* drawing histo */
    for(i=0; i<256; i++) {
        for (j = ( h*context->histo[i] )/max_histo; j>=0; j--) {
            context->pixels[(ybegin-1-j)*context->sz_x+9+i] = HISTO_COLOR;
        }
    }
}

/**
 * Displays a small square indicating the recording is going on
 * The square is blinking on screen
 */
static INLINE void DRAW_RECORD()
{
    int x,y;
    
    /* blinking at 2hz */
    /* this is ensured by looking at the call timestamp */
    if ((context->old_call[context->index_fps]/500)%2==0) {
    
        /* drawing the rectangle */
        for (x=0; x<REC_SIZE; x++) {
            for(y=0; y<REC_SIZE; y++) {
                context->pixels[(REC_SIZE+y)*context->sz_x+(context->sz_x)-REC_SIZE-x] = REC_COLOR;
            }
        }
    }
}

/**
 * Initializes SDL and creates the video display (SDL screen)
 * \param w width of the display (resolution)
 * \param h height of the display (resolution)
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_CreateDisplay(int w, int h)
{
    int i;
    Uint32 call;
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;
    
    /* Initialization of SDL video part */
    if (SDL_Init (SDL_INIT_VIDEO) < 0)
    {
        /*failure*/
        return MBRT_ERR_INIT_DISPLAY;
    }
    
    /* SDL_Quit must be called when the program exits */
    atexit(SDL_Quit);
    
    /* screen size */
    context->sz_x = w;
    context->sz_y = h;
    
    /* the original palette is set to grey level */
    for(i=0;i<256;i++) {
        context->palette[i].r=i;
        context->palette[i].g=i;
        context->palette[i].b=i;
    }

    /*SDL windows, rendering and textures init*/
    context->window = SDL_CreateWindow(
        MBRT_TITLE,
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        context->sz_x, context->sz_y,
        0);
    if (context->window==NULL) {
       /* no windows created */
       return MBRT_ERR_INIT_DISPLAY;
    }
    context->renderer = SDL_CreateRenderer(context->window, -1, 0);
    if (context->renderer==NULL) {
       /* no renderer created */
       return MBRT_ERR_INIT_DISPLAY;
    }
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "linear");
    SDL_RenderSetLogicalSize(context->renderer, context->sz_x, context->sz_y);
    context->texture = SDL_CreateTexture(
        context->renderer,
        SDL_PIXELFORMAT_ARGB8888,
        SDL_TEXTUREACCESS_STREAMING,
        context->sz_x, context->sz_y);
    if (context->texture==NULL) {
       /* no texture created */
       return MBRT_ERR_INIT_DISPLAY;
    }
    context->pixels = (Uint32 *) malloc(context->sz_x*context->sz_y*sizeof(Uint32));
    if (context->pixels==NULL) {
       /* no pixels created */
       return MBRT_ERR_INIT_DISPLAY;
    }
    
    /* framerate information update */
    call = SDL_GetTicks();
    context->isFpsDisplayed = 0;
    for(context->index_fps=0; context->index_fps<FPS_MEAN_SIZE; context->index_fps++) {
        context->old_call[context->index_fps]=call;
    }
    
    /* framerate information update */
    context->isHistoDisplayed = 0;
    
    return MBRT_NO_ERR;
}

/**
 * Destroys the video display (SDL screen) and quits SDL
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_DestroyDisplay()
{
    if (context!=NULL)
    {
        if (context->window) {
            SDL_DestroyWindow(context->window);
            context->window = NULL;
        }
        if (context->renderer) {
            SDL_DestroyRenderer(context->renderer);
            context->renderer = NULL;
        }
        if (context->texture) {
            SDL_DestroyTexture(context->texture);
            context->texture = NULL;
        }
        if (context->pixels) {
            free(context->pixels);
            context->pixels = NULL;
        }
    }
    SDL_Quit();
    
    return MBRT_NO_ERR;
}

/**
 * Updates the display with the content of a given Mamba image structure
 * \param src the image displayed
 * \param wfps input the desired framerate
 * \param ofps output the framerate
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_UpdateDisplay(MB_Image *src, double wfps, double *ofps)
{
    PIX8 *bufp, *pixels, pix;
    Uint32 i,j,v;
    Uint32 current_call;
    int val;
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;
    /* verification over display */
    if (context->pixels==NULL) return MBRT_ERR_INVALID_DISPLAY;
    
    /* only 8-bit images can be displayed*/
    if (src->depth!=8) {
        return MBRT_ERR_DEPTH;
    }
    
    /* image must have the correct size */
    if ((src->width!=context->sz_x) || (src->height!=context->sz_y)) {
        return MBRT_ERR_SIZE;
    }
    
    /* reset of the histogram */
    if (context->isHistoDisplayed)
        memset(context->histo, 0, 256*sizeof(Uint32));
    
    pixels = ((PIX8 *)context->pixels);
    for(j=0; j<context->sz_y; j++) {
        for(i=0; i<context->sz_x; i++) {
            bufp = pixels + j*context->sz_x*4 + 4*i;
            pix = *(src->plines[j]+i);
            RED(bufp) = context->palette[pix].r;
            GREEN(bufp) = context->palette[pix].g;
            BLUE(bufp) = context->palette[pix].b;
            if (context->isHistoDisplayed)
                context->histo[pix]++;
        }
    }
    
    /* icon display */
    for(j=0, v=0; j<(Uint32)context->iconh; j++) {
        for(i=0; i<(Uint32)context->iconw; i++, v++) {
            bufp = pixels + (16+j)*context->sz_x*4 + (16+i)*4;
            if (context->icon[v>>5] & (0x80000000>>(v&0x1f))) {
                *((Uint32 *)bufp) = FRAME_COLOR;
            } else {
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
                bufp++;
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
                bufp++;
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
            }
        }
    }
    
    /* timestamp recording (used for video recording, blinking, and framerate computation */
    current_call = SDL_GetTicks();
    context->index_fps = (context->index_fps+1)%FPS_MEAN_SIZE;
    context->old_call[context->index_fps]=current_call;
    /* framerate computation averaged over FPS_MEAN_SIZE samples */
    *ofps = (FPS_MEAN_SIZE*1000.0)/((double) (current_call - context->old_call[(context->index_fps+1)%FPS_MEAN_SIZE]));
    
    /* frame rate display */
    if (context->isFpsDisplayed) {
        DRAW_FPS_RATE(*ofps, wfps);
    }
    /* histogram display */
    if (context->isHistoDisplayed) {
        DRAW_HISTO();
    }
    /* recording display */
    if (context->isRecording) {
        DRAW_RECORD();
    }

    SDL_UpdateTexture(context->texture, NULL, context->pixels, context->sz_x*sizeof(Uint32));
    SDL_RenderClear(context->renderer);
    SDL_RenderCopy(context->renderer, context->texture, NULL, NULL);
    SDL_RenderPresent(context->renderer);
    return MBRT_NO_ERR;
}

/**
 * Updates the display with the content of a given Mamba image structure
 * \param srcRed image displayed red channel
 * \param srcGreen image displayed green channel
 * \param srcBlue image displayed blue channel
 * \param wfps input the desired framerate
 * \param ofps output the framerate
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_UpdateDisplayColor(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue,
                                     double wfps, double *ofps)
{
    PIX8 *bufp, *pixels;
    Uint32 i,j,v;
    Uint32 current_call;
    int val;
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;
    /* verification over display */
    if (context->pixels==NULL) return MBRT_ERR_INVALID_DISPLAY;
    
    /* only 8-bit images can be displayed*/
    if ( (srcRed->depth!=8) ||
         (srcBlue->depth!=8) ||
         (srcGreen->depth!=8) ) {
        return MBRT_ERR_DEPTH;
    }
    
    /* histogram cannot be compute with color images */
    context->isHistoDisplayed = 0;
    
    /* image must have the correct size */
    if ((srcRed->width!=context->sz_x) || (srcRed->height!=context->sz_y) ||
        (srcBlue->width!=context->sz_x) || (srcBlue->height!=context->sz_y) ||
        (srcGreen->width!=context->sz_x) || (srcGreen->height!=context->sz_y)) {
        return MBRT_ERR_SIZE;
    }
    
    pixels = ((PIX8 *)context->pixels);
    for(j=0; j<context->sz_y; j++) {
        for(i=0; i<context->sz_x; i++) {
            bufp = pixels + j*context->sz_x*4 + i*4;
            RED(bufp) = *(srcRed->plines[j]+i);
            GREEN(bufp) = *(srcGreen->plines[j]+i);
            BLUE(bufp) = *(srcBlue->plines[j]+i);
        }
    }
    
    /* icon display */
    for(j=0, v=0; j<(Uint32)context->iconh; j++) {
        for(i=0; i<(Uint32)context->iconw; i++, v++) {
            bufp = pixels + (16+j)*context->sz_x*4 + (16+i)*4;
            if (context->icon[v>>5] & (0x80000000>>(v&0x1f))) {
                *((Uint32 *)bufp) = FRAME_COLOR;
            } else {
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
                bufp++;
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
                bufp++;
                val = ((int) *bufp) - HISTO_BLACKENING;
                *bufp = val<0 ? 0 :(PIX8) val;
            }
        }
    }
    
    /* timestamp recording (used for video recording, blinking, and framerate computation */
    current_call = SDL_GetTicks();
    context->index_fps = (context->index_fps+1)%FPS_MEAN_SIZE;
    context->old_call[context->index_fps]=current_call;
    /* framerate computation averaged over FPS_MEAN_SIZE samples */
    *ofps = (FPS_MEAN_SIZE*1000.0)/((double) (current_call - context->old_call[(context->index_fps+1)%FPS_MEAN_SIZE]));
    
    /* frame rate display */
    if (context->isFpsDisplayed) {
        DRAW_FPS_RATE(*ofps, wfps);
    }
    /* recording display */
    if (context->isRecording) {
        DRAW_RECORD();
    }

    SDL_UpdateTexture(context->texture, NULL, context->pixels, context->sz_x*sizeof(Uint32));
    SDL_RenderClear(context->renderer);
    SDL_RenderCopy(context->renderer, context->texture, NULL, NULL);
    SDL_RenderPresent(context->renderer);
    return MBRT_NO_ERR;
}

/**
 * Changes the icon (black and white) in the upper left corner of 
 * the display. This allows to inform the user of some events. The icon is an 
 * array of binary 32bit integers.
 * \param width
 * \param height
 * \param icon the icon pixels array
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_IconDisplay(int width, int height, Uint32 *icon)
{
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;
    /* icon must be smaller than 64 pixels */
    if ((width>64) || (height>64)) return MBRT_ERR_ICON_SIZE;
    
    context->iconw = width;
    context->iconh = height;
    if (width*height>0) {
        memcpy(context->icon, icon, (width*height*sizeof(Uint32))/32);
    }
    
    return MBRT_NO_ERR;
}

/**
 * Changes the palette associated with the display
 * \param palette an array containing the complete palette definition (256*3 
 * integers)
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_PaletteDisplay(Uint8 *palette)
{
    int i;
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;

    for(i=0;i<256;i++) {
        context->palette[i].r = *palette++;
        context->palette[i].g = *palette++;
        context->palette[i].b = *palette++;
    }
    
    return MBRT_NO_ERR;
}

/**
 * Handles event that have occurred in the display
 * \param event_code an integer representing a specific event (output)
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_PollDisplay(MBRT_eventcode *event_code)
{
    SDL_Event event;
    
    /* Normally no events */
    *event_code = NO_EVENT;
    
    /* Verification over context */
    if (context==NULL) return MBRT_ERR_INVD_CTX;
    /* verification over display */
    if (context->pixels==NULL) return MBRT_ERR_INVALID_DISPLAY;
   
    /* Looking for pending events and handling them */
    while ( SDL_PollEvent(&event) ) {
        switch (event.type) {
            case SDL_QUIT:
                *event_code = EVENT_CLOSE;
                break;
            case SDL_KEYDOWN:
                switch(event.key.keysym.sym) {
                case SDLK_ESCAPE:
                    if (context->isFullscreen==1) {
                        /* in fullscreen mode, the escape is used to exit the */
                        /* fullscreen (too obvious way to move out of the */
                        /* fullscreen that it may cause troubles if the result */
                        /* is to close the complete operation */
                        SDL_SetWindowFullscreen(context->window, 0);
                        SDL_ShowCursor(1);
                        context->isFullscreen = 0;
                    } else {
                        /* in the other case, the realtime process is closed */
                        *event_code = EVENT_CLOSE;
                    }
                    break;
                case SDLK_PAUSE:
                    /* produce a pause event */
                    *event_code = EVENT_PAUSE;
                    break;
                case SDLK_f:
                    /* toggle fullscreen */
                    if (context->isFullscreen==1) {
                        SDL_SetWindowFullscreen(context->window, 0);
                        SDL_ShowCursor(1);
                        context->isFullscreen = 0;
                    } else {
                        SDL_SetWindowFullscreen(context->window, SDL_WINDOW_FULLSCREEN);
                        SDL_ShowCursor(0);
                        context->isFullscreen = 1;
                    }
                    break;
                case SDLK_p:
                    /* toggle the palette */
                    *event_code = EVENT_PALETTE;
                    break;
                case SDLK_r:
                    /* toggle the framerate display */
                    context->isFpsDisplayed = (1-context->isFpsDisplayed);
                    break;
                case SDLK_h:
                    /* toggle the framerate display */
                    context->isHistoDisplayed = (1-context->isHistoDisplayed);
                    break;
                case SDLK_o:
                    /* toggle the process on or off */
                    *event_code = EVENT_PROCESS;
                    break;
                case SDLK_c:
                    /* toggles the color on or off */
                    *event_code = EVENT_COLOR;
                    break;
                default:
                    break;
                }
                break;
            default:
                break;
       }
   }

   return MBRT_NO_ERR;
}
