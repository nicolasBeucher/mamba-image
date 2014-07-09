"""
This module provides classes, methods and functions to perform morphological
computations over sequences of images.

This module can be considered as a restricted 3-D extension of mamba.
"""

# contributor: Nicolas BEUCHER

import mamba
import glob
import os

###############################################################################
#  Classes
###############################################################################

class sequenceMb:
    """
    A sequence of images is represented by an instance of this class.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for a mamba image sequence.
        A sequence is defined by its images width and height and by its length
        (the number of images in it).
        
        There is a wide range of possibilities :
            * sequenceMb() : without arguments will create an empty greyscale 
            image sequence.
            * sequenceMb(seq) : will create a sequence using the same size, depth 
             and length than sequence 'seq'.
            * sequenceMb(im) : will create a sequence using the same size and 
            depth than image 'im'.
            * sequenceMb(depth) : will create an image sequence with the desired 
            'depth' (1, 8 or 32) for the mamba images.
            * sequenceMb(path) : will load the image sequence located in 'path',
            see the load method.
            * sequenceMb(seq, depth) : will create a sequence using the same size
            than sequence 'seq' and the specified 'depth'.
            * sequenceMb(im, length) : will create a sequence using the same size
            than image 'im' and the specified 'length'.
            * sequenceMb(path, depth) : will load the image sequence located in
            'path' and convert it to the specified 'depth'.
            * sequenceMb(width, height, length) : will create an image sequence
            with size 'width'x'height' and 'length'.
            * sequenceMb(width, height, length, depth) : will create an image 
            sequence with size 'width'x'height', 'depth' and 'length'.
            
        When not specified, the width, height and length of the sequence will 
        be set to 256. The default depth is 8 (greyscale).
        
        When loading an image sequence make sure all the images have the same 
        size.
        """
        
        self._index = 0
        
        # List of all the parameters that must be retrieved from the arguments
        self.rgbfilter = None
        self.displayer = None
        
        # First we look into the dictionnary to see if they were specified
        # specifically by the user
        if "rgbfilter" in kwargs:
            self.rgbfilter = kwargs["rgbfilter"]
        if "displayer" in kwargs:
            self.displayer = kwargs["displayer"]
            
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
        
    def _createSeq(self, w, h, d, l):
        # Create the sequence according to the parameters
        self.length = l
        self.seq = []
        self.name = "Mamba image sequence"
        for i in range(self.length):
            self.seq.append(mamba.imageMb(w, h, d, displayer=self.displayer, rgbfilter=self.rgbfilter))
        self.width, self.height = self.seq[0].getSize()
        self.depth = self.seq[0].getDepth()
        
    def __str__(self):
        return 'Mamba sequence object : '+self.name+' - '+str(self.depth)

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

    def load(self, path, rgbfilter=None):
        """
        Loads a sequence of image as found in directory 'path'.

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
        Saves the images of the sequence inside a directory located at 'path'.
        
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
        Returns the depth of the sequence.
        """
        
        return self.depth
    
    def getSize(self):
        """
        Returns the size (tuple with width, height) of the sequence.
        """
        
        return (self.width, self.height)
            
    def getName(self):
        """
        Returns the name of the sequence.
        """
        
        return self.name
            
    def __len__(self):
        """
        Returns the length of the sequence.
        """
        
        return self.length
            
    def getLength(self):
        """
        Returns the length of the sequence.
        """
        
        return self.length
            
    def setPalette(self, pal):
        """
        Defines the palette to use to convert the images in color for display
        and save. Apply to all the images in the sequence.
        """
        
        for im in self.seq:
            im.setPalette(pal)
            
    def resetPalette(self):
        """
        Undefines the palette to use to convert the images in color for display
        and save. The images will be grey scale.
        """
        
        for im in self.seq:
            im.resetPalette()

    def fill(self,v):
        """
        Fills all the images in the sequence with value 'v'
        A zero value makes the image completely dark.
        """
        
        for im in self.seq:
            im.fill(v)

    def reset(self):
        """
        Reset the sequence (all the pixels are put to 0).
        """
        
        for im in self.seq:
            im.reset()

    def showAllImages(self):
        """
        Activates the image display for all the images in the sequence.
        """
        
        for im in self.seq:
            im.show()
    
    def showImage(self, index):
        """
        Activates the image display for image at 'index' in the sequence.
        """
        
        self.seq[index].show()

    def hideAllImages(self):
        """
        Deactivates the image display for all the images in the sequence.
        """
        
        for im in self.seq:
            im.hide()

    def hideImage(self, index):
        """
        Deactivates the image display for image at 'index' in the sequence.
        """
        
        self.seq[index].hide()

################################################################################
#  Functions
################################################################################

def copySequence(sequenceIn, sequenceOut):
    """
    Copies the content of 'sequenceIn' into 'sequenceOut'. The copy is stopped
    by the smallest sequence.
    """
    
    for i in range(min(sequenceOut.getLength(), sequenceIn.getLength())):
        mamba.copy(sequenceIn[i], sequenceOut[i])

def erodeByCylinderSequence(sequence, height, section):
    """
    Erodes the 'sequence' using a cylinder with an hexagonal section of size 
    2x'section' and a height of 2x'height'. The sequence is modified by this
    function.
    """
    
    l = sequence.getLength()
    for im in sequence:
        mamba.erode(im, im, section, se=mamba.HEXAGON)
    provSeq = sequenceMb(sequence)
    for i in range(l):
        mamba.copy(sequence[i], provSeq[i])
        for j in range(max(0,i-height), min(l,i+height+1)):
            mamba.logic(provSeq[i], sequence[j], provSeq[i], "inf")
    copySequence(provSeq, sequence)
        
def dilateByCylinderSequence(sequence, height, section):
    """
    Dilates the 'sequence' using a cylinder with an hexagonal section of size 
    2x'section' and a height of 2x'height'. The sequence is modified by this
    function.
    """
    
    l = sequence.getLength()
    for im in sequence:
        mamba.dilate(im, im, section, se=mamba.HEXAGON)
    provSeq = sequenceMb(sequence)
    for i in range(l):
        mamba.copy(sequence[i], provSeq[i])
        for j in range(max(0,i-height), min(l,i+height+1)):
            mamba.logic(provSeq[i], sequence[j], provSeq[i], "sup")
    copySequence(provSeq, sequence)

def openByCylinderSequence(sequence, height, section):
    """
    Opening using the dilation and erosion by a cylinder.
    """
    
    erodeByCylinderSequence(sequence, height, section)
    dilateByCylinderSequence(sequence, height, section)
    
def closeByCylinderSequence(sequence, height, section):
    """
    Closing using the dilation and erosion by a cylinder.
    """
    
    dilateByCylinderSequence(sequence, height, section)
    erodeByCylinderSequence(sequence, height, section)
