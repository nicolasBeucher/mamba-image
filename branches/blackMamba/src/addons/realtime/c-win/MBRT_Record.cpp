/**
 * \file MBRT_Record.cpp
 * \author Nicolas Beucher
 * \date 17-04-2010
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
 * Starts the recording. This function activates the libavformat and libavcodec
 * libraries to encode the image using MPEG2 codec (DVD format).
 * \param filename the path to the created video file
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordStart(char *filename)
{
    int ret;
    MBRT_errcode err;
    AVCodec *codec;
    
    /* if recording is already on no need to activate it */
    if (context->isRecording==0) {
    
        /* registering all codecs, formats ... */
        avcodec_register_all();

        /* disabling logging (mess with the Python command line) */
        av_log_set_level(-1);
        
        /* Selecting the MPEG2 codec to record */
        codec = avcodec_find_encoder(AV_CODEC_ID_MPEG2VIDEO);
        if (!codec)
            return MBRT_ERR_AVC_REC_NO_CODEC;
        
        /* allocating the format context */
        context->rec_codctx = avcodec_alloc_context3(codec);
        if (!context->rec_codctx) {
            return MBRT_ERR_AVC_REC_CODCTX;
        }
        
        /* put sample parameters */
        context->rec_codctx->bit_rate = 2000000;
        /* resolution */
        context->rec_codctx->width = context->sz_x;
        context->rec_codctx->height = context->sz_y;
        /* frames per second */
        context->rec_codctx->time_base.num = 1;
        context->rec_codctx->time_base.den = 50;
        context->rec_codctx->gop_size = 10; /* emit one intra frame every twelve frames at most */
        context->rec_codctx->pix_fmt = AV_PIX_FMT_YUV420P;
        context->rec_codctx->max_b_frames = 2;

        /* opening the codec */
        if (avcodec_open2(context->rec_codctx, codec, NULL) < 0) {
            err = MBRT_ERR_AVC_REC_CODEC_OPEN;
            goto fb_err_avc_rec_codec_open;
        }

        /* creating the output file */
        context->rec_file = fopen(filename, "wb");
        if (!context->rec_file) {
            err = MBRT_ERR_AVC_REC_FILE_OPEN;
            goto fb_err_avc_rec_file_open;
        }
        
        /* allocating the frames */
        /* first the frame in the correct format */
        context->rec_picYUV = av_frame_alloc();
        if (!context->rec_picYUV) {
            err = MBRT_ERR_AVC_REC_PICT_ALLOC;
            goto fb_err_avc_rec_pict_yuv_alloc;
        }
        (context->rec_picYUV)->format = context->rec_codctx->pix_fmt;
        (context->rec_picYUV)->width = context->rec_codctx->width;
        (context->rec_picYUV)->height = context->rec_codctx->height;
        ret = av_image_alloc((context->rec_picYUV)->data,
                             (context->rec_picYUV)->linesize,
                             (context->rec_picYUV)->width,
                             (context->rec_picYUV)->height,
                             (AVPixelFormat)(context->rec_picYUV)->format,
                             32);
        if (ret<0) {
            err = MBRT_ERR_AVC_REC_PICT_ALLOC;
            goto fb_err_avc_rec_pict_yuv_image_alloc;
        }
        context->rec_picYUV->pts = 0;
        
        /* second the frame in RGB used filled with the mamba image data */
        /* and converted to YUV */
        context->rec_picRGB = av_frame_alloc();
        if (!context->rec_picRGB) {
            err = MBRT_ERR_AVC_REC_PICT_ALLOC;
            goto fb_err_avc_rec_pict_rgb_alloc;
        }
        (context->rec_picRGB)->format = AV_PIX_FMT_RGB24;
        (context->rec_picRGB)->width = context->rec_codctx->width;
        (context->rec_picRGB)->height = context->rec_codctx->height;
        ret = av_image_alloc((context->rec_picRGB)->data,
                             (context->rec_picRGB)->linesize,
                             (context->rec_picRGB)->width,
                             (context->rec_picRGB)->height,
                             (AVPixelFormat)(context->rec_picRGB)->format,
                             32);
        if (ret<0) {
            err = MBRT_ERR_AVC_REC_PICT_ALLOC;
            goto fb_err_avc_rec_pict_rgb_image_alloc;
        }
        
        /* create a converter from RGB to YUV */
        context->rec_convctx = sws_getContext(context->sz_x, context->sz_y,
                                              AV_PIX_FMT_RGB24,
                                              context->sz_x, context->sz_y,
                                              context->rec_codctx->pix_fmt,
                                              SWS_BICUBIC, NULL, NULL, NULL);
        if (!context->rec_convctx) {
            err = MBRT_ERR_AVC_REC_CONVERT_CTX;
            goto fb_err_avc_rec_convert_ctx;
            
        }
        
        context->isRecording = 1;
    }
    
    return MBRT_NO_ERR;
    
/* Fallback from errors */
fb_err_avc_rec_convert_ctx:
    av_freep(&context->rec_picRGB->data[0]);
fb_err_avc_rec_pict_rgb_image_alloc:
    av_frame_free(&context->rec_picRGB);
fb_err_avc_rec_pict_rgb_alloc:
    av_freep(&context->rec_picYUV->data[0]);
fb_err_avc_rec_pict_yuv_image_alloc:
    av_frame_free(&context->rec_picYUV);
fb_err_avc_rec_pict_yuv_alloc:
    fclose(context->rec_file);
    context->rec_file = NULL;
fb_err_avc_rec_file_open:
    avcodec_close(context->rec_codctx);
fb_err_avc_rec_codec_open:
    av_free(context->rec_codctx);
    return err;
}

/**
 * Ends the recording. Closes the codec and terminates the file.
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordEnd()
{
    int ret, got_output;
    uint8_t endcode[] = { 0, 0, 1, 0xb7 };
    
    if (context->isRecording==1) {
        /* writing the delayed frames */
        for (got_output = 1; got_output; ) {
            ret = avcodec_encode_video2(context->rec_codctx, &(context->rec_pkt), NULL, &got_output);
            if (ret < 0) 
                return MBRT_ERR_AVC_REC_ENCODE;

            if (got_output) {
                fwrite(context->rec_pkt.data, 1, context->rec_pkt.size, context->rec_file);
                av_free_packet(&(context->rec_pkt));
            }
        }
        
        /* add sequence end to have a real mpeg file */
        fwrite(endcode, 1, sizeof(endcode), context->rec_file);
        /* Close the recording file */
        fclose(context->rec_file);
        context->rec_file = NULL;

        /* restoring the memory */
        av_freep(&context->rec_picRGB->data[0]);
        av_frame_free(&context->rec_picRGB);
        av_freep(&context->rec_picYUV->data[0]);
        av_frame_free(&context->rec_picYUV);
        avcodec_close(context->rec_codctx);
        av_free(context->rec_codctx);
        
        context->isRecording = 0;
    }
    
    return MBRT_NO_ERR;
}

/**
 * Records an image 
 * \param src the mamba image to record
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordImage(MB_Image *src)
{
    int i, j, ret, got_output;
    PIX8 pix;
    PLINE ptr0;
    Uint32 current_call, last_call;
    
    /* if recording is not activated */
    if (context->isRecording==0) 
        return MBRT_ERR_AVC_REC_INV_CTX;
        
    /* only 8-bit images can be recorded*/
    if (src->depth!=8) {
        return MBRT_ERR_DEPTH;
    }

    /* filling the picture in RGB */
    for(j=0; j<(int)context->sz_y; j++) {
        ptr0 = (PLINE) (context->rec_picRGB->data[0]+j*context->rec_picRGB->linesize[0]);
        for(i=0; i<(int)context->sz_x; i++) {
            pix = *(src->plines[j]+i);
            *ptr0 = context->palette[pix].r;
            ptr0++;
            *ptr0 = context->palette[pix].g;
            ptr0++;
            *ptr0 = context->palette[pix].b;
            ptr0++;
        }
    }

    /* format conversion RGB to codec pixformat */
    sws_scale(context->rec_convctx,
              (const uint8_t* const*) (context->rec_picRGB)->data,
              (context->rec_picRGB)->linesize,
              0, context->rec_codctx->height,
              (context->rec_picYUV)->data,
              (context->rec_picYUV)->linesize);

    /* time between the two calls */
    current_call = context->old_call[context->index_fps];
    last_call = context->old_call[(context->index_fps+FPS_MEAN_SIZE-1)%FPS_MEAN_SIZE];
    /* the picture is stored to represent the length of time it was displayed */
    for(i=0; i<(int)(50*(current_call-last_call))/1000; i++) {
        av_init_packet(&(context->rec_pkt));
        context->rec_pkt.data = NULL; // packet data will be allocated by the encoder
        context->rec_pkt.size = 0;
        
        /* encode the image */
        ret = avcodec_encode_video2(context->rec_codctx,
                                    &(context->rec_pkt),
                                    context->rec_picYUV,
                                    &got_output);
        if (ret < 0) {
            return MBRT_ERR_AVC_REC_ENCODE;
        }
        if (got_output) {
            fwrite(context->rec_pkt.data, 1, context->rec_pkt.size, context->rec_file);
            av_free_packet(&(context->rec_pkt));
        }
        context->rec_picYUV->pts++;
    }

    return MBRT_NO_ERR;
}

/**
 * Records a color image 
 * \param srcRed the mamba image to record (red channel)
 * \param srcGreen the mamba image to record (green channel)
 * \param srcBlue the mamba image to record (blue channel)
 * \return An error code (MBRT_NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordColorImage(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue)
{
    int i, j, ret, got_output;
    PLINE ptr0;
    Uint32 current_call, last_call;
    
    /* if recording is not activated */
    if (context->isRecording==0) 
        return MBRT_ERR_AVC_REC_INV_CTX;
        
    /* only 8-bit images can be recorded*/
    if ( (srcRed->depth!=8) ||
         (srcBlue->depth!=8) ||
         (srcGreen->depth!=8) ) {
        return MBRT_ERR_DEPTH;
    }

    /* filling the picture in RGB */
    for(j=0; j<(int)context->sz_y; j++) {
        ptr0 = (PLINE) (context->rec_picRGB->data[0]+j*context->rec_picRGB->linesize[0]);
        for(i=0; i<(int)context->sz_x; i++) {
            *ptr0 = *(srcRed->plines[j]+i);
            ptr0++;
            *ptr0 = *(srcGreen->plines[j]+i);
            ptr0++;
            *ptr0 = *(srcBlue->plines[j]+i);
            ptr0++;
        }
    }

    /* format conversion RGB to codec pixformat */
    sws_scale(context->rec_convctx,
              (const uint8_t* const*) (context->rec_picRGB)->data,
              (context->rec_picRGB)->linesize,
              0, context->rec_codctx->height,
              (context->rec_picYUV)->data,
              (context->rec_picYUV)->linesize);

    /* time between the two calls */
    current_call = context->old_call[context->index_fps];
    last_call = context->old_call[(context->index_fps+FPS_MEAN_SIZE-1)%FPS_MEAN_SIZE];
    /* the picture is stored to represent the length of time it was displayed */
    for(i=0; i<(int)(50*(current_call-last_call))/1000; i++) {
        av_init_packet(&(context->rec_pkt));
        context->rec_pkt.data = NULL; // packet data will be allocated by the encoder
        context->rec_pkt.size = 0;
        
        /* encode the image */
        ret = avcodec_encode_video2(context->rec_codctx,
                                    &(context->rec_pkt),
                                    context->rec_picYUV,
                                    &got_output);
        if (ret < 0) {
            return MBRT_ERR_AVC_REC_ENCODE;
        }
        if (got_output) {
            fwrite(context->rec_pkt.data, 1, context->rec_pkt.size, context->rec_file);
            av_free_packet(&(context->rec_pkt));
        }
        context->rec_picYUV->pts++;
    }

    return MBRT_NO_ERR;
}
