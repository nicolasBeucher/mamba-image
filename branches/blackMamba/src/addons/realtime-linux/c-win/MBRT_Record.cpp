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
 * \return An error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordStart(char *filename)
{
    AVOutputFormat *rec_ofmt;
    AVCodecContext *cod_ctx;
    AVCodec *codec;
    AVStream *stream;
    uint8_t *picture_buf;
    int size;
    
    /* if recording is already on no need to activate it */
    if (context->isRecording==0) {
    
        /* registering all codecs, formats ... */
        av_register_all();

        /* disabling logging (mess with the Python command line) */
        av_log_set_level(-1);
        
        /* format is set to MPEG2 (DVD) for recording (simple and fast) */
        rec_ofmt = av_guess_format("dvd", NULL, NULL);
        if (!rec_ofmt)
            return ERR_AVC_REC_FORMAT;
        
        /* allocating the format context */
        context->rec_fmt_ctx = avformat_alloc_context();
        if (!context->rec_fmt_ctx)
            return ERR_AVC_REC_FMTCTX;
        context->rec_fmt_ctx->oformat = rec_ofmt;
        _snprintf(context->rec_fmt_ctx->filename,
                 sizeof(context->rec_fmt_ctx->filename),
                 "%s", filename);
        
        /* stream creation */
        stream = av_new_stream(context->rec_fmt_ctx, 0);
        if (!stream)
            return ERR_AVC_REC_STREAM;

        /* codec fine tuning */
        cod_ctx = stream->codec;
        cod_ctx->codec_id = rec_ofmt->video_codec;
        cod_ctx->codec_type = CODEC_TYPE_VIDEO;
        /* put sample parameters */
        cod_ctx->bit_rate = 2000000;
        /* resolution */
        cod_ctx->width = context->sz_x;
        cod_ctx->height = context->sz_y;
        cod_ctx->time_base.den = 50;
        cod_ctx->time_base.num = 1;
        cod_ctx->gop_size = 10; /* emit one intra frame every twelve frames at most */
        cod_ctx->pix_fmt = PIX_FMT_YUV420P;
        cod_ctx->max_b_frames = 2;
        if(rec_ofmt->flags & AVFMT_GLOBALHEADER)
            cod_ctx->flags |= CODEC_FLAG_GLOBAL_HEADER;

        /* set the output parameters */
        if (av_set_parameters(context->rec_fmt_ctx, NULL) < 0)
            return ERR_AVC_REC_PARAM_SET;
        
        /* finding the codec */
        codec = avcodec_find_encoder(cod_ctx->codec_id);
        if (!codec)
            return ERR_AVC_REC_NO_CODEC;

        /* opening the codec */
        if (avcodec_open(cod_ctx, codec) < 0)
            return ERR_AVC_REC_CODEC_OPEN;

        /* allocating the encoded raw picture and corresponding buffer */
        context->video_outbuf = (uint8_t *) malloc(200000);
        if (context->video_outbuf==NULL)
            return ERR_AVC_REC_PICT_ALLOC;
            
        context->picture = avcodec_alloc_frame();
        if (!context->picture)
            return ERR_AVC_REC_PICT_ALLOC;
        size = avpicture_get_size(cod_ctx->pix_fmt, context->sz_x, context->sz_y);
        picture_buf = (uint8_t *) av_malloc(size);
        if (!picture_buf) {
            av_free(context->picture);
            return ERR_AVC_REC_PICT_ALLOC;
        }
        memset(picture_buf, 128, size);
        avpicture_fill((AVPicture *)context->picture,
                       picture_buf,
                       cod_ctx->pix_fmt,
                       context->sz_x,
                       context->sz_y);
        
        context->pictureRGB = avcodec_alloc_frame();
        if (!context->pictureRGB)
            return ERR_AVC_REC_PICT_ALLOC;
        size = avpicture_get_size(PIX_FMT_RGB24, context->sz_x, context->sz_y);
        picture_buf = (uint8_t *) av_malloc(size);
        if (!picture_buf) {
            av_free(context->pictureRGB);
            return ERR_AVC_REC_PICT_ALLOC;
        }
        memset(picture_buf, 0, size);
        avpicture_fill((AVPicture *)context->pictureRGB,
                       picture_buf,
                       PIX_FMT_RGB24,
                       context->sz_x,
                       context->sz_y);
        
        context->img_convert_ctx = sws_getContext(context->sz_x, context->sz_y,
                                                  PIX_FMT_RGB24,
                                                  context->sz_x, context->sz_y,
                                                  cod_ctx->pix_fmt,
                                                  SWS_BICUBIC, NULL, NULL, NULL);
        if (!context->img_convert_ctx) 
            return ERR_AVC_REC_PICT_ALLOC;
        
        /* opening the output file, if needed */
        if (url_fopen(&context->rec_fmt_ctx->pb, filename, URL_WRONLY) < 0)
            return ERR_AVC_REC_FILE_OPEN;
        
        /* writing the stream header */
        av_write_header(context->rec_fmt_ctx);
        
        context->isRecording = 1;
    }
    
    return NO_ERR;
}

/**
 * Ends the recording. Closes the codec and terminates the file.
 * \return An error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordEnd()
{
    if (context->isRecording==1) {
        av_write_trailer(context->rec_fmt_ctx);
        
        avcodec_close(context->rec_fmt_ctx->streams[0]->codec);
        free(context->video_outbuf);
        av_free(context->picture->data[0]);
        av_free(context->picture);
        av_free(context->pictureRGB->data[0]);
        av_free(context->pictureRGB);
        
        sws_freeContext(context->img_convert_ctx);
        
        /* free the streams */
        av_freep(&context->rec_fmt_ctx->streams[0]->codec);
        av_freep(&context->rec_fmt_ctx->streams[0]);

        /* close the output file */
        url_fclose(context->rec_fmt_ctx->pb);

        /* free the format context */
        av_free(context->rec_fmt_ctx);
        
        context->isRecording = 0;
    }
    
    return NO_ERR;
}

/**
 * Records an image 
 * \param src the mamba image to record
 * \return An error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordImage(MB_Image *src)
{
    SDL_Color *palette;
    AVCodecContext *cod_ctx;
    AVStream *stream;
    AVPacket pkt;
    int i, j, ret, size;
    PIX8 pix;
    PLINE ptr0; /* ptr1, ptr2;*/
    Uint32 current_call, last_call;
    
    /* if recording is not activated */
    if (context->isRecording==0) 
        return ERR_AVC_REC_INV_CTX;
        
    /* only 8-bit images can be recorded*/
    if (src->depth!=8) {
        return ERR_DEPTH;
    }
    
    /* color palette */
    if (context->isPalettized) {
        palette = context->color_palette;
    } else {
        palette = context->standard_palette;
    }

    /* getting the codec context and stream */
    stream = context->rec_fmt_ctx->streams[0];
    cod_ctx = stream->codec;

    /* filling the picture in RGB */
    for(j=0; j<((int) context->sz_y); j++) {
        ptr0 = (PLINE) (context->pictureRGB->data[0]+j*context->pictureRGB->linesize[0]);
        for(i=0; i<((int) context->sz_x); i++) {
            pix = *(src->PLINES[j+Y_TOP]+X_LEFT+i);
            *ptr0 = palette[pix].r;
            ptr0++;
            *ptr0 = palette[pix].g;
            ptr0++;
            *ptr0 = palette[pix].b;
            ptr0++;
        }
    }

    /* format conversion RGB to codec pixformat */
    sws_scale(context->img_convert_ctx,
              (context->pictureRGB)->data,
              (context->pictureRGB)->linesize,
              0, cod_ctx->height,
              (context->picture)->data,
              (context->picture)->linesize);

    /* time between the two calls */
    current_call = context->old_call[context->index_fps];
    last_call = context->old_call[(context->index_fps+FPS_MEAN_SIZE-1)%FPS_MEAN_SIZE];
    /* the picture is stored to represent the length of time it was displayed */
    for(i=0; i<((int) (50*(current_call-last_call))/1000); i++) {
        /* encodes the image */
        size = avcodec_encode_video(cod_ctx,
                                    context->video_outbuf,
                                    200000,
                                    context->picture);
        /* if zero size, it means the image was buffered */
        if (size > 0) {
            av_init_packet(&pkt);

            if (cod_ctx->coded_frame->pts != AV_NOPTS_VALUE)
                pkt.pts= av_rescale_q(cod_ctx->coded_frame->pts, cod_ctx->time_base, stream->time_base);
            if(cod_ctx->coded_frame->key_frame)
                pkt.flags |= PKT_FLAG_KEY;
            pkt.stream_index= stream->index;
            pkt.data= context->video_outbuf;
            pkt.size= size;

            /* write the compressed frame in the media file */
            ret = av_interleaved_write_frame(context->rec_fmt_ctx, &pkt);
        } else {
            ret = 0;
        }
        
        /* error while encoding */
        if (ret != 0) 
            return ERR_AVC_REC_ENCODE;
    }

    return NO_ERR;
}

/**
 * Records a color image 
 * \param srcRed the mamba image to record (red channel)
 * \param srcGreen the mamba image to record (green channel)
 * \param srcBlue the mamba image to record (blue channel)
 * \return An error code (NO_ERR if successful)
 */
MBRT_errcode MBRT_RecordColorImage(MB_Image *srcRed, MB_Image *srcGreen, MB_Image *srcBlue)
{
    AVCodecContext *cod_ctx;
    AVStream *stream;
    AVPacket pkt;
    int i, j, ret, size;
    PLINE ptr0; /* ptr1, ptr2;*/
    Uint32 current_call, last_call;
    
    /* if recording is not activated */
    if (context->isRecording==0) 
        return ERR_AVC_REC_INV_CTX;
        
    /* only 8-bit images can be recorded*/
    if ( (srcRed->depth!=8) ||
         (srcBlue->depth!=8) ||
         (srcGreen->depth!=8) ) {
        return ERR_DEPTH;
    }

    /* getting the codec context and stream */
    stream = context->rec_fmt_ctx->streams[0];
    cod_ctx = stream->codec;

    /* filling the picture in RGB */
    for(j=0; j<context->sz_y; j++) {
        ptr0 = (PLINE) (context->pictureRGB->data[0]+j*context->pictureRGB->linesize[0]);
        for(i=0; i<context->sz_x; i++) {
            *ptr0 = *(srcRed->PLINES[j+Y_TOP]+X_LEFT+i);
            ptr0++;
            *ptr0 = *(srcGreen->PLINES[j+Y_TOP]+X_LEFT+i);
            ptr0++;
            *ptr0 = *(srcBlue->PLINES[j+Y_TOP]+X_LEFT+i);
            ptr0++;
        }
    }

    /* format conversion RGB to codec pixformat */
    sws_scale(context->img_convert_ctx,
              (context->pictureRGB)->data,
              (context->pictureRGB)->linesize,
              0, cod_ctx->height,
              (context->picture)->data,
              (context->picture)->linesize);

    /* time between the two calls */
    current_call = context->old_call[context->index_fps];
    last_call = context->old_call[(context->index_fps+FPS_MEAN_SIZE-1)%FPS_MEAN_SIZE];
    /* the picture is stored to represent the length of time it was displayed */
    for(i=0; i<(50*(current_call-last_call))/1000; i++) {
        /* encode the image */
        size = avcodec_encode_video(cod_ctx,
                                    context->video_outbuf,
                                    200000,
                                    context->picture);
        /* if zero size, it means the image was buffered */
        if (size > 0) {
            av_init_packet(&pkt);

            if (cod_ctx->coded_frame->pts != AV_NOPTS_VALUE)
                pkt.pts= av_rescale_q(cod_ctx->coded_frame->pts, cod_ctx->time_base, stream->time_base);
            if(cod_ctx->coded_frame->key_frame)
                pkt.flags |= PKT_FLAG_KEY;
            pkt.stream_index= stream->index;
            pkt.data= context->video_outbuf;
            pkt.size= size;

            /* write the compressed frame in the media file */
            ret = av_interleaved_write_frame(context->rec_fmt_ctx, &pkt);
        } else {
            ret = 0;
        }
        
        /* error while encoding */
        if (ret != 0) 
            return ERR_AVC_REC_ENCODE;
    }

    return NO_ERR;
}
