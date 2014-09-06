/**
 * \file mambaRTApi_loc.h
 * \date 03-27-2009
 *
 * This file contains the various definitions, global variables
 * macro, struct and functions that are shared between components
 * of the library but are not meant to be exported to the outside
 * world.
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
#ifndef MBRT_apilocH
#define MBRT_apilocH

/**@cond */
/* code that must be skipped by Doxygen */
// #pragma include_alias( "dxtrans.h", "qedit.h" )
// #define __IDxtCompositor_INTERFACE_DEFINED__
// #define __IDxtAlphaSetter_INTERFACE_DEFINED__
// #define __IDxtJpeg_INTERFACE_DEFINED__
// #define __IDxtKey_INTERFACE_DEFINED__
/**@endcond*/

// #include <qedit.h> // Sample Grabber, Null Renderer
//
//#pragma comment (lib, "strmiids.lib")

#include "mambaRTApi.h"
#include <SDL.h> 
#include <dshow.h>

// FFmpeg libraries are pure C and thus must be identified as such to 
// work with visual C++ which seems to handle correctly C++ code. 
// In the case of mambaRealtime code, the C++ is a consequence of 
// directshow library. Most of the code is a ripe off mambaRealtime
// for Linux which is pure C
#ifdef __cplusplus
extern "C" {
#endif

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>

#ifdef __cplusplus
}
#endif

/****************************************/
/* Defines                              */
/****************************************/

/** Title displayed in the SDL window*/
#define MBRT_TITLE "Mamba RealTime"

/** Color used by icons */
#define FRAME_COLOR 0xffc000

/** Color used when displaying framerate */
#define FPS_VALUE_COLOR 0xffc000
/** Thickness of the framerate bar */
#define FPS_THICKNESS 3
/** Duration range for computation of the average framerate */
#define FPS_MEAN_SIZE 20

/** Value substracted to the image to blacken it for histogram display */
#define HISTO_BLACKENING 60
/** Color of the histogram */
#define HISTO_COLOR     0xffffff

/** Size of the icon indication recording in progress */
#define REC_SIZE 16
/** Color of the recording icon */
#define REC_COLOR  0xc00000

/****************************************/
/* Macros                               */
/****************************************/
 
/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Directshow device description structure */
typedef struct {
    /** directshow IGraphBuilder */
    IGraphBuilder         *pGraph;
    /** directshow ICaptureGraphBuilder2 */
    ICaptureGraphBuilder2 *pBuild;
    /** directshow IBaseFilter */
    IBaseFilter           *pCap;
    /** directshow ISampleGrabber */
    ISampleGrabber        *pGrab;
    /** directshow IMediaControl */
    IMediaControl         *pCtrl;
    /** device number as given when starting realtime */
    int devnum;
    /** width of the video */
    int w
    /** height of the video */
    int h;
    /** size of the pixels buffer */
    int size;
    /** buffer for pixels */
    void * buffer;
} MBRT_dshowvidT;

/** audio video codec API device description structure */
typedef struct {
    /** Format context */
    AVFormatContext *format_ctx;
    /** Codec context */
    AVCodecContext *codec_ctx; 
    /** index of the video stream */
    int videoStream;
    /** Pointer to a frame */
    AVFrame *frame;
    /** Pointer to a YUV frame */
    AVFrame *yuvframe;
    /** Pointer to a RGB frame */
    AVFrame *rgbframe;
    /** Packet container */
    AVPacket packet;
} MBRT_avcvidT;

/** union for all the possible cases for video acquisition device */
typedef union
{
    /** directshow */
    MBRT_dshowvidT dshow;
    /** AVC */
    MBRT_avcvidT avc;
} MBRT_vidUnion;

/** Realtime library context struct */
typedef struct {
    /** video device type */
    MBRT_vidType type;
    /** video device description */
    MBRT_vidUnion video;
    /** screen */
    SDL_Surface *screen;
    /** display width */
    Uint32 sz_x;
    /** display height */
    Uint32 sz_y;
    /** color palette */
    SDL_Color color_palette[256];
    /** greyscale palette */
    SDL_Color standard_palette[256];
    /** Using color palette */
    Uint32 isPalettized;
    /** framerate information is displayed */
    Uint32 isFpsDisplayed;
    /** Timing storage for FPS computation */
    Uint32 old_call[FPS_MEAN_SIZE];
    /** Current position in FPS computation storage */
    int index_fps;
    /** histogram */
    Uint32 histo[256];
    /** histogram information is displayed */
    Uint32 isHistoDisplayed;
    /** icon */
    Uint8 icon[256];
    /** fullscreen */
    Sint32 isFullscreen;
    /** recording is ON/OFF*/
    Uint32 isRecording;
    /** recording context */
    AVFormatContext *rec_fmt_ctx;
    /** recording color picture */
    AVFrame *pictureRGB;
    /** recording greyscale picture */
    AVFrame *picture;
    /** recording format converter */
    struct SwsContext *img_convert_ctx;
    /** recording buffer */
    uint8_t *video_outbuf;
    
} MBRT_Context;

/****************************************/
/* context global pointer               */
/****************************************/

/** Structure holding the complete context information (display, device, ...) */
extern MBRT_Context *context;

/****************************************/
/* video type specific functions        */
/****************************************/

/*DSHOW*/
MBRT_errcode MBRT_CreateVideoAcq_dshow(int device);
MBRT_errcode MBRT_DestroyVideoAcq_dshow(void);
MBRT_errcode MBRT_GetAcqSize_dshow(int *acq_w, int *acq_h);
MBRT_errcode MBRT_GetAcqFrameRate_dshow(double *fps);
MBRT_errcode MBRT_GetImageFromAcq_dshow(MB_Image *dest);
MBRT_errcode MBRT_GetColorImageFromAcq_dshow(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue);
MBRT_errcode MBRT_StopAcq_dshow();
MBRT_errcode MBRT_StartAcq_dshow();
/*AVC*/
MBRT_errcode MBRT_CreateVideoAcq_avc(char *video_path);
MBRT_errcode MBRT_DestroyVideoAcq_avc(void);
MBRT_errcode MBRT_GetAcqSize_avc(int *acq_w, int *acq_h);
MBRT_errcode MBRT_GetAcqFrameRate_avc(double *fps);
MBRT_errcode MBRT_GetImageFromAcq_avc(MB_Image *dest);
MBRT_errcode MBRT_GetColorImageFromAcq_avc(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue);
MBRT_errcode MBRT_StopAcq_avc();
MBRT_errcode MBRT_StartAcq_avc();


#endif
