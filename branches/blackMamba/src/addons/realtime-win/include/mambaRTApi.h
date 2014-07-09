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
#include "mambaCommon.h"
#include "MBRT_error.h"

#include <dshow.h>

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
/** Event to activate or deactive the color */
    EVENT_COLOR
} MBRT_eventcode;

/** Type definition for the acquisition device */
typedef enum {
/** DirectShow API type device */
    DSHOW_TYPE,
/** Audio video codec API type device (video file) */
    AVC_TYPE,
/** No device */
    NONE_TYPE,
} MBRT_vidType;

/****************************************/
/* Global variables                     */
/****************************************/

/****************************************/
/* Context functions                    */
/****************************************/
MBRT_errcode MBRT_CreateContext(void);
MBRT_errcode MBRT_DestroyContext(void);

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
MBRT_errcode MBRT_CreateDisplay(int w, int h);
MBRT_errcode MBRT_DestroyDisplay(void);
MBRT_errcode MBRT_UpdateDisplay(MB_Image *src, double wfps, double *ofps);
MBRT_errcode MBRT_UpdateDisplayColor(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue,
                                     double wfps, double *ofps);
MBRT_errcode MBRT_PaletteDisplay(Uint8 *palette);
MBRT_errcode MBRT_IconDisplay(Uint8 *icon);
MBRT_errcode MBRT_PollDisplay(MBRT_eventcode *event_code);

#ifdef __cplusplus
}
#endif

#endif

