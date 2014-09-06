/**
 * \file MBRT_VideoAcq_avc.cpp
 * \author Nicolas Beucher
 * \date 04-01-2010
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

/**
 * Opens a video file as a video acquisition device using the advanced video
 * codec (AVC) library.
 * \param video_path path to the video file (supported codec depends on your local
 * implementation of the libavcodec)
 * \return an error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_CreateVideoAcq_avc(char *video_path)
{
    int i;
    AVFormatContext *format_ctx; /* local pointer to keep the code simpler */
    AVCodecContext *codec_ctx;
    AVCodec *codec; 
    uint8_t *picture_buf;
    int size;

    /* registering all codecs, formats ... */
    av_register_all();
    
    /* disabling logging (mess with the Python command line) */
    av_log_set_level(-1);
    
    /* opening the video file */
    if(av_open_input_file(&format_ctx, video_path, NULL, 0, NULL)!=0) {
        context->type = NONE_TYPE;
        return MBRT_ERR_AVC_VID_OPEN;
    }
    context->video.avc.format_ctx = format_ctx;
    
    /* Retrieving stream information */
    if(av_find_stream_info(format_ctx)<0) {
        context->type = NONE_TYPE;
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_STREAM_INFO;
    }
    
    /* Retrieving the video stream number in the file */
    context->video.avc.videoStream=-1;
    for(i=0; i<format_ctx->nb_streams; i++) {
        if((format_ctx->streams[i])->codec->codec_type==CODEC_TYPE_VIDEO)
        {
            context->video.avc.videoStream=i;
            break;
        }
    }
    if(context->video.avc.videoStream==-1) {
        context->type = NONE_TYPE;
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_NO_VID_STREAM; 
    }
    
    /* codec pointer is extracted */
    codec_ctx = format_ctx->streams[context->video.avc.videoStream]->codec;
    context->video.avc.codec_ctx = codec_ctx;

    /* finding the decoder for the video stream */
    codec=avcodec_find_decoder(codec_ctx->codec_id);
    if(codec==NULL) {
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_NO_CODEC;
    }

    /* opening the codec */
    if(avcodec_open(codec_ctx, codec)<0) {
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_CODEC_OPEN; 
    }

    /* creating the video frame */
    context->video.avc.frame=avcodec_alloc_frame();
    if(context->video.avc.frame==NULL) {
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_FRAME_ALLOC;
    }
    /* yuv frame */
    context->video.avc.yuvframe=avcodec_alloc_frame();
    if(context->video.avc.yuvframe==NULL) {
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_FRAME_ALLOC;
    }
    size = avpicture_get_size(PIX_FMT_YUV420P, codec_ctx->width, codec_ctx->height);
    picture_buf = (uint8_t *) av_malloc(size);
    if (!picture_buf) {
        av_free(context->video.avc.yuvframe);
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_FRAME_ALLOC;
    }
    avpicture_fill((AVPicture *)context->video.avc.yuvframe,
                   picture_buf,
                   PIX_FMT_YUV420P,
                   codec_ctx->width,
                   codec_ctx->height);
    /* rgb frame */
    context->video.avc.rgbframe=avcodec_alloc_frame();
    if(context->video.avc.rgbframe==NULL) {
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_FRAME_ALLOC;
    }
    size = avpicture_get_size(PIX_FMT_RGB24, codec_ctx->width, codec_ctx->height);
    picture_buf = (uint8_t *) av_malloc(size);
    if (!picture_buf) {
        av_free(context->video.avc.rgbframe);
        context->type = NONE_TYPE;
        avcodec_close(context->video.avc.codec_ctx);
        av_close_input_file(context->video.avc.format_ctx);
        return MBRT_ERR_AVC_FRAME_ALLOC;
    }
    avpicture_fill((AVPicture *)context->video.avc.rgbframe,
                   picture_buf,
                   PIX_FMT_RGB24,
                   codec_ctx->width,
                   codec_ctx->height);
    
    /* initializing some values */
    context->video.avc.packet.data=NULL;
    
    return MBRT_NO_ERR;
}


/**
 * Closes the video file playback (AVC) and reset the structure
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_DestroyVideoAcq_avc()
{
    /* Frees the frame, codec and format */
    av_free(context->video.avc.frame);
    avcodec_close(context->video.avc.codec_ctx);
    av_close_input_file(context->video.avc.format_ctx);

    return MBRT_NO_ERR;
}
/**
 * Returns the video played size (AVC).
 * \param acq_w the width (output)
 * \param acq_h the height (output)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqSize_avc(int *acq_w, int *acq_h)
{
    *acq_h = context->video.avc.codec_ctx->height;
    *acq_w = context->video.avc.codec_ctx->width;
    
    return MBRT_NO_ERR;
}

/**
 * Returns the acquisition device default framerate (AVC).
 * \param ofps the framerate in frame per second (output)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetAcqFrameRate_avc(double *ofps)
{
    AVRational r_fps;
    
    r_fps = context->video.avc.format_ctx->streams[context->video.avc.videoStream]->r_frame_rate;
    
    *ofps = ((double) r_fps.num);
    *ofps /= ((double) r_fps.den);
    return MBRT_NO_ERR;
}

/**
 * Obtains an image from the video (AVC)
 * \param dest the mamba image filled by the device
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetImageFromAcq_avc(MB_Image *dest) {
    int nb_bytes;
    int readFrameRet;
    int isFrameComplete;
    int i,j;
    PLINE ptr,pdest;
    AVPacket *packet;
    struct SwsContext *img_convert_ctx;
    
    /* packet pointer */
    packet = &(context->video.avc.packet);

    /* only 8-bit images can be filled*/
    if (dest->depth!=8) {
        return MBRT_ERR_DEPTH;
    }
    
    /* reading the frame of the video stream */
    do {
        if(packet->data!=NULL) {
            av_free_packet(packet);
        }
        
        readFrameRet = av_read_frame(context->video.avc.format_ctx, packet);
    } while(packet->stream_index!=context->video.avc.videoStream);

    if (readFrameRet < 0) {
        /* Error or end of file, we will assume the last possibility */
        /* and the video is rewinded completely to the begining */
        av_seek_frame(context->video.avc.format_ctx,
                      context->video.avc.videoStream,
                      0, AVSEEK_FLAG_BACKWARD);
    } else {
        /* decoding the data in the packet */
        nb_bytes = avcodec_decode_video2(
            context->video.avc.codec_ctx,
            context->video.avc.frame,
            &isFrameComplete,
            packet
        );
        if(nb_bytes < 0) {
            return MBRT_ERR_AVC_DECODING;
        }
        
        if (isFrameComplete) {
            
            /* Converting the image into YUV format */
            img_convert_ctx = sws_getContext(
                context->video.avc.codec_ctx->width,
                context->video.avc.codec_ctx->height,
                context->video.avc.codec_ctx->pix_fmt,
                context->video.avc.codec_ctx->width,
                context->video.avc.codec_ctx->height,
                PIX_FMT_YUV420P,
                SWS_SPLINE, NULL, NULL, NULL); 
            sws_scale(
                img_convert_ctx,
                context->video.avc.frame->data,
                context->video.avc.frame->linesize, 
                0,
                context->video.avc.codec_ctx->height,
                context->video.avc.yuvframe->data,
                context->video.avc.yuvframe->linesize); 
        
            /* Copy the image into destination */
            for(j=0; j<context->video.avc.codec_ctx->height; j++) {
                ptr = (PLINE) (context->video.avc.yuvframe->data[0]+j*context->video.avc.yuvframe->linesize[0]);
                pdest = (dest->PLINES[Y_TOP+j]+X_LEFT);
                for(i=0; i<context->video.avc.codec_ctx->width; i++, ptr++, pdest++) {
                    *pdest = *ptr;
                }
            }
        }
    }
    
    return MBRT_NO_ERR;
}

/**
 * Obtains a color image from the video (AVC)
 * \param destRed the mamba image filled by the device with the red channel
 * \param destGreen the mamba image filled by the device with the green channel
 * \param destBlue the mamba image filled by the device with the blue channel
 * 
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_GetColorImageFromAcq_avc(MB_Image *destRed, MB_Image *destGreen, MB_Image *destBlue)
{
    int nb_bytes;
    int readFrameRet;
    int isFrameComplete;
    int i,j;
    PLINE ptr,pdR, pdG, pdB;
    AVPacket *packet;
    struct SwsContext *img_convert_ctx;
    
    /* packet pointer */
    packet = &(context->video.avc.packet);

    /* only 8-bit images can be filled*/
    if ( (destRed->depth!=8) ||
         (destBlue->depth!=8) ||
         (destGreen->depth!=8) ) {
        return MBRT_ERR_DEPTH;
    }
    
    /* reading the frame of the video stream */
    do {
        if(packet->data!=NULL) {
            av_free_packet(packet);
        }
        
        readFrameRet = av_read_frame(context->video.avc.format_ctx, packet);
    } while(packet->stream_index!=context->video.avc.videoStream);

    if (readFrameRet < 0) {
        /* Error or end of file, we will assume the last possibility */
        /* and the video is rewinded completely to the begining */
        av_seek_frame(context->video.avc.format_ctx,
                      context->video.avc.videoStream,
                      0, AVSEEK_FLAG_BACKWARD);
    } else {
        /* decoding the data in the packet */
        nb_bytes = avcodec_decode_video2(
            context->video.avc.codec_ctx,
            context->video.avc.frame,
            &isFrameComplete,
            packet
        );
        if(nb_bytes < 0) {
            return MBRT_ERR_AVC_DECODING;
        }
        
        if (isFrameComplete) {
            
            /* Converting the image into YUV format */
            img_convert_ctx = sws_getContext(
                context->video.avc.codec_ctx->width,
                context->video.avc.codec_ctx->height,
                context->video.avc.codec_ctx->pix_fmt,
                context->video.avc.codec_ctx->width,
                context->video.avc.codec_ctx->height,
                PIX_FMT_RGB24,
                SWS_SPLINE, NULL, NULL, NULL); 
            sws_scale(
                img_convert_ctx,
                context->video.avc.frame->data,
                context->video.avc.frame->linesize, 
                0,
                context->video.avc.codec_ctx->height,
                context->video.avc.rgbframe->data,
                context->video.avc.rgbframe->linesize); 
        
            /* Copy the image into destination */
            for(j=0; j<context->video.avc.codec_ctx->height; j++) {
                ptr = (PLINE) (context->video.avc.rgbframe->data[0]+j*context->video.avc.rgbframe->linesize[0]);
                pdR = (destRed->PLINES[Y_TOP+j]+X_LEFT);
                pdG = (destGreen->PLINES[Y_TOP+j]+X_LEFT);
                pdB = (destBlue->PLINES[Y_TOP+j]+X_LEFT);
                for(i=0; i<context->video.avc.codec_ctx->width; i++, pdR++, pdG++, pdB++) {
                    *pdR = *ptr;
                    ptr++;
                    *pdG = *ptr;
                    ptr++;
                    *pdB = *ptr;
                    ptr++;
                }
            }
        }
    }
    
    return MBRT_NO_ERR;
}

/**
 * Starts the acquisition device capture process (AVC)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_StartAcq_avc()
{
    /* nothing to do for this kind of acquisition */
    return MBRT_NO_ERR;
}

/**
 * Stops the acquisition device capture process (AVC)
 * \return MBRT_NO_ERR if successful
 */
MBRT_errcode MBRT_StopAcq_avc()
{
    /* nothing to do for this kind of acquisition */
    return MBRT_NO_ERR;
}
