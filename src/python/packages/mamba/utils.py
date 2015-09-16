"""
This module provides a set of functions that simplify code inside mamba 
modules.

These functions are not meant to be used by the end user.
"""

import mamba.core as core
from .error import *

import struct

from PIL import Image

###############################################################################
#  Utilities functions
#
# These functions do not perform computations but allow you to load, save or 
# convert mamba image structures easily. They also allow you to set the global
# variables used for computations.
        
def create(width,height,depth):
    """
    Creates an empty C core image (filled with black, i.e. 0) of size 
    'width'x'height' with the required 'depth' of the image.
    
    Returns a mamba image structure.
    """

    # Creating the image.
    im = core.MB_Image()
    err = core.MB_Create(im,width,height,depth)
    raiseExceptionOnError(err)
    
    return im

def loadFromPILFormat(pilim, size=None, rgb2l = None):
    """
    Converts a PIL/PILLOW image into a C core image. All images are converted in grey 
    scale format (i.e. "L" in PIL/PILLOW) before performing computations. The 
    conversion uses the 3 items sequence 'rgb2l' if given :
        L = rgb2l[0]*R + rgb2l[1]*G + rgb2l[2]*B
    Otherwise, the conversion will be done following this formula :
        L = 0.299*R + 0.587*G + 0.114*B
    
    'pilim' is the PIL/PILLOW format image.
    
    If the image is not fitting in the current size, the image is either padded
    or cropped.
    
    Returns a mamba image structure.
    """
    
    # Conversion matrix
    if rgb2l==None or len(rgb2l)!=3:
        rgb2l = (0.299, 0.587, 0.114, 0)
    else:
        rgb2l = tuple(rgb2l) + (0,)
        
    # Mode management
    # By default, the image depth is 8-bit
    # 32-bit images are extracted from I and F modes
    depth = 8
    if pilim.mode == 'RGB':
        pilim = pilim.convert("L", rgb2l)
        depth = 8
    elif pilim.mode == 'RGBA':
        pilim = pilim.convert("RGB").convert("L", rgb2l)
        depth = 8
    elif pilim.mode == '1':
        pilim = pilim.convert("L")
        depth = 8
    elif pilim.mode == 'P':
        pilim = pilim.convert("L")
        depth = 8
    elif pilim.mode == 'L':
        depth = 8
    elif pilim.mode=='I;16':
        depth = 32
        fmt = "H"
        end = ""
    elif pilim.mode=='I;16B':
        depth = 32
        fmt = "H"
        end = ">"
    elif pilim.mode=='I;32' or pilim.mode=='I':
        depth = 32
        fmt = "I"
        end = ""
    elif pilim.mode=='F;32' or pilim.mode=='F':
        depth = 32
        fmt = "f"
        end = ""
    else:
        # Ugly ...
        depth = 8
        pilim = pilim.convert('RGB').convert("L", rgb2l)
        
    # PIL/PILLOW image size or given size
    if size!=None:
        (w,h) = size
    else:
        (w,h)= pilim.size
    
    # Creating the mamba image. 
    im_out = core.MB_Image()
    err = core.MB_Create(im_out,w,h,depth)
    raiseExceptionOnError(err)
    
    # Loading the image data.
    wc = im_out.width
    hc = im_out.height
    (w,h)= pilim.size
    # Because the created image can have a different size, it means that we must
    # force the size of the loaded image to fit.
    if (wc!=w) or (hc!=h):
        # Here we crop and paste the image to be loaded in order to make
        # it fit in the contextual size.
        prov_im = Image.new(pilim.mode, (wc,hc), 0)
        pilim_crop = pilim.crop((0,0,min(wc, w),min(hc, h)))
        prov_im.paste(pilim_crop, (0,0,min(wc, w),min(hc, h)))
        pilim = prov_im
    s = pilim.tobytes()
    if depth==32:
        # For 32-bit image, the pil image format may not be exacty the
        # desired format (unsigned 32-bit value). The data are converted
        # into the appropriate format.
        bypd = struct.calcsize(fmt)
        unpack_data = struct.unpack(end+wc*hc*fmt, s)
        unpack_data = [int(v) for v in unpack_data]
        s = struct.pack(wc*hc*"I", *unpack_data)
    err = core.MB_Load(im_out,s,len(s))
    raiseExceptionOnError(err)
    
    return im_out
        
def load(filename, size=None, rgb2l = None):
    """
    Loads an image into a C core image object. You can give any image format
    that is actually supported by PIL/PILLOW. All images are converted in grey scale
    format (i.e. "L" in PIL/PILLOW) before performing computations. The conversion use
    the 3 items sequence 'rgb2l' if given :
        L = rgb2l[0]*R + rgb2l[1]*G + rgb2l[2]*B
    Otherwise, the conversion will be done following this formula :
        L = 0.299*R + 0.587*G + 0.114*B
    
    'filename' is the image file path.
    
    If the image is not fitting in the current size, the image is either padded
    or cropped.
    
    Returns a mamba image structure.
    """
    
    # Mode management
    pilim = Image.open(filename)
    im_out = loadFromPILFormat(pilim, size, rgb2l)
    
    return im_out

def convertToPILFormat(im_in):
    """
    Converts a mamba C core image 'im_in' structure into a PIL image.
    'palette' is used to colorize the image if wanted.

    32-bit images are converted into an image that contains the four byte planes
    stitched together.
    
    The palette is a sequence as defined by the putpalette method of PIL images.
    If not given the image stays in greyscale.
    """
    # Extracting image size information.
    w = im_in.width
    h = im_in.height
    
    # Extracting the data from the image.
    if im_in.depth==32:
        # 32-bit images
        err,s = core.MB_Extract(im_in)
        raiseExceptionOnError(err)
        # Creating the PIL image 
        pilim = Image.frombytes("I",(w,h),s)
    elif im_in.depth==1:
        # Binary images
        im = create(im_in.width, im_in.height, 8)
        err = core.MB_Convert(im_in,im)
        raiseExceptionOnError(err)
        err,s = core.MB_Extract(im)
        raiseExceptionOnError(err)
        # Creating the PIL image 
        pilim = Image.frombytes("L",(w,h),s)
    else:
        # Greyscale images
        err,s = core.MB_Extract(im_in)
        raiseExceptionOnError(err)
        # Creating the PIL image 
        pilim = Image.frombytes("L",(w,h),s)
    
    return pilim

