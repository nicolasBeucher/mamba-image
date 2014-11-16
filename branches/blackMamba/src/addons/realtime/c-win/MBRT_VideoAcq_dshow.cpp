/**
 * \file MBRT_VideoAcq_dshow.cpp
 * \author Nicolas Beucher
 * \date 03-27-2009
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

/** error handling macro */
#define RETURN_ON_ERR(hr,MBRT_ERR_type) \
    if (FAILED(hr)) { \
        STOP_AND_CLEANUP(); \
        return MBRT_ERR_type; \
    } \

/**
 * Stops the device started and releases the different COM objects
 */
static INLINE void STOP_AND_CLEANUP(){
    MBRT_dshowvidT *acqDevice;
     
    context->type = NONE_TYPE;
    
    acqDevice = &(context->video.dshow);
    
    if (acqDevice!=NULL) {
        if (acqDevice->pCtrl != NULL)
            acqDevice->pCtrl->Release();
        if (acqDevice->pGrab != NULL)
            acqDevice->pGrab->Release();
        if (acqDevice->pCap != NULL)
            acqDevice->pCap->Release();
        if (acqDevice->pBuild != NULL)
            acqDevice->pBuild->Release();
        if (acqDevice->pGraph != NULL)
            acqDevice->pGraph->Release();

        if (acqDevice->buffer!=NULL)
            free(acqDevice->buffer);
    }
}

/**
 * Fills the video acquisition structure with the parameters of the given
 * device and initializes it (DSHOW).
 * \param device the video device (usually 0)
 * \return an error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_CreateVideoAcq_dshow(int device)
{
    int i;
    HRESULT hr;
    AM_MEDIA_TYPE mt;
    VIDEOINFOHEADER *pVideoHeader;
    IVideoWindow *pWindow;
    IBaseFilter *pF = NULL;
    IMoniker *pMoniker = NULL;
    ICreateDevEnum *pDevEnum = NULL;
    IEnumMoniker *pClassEnum = NULL;
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);
    
    /* device structure is prefilled */
    acqDevice->pGraph = NULL;
    acqDevice->pBuild = NULL;
    acqDevice->pCap = NULL;
    acqDevice->pGrab = NULL;
    acqDevice->pCtrl = NULL;
    acqDevice->devnum = device;
    acqDevice->w = 0;
    acqDevice->h = 0;
    acqDevice->size = 0;
    acqDevice->buffer = NULL;

    /* Create the filter graph. */
    hr = CoCreateInstance(CLSID_FilterGraph, NULL, CLSCTX_INPROC,
                          IID_IGraphBuilder, (void **)&acqDevice->pGraph);
    RETURN_ON_ERR(hr,MBRT_ERR_DSHOW_FILTER_GRAPH)

    /* Creates the capture graph builder. */
    hr = CoCreateInstance(CLSID_CaptureGraphBuilder2, NULL, CLSCTX_INPROC,
                          IID_ICaptureGraphBuilder2, (void **)&acqDevice->pBuild);
    RETURN_ON_ERR(hr,MBRT_ERR_DSHOW_CAPT_GRAPH_BUILD)

    /* Initializes the capture graph builder */
    hr = acqDevice->pBuild->SetFiltergraph(acqDevice->pGraph);
    RETURN_ON_ERR(hr,MBRT_ERR_DSHOW_INIT_CAPT_GRAPH_BUILD)

    /* Selecting a Capture Device through enumerator */
    /* Create the system device enumerator */
    hr = CoCreateInstance(CLSID_SystemDeviceEnum, NULL, CLSCTX_INPROC,
                          IID_ICreateDevEnum, (void **)&pDevEnum);
    RETURN_ON_ERR(hr,MBRT_ERR_DSHOW_DEV_ENUM)

    /* Creates an enumerator for video capture category */
    hr = pDevEnum->CreateClassEnumerator(CLSID_VideoInputDeviceCategory, &pClassEnum, 0);
    pDevEnum->Release();
    RETURN_ON_ERR(hr,MBRT_ERR_DSHOW_VIDCAP_ENUM)

    /* the enumerator is browsed until the appropriate device is found */
    for(i=0; i<=acqDevice->devnum; i++) {
        if (pClassEnum->Next(1, &pMoniker, NULL) != S_OK)
        {
            /* If any element of the enumerator could not be extracted */
            /* then we return on error */
            pClassEnum->Release();
            STOP_AND_CLEANUP();
            return MBRT_ERR_DSHOW_DEV_NOT_FOUND;
        }
    }
    pClassEnum->Release();

    /* Binds the moniker of the found device to a filter object. */
    if (acqDevice->pCap == NULL)
    {
        hr = pMoniker->BindToObject(0, 0, IID_IBaseFilter, (void**)&acqDevice->pCap);
        RETURN_ON_ERR(hr,MBRT_ERR_VID)
    }
    pMoniker->Release();

    /* The capture filter is added to the graph */
    hr = acqDevice->pGraph->AddFilter(acqDevice->pCap, L"Capture Filter");
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Creating a Sample Grabber filter */
    hr = CoCreateInstance(CLSID_SampleGrabber, NULL, CLSCTX_INPROC,
                          IID_IBaseFilter, (LPVOID *)&pF);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* setting up the sample grabber interface to the filter */
    hr = pF->QueryInterface(IID_ISampleGrabber, (void **)&acqDevice->pGrab);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Adding the filter to the graph filter */
    hr = acqDevice->pGraph->AddFilter(pF, L"Grabber");
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Specifying the media type and setting the grabber */
    ZeroMemory(&mt, sizeof(AM_MEDIA_TYPE));
    mt.majortype = MEDIATYPE_Video;
    mt.subtype = MEDIASUBTYPE_RGB24;
    mt.formattype = FORMAT_VideoInfo;
    hr = acqDevice->pGrab->SetMediaType(&mt);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Rendering the Streams */
    hr = acqDevice->pBuild->RenderStream(
            &PIN_CATEGORY_CAPTURE, 
            &MEDIATYPE_Video,
            acqDevice->pCap, 
            pF,   
            NULL 
        );
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    pF->Release();

    /* Do not display the window (obtains its handle and sets show to false) */
    hr = acqDevice->pGraph->QueryInterface(IID_IVideoWindow, (void **)&pWindow);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)
    hr = pWindow->put_AutoShow(OAFALSE);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)
    pWindow->Release();
    
    /* Grabs the control over the graph */
    hr = acqDevice->pGraph->QueryInterface(IID_IMediaControl, (void **)&acqDevice->pCtrl);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* the data grab is copied to a buffer */
    hr = acqDevice->pGrab->SetBufferSamples(TRUE);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Set up one-shot mode */
    hr = acqDevice->pGrab->SetOneShot(FALSE);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Retrieve media information */
    hr = acqDevice->pGrab->GetConnectedMediaType(&mt);
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    /* Gets a pointer to the video header and retrieve information */
    pVideoHeader = (VIDEOINFOHEADER*)mt.pbFormat;
    acqDevice->w = pVideoHeader->bmiHeader.biWidth;
    acqDevice->h = pVideoHeader->bmiHeader.biHeight;
    acqDevice->size = pVideoHeader->bmiHeader.biSizeImage;

    /* Allocates memory for pixel buffer */
    acqDevice->buffer = malloc(acqDevice->size);
    if (acqDevice->buffer==NULL) {
        STOP_AND_CLEANUP();
        return MBRT_ERR_VID;
    }

    /* Frees the format block */
    CoTaskMemFree(mt.pbFormat);

    return MBRT_NO_ERR;
}

/**
 * Stops the acquisition device capture process (DSHOW).
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_StopAcq_dshow()
{
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);

    if (acqDevice->pCtrl != NULL)
        acqDevice->pCtrl->Stop();

    return MBRT_NO_ERR;
}

/**
 * Starts the acquisition device capture process (DSHOW).
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_StartAcq_dshow()
{
    HRESULT hr;
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);

    /* Runs the graph */
    hr = acqDevice->pCtrl->Run();
    RETURN_ON_ERR(hr,MBRT_ERR_VID)

    return MBRT_NO_ERR;
}

/**
 * Obtains an image from the acquisition device (DSHOW).
 * \param dest the mamba image filled by the device
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetImageFromAcq_dshow(MB_Image *dest)
{
    HRESULT hr;
    int i,j;
    PLINE buf, ptr, rowptr;
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);

    if (dest->depth!=8) {
        /* Image depth must be 8 */
        return MBRT_ERR_DEPTH;
    }

    long size = (long) acqDevice->size;
 
    /* Copy the image into the buffer. */
    while (true)
    {
        hr = acqDevice->pGrab->GetCurrentBuffer(&size, (long *)acqDevice->buffer);
        if (hr == VFW_E_WRONG_STATE)
            Sleep(100);
        else
            break;
    }
    if (FAILED(hr))
        return MBRT_ERR_VID;

    /* copies the buffer content into the dest mamba image */
    /* the buffer contains the image with the last line first and */
    /* pixels in order BGR */
    buf = (PLINE) acqDevice->buffer;
    for(i=0; i<acqDevice->h; i++) {
        rowptr = (PLINE) (dest->plines[i]);
        ptr = (buf+(acqDevice->h-1-i)*acqDevice->w*3);
        for(j=0; j<acqDevice->w; j++, rowptr++) {
            /* the BGR format is converted into greyscale format */
            *rowptr = 114* (*(ptr))/1000 + 587* (*(ptr+1))/1000 + 299* (*ptr+1)/1000;
            ptr += 3;
        }
    }

    return MBRT_NO_ERR;
}

/**
 * Obtains an color image from the acquisition device (DSHOW).
 * \param destRed the mamba image filled by the device with the red channel
 * \param destGreen the mamba image filled by the device with the green channel
 * \param destBlue the mamba image filled by the device with the blue channel
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetColorImageFromAcq_dshow(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue)
{
    HRESULT hr;
    int i,j;
    PLINE buf, ptr, rowptrR, rowptrB, rowptrG;
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);

    /* only 8-bit images can be filled*/
    if ( (destRed->depth!=8) ||
         (destBlue->depth!=8) ||
         (destGreen->depth!=8) ) {
        return MBRT_ERR_DEPTH;
    }

    long size = (long) acqDevice->size;
 
    /* Copy the image into the buffer. */
    while (true)
    {
        hr = acqDevice->pGrab->GetCurrentBuffer(&size, (long *)acqDevice->buffer);
        if (hr == VFW_E_WRONG_STATE)
            Sleep(100);
        else
            break;
    }
    if (FAILED(hr))
        return MBRT_ERR_VID;

    /* copies the buffer content into the dest mamba image */
    /* the buffer contains the image with the last line first and */
    /* pixels in order BGR */
    buf = (PLINE) acqDevice->buffer;
    for(i=0; i<acqDevice->h; i++) {
        rowptrR = (PLINE) (destRed->plines[i]);
        rowptrG = (PLINE) (destGreen->plines[i]);
        rowptrB = (PLINE) (destBlue->plines[i]);
        ptr = (buf+(acqDevice->h-1-i)*acqDevice->w*3);
        for(j=0; j<acqDevice->w; j++, rowptrR++, rowptrG++, rowptrB++) {
            /* the BGR format is converted into greyscale format */
            *rowptrB = *ptr;
            *rowptrG = *(ptr+1);
            *rowptrR = *(ptr+2);
            ptr += 3;
        }
    }

    return MBRT_NO_ERR;
}

/**
 * Closes the acquisition device and reset the structure (DSHOW).
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_DestroyVideoAcq_dshow()
{
    STOP_AND_CLEANUP();

    return MBRT_NO_ERR;
}

/**
 * Returns the acquisition device resolution (DSHOW).
 * \param acq_w the width (output)
 * \param acq_h the height (output)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqSize_dshow(int *acq_w, int *acq_h)
{
    MBRT_dshowvidT *acqDevice;
    
    /* pointer to the video structure */
    acqDevice = &(context->video.dshow);
    
    *acq_w = acqDevice->w;
    *acq_h = acqDevice->h;

    return MBRT_NO_ERR;
}

/**
 * Returns the acquisition device default framerate (DSHOW).
 * \param ofps the framerate in frame per second (output)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqFrameRate_dshow(double *ofps)
{
    *ofps = 20.0;
    
    return MBRT_NO_ERR;
}

