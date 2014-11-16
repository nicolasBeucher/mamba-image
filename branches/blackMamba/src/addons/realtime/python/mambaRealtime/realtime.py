"""
This module provides an interface to the realtime module of Mamba.
It provides functions to open the realtime thread and communicate with it.
"""
import threading
import time
import sys
import platform
try:
    import queue
except ImportError:
    import Queue as queue
import traceback

import core

try:
    import mamba
    import mamba3D
    import mambaDisplay
except ImportError:
    raise ImportError("Missing Mamba library - http://www.mamba-image.org")
_mb_version = mamba.VERSION.split('.')
if int(_mb_version[0])!=2 and int(_mb_version[1])!=0:
    raise ImportError("mambaRealtime requires mamba version 2.0 (current=%s)" %
                      _mb_version)

# Handling specific tkinter error
from Tkinter import TclError

# Type of items that can be inserted inside the communication queue
_FREQ = 2
_ORDER = 3
_PICTURE = 4
_PROC_SET = 5
_PROC_RST = 6
_PROC_ADD = 7
_REC_START = 8
_REC_STOP = 9
_ERR_DEL = 10

_errorIcon = [
    0b00000000000000000000000000000000, 0b00000000000000000000000000000000,
    0b00000000000000000000000000000011, 0b11000000000000000000000000000000,
    0b00000000000000000000000000000011, 0b11000000000000000000000000000000,
    0b00000000000000000000000000000110, 0b01100000000000000000000000000000,
    0b00000000000000000000000000000110, 0b01100000000000000000000000000000,
    0b00000000000000000000000000001100, 0b00110000000000000000000000000000,
    0b00000000000000000000000000001100, 0b00110000000000000000000000000000,
    0b00000000000000000000000000011000, 0b00011000000000000000000000000000,
    0b00000000000000000000000000011000, 0b00011000000000000000000000000000,
    0b00000000000000000000000000110000, 0b00001100000000000000000000000000,
    0b00000000000000000000000000110000, 0b00001100000000000000000000000000,
    0b00000000000000000000000001100000, 0b00000110000000000000000000000000,
    0b00000000000000000000000001100000, 0b00000110000000000000000000000000,
    0b00000000000000000000000011000000, 0b00000011000000000000000000000000,
    0b00000000000000000000000011000011, 0b11000011000000000000000000000000,
    0b00000000000000000000000110000011, 0b11000001100000000000000000000000,
    0b00000000000000000000000110000011, 0b11000001100000000000000000000000,
    0b00000000000000000000001100000011, 0b11000000110000000000000000000000,
    0b00000000000000000000001100000011, 0b11000000110000000000000000000000,
    0b00000000000000000000011000000011, 0b11000000011000000000000000000000,
    0b00000000000000000000011000000011, 0b11000000011000000000000000000000,
    0b00000000000000000000110000000011, 0b11000000001100000000000000000000,
    0b00000000000000000000110000000011, 0b11000000001100000000000000000000,
    0b00000000000000000001100000000011, 0b11000000000110000000000000000000,
    0b00000000000000000001100000000011, 0b11000000000110000000000000000000,
    0b00000000000000000011000000000011, 0b11000000000011000000000000000000,
    0b00000000000000000011000000000011, 0b11000000000011000000000000000000,
    0b00000000000000000110000000000011, 0b11000000000001100000000000000000,
    0b00000000000000000110000000000011, 0b11000000000001100000000000000000,
    0b00000000000000001100000000000011, 0b11000000000000110000000000000000,
    0b00000000000000001100000000000011, 0b11000000000000110000000000000000,
    0b00000000000000011000000000000011, 0b11000000000000011000000000000000,
    0b00000000000000011000000000000011, 0b11000000000000011000000000000000,
    0b00000000000000110000000000000011, 0b11000000000000001100000000000000,
    0b00000000000000110000000000000011, 0b11000000000000001100000000000000,
    0b00000000000001100000000000000011, 0b11000000000000000110000000000000,
    0b00000000000001100000000000000011, 0b11000000000000000110000000000000,
    0b00000000000011000000000000000011, 0b11000000000000000011000000000000,
    0b00000000000011000000000000000011, 0b11000000000000000011000000000000,
    0b00000000000110000000000000000011, 0b11000000000000000001100000000000,
    0b00000000000110000000000000000011, 0b11000000000000000001100000000000,
    0b00000000001100000000000000000011, 0b11000000000000000000110000000000,
    0b00000000001100000000000000000011, 0b11000000000000000000110000000000,
    0b00000000011000000000000000000011, 0b11000000000000000000011000000000,
    0b00000000011000000000000000000011, 0b11000000000000000000011000000000,
    0b00000000110000000000000000000011, 0b11000000000000000000001100000000,
    0b00000000110000000000000000000011, 0b11000000000000000000001100000000,
    0b00000001100000000000000000000011, 0b11000000000000000000000110000000,
    0b00000001100000000000000000000011, 0b11000000000000000000000110000000,
    0b00000011000000000000000000000011, 0b11000000000000000000000011000000,
    0b00000011000000000000000000000011, 0b11000000000000000000000011000000,
    0b00000110000000000000000000000011, 0b11000000000000000000000001100000,
    0b00000110000000000000000000000011, 0b11000000000000000000000001100000,
    0b00001100000000000000000000000000, 0b00000000000000000000000000110000,
    0b00001100000000000000000000000000, 0b00000000000000000000000000110000,
    0b00011000000000000000000000000011, 0b11000000000000000000000000011000,
    0b00011000000000000000000000000011, 0b11000000000000000000000000011000,
    0b00110000000000000000000000000011, 0b11000000000000000000000000001100,
    0b00110000000000000000000000000011, 0b11000000000000000000000000001100,
    0b01100000000000000000000000000000, 0b00000000000000000000000000000110,
    0b01100000000000000000000000000000, 0b00000000000000000000000000000110,
    0b01111111111111111111111111111111, 0b11111111111111111111111111111110,
    0b01111111111111111111111111111111, 0b11111111111111111111111111111110,
    0b00000000000000000000000000000000, 0b00000000000000000000000000000000,
]

###############################################################################
#  Definitions
if platform.system()=='Windows':
    """ Value to use when using a directshow video API device"""
    DSHOW = core.DSHOW_TYPE

if platform.system()=='Linux':
    """ Value to use when using a video for linux 2 api device"""
    V4L2 = core.V4L2_TYPE

""" Value to use when using a video file (through audio video codec API)"""
AVC = core.AVC_TYPE

""" Value to use when the process uses an image sequence"""
SEQUENTIAL = 1

""" Value to use when the process uses only the last image from the video device"""
INSTANT = 0


################################################################################
# Classes
################################################################################

class MambaRealtimeError(Exception):
    """
    Mamba Realtime basic exception.
    Occurs when improper call to a function is made.
    """
    
    def __init__(self, errMsg):
        self.errMsg = errMsg
        
    def __str__(self):
        return self.errMsg

class _MBRT_Item:
    # Items used in the communication queue

    def __init__(self, type, value, options=[]):
        self.type = type
        self.value = value
        self.options = options

class _MBRT_Thread(threading.Thread):
    # Thread for the acquisition, process and display of the video
    
    def __init__(self, queue, seqdepth=10):
        threading.Thread.__init__(self)
        self.daemon = True
        self.q = queue
        self.seqDepth = seqdepth
        self.mustStop = False
        
    def run(self):
        # The main loop for the realtime module is in a separated thread
        # so as to let the user keep the control of the console
        
        # Variables init
        self.pauseOn = False
        self.colorOn = False
        self.recOn = False
        self.displayCreated = False
        self.error = ""
        self.curIcon = None
        self.palname = ""
        # process variables
        self.procList = []
        self.procType = None
        self.procOn = False
        
        # First acquisition device init
        (w,h) = self.initAcquisition()
        # Then display init
        self.initDisplay(w,h)

        # internal time reference (for frequency handling)
        self.timeIndex = time.time()

        # Loop as long as the main thread is alive
        while not self.mustStop:
            
            # Screen events handling
            self.handleScreenEvents()
            # Console commands queue handling
            self.handleQueueCommands()
            
            # If the acquisition is not on pause
            if not self.pauseOn:
                # gets the image from the device
                self.acquireImageFromDevice()
                # Then process it
                self.handleProcess()
            
            # Display the results into the screen
            self.displayResult()
            # Then eventually display info on it
            self.displayInfo()
            
            # records the picture if activated
            if self.recOn:
                self.recordResult()
                
            # sequence index update
            self.seqIndex = (self.seqIndex+1)%self.seqDepth
            
            # framerate control
            self.waitFrame()
            
        # Destroying created structures and memory freeing
        self.closeAll()
        
    # INIT and END #############################################################

    def initAcquisition(self):
        # At the beginning, the thread creates the acquisition device and extracts
        # specific information. This allow to create the mamba images and
        # sequences.
        
        err,w,h = core.MBRT_GetAcqSize()
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            self.mustStop = True
            return (0,0)
        err, freq = core.MBRT_GetAcqFrameRate()
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            self.mustStop = True
            return (0,0)
        self.frequency = freq
        self.period = 1.0/self.frequency

        core.MBRT_StartAcq()
        
        self.red = mamba.imageMb(w,h)
        self.green = mamba.imageMb(w,h)
        self.blue = mamba.imageMb(w,h)
        self.redSeq = mamba3D.sequenceMb(w,h,self.seqDepth)
        self.greenSeq = mamba3D.sequenceMb(w,h,self.seqDepth)
        self.blueSeq = mamba3D.sequenceMb(w,h,self.seqDepth)
        self.seqIndex = 0
        
        return self.red.getSize()
        
    def initDisplay(self, w, h):
        # Creates the display for width w and height h
        if not self.mustStop:
            err = core.MBRT_CreateDisplay(w, h)
            if err!=core.MBRT_NO_ERR:
                self.error = core.MBRT_StrErr(err)
                self.mustStop = True
                return
            self.displayCreated = True
            
    def closeAll(self):
        # Closes all the created strcutures and components
        if self.displayCreated:
            core.MBRT_DestroyDisplay()
        core.MBRT_StopAcq()
        
    # EVENTS and COMMANDS ######################################################
        
    def setPaletteDisplay(self):
        # Changes the display color palette
        try:
            
            names = [""] + mambaDisplay.listPalettes()
            try:
                i = names.index(self.palname)
            except:
                i = 0
            i = (i+1)%len(names)
            self.palname = names[i]
            
            if self.palname:
                pal = mambaDisplay.getPalette(self.palname)
            else:
                pal = ()
                for i in range(256):
                    pal += (i,i,i)
            err = core.MBRT_PaletteDisplay(list(pal))
            if err!=core.MBRT_NO_ERR:
                self.error = core.MBRT_StrErr(err)
        except ValueError as exc:
            self.error = str(exc)
            
    def handleQueueCommands(self):
        # gets the command from the communication queue and changes the 
        # parameters of the realtime.
        try:
            item = self.q.get_nowait()
            if item.type == _PROC_SET:
                # Sets the process (replace the previous ones)
                if item.options[0]==INSTANT or item.options[0]==SEQUENTIAL:
                    self.procList = [[item.value, item.options[1], item.options[2]]]
                    self.procOn = True
                    self.procType = item.options[0]
            elif item.type == _PROC_RST:
                # Resets the process (no process is applied)
                self.procList = []
                self.procOn = False
                self.procType = None
            elif item.type == _PROC_ADD:
                # Adds a process to the process list
                # Process must be INSTANT
                if self.procList==[]:
                    item.options[0] = INSTANT
                if item.options[0]==INSTANT:
                    self.procList.append([item.value, item.options[1], item.options[2]])
                    self.procOn = True
            elif item.type == _REC_START:
                # recording is started
                if not self.recOn:
                    err = core.MBRT_RecordStart(item.value)
                    if err!=core.MBRT_NO_ERR:
                        self.error = core.MBRT_StrErr(err)
                    else:
                        self.recOn = True
            elif item.type == _REC_STOP:
                # recording is stopped
                core.MBRT_RecordEnd()
                self.recOn = False
            elif item.type == _FREQ:
                # Changes the framerate
                try:
                    self.frequency = float(item.value)
                except ValueError:
                    self.error = "Frequency must be a float number"
                    pass
                self.frequency=min(self.frequency, 50.0)
                self.frequency=max(self.frequency, 1.0)
                self.period = 1.0/self.frequency
            elif item.type == _ORDER:
                # Other type of command
                if item.value=="close":
                    self.mustStop = True
                elif item.value=="pause":
                    self.pauseOn = not self.pauseOn
                elif item.value=="color":
                    if not self.pauseOn:
                        self.colorOn = not self.colorOn
                        self.redSeq.reset()
                        self.greenSeq.reset()
                        self.blueSeq.reset()
                        self.seqIndex = 0
            elif item.type == _PICTURE:
                # Takes a snapshot
                try:
                    if not self.colorOn:
                        self.red.save(str(item.value))
                    else:
                        mamba.mix(self.red,self.green,self.blue).save(str(item.value))
                except ValueError:
                    self.error = "The picture path is invalid"
                    pass
            elif item.type == _ERR_DEL:
                # Erases the error stored
                self.error = ""
            else:
                # Error
                self.error = "Unknown command sent to the display thread"
                self.mustStop = True
            self.q.task_done()
        except queue.Empty:
            pass
            
    def handleScreenEvents(self):
        # Handles the events occuring within the display (close, key, mouse ...)
        err, event_code = core.MBRT_PollDisplay()
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            self.mustStop = True
        elif event_code == core.EVENT_CLOSE:
            self.mustStop = True
        elif event_code == core.EVENT_PROCESS:
            self.procOn = not self.procOn
        elif event_code == core.EVENT_PAUSE:
            self.pauseOn = not self.pauseOn
        elif event_code == core.EVENT_PALETTE:
            self.setPaletteDisplay()
        elif event_code == core.EVENT_COLOR:
            if not self.pauseOn:
                self.colorOn = not self.colorOn
                self.redSeq.reset()
                self.greenSeq.reset()
                self.blueSeq.reset()
                self.seqIndex = 0
            
    def waitFrame(self):
        # Waits the required amount of time to ensure the framerate
            
        # frequency computation
        t = time.time()
        self.timeIndex = self.timeIndex+self.period
        dt = self.timeIndex-t
        if dt>0:
            time.sleep(dt)
        else:
            # Reajusting and sleeping just a bit
            self.timeIndex = t
            time.sleep(0.001)
    
    # PROCESS and ERRORS #######################################################
    
    def handleProcess(self):
        # Manages the process applied to the acquired images.
        if self.procOn and self.procList!=[]:
            for index, procCtx in enumerate(self.procList):
                try:
                    if self.procType==SEQUENTIAL and index==0:
                        if self.colorOn:
                            args = (self.redSeq, self.greenSeq, self.blueSeq,
                                    self.seqIndex,
                                    self.red, self.green, self.blue) + procCtx[1]
                        else:
                            args = (self.redSeq, self.seqIndex, self.red) + procCtx[1]
                    elif index==0:
                        if self.colorOn:
                            args = (self.redSeq[self.seqIndex],
                                    self.greenSeq[self.seqIndex],
                                    self.blueSeq[self.seqIndex],
                                    self.red,
                                    self.green,
                                    self.blue) + procCtx[1]
                        else:
                            args = (self.redSeq[self.seqIndex], self.red) + procCtx[1]
                    else:
                        if self.colorOn:
                            args = (self.red,
                                    self.green,
                                    self.blue,
                                    self.red,
                                    self.green,
                                    self.blue) + procCtx[1]
                        else:
                            args = (self.red, self.red) + procCtx[1]
                    procCtx[0](*args, **procCtx[2])
                except TclError:
                    self.error = "exception in realtime 'process' - Please check for any activated display and remove it"
                    self.procList = []
                    self.procOn = False
                    break
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.error = "exception in realtime 'process' \n"
                    self.error += '-'*60+'\n'
                    self.error += ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    self.error += '-'*60+'\n'
                    self.procList = []
                    self.procOn = False
                    break
        else:
            if self.colorOn:
                mamba.copy(self.redSeq[self.seqIndex], self.red)
                mamba.copy(self.greenSeq[self.seqIndex], self.green)
                mamba.copy(self.blueSeq[self.seqIndex], self.blue)
            else:
                mamba.copy(self.redSeq[self.seqIndex], self.red)
    
    # DISPLAY and ACQUISITION ##################################################

    def acquireImageFromDevice(self):
        # Obtains the images from the acquisition device
        # the red channel is used when working greyscale only
        if self.colorOn:
            err = core.MBRT_GetColorImageFromAcq(
                                    self.redSeq[self.seqIndex].mbIm,
                                    self.greenSeq[self.seqIndex].mbIm,
                                    self.blueSeq[self.seqIndex].mbIm)
        else:
            err = core.MBRT_GetImageFromAcq(self.redSeq[self.seqIndex].mbIm)
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            self.mustStop = True

    def displayResult(self):
        # Updates the display with the computed image
        if self.colorOn:
            err, fps = core.MBRT_UpdateDisplayColor(
                           self.red.mbIm,
                           self.green.mbIm,
                           self.blue.mbIm,
                           self.frequency)
        else:
            err, fps = core.MBRT_UpdateDisplay(self.red.mbIm, self.frequency)
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            self.mustStop = True
        
    def displayInfo(self):
        # Display some information on the screen
            
        # Displays an icon signaling an error
        if self.error and self.curIcon==None:
            self.curIcon = _errorIcon
            err = core.MBRT_IconDisplay(64,64,self.curIcon)
            if err!=core.MBRT_NO_ERR:
                self.error = core.MBRT_StrErr(err)
                self.mustStop = True
        if not self.error and self.curIcon!=None:
            self.curIcon = None
            err = core.MBRT_IconDisplay(0,0,[])
            if err!=core.MBRT_NO_ERR:
                self.error = core.MBRT_StrErr(err)
                self.mustStop = True
        
    def recordResult(self):
        # Records the image
        if self.colorOn:
            err = core.MBRT_RecordColorImage(
                                    self.red.mbIm,
                                    self.green.mbIm,
                                    self.blue.mbIm)
        else:
            err = core.MBRT_RecordImage(self.red.mbIm)
        if err!=core.MBRT_NO_ERR:
            self.error = core.MBRT_StrErr(err)
            # recording is stopped
            core.MBRT_RecordEnd()
            self.rec0n = False
            
    # OTHERS ###################################################################
    
    def getError(self):
        # Returns the error value
        return self.error[:]

_com_queue = queue.Queue()
_display_thread = None

################################################################################
# Functions
################################################################################

def launch(device, devType, seqlength=10):
    """
    Initializes and activates the realtime module using 'device' for the 
    acquisition.
    
    The options are similar to the ones used in function initialize.
    
    This function is similar to calling successively initialize and
    activate.
    """
    initialize(device, devType, seqlength)
    activate()

def initialize(device, devType, seqlength=10):
    """
    Initializes the realtime module using 'device' for the acquisition.
    'devType' indicates the type of the device (either V4L2(linux), DSHOW(windows) or AVC).
    This function must be called before any other.

    'seqlength' controls the length of the image sequence the thread is
    filling with the acquisition image. This sequence can be used in computation
    as an input.
    """
    global _display_thread

    # Verification over the display thread, it must be None
    # so the init function could create a new one
    if _display_thread:
        if _display_thread.isAlive():
            raise MambaRealtimeError("Realtime is already initialized and running")
        else:
            # In the case _display_thread is only created but not running
            # then it is deleted
            _display_thread = None

    # The context is destroyed by precaution
    core.MBRT_DestroyContext()

    # The context and video acquisition inits are called in the main thread
    # due to directshow API restrictions (COM)
    
    err = core.MBRT_CreateContext()
    if err!=core.MBRT_NO_ERR:
        raise MambaRealtimeError(core.MBRT_StrErr(err))

    err = core.MBRT_CreateVideoAcq(device, devType)
    if err!=core.MBRT_NO_ERR:
        raise MambaRealtimeError(core.MBRT_StrErr(err))

    _display_thread = _MBRT_Thread(_com_queue,seqlength)

def activate():
    """
    Activates the realtime module. Opens the acquisition device and creates the 
    display in a separate thread. The thread ensures the acquisition and display 
    of an image at a frequency of 10Hz with no treatment applied.
    """
    global _display_thread

    if not _display_thread:
        raise MambaRealtimeError("realtime not properly initialized")

    if _display_thread.isAlive():
        raise MambaRealtimeError("Realtime is already initialized and running")

    if _display_thread.mustStop:
        # The thread is not alive but was not initialized it is the remains of 
        # the previous one
        raise MambaRealtimeError("realtime not properly initialized")

    _display_thread.start()
    while(not _display_thread.isAlive()):
        time.sleep(0.01)
    time.sleep(0.5)

def deactivate():
    """
    Deactivates the realtime module. Closes the acquisition device and the display.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_ORDER, "close")
        _com_queue.put(item)
        while(_display_thread.isAlive()):
            time.sleep(0.01)
        _display_thread = None
    core.MBRT_DestroyVideoAcq()
    core.MBRT_DestroyContext()

def isActivated():
    """
    Returns True if the realtime thread is active and alive.
    """
    global _display_thread
    return _display_thread and _display_thread.isAlive()

def getError():
    """
    Returns the last error that occured in the realtime thread. The thread does
    not produce exceptions so if your request did not work, use this function
    do get the error message.
    
    The function will return an empty string if no error occured.
    """
    global _display_thread
    if not _display_thread:
        return "realtime not properly initialized"
    else:
        err = _display_thread.getError()
        if _display_thread.isAlive():
            item = _MBRT_Item(_ERR_DEL, None)
            _com_queue.put(item)
        return err

def getSize():
    """
    Returns a tuple containing the size of the images acquired and displayed
    by the realtime module.

    If the realtime module is not properly initialized the returned size will
    be negative.
    """
    global _display_thread
    if _display_thread and _display_thread.isAlive():
        err,w,h = core.MBRT_GetAcqSize()
        if err!=core.MBRT_NO_ERR:
            raise MambaRealtimeError(core.MBRT_StrErr(err))
    else:
        w = h = -1
    
    return (w,h)

def setProcess(process, type, *args, **kwargs):
    """
    Changes the 'process' (treatment) applied to the images acquired and displayed 
    by the realtime thread. This function will replace any process or chains of
    processes that may be currently active.
    
    if 'type' is set to INSTANT, 'process' must be a function/method whom 
    prototype must be one of the following:
        * process(imIn, imOut, ...) when processing in greyscale
        * process(imInR, imInG, imInB, imOutR, imOutG, imOutB, ...) when 
        processing in color
    where imIn(X) and imOut(X) are mamba.imageMb objects.
    imIn(X) are given by the acquisition device and imOut(X) will be displayed.
    
    if 'type' is set to SEQUENTIAL, 'process' must be a function/method whom 
    prototype must be one of the following:
        * process(seqIn, seqIndex, imOut, ...) when processing in greyscale
        * process(seqInR, seqInG, seqInB, seqIndex, imOutR, imOutG, imOutB, ...)
        when processing in color
    where imOut(X) are mamba.imageMb objects. seqIn(X) are sequences as 
    defined in module mambaComposed.sequence that contains the last 10 
    images obtained from the acqusition device. seqIndex indicates the
    index of the most recent. imOut(X) will be displayed. 
    
    Others arguments can be passed through 'args' and 'kwargs'.
        
    If process is not compliant with this, the treatment will be deactivated in 
    realtime. Be aware that activating a greyscale process while the display
    is color (or the reverse) is not allowed.
    
    Take also care to remove any display activation (show method).
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_PROC_SET, process, [type, args, kwargs])
        _com_queue.put(item)

def addProcess(process, *args, **kwargs):
    """
    Adds the given 'process' (treatment) to the list of process to apply to the
    acquired image. This function will append the process to the list of
    processes currently applied.
    
    'process' must be a function/method whom prototype must be one of the
    following:
        * process(imIn, imOut, ...) when processing in greyscale
        * process(imInR, imInG, imInB, imOutR, imOutG, imOutB, ...) when 
        processing in color
    where imIn(X) and imOut(X) are mamba.imageMb objects.
    imIn(X) are given by the acquisition device and imOut(X) will be displayed.
    
    Others arguments can be passed through 'args' and 'kwargs'.
        
    If process is not compliant with this, the treatment will be deactivated in 
    realtime. Be aware that activating a greyscale process while the display
    is color (or the reverse) is not allowed.
    
    Take also care to remove any display activation (show method).
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_PROC_ADD, process, [INSTANT, args, kwargs])
        _com_queue.put(item)

def resetProcess():
    """
    Resets the realtime thread so that no process (treatment) is applied to the 
    images acquired and displayed.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_PROC_RST, None)
        _com_queue.put(item)

def setFramerate(f):
    """
    Sets the framerate 'f' of acquisition and display in the realtime thread.
    This is strongly limited by the acquisition module and the selected process.
    
    The framerate is nonetheless limited inside the [1.0, 50.0] fps range by the
    realtime module.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_FREQ, f)
        _com_queue.put(item)

def takePicture(path):
    """
    Takes a picture of the current image displayed (at the moment the function
    is called) and puts it into file 'path'.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_PICTURE, path)
        _com_queue.put(item)

def startRecording(path):
    """
    Starts the recording of the realtime footage into file 'path'. The created 
    file will be a video encoded using MPEG2 codec (DVD format).
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_REC_START, path)
        _com_queue.put(item)

def stopRecording():
    """
    Stops the recording of the realtime footage.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_REC_STOP, None)
        _com_queue.put(item)

def toggleColor():
    """
    Toggles the color acquisition and display ON/OFF depending on its
    current status. By default the acquisition is greyscale.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_ORDER, "color")
        _com_queue.put(item)

def togglePause():
    """
    Toggles the pause ON/OFF depending on its current status. When paused
    acquisition and process are not executed but you can still execute
    commands (such as palette selection, histogram view...) and see the display.
    """
    global _display_thread, _com_queue
    if _display_thread and _display_thread.isAlive():
        item = _MBRT_Item(_ORDER, "pause")
        _com_queue.put(item)
