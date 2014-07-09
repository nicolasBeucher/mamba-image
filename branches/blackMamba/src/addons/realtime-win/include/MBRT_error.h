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
    NO_ERR,
/** Cannot create (memory allocation) context */
    ERR_CANT_CREATE_CONTEXT,
/** Context is not properly initialized */
    ERR_INVD_CTX,
/** Init SDL display error */
    ERR_INIT_DISPLAY,
/** SDL display cannot support requested format */
    ERR_FORMAT_DISPLAY,
/** Locking screen for updating failure */
    ERR_LOCK_DISPLAY,
/** Incorrect display (not initialized) error */
    ERR_INVALID_DISPLAY,
/** Video acquisition module error */
    ERR_VID,
/** Cannot create the directshow filter graph */
	ERR_DSHOW_FILTER_GRAPH,
/** Cannot create the directshow capture graph builder */
	ERR_DSHOW_CAPT_GRAPH_BUILD,
/** Cannot initialize the directshow capture graph builder */
	ERR_DSHOW_INIT_CAPT_GRAPH_BUILD,
/** Cannot create the directshow device enumerator */
	ERR_DSHOW_DEV_ENUM,
/** Cannot create a directshow video capture device enumerator */
	ERR_DSHOW_VIDCAP_ENUM,
/** Cannot found the directshow device */
	ERR_DSHOW_DEV_NOT_FOUND,
/** Unsupported palette format */
    ERR_PAL_VID,
/** Type of the video acquisition is incorrect */
    ERR_VID_TYPE,
/** The depth of the mamba image given in argument is incompatible */
    ERR_DEPTH,
/** The size of the mamba image given in argument is incompatible */
    ERR_SIZE,
/** Cannot open the video file */
    ERR_AVC_VID_OPEN,
/** Cannot retrieve video stream information */
    ERR_AVC_STREAM_INFO,
/** No video stream present in video file */
    ERR_AVC_NO_VID_STREAM,
/** Cannot find appropriate video decoder */
    ERR_AVC_NO_CODEC,
/** Cannot open the video codec */
    ERR_AVC_CODEC_OPEN,
/** Cannot allocate the video frame */
    ERR_AVC_FRAME_ALLOC,
/** Cannot decode video frame */
    ERR_AVC_DECODING,
/** Cannot find format for recording */
    ERR_AVC_REC_FORMAT,
/** Cannot allocate format context for recording */
    ERR_AVC_REC_FMTCTX,
/** Cannot create stream for recording */
    ERR_AVC_REC_STREAM,
/** Invalid output format parameters for recording */
    ERR_AVC_REC_PARAM_SET,
/** Cannot find appropriate video decoder for recording */
    ERR_AVC_REC_NO_CODEC,
/** Cannot open the video codec for recording */
    ERR_AVC_REC_CODEC_OPEN,
/** Cannot allocate picture for recording */
    ERR_AVC_REC_PICT_ALLOC,
/** Cannot open the output file for recording */
    ERR_AVC_REC_FILE_OPEN,
/** Cannot encode the image for recording */
    ERR_AVC_REC_ENCODE,
/** Invalid recording context (not started) */
    ERR_AVC_REC_INV_CTX,
/** Unknown error */
    ERR_UNKNOWN
} MBRT_errcode;

/****************************************/
/* Functions                            */
/****************************************/

char *MBRT_StrErr(MBRT_errcode error_nb);

#ifdef __cplusplus
}
#endif

#endif
