"""
Extra displays.

This module defines specific extra displays that are meant to be used
interactively with the user. This module is not loaded by default with
mambaDisplay.
"""

import mamba.core as core
import mamba.utils as utils
import mamba

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog
    import tkinter.colorchooser as colorchooser   
except ImportError:
    try:
        import Tkinter as tk
        import ttk
        import tkFileDialog as filedialog
        import tkColorChooser as colorchooser
    except ImportError:
        print("Missing Tkinter library")
        raise
try:
    from PIL import ImageTk
    from PIL import Image
except ImportError:
    print("Missing PIL library (pillow) - https://pypi.python.org/pypi/Pillow/")
    raise
    
from . import constants

################################################################################
# Dynamic threshold
################################################################################
# This display opens a window in which the image can be thresholded dynamically
# using the keyboard.

class _imageThreshold(tk.Toplevel):

    # Constructor ##############################################################
    def __init__(self, mbIm):
        tk.Toplevel.__init__(self, None)
        self.mbIm = mbIm
        self.mbImThresh = utils.create(self.mbIm.width,self.mbIm.height,1)
        self.body()
        self.grab_set()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.initial_focus.focus_set()
        
        # Events bindings
        self.canvas.bind("<Motion>", self.mouseMotionEvent)
        self.canvas.bind("<Configure>", self.resizeEvent)
        self.canvas.bind("<Button-4>", self.mouseEvent)
        self.canvas.bind("<Button-5>", self.mouseEvent)
        self.bind("<MouseWheel>", self.mouseEvent)
        self.canvas.bind("<Button-1>", self.mouseEvent)
        self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
        self.bind("<KeyPress>", self.keyboardEvent)
        
        self.wait_window(self)

    def body(self):
        # Size of the image, canvas and display.
        self.osize = [self.mbIm.width,self.mbIm.height]
        imsize = self.osize[:]
        self.zoom = 1.0
        while imsize < [constants._MIN, constants._MIN]:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            self.zoom = self.zoom*2
        while imsize > [constants._MAX, constants._MAX]:
            imsize[0] = imsize[0]/2
            imsize[1] = imsize[1]/2
            self.zoom = self.zoom/2
        
        self.title('thresholder - %d%%' % (int(self.zoom*100)))
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.imid = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.computeThresholdLimits()
        
        # Resize configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Threshold infos
        self.thresholdInfos = tk.StringVar(self)
        lab = ttk.Label(self, anchor=tk.W, textvariable=self.thresholdInfos)
        lab.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.thresholdInfos.set("threshold - low : "+str(self.low)+" - high : "+str(self.high))
        # Image display
        self.canvas_vb = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_vb.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.canvas_hb = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas_hb.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.canvas = tk.Canvas(self,
                                bd=0,
                                xscrollcommand=self.canvas_hb.set,
                                yscrollcommand=self.canvas_vb.set)
        self.canvas_hb.config(command=self.canvas.xview)
        self.canvas_vb.config(command=self.canvas.yview)
        self.canvas.grid(row=1, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()        
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        # Statusbar
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(1, weight=1)
        statusbar.grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.bclose = ttk.Button(statusbar, text="close", command=self.close)
        self.bclose.grid(row=0, column=0, sticky=tk.W)
        self.bsave = ttk.Button(statusbar, text="save", command=self.saveImage)
        self.bsave.grid(row=0, column=1, sticky=tk.W)
        self.infos= tk.StringVar(self)
        lab = ttk.Label(statusbar, anchor=tk.W, textvariable=self.infos)
        lab.grid(row=0, column=2, sticky=tk.E+tk.W)

        self.updateim()
        
    def computeThresholdLimits(self):
        if self.mbIm.depth==8:
            self.low = 0
            self.lowlim = 0
            self.high = 255
            self.highlim = 255
        elif self.mbIm.depth==32:
            self.low = 0
            self.lowlim = 0
            self.high = 0xffffffff
            self.highlim = 0xffffffff
    
    # Events handling functions ################################################
        
    def resizeEvent(self, event):
        # Handles the resizing of the display window.
        self.csize = [event.width, event.height]
        self.drawImage()
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
        
    def keyboardEvent(self, event):
        # Handles keyboard events
        
        #Zoom
        if event.char == "z":
            # ZOOM IN
            if self.zoom<=0.25:
                self.setZoom(self.zoom*2)
            else:
                self.setZoom(self.zoom+0.25)
        elif event.char == "a":
            # ZOOM OUT
            if self.zoom<=0.25:
                zoom = self.zoom/2
                if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                    self.setZoom(zoom)
            else:
                self.setZoom(self.zoom-0.25)
                
        # Threshold change
        elif event.char == "q":
            self.low = min(self.low+1, self.high)
            self.thresholdInfos.set("threshold - low : "+str(self.low)+" - high : "+str(self.high))
            self.updateim()
        elif event.char == "w":
            self.low = max(self.low-1, self.lowlim)
            self.thresholdInfos.set("threshold - low : "+str(self.low)+" - high : "+str(self.high))
            self.updateim()
        elif event.char == "s":
            self.high = min(self.high+1, self.highlim)
            self.thresholdInfos.set("threshold - low : "+str(self.low)+" - high : "+str(self.high))
            self.updateim()
        elif event.char == "x":
            self.high = max(self.high-1, self.low)
            self.thresholdInfos.set("threshold - low : "+str(self.low)+" - high : "+str(self.high))
            self.updateim()
    
    def mouseEvent(self, event):
        # Handles mouse events (except menu pop up)
        # Mainly zoom in or out using the mouse wheel, and moving the image
        if event.type=="4":
            if event.num==1:
                self.canvas.config(cursor="fleur")
            elif event.num==4:
                # Mouse wheel scroll up under Linux
                # ZOOM IN
                if self.zoom<=0.25:
                    self.setZoom(self.zoom*2)
                else:
                    self.setZoom(self.zoom+0.25)
            elif event.num==5:
                # Mouse wheel scroll down under Linux
                # ZOOM OUT
                if self.zoom<=0.25:
                    zoom = self.zoom/2
                    if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                        self.setZoom(zoom)
                else:
                    self.setZoom(self.zoom-0.25)
            
        elif event.type=="5":
            if event.num==1:
                # Button 1 released
                self.canvas.config(cursor="arrow")
            
        elif event.type=="38":
            # Mouse wheel under Windows
            if event.delta>0:
                # ZOOM IN
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        self.setZoom(self.zoom*2)
                    else:
                        self.setZoom(self.zoom+0.25)
            else:
                # ZOOM OUT
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        zoom = self.zoom/2
                        if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                            self.setZoom(zoom)
                    else:
                        self.setZoom(self.zoom-0.25)
            
    def mouseMotionEvent(self, event):
        # Indicates the position of the mouse inside the image.
        x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])/2,0)
        y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])/2,0)
        
        x = max(min(x,self.dsize[0]-1), 0)
        y = max(min(y,self.dsize[1]-1), 0)
        x = int((float(x)/self.dsize[0])*self.osize[0])
        y = int((float(y)/self.dsize[1])*self.osize[1])
        err, v1 = core.MB_GetPixel(self.mbIm, x, y)
        err, vt = core.MB_GetPixel(self.mbImThresh, x, y)
        vt = bool(vt)
        self.infos.set("At ("+str(x)+","+str(y)+") = ["+str(v1)+","+str(vt)+"]")
        
        if event.state&0x0100==0x0100 :
            if not self.dsize[0] <= self.csize[0]:
                dx = event.x-self.mouse_x
                posx = self.canvas_hb.get()[0] - float(dx)/self.dsize[0]
                self.canvas.xview_moveto(posx)
            if not self.dsize[1] <= self.csize[1]:
                dy = event.y-self.mouse_y
                posy = self.canvas_vb.get()[0] - float(dy)/self.dsize[1]
                self.canvas.yview_moveto(posy)
            
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    # Helper functions #########################################################
    
    def setZoom(self, zoom):
        # Sets the zoom value and changes the display accordingly.
        oz = self.zoom
        self.zoom = zoom
        self.dsize[0] = int(self.zoom*self.osize[0])
        self.dsize[1] = int(self.zoom*self.osize[1])
        self.canvas.config(scrollregion=(0,0,self.dsize[0]-1,self.dsize[1]-1))
        self.drawImage()
        self.title('thresholder - %d%%' % (int(self.zoom*100)))
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
            
    def updateim(self):
        # Updates the display with the new contents of the mamba image.
        
        err = core.MB_Thresh(self.mbIm, self.mbImThresh, self.low, self.high)
        self.pilImage = utils.convertToPILFormat(self.mbImThresh)
        m = max(self.osize)
        icon_size = ((constants._icon_max_size*self.osize[0])//m,(constants._icon_max_size*self.osize[1])//m)
        self.icon = ImageTk.PhotoImage(self.pilImage.resize(icon_size, Image.NEAREST))
        self.tk.call('wm','iconphoto', self._w, self.icon)
        self.drawImage()
        
    def drawImage(self):
        # Draws the image inside the canvas.
        self.tkpi = ImageTk.PhotoImage(self.pilImage.resize(self.dsize))
        if self.imid:
            self.canvas.delete(self.imid)
        self.imid = self.canvas.create_image(max((self.csize[0]-self.dsize[0])/2, 0),
                                             max((self.csize[1]-self.dsize[1])/2, 0),
                                             anchor=tk.NW,
                                             image=self.tkpi)
        self.update()
        
    def saveImage(self):
        # Saves the displayed image in a specified location
        filetypes=[("JPEG", "*.jpg"),("PNG", "*.png"),("all files","*")]
        f_name = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=filetypes)
        if f_name:
            self.pilImage.convert("RGB").save(f_name)

    def close(self, event=None):
        # Closes the window and sets the result.
        self.withdraw()
        self.update_idletasks()
        self.result = (self.low, self.high)
        self.destroy()

# Caller function
def dynamicThreshold(imIn):
    """
    Opens a separate display in which you can dynamically perform a threshold
    operation over image 'imIn'.
    
    Once the close button is pressed, the result of the dynamic threshold is
    returned. This result is a tuple (low, high) used to obtain the image
    displayed using the threshold operation from mamba.
    
    While the window is opened, you can increase or decrease the low level using
    keys Q and W respectively. The high level is modified by the keys S 
    (increasing) and X (decreasing).
    """
    if imIn.getDepth()==1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    mamba.getDisplayer() # To activate Tk root window and hide it
    im = _imageThreshold(imIn.mbIm)
    return im.result
    
################################################################################
# Interactive segment
################################################################################
# This display opens a window in which the image can be segmented interactively
# by the user

class _imageSegment(tk.Toplevel):

    # Constructor ##############################################################
    def __init__(self, imIn, imOut):
        tk.Toplevel.__init__(self, None)
        self.imIn = imIn
        self.imOut = imOut
        self.imWrk = mamba.imageMb(imIn, 8)
        mamba.convert(imIn, self.imWrk)
        self.markers = []
        self.body()
        self.grab_set()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.initial_focus.focus_set()
        
        # Events bindings
        self.canvas.bind("<Motion>", self.mouseMotionEvent)
        self.canvas.bind("<Configure>", self.resizeEvent)
        self.canvas.bind("<Button-4>", self.mouseEvent)
        self.canvas.bind("<Button-5>", self.mouseEvent)
        self.bind("<MouseWheel>", self.mouseEvent)
        self.canvas.bind("<Button-1>", self.mouseEvent)
        self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
        self.bind("<KeyPress>", self.keyboardEvent)
        self.bind("<Control-z>", self.undoEvent)
        
        self.wait_window(self)

    def body(self):
        # Size of the image, canvas and display.
        self.osize = list(self.imIn.getSize())
        imsize = self.osize[:]
        self.zoom = 1.0
        while imsize < [constants._MIN, constants._MIN]:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            self.zoom = self.zoom*2
        while imsize > [constants._MAX, constants._MAX]:
            imsize[0] = imsize[0]/2
            imsize[1] = imsize[1]/2
            self.zoom = self.zoom/2
        
        self.title('interactive segment - %d%%' % (int(self.zoom*100)))
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.imid = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_move = False
        self.palette = ()
        for i in range(254):
            self.palette += (i,i,i)
        self.palette += (0,255,0)
        self.palette += (255,0,0)
        
        # Resize configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Infos
        l = ttk.Label(self, text="Press Ctrl-Z to erase last marker (e to erase all)")
        l.grid(row=0, column=0, columnspan=2)
        
        # Image display
        self.canvas_vb = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_vb.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.canvas_hb = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas_hb.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.canvas = tk.Canvas(self,
                                bd=0,
                                xscrollcommand=self.canvas_hb.set,
                                yscrollcommand=self.canvas_vb.set)
        self.canvas_hb.config(command=self.canvas.xview)
        self.canvas_vb.config(command=self.canvas.yview)
        self.canvas.grid(row=1, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()        
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        # Statusbar
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(1, weight=1)
        statusbar.grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.bclose = ttk.Button(statusbar, text="close", command=self.close)
        self.bclose.grid(row=0, column=0, sticky=tk.W)
        self.infos= tk.StringVar(self)
        lab = ttk.Label(statusbar, anchor=tk.W, textvariable=self.infos)
        lab.grid(row=0, column=2, sticky=tk.E+tk.W)

        self.updateim()
    
    # Events handling functions ################################################
        
    def resizeEvent(self, event):
        # Handles the resizing of the display window.
        self.csize = [event.width, event.height]
        self.drawImage()
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
            
    def undoEvent(self, event):
        # Called when the user press Ctrl-Z
        # Removes the last marker
        if self.markers:
            self.markers = self.markers[:-1]
            self.updateim()
        
    def keyboardEvent(self, event):
        # Handles keyboard events
        
        # Zoom
        if event.char == "z":
            # ZOOM IN
            if self.zoom<=0.25:
                self.setZoom(self.zoom*2)
            else:
                self.setZoom(self.zoom+0.25)
        elif event.char == "a":
            # ZOOM OUT
            if self.zoom<=0.25:
                zoom = self.zoom/2
                if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                    self.setZoom(zoom)
            else:
                self.setZoom(self.zoom-0.25)
                
        # Marker erase
        elif event.char == "e":
            self.markers = []
            self.updateim()
    
    def mouseEvent(self, event):
        # Handles mouse events (except menu pop up)
        # Mainly zoom in or out using the mouse wheel, and moving the image
        if event.type=="4":
            if event.num==1:
                self.canvas.config(cursor="fleur")
            elif event.num==4:
                # Mouse wheel scroll up under linux
                # ZOOM IN
                if self.zoom<=0.25:
                    self.setZoom(self.zoom*2)
                else:
                    self.setZoom(self.zoom+0.25)
            elif event.num==5:
                # Mouse wheel scroll down under linux
                # ZOOM OUT
                if self.zoom<=0.25:
                    zoom = self.zoom/2
                    if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                        self.setZoom(zoom)
                else:
                    self.setZoom(self.zoom-0.25)
            
        elif event.type=="5":
            if event.num==1:
                # Button 1 released
                self.canvas.config(cursor="arrow")
                if not self.mouse_move:
                    x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])/2,0)
                    y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])/2,0)
                    if x<self.dsize[0] and x>=0 and y<self.dsize[1] and y>=0:
                        x = int((float(x)/self.dsize[0])*self.osize[0])
                        y = int((float(y)/self.dsize[1])*self.osize[1])
                        if event.state&0x0004==0x0004 and self.markers:
                            # If the ctrl key is hold the point is added
                            # to the previous one to form a line
                            self.markers[-1] += (x,y)
                        else:
                            self.markers.append((x,y))
                        self.updateim()
                self.mouse_move = False
            
        elif event.type=="38":
            # Mouse wheel under windows
            if event.delta>0:
                # ZOOM IN
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        self.setZoom(self.zoom*2)
                    else:
                        self.setZoom(self.zoom+0.25)
            else:
                # ZOOM OUT
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        zoom = self.zoom/2
                        if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                            self.setZoom(zoom)
                    else:
                        self.setZoom(self.zoom-0.25)
            
    def mouseMotionEvent(self, event):
        # Indicates the position of the mouse inside the image.
        x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])/2,0)
        y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])/2,0)
        
        x = max(min(x,self.dsize[0]-1), 0)
        y = max(min(y,self.dsize[1]-1), 0)
        x = int((float(x)/self.dsize[0])*self.osize[0])
        y = int((float(y)/self.dsize[1])*self.osize[1])
        v1 = self.imIn.getPixel((x, y))
        self.infos.set("At ("+str(x)+","+str(y)+") = ["+str(v1)+"]")
        
        if event.state&0x0100==0x0100:
            self.mouse_move = True
            if not self.dsize[0] <= self.csize[0]:
                dx = event.x-self.mouse_x
                posx = self.canvas_hb.get()[0] - float(dx)/self.dsize[0]
                self.canvas.xview_moveto(posx)
            if not self.dsize[1] <= self.csize[1]:
                dy = event.y-self.mouse_y
                posy = self.canvas_vb.get()[0] - float(dy)/self.dsize[1]
                self.canvas.yview_moveto(posy)
            
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    # Helper functions #########################################################
    
    def setZoom(self, zoom):
        # Sets the zoom value and changes the display accordingly.
        oz = self.zoom
        self.zoom = zoom
        self.dsize[0] = int(self.zoom*self.osize[0])
        self.dsize[1] = int(self.zoom*self.osize[1])
        self.canvas.config(scrollregion=(0,0,self.dsize[0]-1,self.dsize[1]-1))
        self.drawImage()
        self.title('interactive segment - %d%%' % (int(self.zoom*100)))
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
            
    def updateim(self):
        # Updates the display with the new contents of the mamba image.
        self.imOut.reset()
        if self.markers:
            im1 = mamba.imageMb(self.imIn)
            im2 = mamba.imageMb(self.imIn, 8)
            # Putting the markers
            for i,pixel in enumerate(self.markers):
                if len(pixel)==2:
                    self.imOut.setPixel(i+1, pixel)
                else:
                    for pi in range(0,len(pixel)-2,2):
                        mamba.drawLine(self.imOut, pixel[pi:pi+4], i+1)
            # Computing the gradient
            mamba.gradient(self.imIn, im1)
            mamba.watershedSegment(im1, self.imOut)
            mamba.copyBytePlane(self.imOut, 3, self.imWrk)
            mamba.convert(self.imIn, im2)
            mamba.subConst(im2, 2, im2)
            for i,pixel in enumerate(self.markers):
                if len(pixel)==2:
                    im2.setPixel(254, pixel)
                else:
                    for pi in range(0,len(pixel)-2,2):
                        mamba.drawLine(im2, pixel[pi:pi+4], 254)
            mamba.logic(im2, self.imWrk, self.imWrk, "sup")
            self.pilImage = utils.convertToPILFormat(self.imWrk.mbIm)
            self.pilImage.putpalette(self.palette)
        else:
            mamba.convert(self.imIn, self.imWrk)
            self.pilImage = utils.convertToPILFormat(self.imWrk.mbIm)
        m = max(self.osize)
        icon_size = ((constants._icon_max_size*self.osize[0])//m,(constants._icon_max_size*self.osize[1])//m)
        self.icon = ImageTk.PhotoImage(self.pilImage.resize(icon_size, Image.NEAREST))
        self.tk.call('wm','iconphoto', self._w, self.icon)
        self.drawImage()
        
    def drawImage(self):
        # Draws the image inside the canvas.
        self.tkpi = ImageTk.PhotoImage(self.pilImage.resize(self.dsize))
        if self.imid:
            self.canvas.delete(self.imid)
        self.imid = self.canvas.create_image(max((self.csize[0]-self.dsize[0])/2, 0),
                                             max((self.csize[1]-self.dsize[1])/2, 0),
                                             anchor=tk.NW,
                                             image=self.tkpi)
        self.update()

    def close(self, event=None):
        # Closes the window and sets the result.
        self.withdraw()
        self.update_idletasks()
        self.result = self.markers
        self.destroy()

# Caller function
def interactiveSegment(imIn, imOut):
    """
    Opens an interactive display where you can select the marker and perform
    a segmentation using the watershed algorithm on greyscale image 'imIn'.
    
    Once the close button is pressed, the result of the segmentation is
    returned in 32-bit imgae 'imOut'.
    
    Returns the list of markers selected by the user (list of tuple in 
    the (x,y) format).
    """
    if imIn.getDepth()==1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    mamba.getDisplayer() # To activate Tk root window and hide it
    im = _imageSegment(imIn, imOut)
    imOut.update()
    return im.result[:]
    
################################################################################
# Superpose display
################################################################################
# This displays 2 images using imposition techniques

class _imageSuperpose(tk.Toplevel):

    # Constructor ##############################################################
    def __init__(self, Im1, Im2):
        tk.Toplevel.__init__(self, None)
        # im2 is the deepest
        if Im1.getDepth() > Im2.getDepth():
            self.Im1 = Im2
            self.Im2 = Im1
        else:
            self.Im1 = Im1
            self.Im2 = Im2
        self.ImOut = mamba.imageMb(self.Im2, 8)
        self.body()
        self.grab_set()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.initial_focus.focus_set()
        
        # Events bindings
        self.canvas.bind("<Motion>", self.mouseMotionEvent)
        self.canvas.bind("<Configure>", self.resizeEvent)
        self.canvas.bind("<Button-4>", self.mouseEvent)
        self.canvas.bind("<Button-5>", self.mouseEvent)
        self.bind("<MouseWheel>", self.mouseEvent)
        self.canvas.bind("<Button-1>", self.mouseEvent)
        self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
        self.bind("<KeyPress>", self.keyboardEvent)
        for c,l in self.legendCols:
            c.bind("<Button-1>", self.colorChangeEvent)
        self.wait_window(self)

    def body(self):
        # Size of the image, canvas and display
        self.osize = list(self.Im1.getSize())
        imsize = self.osize[:]
        self.zoom = 1.0
        while imsize < [constants._MIN, constants._MIN]:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            self.zoom = self.zoom*2
        while imsize > [constants._MAX, constants._MAX]:
            imsize[0] = imsize[0]/2
            imsize[1] = imsize[1]/2
            self.zoom = self.zoom/2
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.imid = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.currentIm = 0
        
        self.title('superposer - %d%%' % (int(self.zoom*100)))
        
        # Resize configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Superpose infos
        legendF = ttk.Frame(self)
        legendF.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)
        legendF.columnconfigure(1, weight=1)
        self.legendCols = []
        for i in range(3):
            c=tk.Canvas(legendF, height=10, width=10, bd=2, relief=tk.RIDGE)
            c.grid(row=i, column=0)
            l=ttk.Label(legendF, anchor=tk.NW)
            l.grid(row=i, column=1, sticky=tk.W+tk.E)
            self.legendCols.append((c,l))

        # Image display
        self.canvas_vb = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_vb.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.canvas_hb = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas_hb.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.canvas = tk.Canvas(self,
                                bd=0,
                                xscrollcommand=self.canvas_hb.set,
                                yscrollcommand=self.canvas_vb.set)
        self.canvas_hb.config(command=self.canvas.xview)
        self.canvas_vb.config(command=self.canvas.yview)
        self.canvas.grid(row=1, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()        
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        
        # Statusbar
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(1, weight=1)
        statusbar.grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.bclose = ttk.Button(statusbar, text="close", command=self.close)
        self.bclose.grid(row=0, column=0, sticky=tk.W)
        self.bsave = ttk.Button(statusbar, text="save", command=self.saveImage)
        self.bsave.grid(row=0, column=1, sticky=tk.W)
        self.infos= tk.StringVar(self)
        lab = ttk.Label(statusbar, anchor=tk.W, textvariable=self.infos)
        lab.grid(row=0, column=2, sticky=tk.E+tk.W)

        self.updateim()
        
    # Events handling functions ################################################
        
    def resizeEvent(self, event):
        # Handles the resizing of the display window.
        self.csize = [event.width, event.height]
        self.drawImage()
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
        
    def keyboardEvent(self, event):
        # Handles keyboard events.
        
        # Zoom
        if event.keycode==65:
            # change of image
            self.currentIm = 1 - self.currentIm
            self.updateim()
        elif event.char == "z":
            # ZOOM IN
            if self.zoom<=0.25:
                self.setZoom(self.zoom*2)
            else:
                self.setZoom(self.zoom+0.25)
        elif event.char == "a":
            # ZOOM OUT
            if self.zoom<=0.25:
                zoom = self.zoom/2
                if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                    self.setZoom(zoom)
            else:
                self.setZoom(self.zoom-0.25)
    
    def mouseEvent(self, event):
        # Handles mouse events (except menu pop up)
        # Mainly zoom in or out using the mouse wheel, and moving the image
        if event.type=="4":
            if event.num==1:
                self.canvas.config(cursor="fleur")
            elif event.num==4:
                # Mouse wheel scroll up under Linux
                # ZOOM IN
                if self.zoom<=0.25:
                    self.setZoom(self.zoom*2)
                else:
                    self.setZoom(self.zoom+0.25)
            elif event.num==5:
                # Mouse wheel scroll down under Linux
                # ZOOM OUT
                if self.zoom<=0.25:
                    zoom = self.zoom/2
                    if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                        self.setZoom(zoom)
                else:
                    self.setZoom(self.zoom-0.25)
            
        elif event.type=="5":
            if event.num==1:
                # Button 1 released
                self.canvas.config(cursor="arrow")
            
        elif event.type=="38":
            # Mouse wheel under Windows
            if event.delta>0:
                # ZOOM IN
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        self.setZoom(self.zoom*2)
                    else:
                        self.setZoom(self.zoom+0.25)
            else:
                # ZOOM OUT
                for i in range(abs(event.delta)/120):
                    if self.zoom<=0.25:
                        zoom = self.zoom/2
                        if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                            self.setZoom(zoom)
                    else:
                        self.setZoom(self.zoom-0.25)
            
    def mouseMotionEvent(self, event):
        # Indicates the mouse position inside the image.
        x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])/2,0)
        y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])/2,0)
        
        x = max(min(x,self.dsize[0]-1), 0)
        y = max(min(y,self.dsize[1]-1), 0)
        x = int((float(x)/self.dsize[0])*self.osize[0])
        y = int((float(y)/self.dsize[1])*self.osize[1])
        v1 = self.Im1.getPixel((x, y))
        v2 = self.Im2.getPixel((x, y))
        self.infos.set("At ("+str(x)+","+str(y)+") = ["+str(v1)+","+str(v2)+"]")
        
        if event.state&0x0100==0x0100 :
            if not self.dsize[0] <= self.csize[0]:
                dx = event.x-self.mouse_x
                posx = self.canvas_hb.get()[0] - float(dx)/self.dsize[0]
                self.canvas.xview_moveto(posx)
            if not self.dsize[1] <= self.csize[1]:
                dy = event.y-self.mouse_y
                posy = self.canvas_vb.get()[0] - float(dy)/self.dsize[1]
                self.canvas.yview_moveto(posy)
            
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def colorChangeEvent(self, event):
        # Color change in the legend
        (c, l) = colorchooser.askcolor(event.widget.cget("bg"))
        if c==None:
            return
        # Ugly patch to correct a bug in tkinter askcolor with Python 3
        new_color = ((int(c[0]), int(c[1]), int(c[2])), l)
        if self.Im1.getDepth()==1 and self.Im2.getDepth()==1:
            event.widget.config(bg=new_color[1])
            event.widget.color_tuple = new_color[0]
            palette = (0,0,0)
            for c,l in self.legendCols:
                palette = palette + c.color_tuple
            palette = palette+252*(0,0,0)
        elif self.Im1.getDepth()==1:
            palette = (0,0,0)
            for i in range(1,255):
                palette = palette+(i,i,i)
            palette = palette+new_color[0]
            event.widget.config(bg=new_color[1])
        else:
            return
        
        self.pilImage.putpalette(palette)
        m = max(self.osize)
        icon_size = ((constants._icon_max_size*self.osize[0])//m,(constants._icon_max_size*self.osize[1])//m)
        self.icon = ImageTk.PhotoImage(self.pilImage.resize(icon_size, Image.NEAREST))
        self.tk.call('wm','iconphoto', self._w, self.icon)
        self.drawImage()
        
    # Helper functions #########################################################
    
    def setZoom(self, zoom):
        # Sets the zoom value and changes the display accordingly.
        oz = self.zoom
        self.zoom = zoom
        self.dsize[0] = int(self.zoom*self.osize[0])
        self.dsize[1] = int(self.zoom*self.osize[1])
        self.canvas.config(scrollregion=(0,0,self.dsize[0]-1,self.dsize[1]-1))
        self.drawImage()
        self.title('superposer - %d%%' % (int(self.zoom*100)))
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
            
    def updateim(self):
        # Updates the display with the new contents of the mamba image.
        if self.Im1.getDepth()==1 and self.Im2.getDepth()==1:
            # both images are binary
            self.ImOut.reset()
            mamba.copyBitPlane(self.Im2, 0, self.ImOut)
            mamba.copyBitPlane(self.Im1, 1, self.ImOut)
            palette = (0,0,0, 255,0,0, 0,255,0, 0,0,255)+252*(0,0,0)
            colors = ["#ff0000","#00ff00","#0000ff"]
            texts = ["in image 2 only ("+self.Im2.getName()+")",
                     "in image 1 only ("+self.Im1.getName()+")",
                     "in both images ("+self.Im1.getName()+" and "+self.Im2.getName()+")"]
            for i in range(3):
                self.legendCols[i][0].config(bg=colors[i])
                self.legendCols[i][0].color_tuple = palette[i*3+3:i*3+6]
                self.legendCols[i][1].config(text=texts[i])
                
        elif self.Im1.getDepth()==1:
            # image 1 is binary, 2 is not
            prov = mamba.imageMb(self.ImOut)
            mamba.convert(self.Im1, self.ImOut)
            mamba.convert(self.Im2, prov)
            mamba.subConst(prov, 1, prov)
            mamba.logic(self.ImOut, prov, self.ImOut, "sup")
            palette = (0,0,0)
            for i in range(1,255):
                palette = palette+(i,i,i)
            palette = palette+(255,0,255)
            self.legendCols[0][0].config(bg="#808080")
            self.legendCols[0][1].config(text="image ("+self.Im2.getName()+")")
            self.legendCols[1][0].config(bg="#ff00ff")
            self.legendCols[1][1].config(text="binary image ("+self.Im1.getName()+")")
            self.legendCols[2][0].grid_remove()
            self.legendCols[2][1].grid_remove()
            
        else:
            # Neither image is binary
            if self.currentIm==0:
                endimage = self.Im2
                self.legendCols[0][1].config(text="displayed : "+self.Im2.getName())
                self.legendCols[1][1].config(text="press space to display "+self.Im1.getName())
            else:
                endimage = self.Im1
                self.legendCols[0][1].config(text="displayed : "+self.Im1.getName())
                self.legendCols[1][1].config(text="press space to display "+self.Im2.getName())
            mamba.convert(endimage, self.ImOut)
            palette = None
            self.legendCols[0][0].config(bg="#808080")
            self.legendCols[1][0].config(bg="#808080")
            self.legendCols[2][0].grid_remove()
            self.legendCols[2][1].grid_remove()
                    
        self.pilImage = utils.convertToPILFormat(self.ImOut.mbIm)
        if palette:
            self.pilImage.putpalette(palette)
        m = max(self.osize)
        icon_size = ((constants._icon_max_size*self.osize[0])//m,(constants._icon_max_size*self.osize[1])//m)
        self.icon = ImageTk.PhotoImage(self.pilImage.resize(icon_size, Image.NEAREST))
        self.tk.call('wm','iconphoto', self._w, self.icon)
        self.drawImage()
        
    def drawImage(self):
        # Draws the image inside the canvas.
        self.tkpi = ImageTk.PhotoImage(self.pilImage.resize(self.dsize))
        if self.imid:
            self.canvas.delete(self.imid)
        self.imid = self.canvas.create_image(max((self.csize[0]-self.dsize[0])/2, 0),
                                             max((self.csize[1]-self.dsize[1])/2, 0),
                                             anchor=tk.NW,
                                             image=self.tkpi)
        self.update()
        
    def saveImage(self):
        # Saves the displayed image in a specified location
        filetypes=[("JPEG", "*.jpg"),("PNG", "*.png"),("all files","*")]
        f_name = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=filetypes)
        if f_name:
            self.pilImage.convert("RGB").save(f_name)

    def close(self, event=None):
        # Closes the window and set the result.
        self.withdraw()
        self.update_idletasks()
        self.destroy()

# Caller function
def superpose(imIn1, imIn2):
    """
    Draws images 'imIn1' and 'imIn2' in a common display.
    
    If both images are binary, the display is a combination of their pixel values,
    i.e. black where the pixel is black in both images, blue (default color) if 
    the pixel is set in both images, green (default color) if the pixel is set 
    only in 'imIn1' and red (default color) if it is only set in 'imIn2'.
    
    If one image is greyscale and the other is binary, the binary image is
    redrawn over the greyscale image in purple (default color).
    
    Image superposition is not possible if both images are greyscale.
    
    The default colors can be changed while displaying by clicking the corresponding
    color box in the caption above the display window. A color palette will appear
    where a new color can be selected.
    
    """
    if imIn1.getSize()!=imIn2.getSize():
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    mamba.getDisplayer() # To activate Tk root window and hide it
    im = _imageSuperpose(imIn1, imIn2)

################################################################################
# Hit-or-Miss pattern selector
################################################################################
# Helps the user to create patterns for the Hit-or-Miss operator.

class _hitormissPatternSelector(tk.Toplevel):
    _BL = 35
    _DEC = 5
    textStatus = ["Undef", "True", "False"]
    
    def __init__(self, grid):
        tk.Toplevel.__init__(self, None)
        self.title('pattern selector')
        self.resizable(False, False)
        self.grid = grid
        self.gridStatus = 9*[0]
        self.body()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.validate)
        self.initial_focus.focus_set()
        self.canvas.bind("<Button-1>", self.mouseButtonEvent)
        self.wait_window(self)

    def body(self):
        # Resize configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Image display
        self.canvas = tk.Canvas(self,bd=0)
        self.canvas.grid(row=1, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
        self.canvas.config(width=6*self._BL+2*self._DEC,
                           height=7*self._BL+2*self._DEC,
                           scrollregion=(0,0,6*self._BL+2*self._DEC,7*self._BL+2*self._DEC),
                           bg="white")
        self.drawGrid()
        
        # Statusbar
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(1, weight=1)
        statusbar.grid(row=2, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.bclose = ttk.Button(statusbar, text="validate", command=self.validate)
        self.bclose.grid(row=0, column=0, sticky=tk.W)
        
    def drawGrid(self):
        if self.grid==mamba.HEXAGONAL:
            self.drawHexagon("0", self.gridStatus[0], 2*self._BL,2*self._BL)      #0
            self.drawHexagon("1", self.gridStatus[1], 3*self._BL,0)               #1
            self.drawHexagon("2", self.gridStatus[2], 4*self._BL,2*self._BL)      #2
            self.drawHexagon("3", self.gridStatus[3], 3*self._BL,4*self._BL)      #3
            self.drawHexagon("4", self.gridStatus[4], self._BL,4*self._BL)        #4
            self.drawHexagon("5", self.gridStatus[5], 0,2*self._BL)               #5
            self.drawHexagon("6", self.gridStatus[6], self._BL,0)                 #6
        else:
            self.drawSquare("0", self.gridStatus[0], 2*self._BL,2*self._BL)       #0
            self.drawSquare("1", self.gridStatus[1], 2*self._BL,0)                #1
            self.drawSquare("2", self.gridStatus[2], 4*self._BL,0)                #2
            self.drawSquare("3", self.gridStatus[3], 4*self._BL,2*self._BL)       #3
            self.drawSquare("4", self.gridStatus[4], 4*self._BL,4*self._BL)       #4
            self.drawSquare("5", self.gridStatus[5], 2*self._BL,4*self._BL)       #5
            self.drawSquare("6", self.gridStatus[6], 0,4*self._BL)                #6
            self.drawSquare("7", self.gridStatus[7], 0,2*self._BL)                #7
            self.drawSquare("8", self.gridStatus[8], 0,0)                         #8
        
    def drawSquare(self,text,status,x,y):
        x=x+self._DEC
        y=y+self._DEC
        if status==1:
            color = "#80b080"
        elif status==2:
            color = "#b08080"
        else:
            color = ""
        self.canvas.create_rectangle(x,y,
                                     x+2*self._BL,y+2*self._BL,
                                     outline="black",
                                     width=2,
                                     fill=color)
        self.canvas.create_text (x+self._BL,y+self._BL, text=text)
        self.canvas.create_text (x+self._BL,y+1.5*self._BL, text=self.textStatus[status])
        
    def drawHexagon(self,text,status,x,y):
        x=x+self._DEC
        y=y+self._DEC
        if status==1:
            color = "#80b080"
        elif status==2:
            color = "#b08080"
        else:
            color = ""
        self.canvas.create_polygon(x,y+self._BL,
                                   x+self._BL,y,
                                   x+2*self._BL,y+self._BL,
                                   x+2*self._BL,y+2*self._BL,
                                   x+self._BL,y+3*self._BL,
                                   x,y+2*self._BL,
                                   outline="black",
                                   width=2,
                                   fill=color)
        self.canvas.create_text (x+self._BL,y+1.5*self._BL, text=text)
        self.canvas.create_text (x+self._BL,y+2*self._BL, text=self.textStatus[status])
        
    def updateGridStatusHexagonal(self,x,y):
        if x>self._BL and x<3*self._BL and y>abs(x-2*self._BL) and y<(3*self._BL-abs(x-2*self._BL)):
            self.gridStatus[6] = (self.gridStatus[6]+1)%3;
        elif x>3*self._BL and x<5*self._BL and y>abs(x-4*self._BL) and y<(3*self._BL-abs(x-4*self._BL)):
            self.gridStatus[1] = (self.gridStatus[1]+1)%3;
        elif x>0 and x<2*self._BL and y>2*self._BL+abs(x-self._BL) and y<(5*self._BL-abs(x-self._BL)):
            self.gridStatus[5] = (self.gridStatus[5]+1)%3;
        elif x>2*self._BL and x<4*self._BL and y>2*self._BL+abs(x-3*self._BL) and y<(5*self._BL-abs(x-3*self._BL)):
            self.gridStatus[0] = (self.gridStatus[0]+1)%3;
        elif x>4*self._BL and x<6*self._BL and y>2*self._BL+abs(x-5*self._BL) and y<(5*self._BL-abs(x-5*self._BL)):
            self.gridStatus[2] = (self.gridStatus[2]+1)%3;
        elif x>self._BL and x<3*self._BL and y>4*self._BL+abs(x-2*self._BL) and y<(7*self._BL-abs(x-2*self._BL)):
            self.gridStatus[4] = (self.gridStatus[4]+1)%3;
        elif x>3*self._BL and x<5*self._BL and y>4*self._BL+abs(x-4*self._BL) and y<(7*self._BL-abs(x-4*self._BL)):
            self.gridStatus[3] = (self.gridStatus[3]+1)%3;
        
    def updateGridStatusSquare(self,x,y):
        if x>0 and x<2*self._BL and y>0 and y<2*self._BL:
            self.gridStatus[8] = (self.gridStatus[8]+1)%3;
        elif x>2*self._BL and x<4*self._BL and y>0 and y<2*self._BL:
            self.gridStatus[1] = (self.gridStatus[1]+1)%3;
        elif x>4*self._BL and x<6*self._BL and y>0 and y<2*self._BL:
            self.gridStatus[2] = (self.gridStatus[2]+1)%3;
        elif x>0 and x<2*self._BL and y>2*self._BL and y<4*self._BL:
            self.gridStatus[7] = (self.gridStatus[7]+1)%3;
        elif x>2*self._BL and x<4*self._BL and y>2*self._BL and y<4*self._BL:
            self.gridStatus[0] = (self.gridStatus[0]+1)%3;
        elif x>4*self._BL and x<6*self._BL and y>2*self._BL and y<4*self._BL:
            self.gridStatus[3] = (self.gridStatus[3]+1)%3;
        elif x>0 and x<2*self._BL and y>4*self._BL and y<6*self._BL:
            self.gridStatus[6] = (self.gridStatus[6]+1)%3;
        elif x>2*self._BL and x<4*self._BL and y>4*self._BL and y<6*self._BL:
            self.gridStatus[5] = (self.gridStatus[5]+1)%3;
        elif x>4*self._BL and x<6*self._BL and y>4*self._BL and y<6*self._BL:
            self.gridStatus[4] = (self.gridStatus[4]+1)%3;
    
    def mouseButtonEvent(self, event):
        # Indicates the position of the mouse inside the image.
        x = self.canvas.canvasx(event.x)-self._DEC
        y = self.canvas.canvasy(event.y)-self._DEC
        if self.grid==mamba.HEXAGONAL:
            self.updateGridStatusHexagonal(x,y)
        else:
            self.updateGridStatusSquare(x,y)
        for id in self.canvas.find_all():
            self.canvas.delete(id)
        self.drawGrid()
        
    def validate(self, event=None):
        # Closes the window and sets the result.
        self.withdraw()
        self.update_idletasks()
        self.es0 = []
        self.es1 = []
        for i, gs in enumerate(self.gridStatus):
            if gs==1:
                self.es1.append(i)
            elif gs==2:
                self.es0.append(i)
        self.destroy()
        
# Caller function
def hitormissPatternSelector(grid=mamba.DEFAULT_GRID):
    """
    Helps the user to create patterns for the Hit-or-Miss operator defined in 
    the Mamba module.
    
    The function returns a double structuring elements 'es0' and 'es1'
    (in that order) used as entry in the hitOrMiss function. 
    
    You can select the desired grid for the pattern selector. If not specified,
    the function will use the grid currently in use.
    
    Example with the hitOrMiss function :
        hitOrMiss(imIn, imOut, hitormissPatternSelector())
    
    """
    mamba.getDisplayer() # To activate Tk root window and hide it
    ps = _hitormissPatternSelector(grid)
    return mamba.doubleStructuringElement(ps.es0, ps.es1, grid)

