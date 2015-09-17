"""
This module defines a 2D data displayer for mamba.
"""

from . import constants
from . import palette
from . import popup

import mamba
import mamba.utils as utils
from mamba.error import *

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog
except ImportError:
    try:
        import Tkinter as tk
        import ttk
        import tkFileDialog as filedialog
    except ImportError:
        print("Missing Tkinter library")
        raise

from PIL import ImageTk
from PIL import Image

###############################################################################
#  Utilities functions

def _copyFromClipboard(size=None):
    """
    Looks into the clipboard to see if an image is present and extract it if 
    this is the case.
    
    This function works only on Windows.
    
    Returns a mamba image or None if no image was found.
    """
    import platform
        
    im = None

    if platform.system()=='Windows':
        # Under Windows
        from PIL import ImageGrab
        # The image is extracted from the clipboard.
        # !! There is a bug in PIL 1.1.6 with the clipboard:
        # !! it is not closed if there is no image in it
        # !! and thus this can have very bad effects on Windows
        # !! copy/paste operations.
        im_clipbd = ImageGrab.grabclipboard()
        if im_clipbd!=None:
            im = utils.loadFromPILFormat(im_clipbd, size=size)
    
    return im

###############################################################################
#  Classes
#
# This class is used to create windows for 2D image display.
# The class inherits Tkinter.Toplevel to do so.
# Functions are offered to update, retitle, show or hide the display.
class Display2D(tk.Toplevel):

    # Constructor ##############################################################
    def __init__(self, master):
    
        # Window creation
        tk.Toplevel.__init__(self,master)
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.popup = popup.Popup(self)
        self.popup.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.popup.grid_remove()
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
        self.createInfoBar()
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()
        
        # Internal variables
        self.im_ref = None
        self.bplane = 4
        self.frozen = False
        self.imid = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.std_geometry = ""
        self.palname = ""
        
        # Context menu
        self.createContextMenu()
        
        # Events bindings
        self.canvas.bind("<Motion>", self.mouseMotionEvent)
        self.canvas.bind("<Configure>", self.resizeEvent)
        self.canvas.bind("<Button-3>", self.contextMenuEvent)
        self.canvas.bind("<Button-4>", self.mouseEvent)
        self.canvas.bind("<Button-5>", self.mouseEvent)
        self.bind("<MouseWheel>", self.mouseEvent)
        self.canvas.bind("<Button-1>", self.mouseEvent)
        self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
        self.bind("<KeyPress>", self.keyboardEvent)
        self.bind("<Control-v>", self.copyEvent)
        self.bind("<Control-f>", self.freezeEvent)
        self.bind("<Control-r>", self.restoreEvent)
        self.bind("<FocusIn>", self.focusEvent)
        
        # Upon creation, the image is automatically withdrawn.
        self.withdraw()
        
    # Sub-creation functions ###################################################
        
    def createContextMenu(self):
        # Creates the contextual menu.
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="save as..", command=self.saveImage)
        self.context_menu.add_command(label="load", command=self.loadImage)
        self.context_menu.add_command(label="paste..", 
                                      command=self.pasteFromClipBoard,
                                      state=tk.DISABLED)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="100%", command=self.resetZoom)
        self.context_menu.add_command(label="200%", command=self.doubleZoom)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="")
        
    def createInfoBar(self):
        # Creates the info status bar.
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(0, weight=1)
        statusbar.columnconfigure(1, weight=1)
        statusbar.grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.infos = []
        for i in range(3):
            v = tk.StringVar(self)
            ttk.Label(statusbar, anchor=tk.W, textvariable=v).grid(row=0, column=i, sticky=tk.E+tk.W)
            self.infos.append(v)
    
    # Events handling functions ################################################
    
    def focusEvent(self, event):
        # The window is activated.
        self.updateim()
        
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
        
    def mouseMotionEvent(self, event):
        # Indicates the position of the mouse inside the image.
        # Displays in the info bar the position inside the image along with the
        # pixel value.
        x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])//2,0)
        y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])//2,0)
        x = max(min(x,self.dsize[0]-1), 0)
        y = max(min(y,self.dsize[1]-1), 0)
        x = int((float(x)/self.dsize[0])*self.osize[0])
        y = int((float(y)/self.dsize[1])*self.osize[1])
        v = str(self.im_ref().getPixel((x,y)))
        self.infos[2].set("At ("+str(x)+","+str(y)+") = "+v)
        
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
    
    def mouseEvent(self, event):
        # Handles mouse events (except menu pop up)
        # Mainly zoom in or out using the mouse wheel, and moving the image
        if event.type=="4":
            if event.num==1:
                self.canvas.config(cursor="fleur")
            elif event.num==4:
                # Mouse wheel scroll up under linux
                self.increaseZoom()
            elif event.num==5:
                # Mouse wheel scroll down under linux
                self.decreaseZoom()
            
        elif event.type=="5":
            if event.num==1:
                # Button 1 released
                self.canvas.config(cursor="arrow")
            
        elif event.type=="38":
            # Mouse wheel under windows
            if event.delta>0:
                for i in range(abs(event.delta)//120):
                    self.increaseZoom()
            else:
                for i in range(abs(event.delta)//120):
                    self.decreaseZoom()

    def keyboardEvent(self, event):
        # Handles keyboard events
        
        if event.char == "z":
            # ZOOM IN
            self.increaseZoom()
        elif event.char == "a":
            # ZOOM OUT
            self.decreaseZoom()
        elif event.char == "b":
            # BYTE PLANE MODIFICATION (next)
            self.bplane = (self.bplane+1)%5
            self.updateim()
        elif event.char == "n":
            # BYTE PLANE MODIFICATION (previous)
            self.bplane = (self.bplane-1)%5
            self.updateim()
        elif event.char == "p":
            # PALETTE ACTIVATION
            names = [""] + palette.listPalettes()
            try:
                i = names.index(self.palname)
            except:
                i = 0
            i = (i+1)%len(names)
            self.palname = names[i]
            if self.palname:
                self.popup.info("palette set to "+self.palname)
            else:
                self.popup.info("No palette set")
            self.updateim()

    def freezeEvent(self, event):
        # Freeze/Unfreeze event
        if self.frozen:
            self.unfreeze()
        else:
            self.freeze()
    
    def restoreEvent(self, event):
        # Restores original size event
        # The window size and parameter are reset.
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()
        imsize = self.osize[:]
        self.zoom = 1.0
        while imsize[0]<constants._MIN or imsize[1]<constants._MIN:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            self.zoom = self.zoom*2
        while imsize[0]>constants._MAX or imsize[1]>constants._MAX:
            imsize[0] = imsize[0]/2
            imsize[1] = imsize[1]/2
            self.zoom = self.zoom/2
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        self.updateim()
        # Restoring the standard geometry.
        self.geometry(self.std_geometry)
    
    def copyEvent(self, event):
        # Handles copy shortcut event.
        # If an image is present into the clipboard we get it. 
        self._im_to_paste = _copyFromClipboard(size=self.osize)
        if self._im_to_paste:
            self.pasteFromClipBoard()
    
    def contextMenuEvent(self, event):
        # Draws a contextual menu on a mouse right click.
        # If an image is present into the clipboard,
        # we get it. 
        self._im_to_paste = _copyFromClipboard(size=self.osize)
        
        # If an image was retrieved from the clipboard, the paste menu is enabled.
        if self._im_to_paste:
            self.context_menu.entryconfigure(2, state=tk.ACTIVE)
        else:
            self.context_menu.entryconfigure (2, state=tk.DISABLED)
        
        self.context_menu.post(event.x_root, event.y_root)
        
    # Contextual Menu functions ################################################
    def increaseZoom(self):
        # ZOOM IN
        if self.zoom<=0.25:
            self.setZoom(self.zoom*2)
        else:
            self.setZoom(self.zoom+0.25)
    def decreaseZoom(self):
        # ZOOM OUT
        if self.zoom<=0.25:
            zoom = self.zoom/2
            if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                self.setZoom(zoom)
            else:
                self.popup.warn("Cannot zoom out limit reached")
        else:
            self.setZoom(self.zoom-0.25)
    def resetZoom(self):
        self.setZoom(1.0)
    def doubleZoom(self):
        self.setZoom(2.0)
    def loadImage(self):
        # Loads the image from the selected file.
        # The name associated with the image will not be changed.
        try:
            f_name = filedialog.askopenfilename()
            if f_name:
                self.im_ref().load(f_name)
        except Exception as err:
            self.popup.err("Error while opening file : %s" % (str(err)))
    def saveImage(self):
        # Saves the image into the selected file.
        filetypes=[("JPEG", "*.jpg"),("PNG", "*.png"),("TIFF", "*.tif"),("BMP", "*.bmp"),("all files","*")]
        f_name = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=filetypes)
        if f_name:
            self.im_ref().save(f_name)
    def pasteFromClipBoard(self):
        # Pastes the image obtained in the clipboard.
        err = core.MB_Convert(self._im_to_paste, self.im_ref().mbIm)
        raiseExceptionOnError(err)
        self.updateim()
        del(self._im_to_paste)
        self._im_to_paste = None
        
    # Helper functions #########################################################
    
    def setZoom(self, zoom):
        # Sets the zoom value and changes the display accordingly.
        oz = self.zoom
        self.zoom = zoom
        self.dsize[0] = int(self.zoom*self.osize[0])
        self.dsize[1] = int(self.zoom*self.osize[1])
        self.canvas.config(scrollregion=(0,0,self.dsize[0]-1,self.dsize[1]-1))
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
        
    def drawImage(self):
        self.title((self.frozen and "Frozen - " or "") +
                   self.im_ref().getName() +
                   " - " + str(self.im_ref().getDepth()) +
                   " - [" + str(int(self.zoom*100)) + "%]")
        # Draws the image inside the canvas.
        self.tkpi = ImageTk.PhotoImage(self.pilImage.resize(self.dsize, Image.NEAREST))
        if self.imid:
            self.canvas.delete(self.imid)
        self.imid = self.canvas.create_image(max((self.csize[0]-self.dsize[0])//2, 0),
                                             max((self.csize[1]-self.dsize[1])//2, 0),
                                             anchor=tk.NW,
                                             image=self.tkpi)
        
    # Public interface functions ###############################################
    
    def freeze(self):
        # Freezes the display so that update has no effect
        self.frozen = True
        self.title((self.frozen and "Frozen - " or "") + 
                   self.im_ref().getName() +
                   " - " + str(self.im_ref().getDepth()) +
                   " - [" + str(int(self.zoom*100)) + "%]")
    
    def unfreeze(self):
        # Unfreezes the display
        self.frozen = False
        self.updateim()
        
    def updateim(self):
        # Updates the display with the new contents of the mamba image.
        if self.im_ref() and self.state()=="normal" and not self.frozen:
            if self.im_ref().getDepth()==32:
                im = mamba.imageMb(self.im_ref(), 8)
                if self.bplane==4:
                    mamba.convert(self.im_ref(), im)
                    self.infos[1].set("plane : all")
                else:
                    mamba.copyBytePlane(self.im_ref(),self.bplane,im)
                    self.infos[1].set("plane : %d" % (self.bplane))
                self.pilImage = utils.convertToPILFormat(im.mbIm)
            else:
                self.infos[1].set("")
                self.pilImage = utils.convertToPILFormat(self.im_ref().mbIm)
            if self.palname:
                self.pilImage.putpalette(palette.getPalette(self.palname))
            volume = mamba.computeVolume(self.im_ref())
            self.infos[0].set("volume : "+str(volume))
            self.icon = ImageTk.PhotoImage(self.pilImage.resize(self.icon_size, Image.NEAREST))
            self.tk.call('wm','iconphoto', self._w, self.icon)
            self.drawImage()
        
    def connect(self, im_ref):
        # "Connects" the window to a mamba image.
        self.im_ref = im_ref
        
        # Size of the image, canvas and display
        self.osize = list(self.im_ref().getSize())
        imsize = self.osize[:]
        self.zoom = 1.0
        while imsize[0]<constants._MIN or imsize[1]<constants._MIN:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            self.zoom = self.zoom*2
        while imsize[0]>constants._MAX or imsize[1]>constants._MAX:
            imsize[0] = imsize[0]/2
            imsize[1] = imsize[1]/2
            self.zoom = self.zoom/2
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        
        # PIL/PILLOW image and icon
        m = max(self.osize)
        self.icon_size = ((constants._icon_max_size*self.osize[0])//m,(constants._icon_max_size*self.osize[1])//m)
        
        # Adding size info to menu.
        size_info = str(self.osize[0]) + " x " + str(self.osize[1])
        self.context_menu.entryconfigure(8, label=size_info)
        
        self.updateim()
    
    def show(self, **options):
        # Shows the display (enabling update).
        if self.state()!="normal":
            self.deiconify()
            self.updateim()
        if "palette" in options:
            self.palname = options["palette"]
            if self.palname:
                self.popup.info("palette set to "+self.palname)
            else:
                self.popup.info("No palette set")
            self.updateim()
        if "plane" in options:
            self.bplane = options["plane"]
            self.updateim()
        if "zoom" in options:
            self.setZoom(options["zoom"])
        if "at" in options:
            x,y = options["at"]
            posx = float(x)/self.osize[0]
            self.canvas.xview_moveto(posx)
            posy = float(y)/self.osize[0]
            self.canvas.yview_moveto(posy)
            
    def hide(self):
        # Hides the display.
        self.withdraw()

