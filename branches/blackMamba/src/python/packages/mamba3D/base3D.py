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

class image3DMb:
    """
    A 3D image is represented by an instance of this class.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for a mamba 3D image.
        A 3D image is a stack of images defined by width, height and length
        (the number of images in it).
        
        There is a wide range of possibilities :
            * image3DMb() : without arguments will create an empty greyscale 3D
            image.
            * image3DMb(im3D) : will create a 3D image using the same size, depth 
             and length than 3D image 'im3D'.
            * image3DMb(im) : will create a 3D image using the same size and 
            depth than 2D image 'im'.
            * image3DMb(depth) : will create a 3D image with the desired 
            'depth' (1, 8 or 32) for the mamba images.
            * image3DMb(path) : will load the 3D image (sequence) located in
            'path', see the load method.
            * image3DMb(im3D, depth) : will create a 3D image using the same size
            than 3D image 'im3D' and the specified 'depth'.
            * image3DMb(im, length) : will create a 3D image using the same size
            than 2D image 'im' and the specified 'length'.
            * image3DMb(path, depth) : will load the 3D image (sequence)
            located in 'path' and convert it to the specified 'depth'.
            * image3DMb(width, height, length) : will create a 3D image
            with size 'width'x'height' and 'length'.
            * image3DMb(width, height, length, depth) : will create a 3D image 
            with size 'width'x'height', 'depth' and 'length'.
            
        When not specified, the width, height and length of the 3D image will 
        be set to 256. The default depth is 8 (greyscale).
        
        When loading a 3D image as a sequence make sure all the images have
        the same size.
        """
        
        global _image3D_index
        self._index = 0
        
        self.name = "Image3D "+str(_image3D_index)
        _image3D_index = _image3D_index + 1
        
        # List of all the parameters that must be retrieved from the arguments
        self.rgbfilter = None
        
        # First we look into the dictionnary to see if they were specified
        # specifically by the user
        if "rgbfilter" in kwargs:
            self.rgbfilter = kwargs["rgbfilter"]
            
        # We analyze the arguments given to the constructor
        if len(args)==0:
            # First case : no arguments were given, default sequence
            # -> sequenceMb()
            self._createSeq(256,256,8,256)
        elif len(args)==1:
            # Second case : the user gives only one argument
            if isinstance(args[0], sequenceMb):
                # -> sequenceMb(seq)
                self._createSeq(args[0].width, args[0].height, args[0].depth, args[0].length)
            elif isinstance(args[0], mamba.imageMb):
                # -> sequenceMb(im)
                self._createSeq(args[0].mbIm.width, args[0].mbIm.height, args[0].mbIm.depth, 256)
            elif isinstance(args[0], str):
                # -> sequenceMb(path)
                self.seq = []
                self.depth = 8
                self.load(args[0], rgbfilter=self.rgbfilter)
            else:
                # -> sequence(depth)
                self._createSeq(256,256,args[0],256)
        elif len(args)==2:
            # Third case : two arguments
            if isinstance(args[0], mamba.imageMb):
                # -> sequenceMb(im, length)
                self._createSeq(args[0].mbIm.width, args[0].mbIm.height, args[0].mbIm.depth, args[1])
            elif isinstance(args[0], str):
                # -> sequenceMb(path, depth)
                self.seq = []
                self.depth = args[1]
                self.load(args[0])
            else:
                # -> sequenceMb(seq, depth)
                self._createSeq(args[0].width, args[0].height, args[1], args[0].length)
        elif len(args)==3:
            # Fourth case : three arguments
            # -> sequenceMb(width, height, length)
            self._createSeq(args[0],args[1],8,args[2])
        else:
            # Last case: at least 4 arguments are given
            # -> sequenceMb(width, height, length, depth)
            self._createSeq(args[0],args[1],args[3],args[2])
        
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
            
    def _createSeq(self, w, h, d, l):
        # Create the sequence according to the parameters
        self.length = l
        self.seq = []
        for i in range(self.length):
            self.seq.append(mamba.imageMb(w, h, d, rgbfilter=self.rgbfilter))
        self.width, self.height = self.seq[0].getSize()
        self.depth = self.seq[0].getDepth()
        
    def __iter__(self):
        """
        Makes a mamba image sequence iterable.
        """
        return self

    def __next__(self):
        # Support for iterator in python 3
        return self.next()
        
    def next(self):
        """
        The next method for the iteration.
        """
        if self._index == self.length :
            self._index = 0
            raise StopIteration
        im = self.seq[self._index]
        self._index = self._index + 1
        return im

    def __getitem__(self, key):
        """
        Handles direct acces to the image inside the sequence.
        """
        return self.seq[key]
            
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
        
        
    def load(self, path, rgbfilter=None):
        """
        Loads a 3D image stack (sequence) of image as found in directory 'path'.

        To be valid a sequence of images must be composed of at least 'length'
        images to be able to fill the sequence. Their file names must be of
        the form X.ext where X is a number and ext is an image file extension
        (like jpg or png). The sequence will be read in increasing order
        (1 then 2 and so on). However it is not mandatory that the numbers
        follow each other (1 then 5 is legal). You can also mix image
        formats (1.bmp then 2.jpg is legal) but you should make sure
        that files that are not images (txt, pdf, ...) are not named
        following that pattern. Also ensure that two images do not get
        the same number (like 1 and 01).
        """
        
        self.name = path
        all_files = glob.glob(os.path.join(path, '*'))
        files_dict = {}
        for f in all_files:
            try:
                nb = int(os.path.splitext(os.path.basename(f))[0])
                files_dict[nb] = f
            except ValueError:
                # This file is not named <a_number>.ext
                pass
        files_keys = sorted(files_dict.keys())
        
        if self.seq == []:
            # there no image yet in the sequence
            self.length = len(files_keys)
            im = mamba.imageMb(files_dict[files_keys[0]], self.depth, rgbfilter=rgbfilter)
            self.width = im.mbIm.width
            self.height = im.mbIm.height
            self.seq.append(im)
            for i in range(1,self.length):
                self.seq.append(mamba.imageMb(self.width, self.height, self.depth, rgbfilter=rgbfilter))
                self.seq[i].load(files_dict[files_keys[i]], rgbfilter=rgbfilter)
        else:
            l = min(len(files_keys),self.length)
            # the sequence is overloaded 
            for i in range(l):
                self.seq[i].load(files_dict[files_keys[i]], rgbfilter=rgbfilter)
                
    def save(self, path, extension=".png"):
        """
        Saves the images of the 3D image stack (sequence) inside a directory
        located at 'path'.
        
        The function will create the directory if it doesn't exist. If the
        directory exists and already contains images they will be overwritten.
        The images are stored following this pattern (1.png, 2.png ...). You
        can modify the format of the image by changing the optional parameter
        'extension' (refer to PIL documentation for supported format).
        """
        if not os.path.isdir(path):
            os.mkdir(path)
            
        for i,im in enumerate(self.seq):
            im.save(os.path.join(path,"%d%s" % (i+1,extension)))
    
    def getDepth(self):
        """
        Returns the depth of the 3D image.
        """
        
        return self.depth
    
    def getSize(self):
        """
        Returns the size (tuple with width, height) of the 3D image.
        """
        
        return (self.width, self.height)
            
    def __len__(self):
        """
        Returns the length of the 3D image.
        """
        
        return self.length
            
    def getLength(self):
        """
        Returns the length of the 3D image.
        """
        
        return self.length
            
    def getName(self):
        """
        Returns the name of the 3D image.
        """
        
        return self.name

    def fill(self,v):
        """
        Fills the 3D image with value 'v'
        A zero value makes the image completely dark.
        """
        
        for im in self.seq:
            im.fill(v)

    def reset(self):
        """
        Reset the 3D image (all the pixels are put to 0).
        """
        
        for im in self.seq:
            im.reset()
        
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
            

    def showImage(self, index):
        """
        Activates the image display for image at 'index' in the 3D image stack.
        """
        
        self.seq[index].show()

    def hideImage(self, index):
        """
        Deactivates the image display for image at 'index' in the 3D image stack.
        """
        
        self.seq[index].hide()

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

class sequenceMb(image3DMb):
    """
    A sequence of images is represented by an instance of this class.
    This is a complete alias to image3DMb class kept for compatibility
    reasons.
    """
    pass

