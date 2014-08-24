/**
 * \file MBRT_Context.c
 * \author Nicolas Beucher
 * \date 17-04-2010
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

/* General context handler */
MBRT_Context *context = NULL;

/**
 * Initialize the library.
 * Need to be called before anythong else.
 */
MBRT_errcode MBRT_Initialize()
{
    MBRT_errcode err = MBRT_NO_ERR;
    
    return err;
}

/**
 * Creates the context used throughout the library. The context describes the
 * data displayed, the device used for acquisition, and contains general 
 * information needed by all the functions
 */
MBRT_errcode MBRT_CreateContext()
{
    context = malloc(sizeof(MBRT_Context));
    if (context==NULL) {
        return MBRT_ERR_CANT_CREATE_CONTEXT;
    }
    
    /* blanking the structure */
    memset(context, 0, sizeof(MBRT_Context));
    
    context->screen = NULL;
    context->type = NONE_TYPE;
    context->isRecording = 0;

    return MBRT_NO_ERR;
}

/**
 * Destroye the context and all the data associated to it
 */
MBRT_errcode MBRT_DestroyContext()
{
    if (context!=NULL) {
    
        /* if the display and device are initialized */
        /* they are destroyed when the context is */
        /* destroyed */
        if (context->type!=NONE_TYPE) {
            MBRT_DestroyVideoAcq();
        }
        if (context->screen!=NULL) {
            MBRT_DestroyDisplay();
        }
        if (context->isRecording==1) {
            MBRT_RecordEnd();
        }
    
        free(context);
        context = NULL;
    }

    return MBRT_NO_ERR;
}
