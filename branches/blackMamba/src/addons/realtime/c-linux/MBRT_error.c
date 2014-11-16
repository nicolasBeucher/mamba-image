/**
 * \file MBRT_error.c
 * \author Nicolas Beucher
 * \date 3-28-2009
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

/** Error value interpretation*/
char *err_str[] = {
    "No error",
    "Cannot initialize",
    "Cannot create (memory allocation) context",
    "Context is not properly initialized",
    "Initialize display error (SDL)",
    "SDL display cannot support requested format",
    "Locking screen for updating failure",
    "Incorrect display (not initialized) error",
    "Acquisition device error",
    "Cannot create the directshow filter graph",
    "Cannot create the directshow capture graph builder",
    "Cannot initialize the directshow capture graph builder",
    "Cannot create the directshow device enumerator",
    "Cannot create a directshow video capture device enumerator",
    "Cannot find the directshow device",
    "Function is not implemented for video device",
    "Cannot open video device",
    "Not a video for linux device",
    "Not a video for linux 2 device",
    "Device does not support streaming",
    "Cannot obtain device resolution capabilities",
    "Cannot set device format",
    "Unsupported palette format",
    "Type of the video acquisition is incorrect",
    "Incompatible depth for realtime acquisition/display",
    "Incompatible size for realtime acquisition/display",
    "Cannot open the video file",
    "Cannot retrieve video stream information",
    "No video stream present in video file",
    "Cannot find appropriate video decoder",
    "Cannot open the video codec",
    "Cannot allocate the video frame",
    "Cannot decode video frame",
    "Cannot allocate codec context for recording",
    "Cannot find appropriate video encoder for recording",
    "Cannot open the video codec for recording",
    "Cannot allocate picture for recording",
    "Cannot open the output file for recording",
    "Cannot create the rgb->yuv converter",
    "Cannot encode the image for recording",
    "Invalid recording context (not started)",
    "Invalid icon size",
    "Unknown error"
};

/**
 * Returns an explanation of the error code 
 */
char *MBRT_StrErr(MBRT_errcode error_nb) {
    if (error_nb>MBRT_ERR_UNKNOWN) {
        return err_str[MBRT_ERR_UNKNOWN];
    } else {
        return err_str[error_nb];
    }
}
