/**
 * \file MBRT_VideoAcq_v4l2.c
 * \author Nicolas Beucher
 * \date 04-07-2009
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

/** macro to erase a buffer (set to 0) */
#define CLEAR(x) memset (&(x), 0, sizeof (x))

/**
 * Fills the video acquisition (V4L2) structure with the parameters of the given
 * device and initializes it.
 * \param device the video device (usually /dev/video0)
 * \return an error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_CreateVideoAcq_v4l2(char *device)
{
    struct v4l2_capability cap;
    struct v4l2_cropcap cropcap;
    struct v4l2_crop crop;
    struct v4l2_format fmt;
    struct v4l2_requestbuffers req;
    enum v4l2_buf_type type;
    unsigned int i;

    /* opening the device */
    context->fd = v4l2_open(device, O_RDWR);
    if(context->fd<0) {
        return ERR_OPEN_VID;
    }
    
    /* is the device a valid video for linux 2 device? */
    if (v4l2_ioctl(context->fd, VIDIOC_QUERYCAP, &cap) < 0) {
        return ERR_V4L2_VID;
    }

    /* the device must be a capture device (take pictures and support streaming)*/
    if (!(cap.capabilities & (V4L2_CAP_VIDEO_CAPTURE|V4L2_CAP_STREAMING))) {
        return ERR_STRM_VID;
    }
    
    /* Select video input, video standard and tune here. */
    
    /* reseting the device cropping to its default rectangle */
    CLEAR (cropcap);
    cropcap.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    if (v4l2_ioctl(context->fd, VIDIOC_CROPCAP, &cropcap) < 0) {
        /* resolution is unreadable: assuming 640x480 */
        context->video.v4l2.w = 640;
        context->video.v4l2.h = 480;
    } else {
        /* maximum resolution possible */
        context->video.v4l2.w = cropcap.defrect.width;
        context->video.v4l2.h = cropcap.defrect.height;
    }
    crop.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    crop.c = cropcap.defrect; /* reset to default */
    v4l2_ioctl(context->fd, VIDIOC_S_CROP, &crop); /* don't care if there is an error */


    /* selecting format, resolution, ... */
    CLEAR (fmt);
    fmt.type                = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width       = context->video.v4l2.w;
    fmt.fmt.pix.height      = context->video.v4l2.h;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUV420;
    fmt.fmt.pix.field       = V4L2_FIELD_INTERLACED; /* is this needed ?? */
    if (v4l2_ioctl(context->fd, VIDIOC_S_FMT, &fmt) < 0) {
        return ERR_FMT_VID;
    }
    /* VIDIOC_S_FMT may change width and height so... */
    context->video.v4l2.w = fmt.fmt.pix.width;
    context->video.v4l2.h = fmt.fmt.pix.height;
    
    /* requesting buffer in device memory */
    CLEAR(req);
    req.count               = 2;
    req.type                = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory              = V4L2_MEMORY_MMAP;
    if ((v4l2_ioctl(context->fd, VIDIOC_REQBUFS, &req) < 0) ||
        (req.count < 2) ) {
        return ERR_VID;
    }

    /* allocation the buffers */
    context->video.v4l2.buffers = calloc (req.count, sizeof (*(context->video.v4l2.buffers)));
    if (!(context->video.v4l2.buffers)) {
        return ERR_VID;
    }

    /* init of each buffer and memory mapping */
    for (context->video.v4l2.n_buffers = 0; 
         context->video.v4l2.n_buffers < req.count; 
         context->video.v4l2.n_buffers++) {
        struct v4l2_buffer buf;

        CLEAR (buf);

        buf.type        = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory      = V4L2_MEMORY_MMAP;
        buf.index       = context->video.v4l2.n_buffers;
        if (v4l2_ioctl(context->fd, VIDIOC_QUERYBUF, &buf) < 0) {
            return ERR_VID;
        }

        /* memory mapping */
        context->video.v4l2.buffers[context->video.v4l2.n_buffers].length = buf.length;
        context->video.v4l2.buffers[context->video.v4l2.n_buffers].start =
                        v4l2_mmap(NULL /* start anywhere */,
                              buf.length,
                              PROT_READ | PROT_WRITE /* required */,
                              MAP_SHARED /* recommended */,
                              context->fd, buf.m.offset);

        if (MAP_FAILED == context->video.v4l2.buffers[context->video.v4l2.n_buffers].start){
            return ERR_VID;
        }
    }

    /* starting the bufferization */
    for (i=0; i < context->video.v4l2.n_buffers; i++) {
        struct v4l2_buffer buf;
        CLEAR (buf);
        buf.type        = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory      = V4L2_MEMORY_MMAP;
        buf.index       = i;
        if (v4l2_ioctl (context->fd, VIDIOC_QBUF, &buf) < 0 ){
            return ERR_VID;
        }
    }
    /* starting the stream */
    type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    if (v4l2_ioctl (context->fd, VIDIOC_STREAMON, &type) < 0){
        return ERR_VID;
    }
    
    return NO_ERR;
}

/**
 * Closes the acquisition device (V4L2) and resets the structure
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_DestroyVideoAcq_v4l2()
{
    unsigned int i;
    
    /* streaming stop */
    enum v4l2_buf_type type;
    type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    v4l2_ioctl(context->fd, VIDIOC_STREAMOFF, &type);

    /* unmapping and freeing buffers */
    for (i=0; i < context->video.v4l2.n_buffers; i++)
        v4l2_munmap(context->video.v4l2.buffers[i].start, 
                    context->video.v4l2.buffers[i].length);
    free(context->video.v4l2.buffers);

    /* if the device exists it is destroyed */
    v4l2_close(context->fd);
    
    return NO_ERR;
}

/**
 * Returns the acquisition device resolution (V4L2).
 * \param acq_w the width (output)
 * \param acq_h the height (output)
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqSize_v4l2(int *acq_w, int *acq_h)
{
    *acq_h = context->video.v4l2.h;
    *acq_w = context->video.v4l2.w;
    
    return NO_ERR;
}

/**
 * Returns the acquisition device default framerate (V4L2).
 * \param ofps the framerate in frame per second (output)
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqFrameRate_v4l2(double *ofps)
{
    *ofps = 10.0f;
    return NO_ERR;
}

/**
 * Obtains an image from the acquisition device (V4L2)
 * \param dest the mamba image filled by the device
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetImageFromAcq_v4l2(MB_Image *dest) {
    struct v4l2_buffer buf;
    PLINE ptr;

    CLEAR (buf);
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;

    /* only 8-bit images can be filled*/
    if (dest->depth!=8) {
        return ERR_DEPTH;
    }

    if (v4l2_ioctl(context->fd, VIDIOC_DQBUF, &buf) < 0) {
        return ERR_VID;
    }
    if(buf.index >= context->video.v4l2.n_buffers){
        return ERR_VID;
    }
    
    ptr = (PLINE) (context->video.v4l2.buffers[buf.index].start);
    
    memcpy(dest->pixels, ptr, context->video.v4l2.w*context->video.v4l2.h);

    if (v4l2_ioctl (context->fd, VIDIOC_QBUF, &buf) < 0) {
        return ERR_VID;
    }
    
    return NO_ERR;
}

static inline PIX8 CLAMP_255(int value)
{
    return (PIX8) (value > 255 ? 255 : (value<0 ? 0 : value));
}

/**
 * Obtains a color image from the video (V4L2)
 * \param destRed the mamba image filled by the device with the red channel
 * \param destGreen the mamba image filled by the device with the green channel
 * \param destBlue the mamba image filled by the device with the blue channel
 * 
 * \return NO_ERR if successful
 */
MBRT_errcode MBRT_GetColorImageFromAcq_v4l2(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue)
{
    struct v4l2_buffer buf;
    PLINE ptr,pdR, pdG, pdB;
    int posx,posy,w,h,size;
    int y,u,v;

    CLEAR (buf);
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;

    /* only 8-bit images can be filled*/
    if ( (destRed->depth!=8) ||
         (destBlue->depth!=8) ||
         (destGreen->depth!=8) ) {
        return ERR_DEPTH;
    }

    if (v4l2_ioctl(context->fd, VIDIOC_DQBUF, &buf) < 0) {
        return ERR_VID;
    }
    if(buf.index >= context->video.v4l2.n_buffers){
        return ERR_VID;
    }
    
    ptr = (PLINE) (context->video.v4l2.buffers[buf.index].start);
    w = context->video.v4l2.w;
    h = context->video.v4l2.h;
    size = w*h;
    for(posy=0; posy<h; posy++) {
        pdR = destRed->plines[posy];
        pdG = destGreen->plines[posy];
        pdB = destBlue->plines[posy];
        for(posx=0; posx<w; posx++, pdR++, pdG++, pdB++) {
            y = (int) ptr[posy*w + posx] - 16;
            u = (int) ptr[(posy/2)*(w/2) + (posx/2) + size] - 128;
            v = (int) ptr[(posy/2)*(w/2) + (posx/2) + size + (size/4)] - 128;
            *pdR = CLAMP_255((298*y+409*v+128)>>8);
            *pdG = CLAMP_255((298*y-100*u-208*v+128)>>8);
            *pdB = CLAMP_255((298*y+516*u+128)>>8);
        }
    }

    if (v4l2_ioctl (context->fd, VIDIOC_QBUF, &buf) < 0) {
        return ERR_VID;
    }
    
    return NO_ERR;
    return NO_ERR;
}
