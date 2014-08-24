/**
 * \file mambaRTApi.h
 * \date 03-27-2009
 *
 * This file contains the various definitions, global variables
 * macro, struct and functions created for the library.
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
#ifndef MBRT_apiH
#define MBRT_apiH

#ifdef __cplusplus
extern "C" {
#endif

/****************************************/
/* Includes                             */
/****************************************/
#include "mamba/mamba.h"

/****************************************/
/* Defines                              */
/****************************************/

/****************************************/
/* Macros                               */
/****************************************/

/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Type definition for display event code */
typedef enum {
/** No events */
    NO_EVENT,
/** Close event occurs when the user closes the window or press esc inside it */
    EVENT_CLOSE,
/** Event to toggle on/off the process */
    EVENT_PROCESS,
/** Event to activate or deactive the pause */
    EVENT_PAUSE,
/** Event to modify the palette */
    EVENT_PALETTE,
/** Event to activate or deactive the color */
    EVENT_COLOR
} MBRT_eventcode;

/** Type definition for the acquisition device */
typedef enum {
#ifdef MBRT_WIN
/** DirectShow API type device */
    DSHOW_TYPE,
#else
/** Video 4 Linux 2 API type device */
    V4L2_TYPE,
#endif
/** Audio video codec API type device (video file) */
    AVC_TYPE,
/** No device */
    NONE_TYPE,
} MBRT_vidType;

/** Type definition for error code */
typedef enum {
/** Value returned by function when no error was encountered. */
    MBRT_NO_ERR,
/** Cannot initialize */
    MBRT_ERR_INIT,
/** Cannot create (memory allocation) context */
    MBRT_ERR_CANT_CREATE_CONTEXT,
/** Context is not properly initialized */
    MBRT_ERR_INVD_CTX,
/** Init SDL display error */
    MBRT_ERR_INIT_DISPLAY,
/** SDL display cannot support requested format */
    MBRT_ERR_FORMAT_DISPLAY,
/** Locking screen for updating failure */
    MBRT_ERR_LOCK_DISPLAY,
/** Incorrect display (not initialized) error */
    MBRT_ERR_INVALID_DISPLAY,
/** Video acquisition module error */
    MBRT_ERR_VID,
/** Cannot create the directshow filter graph */
    MBRT_ERR_DSHOW_FILTER_GRAPH,
/** Cannot create the directshow capture graph builder */
    MBRT_ERR_DSHOW_CAPT_GRAPH_BUILD,
/** Cannot initialize the directshow capture graph builder */
    MBRT_ERR_DSHOW_INIT_CAPT_GRAPH_BUILD,
/** Cannot create the directshow device enumerator */
    MBRT_ERR_DSHOW_DEV_ENUM,
/** Cannot create a directshow video capture device enumerator */
    MBRT_ERR_DSHOW_VIDCAP_ENUM,
/** Cannot found the directshow device */
    MBRT_ERR_DSHOW_DEV_NOT_FOUND,
/** Function is not implemented for video device */
    MBRT_ERR_NOT_IMPLEMENTED,
/** Cannot open video device */
    MBRT_ERR_OPEN_VID,
/** Not a video for linux device */
    MBRT_ERR_V4L_VID,
/** Not a video for linux 2 device */
    MBRT_ERR_V4L2_VID,
/** Device does not support streaming */
    MBRT_ERR_STRM_VID,
/** Cannot obtain device resolution capabilities */
    MBRT_ERR_CAP_VID,
/** Cannot set device format */
    MBRT_ERR_FMT_VID,
/** Unsupported palette format */
    MBRT_ERR_PAL_VID,
/** Type of the video acquisition is incorrect */
    MBRT_ERR_VID_TYPE,
/** The depth of the mamba image given in argument is incompatible */
    MBRT_ERR_DEPTH,
/** The size of the mamba image given in argument is incompatible */
    MBRT_ERR_SIZE,
/** Cannot open the video file */
    MBRT_ERR_AVC_VID_OPEN,
/** Cannot retrieve video stream information */
    MBRT_ERR_AVC_STREAM_INFO,
/** No video stream present in video file */
    MBRT_ERR_AVC_NO_VID_STREAM,
/** Cannot find appropriate video decoder */
    MBRT_ERR_AVC_NO_CODEC,
/** Cannot open the video codec */
    MBRT_ERR_AVC_CODEC_OPEN,
/** Cannot allocate the video frame */
    MBRT_ERR_AVC_FRAME_ALLOC,
/** Cannot decode video frame */
    MBRT_ERR_AVC_DECODING,
/** Cannot allocate codec context for recording */
    MBRT_ERR_AVC_REC_CODCTX,
/** Cannot find appropriate video decoder for recording */
    MBRT_ERR_AVC_REC_NO_CODEC,
/** Cannot open the video codec for recording */
    MBRT_ERR_AVC_REC_CODEC_OPEN,
/** Cannot allocate picture for recording */
    MBRT_ERR_AVC_REC_PICT_ALLOC,
/** Cannot open the output file for recording */
    MBRT_ERR_AVC_REC_FILE_OPEN,
/** Cannot create the rgb->yuv converter */
    MBRT_ERR_AVC_REC_CONVERT_CTX,
/** Cannot encode the image for recording */
    MBRT_ERR_AVC_REC_ENCODE,
/** Invalid recording context (not started) */
    MBRT_ERR_AVC_REC_INV_CTX,
/** Invalid icon size */
    MBRT_ERR_ICON_SIZE,
/** Unknown error */
    MBRT_ERR_UNKNOWN
} MBRT_errcode;

/****************************************/
/* Global variables                     */
/****************************************/

/****************************************/
/* Context functions                    */
/****************************************/
MBRT_errcode MBRT_Initialize(void);
MBRT_errcode MBRT_CreateContext(void);
MBRT_errcode MBRT_DestroyContext(void);

char *MBRT_StrErr(MBRT_errcode error_nb);

/****************************************/
/* Acquisition functions                */
/****************************************/
MBRT_errcode MBRT_CreateVideoAcq(char *device, MBRT_vidType type);
MBRT_errcode MBRT_DestroyVideoAcq(void);
MBRT_errcode MBRT_GetAcqSize(int *acq_w, int *acq_h);
MBRT_errcode MBRT_GetAcqFrameRate(double *ofps);
MBRT_errcode MBRT_GetImageFromAcq(MB_Image *dest);
MBRT_errcode MBRT_GetColorImageFromAcq(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue);
MBRT_errcode MBRT_StartAcq();
MBRT_errcode MBRT_StopAcq();

/****************************************/
/* Recording functions                  */
/****************************************/
MBRT_errcode MBRT_RecordStart(char *filename);
MBRT_errcode MBRT_RecordEnd(void);
MBRT_errcode MBRT_RecordImage(MB_Image *src);
MBRT_errcode MBRT_RecordColorImage(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue);

/****************************************/
/* Display functions                    */
/****************************************/
MBRT_errcode MBRT_CreateDisplay(int width, int height);
MBRT_errcode MBRT_DestroyDisplay(void);
MBRT_errcode MBRT_UpdateDisplay(MB_Image *src, double wfps, double *ofps);
MBRT_errcode MBRT_UpdateDisplayColor(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue,
                                     double wfps, double *ofps);
MBRT_errcode MBRT_PaletteDisplay(Uint8 *palette);
MBRT_errcode MBRT_IconDisplay(int width, int height, Uint32 *icon);
MBRT_errcode MBRT_PollDisplay(MBRT_eventcode *event_code);

#ifdef __cplusplus
}
#endif

#endif

