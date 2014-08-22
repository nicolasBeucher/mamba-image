/**
 * \file MBRT_error.h
 * \date 3-28-2009
 *
 * This file contains the complete liste of error code 
 * returned by the API functions.
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
#ifndef MBRT_errorH
#define MBRT_errorH

#ifdef __cplusplus
extern "C" {
#endif

/****************************************/
/* Includes                             */
/****************************************/

/****************************************/
/* Defines                              */
/****************************************/

/****************************************/
/* Structures and Typedef               */
/****************************************/

/** Type definition for error code */
typedef enum {
/** Value returned by function when no error was encountered. */
    NO_ERR_RT,
/** Cannot create (memory allocation) context */
    ERR_RT_CANT_CREATE_CONTEXT,
/** Context is not properly initialized */
    ERR_RT_INVD_CTX,
/** Init SDL display error */
    ERR_RT_INIT_DISPLAY,
/** SDL display cannot support requested format */
    ERR_RT_FORMAT_DISPLAY,
/** Locking screen for updating failure */
    ERR_RT_LOCK_DISPLAY,
/** Incorrect display (not initialized) error */
    ERR_RT_INVALID_DISPLAY,
/** Video acquisition module error */
    ERR_RT_VID,
/** Cannot create the directshow filter graph */
	ERR_RT_DSHOW_FILTER_GRAPH,
/** Cannot create the directshow capture graph builder */
	ERR_RT_DSHOW_CAPT_GRAPH_BUILD,
/** Cannot initialize the directshow capture graph builder */
	ERR_RT_DSHOW_INIT_CAPT_GRAPH_BUILD,
/** Cannot create the directshow device enumerator */
	ERR_RT_DSHOW_DEV_ENUM,
/** Cannot create a directshow video capture device enumerator */
	ERR_RT_DSHOW_VIDCAP_ENUM,
/** Cannot found the directshow device */
	ERR_RT_DSHOW_DEV_NOT_FOUND,
/** Function is not implemented for video device */
    ERR_RT_NOT_IMPLEMENTED,
/** Cannot open video device */
    ERR_RT_OPEN_VID,
/** Video for linux 1 (V4L) is not supported */
    ERR_RT_NOT_HAVE_V4L,
/** Not a video for linux device */
    ERR_RT_V4L_VID,
/** Not a video for linux 2 device */
    ERR_RT_V4L2_VID,
/** Device does not support streaming */
    ERR_RT_STRM_VID,
/** Cannot obtain device resolution capabilities */
    ERR_RT_CAP_VID,
/** Cannot set device format */
    ERR_RT_FMT_VID,
/** Unsupported palette format */
    ERR_RT_PAL_VID,
/** Type of the video acquisition is incorrect */
    ERR_RT_VID_TYPE,
/** The depth of the mamba image given in argument is incompatible */
    ERR_RT_DEPTH,
/** The size of the mamba image given in argument is incompatible */
    ERR_RT_SIZE,
/** Cannot open the video file */
    ERR_RT_AVC_VID_OPEN,
/** Cannot retrieve video stream information */
    ERR_RT_AVC_STREAM_INFO,
/** No video stream present in video file */
    ERR_RT_AVC_NO_VID_STREAM,
/** Cannot find appropriate video decoder */
    ERR_RT_AVC_NO_CODEC,
/** Cannot open the video codec */
    ERR_RT_AVC_CODEC_OPEN,
/** Cannot allocate the video frame */
    ERR_RT_AVC_FRAME_ALLOC,
/** Cannot decode video frame */
    ERR_RT_AVC_DECODING,
/** Cannot allocate codec context for recording */
    ERR_RT_AVC_REC_CODCTX,
/** Cannot find appropriate video decoder for recording */
    ERR_RT_AVC_REC_NO_CODEC,
/** Cannot open the video codec for recording */
    ERR_RT_AVC_REC_CODEC_OPEN,
/** Cannot allocate picture for recording */
    ERR_RT_AVC_REC_PICT_ALLOC,
/** Cannot open the output file for recording */
    ERR_RT_AVC_REC_FILE_OPEN,
/** Cannot create the rgb->yuv converter */
    ERR_RT_AVC_REC_CONVERT_CTX,
/** Cannot encode the image for recording */
    ERR_RT_AVC_REC_ENCODE,
/** Invalid recording context (not started) */
    ERR_RT_AVC_REC_INV_CTX,
/** Unknown error */
    ERR_RT_UNKNOWN
} MBRT_errcode;

/****************************************/
/* Functions                            */
/****************************************/

char *MBRT_StrErr(MBRT_errcode error_nb);

#ifdef __cplusplus
}
#endif

#endif
