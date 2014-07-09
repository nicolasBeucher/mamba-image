/**
 * \file MBRT_VideoAcq_v4l.c
 * \author Nicolas Beucher
 * \date 04-07-2009
 *
 */
 
#ifdef MBRT_HAVE_V4L

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


/**
 * Fills the video acquisition (V4L) structure with the parameters of the given
 * device and initializes it.
 * \param device the video device (usually /dev/video0)
 * \return an error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_CreateVideoAcq_v4l(char *device)
{
    int i;
    
    /* opening the device */
    context->fd = v4l1_open(device, O_RDWR);
    if(context->fd<0) {
        return ERR_OPEN_VID;
    }
    
    /* is it a valid video 4 linux device? */
    /* If yes, returns the device capabilities (resolution, ...)*/
    if( v4l1_ioctl(context->fd, VIDIOCGCAP, &(context->video.v4l.vcap) ) < 0 ) {
        return ERR_V4L_VID;
    }
    
    /* get properties for video window */
    if( v4l1_ioctl(context->fd, VIDIOCGWIN, &(context->video.v4l.vwin)) < 0 ) {
        return ERR_CAP_VID;
    }
    
    /* get the palette used by the device */
    if( v4l1_ioctl(context->fd, VIDIOCGPICT, &(context->video.v4l.vpic)) < 0 ) {
        return ERR_CAP_VID;
    }
    
    /* resolution to the max */
    context->video.v4l.vwin.width = context->video.v4l.vcap.maxwidth;
    context->video.v4l.vwin.height = context->video.v4l.vcap.maxheight;
    v4l1_ioctl (context->fd, VIDIOCSWIN, &(context->video.v4l.vwin));
    

    memset (&(context->video.v4l.vmbuf), 0, sizeof (context->video.v4l.vmbuf));
    v4l1_ioctl(context->fd, VIDIOCGMBUF, &(context->video.v4l.vmbuf));

   /* maping the memory of the device to the specific pointer*/
    context->video.v4l.FRAMEBUFFER = (PIX8 *) v4l1_mmap (0, 
                                                 context->video.v4l.vmbuf.size,
                                                 PROT_READ | PROT_WRITE,
                                                 MAP_SHARED,
                                                 context->fd,
                                                 0);

    context->video.v4l.vmmap.width = context->video.v4l.vwin.width;
    context->video.v4l.vmmap.height = context->video.v4l.vwin.height;
    context->video.v4l.vmmap.format = context->video.v4l.vpic.palette;

    for(i=0 ; i<context->video.v4l.vmbuf.frames ; i++) {
        context->video.v4l.vmmap.frame = i;
        v4l1_ioctl (context->fd, VIDIOCMCAPTURE, &(context->video.v4l.vmmap));
    }
    context->video.v4l.vmmap.frame = 0;
   
    return NO_ERR;
}

/**
 * Closes the acquisition device (V4L) and resets the structure
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_DestroyVideoAcq_v4l()
{
    int i;
    
    for(i=0 ; i<context->video.v4l.vmbuf.frames ; i++) {
        v4l1_ioctl(context->fd, VIDIOCSYNC, &i);
    }
    
    /* unmaping the memory of the device*/
    v4l1_munmap(context->video.v4l.FRAMEBUFFER, context->video.v4l.vmbuf.size);
    
    /* if the device exists it is destroyed */
    v4l1_close(context->fd);
    
    return NO_ERR;
}

/**
 * Returns the acquisition device resolution (V4L).
 * \param acq_w the width (output)
 * \param acq_h the height (output)
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqSize_v4l(int *acq_w, int *acq_h)
{
    *acq_h = context->video.v4l.vwin.height;
    *acq_w = context->video.v4l.vwin.width;
    
    return NO_ERR;
}

/**
 * Returns the acquisition device default framerate (V4L).
 * \param ofps the framerate in frame per second (output)
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqFrameRate_v4l(double *ofps)
{
    *ofps = 10.0;
    return NO_ERR;
}

/**
 * Obtains an image from the acquisition device (V4L)
 * \param dest the mamba image filled by the device
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetImageFromAcq_v4l(MB_Image *dest)
{
    int framenb;
    int i,j;
    int tmp;
    PLINE ptr, rowptr;

    /* only 8-bit images can be filled*/
    if (dest->depth!=8) {
        return ERR_DEPTH;
    }

    if( (context->video.v4l.vpic.palette != VIDEO_PALETTE_YUV420P ) && 
        (context->video.v4l.vpic.palette != VIDEO_PALETTE_RGB24) ){
        return ERR_PAL_VID;
    }

    framenb = context->video.v4l.vmmap.frame;
    if( v4l1_ioctl (context->fd, VIDIOCSYNC, &framenb) < 0 ) {
        return ERR_VID;
    }
    context->video.v4l.vmmap.frame = framenb;  
    ptr = context->video.v4l.FRAMEBUFFER + context->video.v4l.vmbuf.offsets[context->video.v4l.vmmap.frame];


    if( context->video.v4l.vpic.palette == VIDEO_PALETTE_YUV420P ) {
        for(i=0 ; i<context->video.v4l.vwin.height; i++) {
            memcpy((dest->PLINES[Y_TOP+i]+X_LEFT), ptr, context->video.v4l.vwin.width);
            ptr += context->video.v4l.vwin.width;
        }
    }else {
        for(i=0 ; i<context->video.v4l.vwin.height ; i++) {
            rowptr = (PLINE) (dest->PLINES[Y_TOP+i]+X_LEFT);
            for(j=0 ; j<context->video.v4l.vwin.width ; j++, rowptr++) {
                tmp = *ptr++;
                tmp += *ptr++;
                tmp += *ptr++;
                *rowptr= (PIX8) (tmp/3);
            }
        }
    }
  
    if((v4l1_ioctl (context->fd, VIDIOCMCAPTURE, &(context->video.v4l.vmmap))) < 0 ) {
        return ERR_VID;
    }
    context->video.v4l.vmmap.frame = (context->video.v4l.vmmap.frame + 1) % context->video.v4l.vmbuf.frames;
  
    return NO_ERR;
}

#endif

