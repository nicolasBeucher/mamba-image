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

/* The local header is the only header called inside each component of
 * the library, The global header is meant for the outside world.
 */
#include "mambaRTApi.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#include <libv4l2.h>
#include <linux/videodev2.h>
#include <sys/mman.h>
#include <sys/file.h>
#include <sys/ioctl.h>
#include <SDL/SDL.h>
#include <libavutil/avutil.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>
#include <libavutil/imgutils.h>

/****************************************/
/* Defines                              */
/****************************************/

#define INLINE inline

/** window title */
#define MBRT_TITLE "Mamba RealTime"

/** color used for on display information */
#define FRAME_COLOR 0xffc000

/** color used for the framerate bar display */
#define FPS_VALUE_COLOR 0xffc000
/** thickness of the framerate bar */
#define FPS_THICKNESS 3
/** framerate buffer size for mean value */
#define FPS_MEAN_SIZE 20

/** blackening value for the histogram background */
#define HISTO_BLACKENING 60
/** color of the histogram */
#define HISTO_COLOR     0xffffff

/** size of the recording icon */
#define REC_SIZE 64
/** color of the recording icon */
#define REC_COLOR  0xc00000

#ifndef AVIO_FLAG_WRITE
/** if mambaRealtime is compiled with an old version of FFmpeg */
#define AVIO_FLAG_WRITE AVIO_WRONLY
#endif

/****************************************/
/* Macros                               */
/****************************************/
 
/****************************************/
/* Structures and Typedef               */
/****************************************/

/* video for linux 2 API */

/** buffer structure */
struct buffer {
    /** address of the beginning of the buffer */
    void * start;
    /** size of the buffer */
    size_t length;
};
/** Information needed by V4L2 acquisition devices */
typedef struct {
    /** buffers to use for image saving */
    struct buffer *buffers;
    /** number of buffers */
    unsigned int n_buffers;
    /** image width */
    int w;
    /** image height */
    int h;
} MBRT_v4l2vidT;

/* audio video codec API */
/** Information needed by AVC acquisition devices */
typedef struct {
    /** AVC format in use */
    AVFormatContext *format_ctx;
    /** AVC video codec in use */
    AVCodecContext *codec_ctx;
    /** id of the video stream in the file */
    int videoStream;
    /** frame buffer in which each video frame is decoded */
    AVFrame *frame;
    /** frame buffer to convert in yuv format */
    AVFrame *yuvframe;
    /** frame buffer to convert in rgb format */
    AVFrame *rgbframe;
    /** packet buffer to extract frame */
    AVPacket packet;
} MBRT_avcvidT;

/** union for all the possible cases for video acquisition device */
typedef union
{
    /** V4L2 */
    MBRT_v4l2vidT v4l2;
    /** AVC */
    MBRT_avcvidT avc;
} MBRT_vidUnion;

/** Realtime library context struct */
typedef struct {
    /** video device type */
    MBRT_vidType type;
    /** file descriptor pointing to the device or file used to feed the acquisition */
    int fd;
    /** the union regrouping all the acquisition device type */
    MBRT_vidUnion video;
    /** screen */
    SDL_Surface *screen;
    /** display size (width) */
    Uint32 sz_x;
    /** display size (height) */
    Uint32 sz_y;
    /** palette */
    SDL_Color palette[256];
    /** framerate information and display */
    Uint32 isFpsDisplayed;
    /** call time history to compute a mean framerate */
    Uint32 old_call[FPS_MEAN_SIZE];
    /** position in the framerate history buffer */
    int index_fps;
    /** histogram array */
    Uint32 histo[256];
    /** is histogram active or not ? */
    Uint32 isHistoDisplayed;
    /** icon array */
    int iconw;
    int iconh;
    Uint32 icon[128];
    /** is fullscreen active or not ?*/
    Sint32 isFullscreen;
    /** is recording in progress or not ? */
    Uint32 isRecording;
    /** The recording codex context */
    AVCodecContext *rec_codctx;
    /** The recording output file */
    FILE *rec_file;
    /** packet for recording */
    AVPacket rec_pkt;
    /** frame buffer to record in rgb format */
    AVFrame *rec_picRGB;
    /** frame buffer to record in codec requested format */
    AVFrame *rec_picYUV;
    /** frame format conversion structure */
    struct SwsContext *rec_convctx;
    
} MBRT_Context;

/****************************************/
/* context global pointer               */
/****************************************/

/** Structure holding the complete context information (display, device, ...) */
extern MBRT_Context *context;

/****************************************/
/* video type specific functions        */
/****************************************/

/*V4L2*/
MBRT_errcode MBRT_CreateVideoAcq_v4l2(char *device);
MBRT_errcode MBRT_DestroyVideoAcq_v4l2(void);
MBRT_errcode MBRT_GetAcqSize_v4l2(int *acq_w, int *acq_h);
MBRT_errcode MBRT_GetAcqFrameRate_v4l2(double *fps);
MBRT_errcode MBRT_GetImageFromAcq_v4l2(MB_Image *dest);
MBRT_errcode MBRT_GetColorImageFromAcq_v4l2(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue);
/*AVC*/
MBRT_errcode MBRT_CreateVideoAcq_avc(char *video_path);
MBRT_errcode MBRT_DestroyVideoAcq_avc();
MBRT_errcode MBRT_GetAcqSize_avc(int *acq_w, int *acq_h);
MBRT_errcode MBRT_GetAcqFrameRate_avc(double *fps);
MBRT_errcode MBRT_GetImageFromAcq_avc(MB_Image *dest);
MBRT_errcode MBRT_GetColorImageFromAcq_avc(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue);


#endif
