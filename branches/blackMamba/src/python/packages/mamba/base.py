"""
This is the base module of the Mamba Image library. It defines the imageMb class
used to contain images. It also contains image display configuration functions.
"""

import mamba.core as core
import mamba.utils as utils
from mambaDisplay import getDisplayer
from .error import *

import os.path

###############################################################################
#  Local variables and constants

_image_index = 1
_always_show = False

###############################################################################
# Public functions are functions dealing with counter and such
    
def setImageIndex(index):
    """
    Sets the image index used for naming to a given value 'index'
    """
    global _image_index
    
    _image_index = index

def setShowImages(showThem):
    """
    Activates automatically the display for new images when 'showThem' is set to
    True.
    """
    global _always_show
    
    _always_show = showThem

def getShowImages():
    """
    Returns the display status ('always_show' value).
    """
    global _always_show
    
    return _always_show
    
def getImageCounter():
    """
    Returns the number of images actually defined and allocated in the Mamba
    library. This function may be useful for debugging purposes.
    """
    return core.MB_getImageCounter()

###############################################################################
#  Classes

class imageMb:
    """
    Defines the imageMb class and its methods.
    All Mamba images are represented by this class.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for a Mamba image object.
        
        This constructor allows a wide range of possibilities for defining an image:
            * imageMb(): without arguments will create an empty greyscale image.
            * imageMb(im): will create an image using the same size and depth
              as 'im'.
            * imageMb(depth): will create an image with the desired 'depth' (1, 8 or 32).
            * imageMb(path): will load the image located in 'path'.
            * imageMb(im, depth): will create an image using the same size as 'im' 
            and the specified 'depth'.
            * imageMb(path, depth): will load the image located in 'path' and 
            convert it to the specified 'depth'.
            * imageMb(width, height): will create an image with size 'width'x'height'.
            * imageMb(width, height, depth): will create an image with size 
            'width'x'height' and the specified 'depth'.
            
        When not specified, the width and height of the image will be set to 
        256x256. The default depth is 8 (greyscale).
        
        When loading an image from a file, please note that Mamba accepts all 
        kinds of images (actually all the PIL or PILLOW supported formats). You can specify
        the RGB filter that will be used to convert a color image into a greyscale 
        image by adding the rgbfilter=<your_filter> to the argument of the
        constructor.
        """
        global _image_index
        
        # List of all the parameters that must be retrieved from the arguments
        rgbfilter = None
        
        # First we look into the dictionnary to see if they were specified
        # specifically by the user
        if "rgbfilter" in kwargs:
            rgbfilter = kwargs["rgbfilter"]
            
        # We analyze the arguments given to the constructor
        if len(args)==0:
            # First case : no argument was given
            # -> imageMb()
            self.mbIm = utils.create(256, 256, 8)
            self.name = "Image "+str(_image_index)
            _image_index = _image_index + 1
        elif len(args)==1:
            # Second case : the user gives only one argument
            if isinstance(args[0], imageMb):
                # -> imageMb(im)
                self.mbIm = utils.create(args[0].mbIm.width, args[0].mbIm.height, args[0].mbIm.depth)
                self.name = "Image "+str(_image_index)
                _image_index = _image_index + 1
            elif isinstance(args[0], str):
                # -> imageMb(path)
                self.mbIm = utils.load(args[0], rgb2l=rgbfilter)
                self.name = os.path.split(args[0])[1]
            else:
                # -> imageMb(depth)
                self.mbIm = utils.create(256, 256, args[0])
                self.name = "Image "+str(_image_index)
                _image_index = _image_index + 1
        elif len(args)==2:
            # Third case : two arguments
            if isinstance(args[0], imageMb):
                # -> imageMb(im, depth)
                self.mbIm = utils.create(args[0].mbIm.width, args[0].mbIm.height, args[1])
                self.name = "Image "+str(_image_index)
                _image_index = _image_index + 1
            elif isinstance(args[0], str):
                # -> imageMb(path, depth)
                next_mbIm = utils.load(args[0], rgb2l=rgbfilter)
                if args[1]==1:
                    self.mbIm = utils.create(next_mbIm.width,next_mbIm.height,1)
                    err = core.MB_Convert(next_mbIm, self.mbIm)
                    raiseExceptionOnError(err)
                elif args[1]==8:
                    self.mbIm = next_mbIm
                else:
                    self.mbIm = utils.create(next_mbIm.width,next_mbIm.height,32)
                    if next_mbIm.depth==8:
                        err = core.MB_CopyBytePlane(next_mbIm, self.mbIm, 0)
                        raiseExceptionOnError(err)
                    else:
                        self.mbIm = next_mbIm
                self.name = os.path.split(args[0])[1]
            else:
                # -> imageMb(width, height)
                self.mbIm = utils.create(args[0], args[1], 8)
                self.name = "Image "+str(_image_index)
                _image_index = _image_index + 1
        else:
            # Last case: at least 3 arguments are given
            # -> imageMb(width, height, depth)
            self.mbIm = utils.create(args[0], args[1], args[2])
            self.name = "Image "+str(_image_index)
            _image_index = _image_index + 1
        
        self.displayId = ''
        self.palette = None
        self.gd = None
        if getShowImages():
            self.show()
            
    def __str__(self):
        return 'Mamba image object : '+self.name+' - '+str(self.mbIm.depth)
        
    def __del__(self):
        if hasattr(self, "displayId") and self.displayId != '':
            self.gd.destroyWindow(self.displayId)
        del self
    
    def getSize(self):
        """
        Returns the size (a tuple width and height) of the image.
        """
        return (self.mbIm.width, self.mbIm.height)
    
    def getDepth(self):
        """
        Returns the depth of the image.
        """
        return self.mbIm.depth
        
    def setName(self, name):
        """
        Use this function to set the image 'name'.
        """
        self.name = name
        if self.displayId != '':
            self.gd.updateWindow(self.displayId)
            
    def getName(self):
        """
        Returns the name of the image.
        """
        return self.name
            
    def setPalette(self, pal):
        """
        Defines the palette used to convert the image in color for display
        and save. 'pal' may be rainbow, inverted_rainbow, patchwork or any
        user-defined palette.
        """
        self.palette = pal
        if self.displayId != '':
            self.gd.updateWindow(self.displayId)
            
    def resetPalette(self):
        """
        Undefines the palette used to convert the image in color for display
        and save. The greyscale palette will be used then.
        """
        self.palette = None
        if self.displayId != '':
            self.gd.updateWindow(self.displayId)
            
    def load(self, path, rgbfilter=None):
        """
        Loads the image in 'path' into the Mamba image.
        
        The optional 'rgbfilter' argument can be used to specify how to convert
        a color image into a greyscale image. It is a sequence of 3 float values 
        indicating the amount of red, green and blue to take from the image to
        obtain the grey value.
        By default, the color conversion uses the ITU-R 601-2 luma transform (see
        PIL/PILLOW documentation for details).
        """
        next_mbIm = utils.load(path, size=(self.mbIm.width,self.mbIm.height), rgb2l=rgbfilter)
        if self.mbIm.depth==1:
            err = core.MB_Convert(next_mbIm, self.mbIm)
            raiseExceptionOnError(err)
        elif self.mbIm.depth==8:
            err = core.MB_Copy(next_mbIm, self.mbIm)
            raiseExceptionOnError(err)
        else:
            err = core.MB_CopyBytePlane(next_mbIm, self.mbIm, 0)
            raiseExceptionOnError(err)
        self.setName(os.path.split(path)[1])
        if self.displayId != '':
            self.gd.reconnectWindow(self.displayId, self)
        
    def save(self, path):
        """
        Saves the image at the corresponding 'path' using PIL/PILLOW library.
        The format is automatically deduced by PIL/PILLOW from the image name extension.
        Note that, if the image comes with a palette, the image is saved with
        this palette.        
        """
        utils.save(self.mbIm, path, self.palette)
        
    def loadRaw(self, data):
        """
        Fills the image with the raw string 'data'. The length of data must
        fit the image size and depth.
        This method only works on 8 and 32-bit images.
        """
        assert(len(data)==self.mbIm.width*self.mbIm.height*(self.mbIm.depth//8))
        err = core.MB_Load(self.mbIm,data,len(data))
        raiseExceptionOnError(err)
        self.update()
        
    def extractRaw(self):
        """
        Extracts and returns the image raw string data.
        This method only works on 8 and 32-bit images.
        """
        err,data = core.MB_Extract(self.mbIm)
        raiseExceptionOnError(err)
        return data
        
    def fill(self, v):
        """
        Completely fills the image with a given value 'v'.
        A zero value makes the image completely dark.
        """
        err = core.MB_ConSet(self.mbIm,v)
        raiseExceptionOnError(err)
        self.update()

    def reset(self):
        """
        Resets the image (all the pixels are put to 0).
        This method is equivalent to im.fill(0).
        """
        self.fill(0)
    
    def convert(self, depth):
        """
        Converts the image depth to the given 'depth'.
        The conversion algorithm is identical to the conversion used in the 
        convert function (see this function for details).
        """
        next_mbIm = utils.create(self.mbIm.width,self.mbIm.height,depth)
        err = core.MB_Convert(self.mbIm, next_mbIm)
        raiseExceptionOnError(err)

        del self.mbIm
        self.mbIm = next_mbIm
        if self.displayId != '':
            self.gd.reconnectWindow(self.displayId, self)
        
    ### Display methods ########################################################
    def update(self):
        """
        Called when the display associated to the image must be updated 
        (the image has changed).
        """
        if self.displayId != '':
            self.gd.updateWindow(self.displayId)
            
    def freeze(self):
        """
        Called to freeze the display of the image. Thus the image may change but
        the display will not show these modifications until the method unfreeze
        is called.
        """
        if self.displayId != '':
            self.gd.controlWindow(self.displayId, "FREEZE")
            
    def unfreeze(self):
        """
        Called to unfreeze the display of the image. Thus the image display will
        be updated along with the modifications inside the image.
        """
        if self.displayId != '':
            self.gd.controlWindow(self.displayId, "UNFREEZE")
            
    def show(self):
        """
        Called to show the display associated to the image.
        Showing the display may significantly slow down your operations.
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
        If the display is hidden, the computations go much faster.
        """
        if self.displayId != '':
            self.gd.hideWindow(self.displayId)
        
    ### Pixel manipulations ####################################################
    def setPixel(self, value, position):
        """
        Sets the pixel at 'position' with 'value'.
        'position' is a tuple holding (x,y).
        """
        err = core.MB_PutPixel(self.mbIm, value, position[0], position[1])
        raiseExceptionOnError(err)
        self.update()
        
    def fastSetPixel(self, value, position):
        """
        Sets the pixel at 'position' with 'value'.
        'position' is a tuple holding (x,y).
        
        This function will not update the display to enable a faster drawing.
        So make sure to call the update() method once your drawing is 
        finished, if you want to see the result.
        """
        err = core.MB_PutPixel(self.mbIm, value, position[0], position[1])
        raiseExceptionOnError(err)
        
    def getPixel(self, position):
        """
        Gets the pixel value at 'position'.
        'position' is a tuple holding (x,y).
        Returns the value of the pixel.
        """
        err, value = core.MB_GetPixel(self.mbIm, position[0], position[1])
        raiseExceptionOnError(err)
        return value

