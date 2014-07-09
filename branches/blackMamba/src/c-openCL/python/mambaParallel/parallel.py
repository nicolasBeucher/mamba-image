"""
This module provides an interface to the parallel package of Mamba.
It provides an implementation using openCL for some of the most useful functions
of Mamba.
"""
import mambaPLCore

try:
    import mamba
    import mambaUtils
    import mambaDisplay
    import mambaError
    import mambaExtra
    import mambaCore
except ImportError:
    raise ImportError("Missing Mamba library - http://www.mamba-image.org")
_mb_version = mamba.VERSION.split('.')
if int(_mb_version[0])!=2 and int(_mb_version[1])!=0:
    raise ImportError("mambaParallel requires mamba version 2.0 (current=%s)" %
                      _mb_version)

################################################################################
# Classes
################################################################################

class MambaParallelError(Exception):
    """
    Mamba basic exception.
    Occurs when the mamba library returns an error (return value different of NO_ERR).
    """
    
    def __init__(self, errValue):
        self.errValue = errValue
        self.errMsg   = mambaPLCore.MBPL_StrErr(self.errValue)
        
    def __str__(self):
        return "[errno "+str(self.errValue)+"] "+self.errMsg

#MB_Add
#MB_And
#MB_Or
#MB_Basins
#MB_BinHitOrMiss
#MB_BldNb32
#MB_BldNb8
#MB_BldNbb
#MB_Check
#MB_Compare
#MB_ConAdd
#MB_ConDiv
#MB_ConMul
#MB_ConSub
#MB_Convert
#MB_CopyBitPlane
#MB_CopyBytePlane
#MB_CopyLine
#MB_CropCopy
#MB_Destroy
#MB_Diff
#MB_DiffNb8
#MB_DiffNbb
#MB_Distanceb
#MB_DualBldNb32
#MB_DualBldNb8
#MB_DualBldNbb
#MB_Extract
#MB_Frame
#MB_GetPixel
#MB_HierarBld
#MB_HierarDualBld
#MB_Histo
#MB_Inf
#MB_InfFarNb32
#MB_InfFarNb8
#MB_InfFarNbb
#MB_InfNb32
#MB_InfNbb
#MB_Inv
#MB_Labelb
#MB_Load
#MB_Lookup
#MB_Mask
#MB_Mul
#MB_Or
#MB_PutPixel
#MB_Range
#MB_Shift32
#MB_Shift8
#MB_Shiftb
#MB_Sub
#MB_Sup
#MB_SupFarNb32
#MB_SupFarNb8
#MB_SupFarNbb
#MB_SupMask
#MB_SupNb32
#MB_SupNb8
#MB_SupNbb
#MB_Thresh
#MB_Watershed
#MB_Xor
#MB_depthRange

class _coreReplacer:

    def __init__(self):
        self.list_mbIm = []

        self.ERR_BAD_DEPTH = mambaPLCore.ERR_INVALID_IM_DEPTH
        self.ERR_BAD_IMAGE_DIMENSIONS = mambaPLCore.ERR_BAD_IMAGE_DIMENSIONS
        self.ERR_BAD_SIZE = mambaPLCore.ERR_INVALID_IM_SIZE
        self.ERR_CANT_ALLOCATE_MEMORY = mambaPLCore.ERR_CANT_CREATE_CL_BUFFER
        self.ERR_LOAD_DATA = mambaPLCore.ERR_INVALID_LOAD_DATA
        self.ERR_UNKNOWN = mambaPLCore.ERR_UNKNOWN
        self.NO_ERR = mambaPLCore.NO_ERR
        
        self.CHARBIT = mambaCore.CHARBIT
        self.ERR_BAD_DIRECTION = mambaCore.ERR_BAD_DIRECTION
        self.ERR_BAD_PARAMETER = mambaCore.ERR_BAD_PARAMETER
        self.ERR_BAD_VALUE = mambaCore.ERR_BAD_VALUE
        
        self.MB_SQUARE_GRID = mambaCore.MB_SQUARE_GRID
        self.MB_HEXAGONAL_GRID = mambaCore.MB_HEXAGONAL_GRID
        self.MB_FILLED_EDGE = mambaCore.MB_FILLED_EDGE
        self.MB_EMPTY_EDGE = mambaCore.MB_EMPTY_EDGE
        
    def replaceMbIm(self, mbIm):
        if mbIm not in self.list_mbIm:
            im = mambaPLCore.MBPL_Image()
            err = mambaPLCore.MBPL_Create(im, mbIm.width, mbIm.height, mbIm.depth)
            if err!=mambaPLCore.NO_ERR:
                raise MambaParallelError(err)
            err = mambaPLCore.MBPL_TransferFromMB(mbIm, im)
            if err!=mambaPLCore.NO_ERR:
                raise MambaParallelError(err)
            mbIm.pl = im
            self.list_mbIm.append(mbIm)

    def restoreMbIms(self):
        for mbIm in self.list_mbIm:
            err = mambaPLCore.MBPL_TransferToMB(mbIm.pl, mbIm)
            if err!=mambaPLCore.NO_ERR:
                raise MambaParallelError(err)
            del(mbIm.pl)
        self.list_mbIm = []
        
    def startReplace(self):
        self.list_mbIm = []
        mamba.mambaCore = self
        mambaUtils.mambaCore = self
        mambaDisplay.mambaCore = self
        mambaError.mambaCore = self
        mambaExtra.mambaCore = self
        
    def endReplace(self):
        self.restoreMbIms()
        mamba.mambaCore = mambaCore
        mambaUtils.mambaCore = mambaCore
        mambaDisplay.mambaCore = mambaCore
        mambaError.mambaCore = mambaCore
        mambaExtra.mambaCore = mambaCore
        
    def MB_Image(self):
        return mambaPLCore.MBPL_Image()

    def MB_StrErr(self, nb_err):
        return mambaPLCore.MBPL_StrErr(nb_err)
        
    def MB_Create(self, im, width, height, depth):
        if isinstance(im, mambaCore.MB_Image):
            if not hasattr(im, 'pl'):
                self.replaceMbIm(im)
            im = im.pl
        return mambaPLCore.MBPL_Create(im, width, height, depth)
    
    def MB_Add(self, src1, src2, dest):
        if isinstance(src1, mambaCore.MB_Image):
            if not hasattr(src1, 'pl'):
                self.replaceMbIm(src1)
            src1 = src1.pl
        if isinstance(src2, mambaCore.MB_Image):
            if not hasattr(src2, 'pl'):
                self.replaceMbIm(src2)
            src2 = src2.pl
        if isinstance(dest, mambaCore.MB_Image):
            if not hasattr(dest, 'pl'):
                self.replaceMbIm(dest)
            dest = dest.pl
        return mambaPLCore.MBPL_Add(src1, src2, dest)
    
    def MB_Copy(self, src, dest):
        if isinstance(src, mambaCore.MB_Image):
            if not hasattr(src, 'pl'):
                self.replaceMbIm(src)
            src = src.pl
        if isinstance(dest, mambaCore.MB_Image):
            if not hasattr(dest, 'pl'):
                self.replaceMbIm(dest)
            dest = dest.pl
        return mambaPLCore.MBPL_Copy(src, dest)

    def MB_Volume(self, src):
        if isinstance(src, mambaCore.MB_Image):
            if not hasattr(src, 'pl'):
                self.replaceMbIm(src)
            src = src.pl
        return mambaPLCore.MBPL_Volume(src)
        
    def MB_ConSet(self, dest, value):
        if isinstance(dest, mambaCore.MB_Image):
            if not hasattr(dest, 'pl'):
                self.replaceMbIm(dest)
            dest = dest.pl
        return mambaPLCore.MBPL_ConSet(dest, value)
        
    def MB_InfNb8(self, src, srcdest, neighbors, grid, edge):
        if isinstance(src, mambaCore.MB_Image):
            if not hasattr(src, 'pl'):
                self.replaceMbIm(src)
            src = src.pl
        if isinstance(srcdest, mambaCore.MB_Image):
            if not hasattr(srcdest, 'pl'):
                self.replaceMbIm(srcdest)
            srcdest = srcdest.pl
        return mambaPLCore.MBPL_InfNb8(src, srcdest, neighbors, grid, edge)
        

################################################################################
# Functions
################################################################################

def getPLImageCounter():
    """
    Returns the number of image currently defined inside the openCL device.
    Should always be 0, except during the runParallel function execution.
    """
    return mambaPLCore.cvar.MBPL_refcounter

def initializeParallel():
    """
    This functions initializes the parallel context (openCL context and CL code
    parsing).
    """
    err = mambaPLCore.MBPL_CreateContext()
    if err!=mambaPLCore.NO_ERR:
        raise MambaParallelError(err)

def closeParallel():
    """
    Closes the parallel context and destroys the existing one.
    """
    err = mambaPLCore.MBPL_DestroyContext()
    if err!=mambaPLCore.NO_ERR:
        raise MambaParallelError(err)

def runParallel(function, *args, **kwargs):
    """
    This function runs the given 'function' with its arguments 'args' and
    'kwargs' using the mambaParallel core API instead of the standard
    mamba core API.
    
    This can leads to great performance increase provided your function
    respect some basic rules.
    """

    core = _coreReplacer()
    
    # Replacing the mambaCore library by the parallel
    # core library
    core.startReplace()
    
    # Running the function (now using the parallel API
    # instead of the mambaCore API)
    retval = function(*args, **kwargs)
    
    # Restoring the mambaCore API as the core library
    core.endReplace()
    
    return retval
