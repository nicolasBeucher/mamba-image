"""
This modules defines the basic 3D image class (which inherits from
the sequenceMb class and adds specific features)
"""

# Contributors : Nicolas BEUCHER

# imports
import mamba3D as m3D
import mamba
import mamba.core as core
from mambaDisplay import getDisplayer

################################################################################
# 3D IMAGE CLASS
################################################################################
# image3DMb class 
# This class is the main class of the mamba3D package. It inherits from
# the mamba.sequenceMB class and adds some methods to it (mainly
# for display and loading).

# Image counter
_image3D_index = 1

class image3DMb(mamba.sequenceMb):
    """
    A 3D image is represented by an instance of this class.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Refer to mamba.sequenceMb constructor documentation.
        """
        global _image3D_index
        mamba.sequenceMb.__init__(self, *args, **kwargs)
        
        self.name = "Image3D "+str(_image3D_index)
        _image3D_index = _image3D_index + 1
        
        self.displayId = ''
        self.palette = None
        self.opacity = None
        self.gd = None
        
        self.mb3DIm = core.MB3D_Image()
        err = core.MB3D_Create(self.mb3DIm, len(self.seq))
        mamba.raiseExceptionOnError(err)
        for position,im in enumerate(self.seq):
            err = core.MB3D_Stack(self.mb3DIm, im.mbIm, position)
            mamba.raiseExceptionOnError(err)
            
    def __str__(self):
        return 'Mamba 3D image object : '+self.name+' - '+str(self.depth)
        
    def __del__(self):
        if hasattr(self, "displayId") and self.displayId != '':
            self.gd.destroyWindow(self.displayId)
        del self
    
    def loadRaw(self, path, preprocfunc=None):
        """
        Load a raw file representing a 3D image inside the image3DMb object.
        The file must contains the expected length of data (i.e. 
        width * height * length * (depth/8) ). The function works only
        with 8 and 32-bit images. If needed you can preprocess the data
        using the optional argument preprocfunc which will be called on the read
        data before loading it into the sequence. The preprocfunc must have the
        following prototype : outdata = preprocfunc(indata). The size 
        verification is performed after the preprocessing (enabling you to
        use zip archives and such).
        """
        # Only for 8 and 32 bit images
        depth = self.getDepth()
        if depth==1:
            mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
            
        # Loading the file
        f = open(path, 'rb')
        data = f.read()
        f.close()
        
        # Preprocessing the data if a function was given
        if preprocfunc:
            data = preprocfunc(data)
        
        # Verification over data size
        (w,h) = self.getSize()
        im_size = w*h*(depth//8)
        assert(len(data)==im_size*self.length)
        
        # Loading the data
        for i,im in enumerate(self.seq):
            err = core.MB_Load(im.mbIm, data[i*im_size:(i+1)*im_size], im_size)
            mamba.raiseExceptionOnError(err)
        self.name = path
        
    def extractRaw(self):
        """
        Extracts and returns the image raw string data.
        This method only works on 8 and 32-bit images.
        """
        data = b""
        for im in self.seq:
            err,s = core.MB_Extract(im.mbIm)
            mamba.raiseExceptionOnError(err)
            data += s
        return data
        
    def convert(self, depth):
        """
        Converts the image depth to the given 'depth'.
        The conversion algorithm is identical to the conversion used in the 
        convert3D function (see this function for details).
        """
        for position,im in enumerate(self.seq):
            im.convert(depth)
            err = core.MB3D_Stack(self.mb3DIm, im.mbIm, position)
            mamba.raiseExceptionOnError(err)
        self.depth = depth
        
        if self.displayId != '':
            self.gd.reconnectWindow(self.displayId, self)
        
    ### Display methods ########################################################
    def show(self):
        """
        Called to show the display associated to the image.
        """
        if self.displayId != '':
            self.gd.showWindow(self.displayId)
        else:
            if self.gd == None:
                self.gd = getDisplayer()
            self.displayId = self.gd.addWindow(im=self)
            self.gd.showWindow(self.displayId)

    def hide(self):
        """
        Called to hide the display associated to the image.
        """
        if self.displayId != '':
            self.gd.hideWindow(self.displayId)

    def update(self):
        """
        Called when the display associated to the image must be updated 
        (Contrary to mamba.imageMb, display is not automatically updated after
        any operation on your image due to performances).
        You can update the display by hitting key F5 in the display window.
        """
        if self.displayId != '':
            self.gd.updateWindow(self.displayId)
            
    def setPalette(self, pal):
        """
        Defines the palette used to convert the image in color for display.
        'pal' may be mamba.rainbow, mamba.inverted_rainbow, mamba.patchwork or
        any user-defined palette.
        """
        self.palette = pal
        if self.displayId != '':
            self.gd.colorizeWindow(self.displayId, self.palette, self.opacity)
            
    def resetPalette(self):
        """
        Undefines the palette used to convert the image in color for display.
        The greyscale palette will be used then.
        """
        self.palette = None
        if self.displayId != '':
            self.gd.colorizeWindow(self.displayId, self.palette, self.opacity)
            
    def setOpacity(self, opa):
        """
        Defines the opacity palette used for the volume rendering display.
        'opa' is a tuple holding 256 value between 0 and 255. a 0
        indicates that the corresponding value will be transparent and 255
        indicates that the value will block light.
        """
        self.opacity = opa
        if self.displayId != '':
            self.gd.colorizeWindow(self.displayId, self.palette, self.opacity)
            
    def resetOpacity(self):
        """
        Resets the opacity palette to its default value.
        """
        self.opacity = None
        if self.displayId != '':
            self.gd.colorizeWindow(self.displayId, self.palette, self.opacity)

    ### Pixel manipulations ####################################################
    def getPixel(self, position):
        """
        Gets the pixel value at 'position'.
        'position' is a tuple holding (x,y,z).
        Returns the value of the pixel.
        """
        (x,y,z) = position
        if z<0 or z>=self.length:
            mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
        err, value = core.MB_GetPixel(self.seq[z].mbIm, x, y)
        mamba.raiseExceptionOnError(err)
        return value
        
    def setPixel(self, value, position):
        """
        Sets the pixel at 'position' with 'value'.
        'position' is a tuple holding (x,y,z).
        """
        (x,y,z) = position
        if z<0 or z>=self.length:
            mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
        err = core.MB_PutPixel(self.seq[z].mbIm, value, position[0], position[1])
        mamba.raiseExceptionOnError(err)

