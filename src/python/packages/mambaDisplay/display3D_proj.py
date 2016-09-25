"""
Projection display for 3D images.
"""

# Contributors : Nicolas BEUCHER

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

import time
from PIL import Image
from PIL import ImageTk

from . import constants
from . import palette

# Mamba imports
import mamba3D as m3D
import mamba

################################################################################
# Projection display

class planeFrame(ttk.LabelFrame):

    def __init__(self,root,size,name,zoom):
        ttk.LabelFrame.__init__(self,root,text=name,labelanchor=tk.NW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.root = root
        self.canvas_vb = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_vb.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas_hb = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas_hb.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.canvas = tk.Canvas(self,
                                bd=0,
                                takefocus=True,
                                xscrollcommand=self.canvas_hb.set,
                                yscrollcommand=self.canvas_vb.set)
        self.canvas_hb.config(command=self.canvas.xview)
        self.canvas_vb.config(command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
        self.canvas_hb.grid_remove()
        self.canvas_vb.grid_remove()
        self.osize = size[:]
        imsize = self.osize[:]
        self.zoom = zoom
        imsize[0] = int(imsize[0]*zoom)
        imsize[1] = int(imsize[1]*zoom)
        self.csize = imsize[:]
        self.dsize = imsize[:]
        self.canvas.config(width=imsize[0],height=imsize[1],
                           scrollregion=(0,0,imsize[0]-1,imsize[1]-1))
        self.config(text=name+" - [" + str(int(self.zoom*100)) + "%]")
        
        # Internal variables
        self.name = name
        self.imid = None
        self.targetid = []
        self.pilImage = None
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Events bindings
        self.canvas.bind("<Motion>", self.mouseMotionEvent)
        self.canvas.bind("<Configure>", self.resizeEvent)
        self.canvas.bind("<Button-4>", self.mouseEvent)
        self.canvas.bind("<Button-5>", self.mouseEvent)
        self.canvas.bind("<MouseWheel>", self.mouseEvent)
        self.canvas.bind("<Button-1>", self.mouseEvent)
        self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
        self.canvas.bind("<KeyPress>", self.keypressEvent)

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
        
    def mouseMotionEvent(self, event):
        # Indicates the position of the mouse inside the image.
        # Displays in the info bar the position inside the image along with the
        # pixel value.
        x = self.canvas.canvasx(event.x) - max((self.csize[0]-self.dsize[0])//2,0)
        y = self.canvas.canvasy(event.y) - max((self.csize[1]-self.dsize[1])//2,0)
        x = max(min(x,self.dsize[0]-1), 0)
        y = max(min(y,self.dsize[1]-1), 0)
        x = int((x*self.osize[0])//self.dsize[0])
        y = int((y*self.osize[1])//self.dsize[1])
        
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
        self.root.movingEvent(x,y,self.name,event.state)

    def keypressEvent(self, event):
        if event.char=="z":
            # ZOOM IN
            if self.zoom<=0.25:
                self.setZoom(self.zoom*2)
            else:
                self.setZoom(self.zoom+0.25)
        elif event.char=="a":
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
            
        elif event.type=="38":
            # Mouse wheel under windows
            if event.delta>0:
                # ZOOM IN
                for i in range(abs(event.delta)//120):
                    if self.zoom<=0.25:
                        self.setZoom(self.zoom*2)
                    else:
                        self.setZoom(self.zoom+0.25)
            else:
                # ZOOM OUT
                for i in range(abs(event.delta)//120):
                    if self.zoom<=0.25:
                        zoom = self.zoom/2
                        if not (int(self.zoom*self.osize[0])<10 or int(self.zoom*self.osize[0])<10):
                            self.setZoom(zoom)
                    else:
                        self.setZoom(self.zoom-0.25)
        
    # Helper functions #########################################################
    
    def setZoom(self, zoom):
        # Sets the zoom value and changes the display accordingly.
        oz = self.zoom
        self.zoom = zoom
        self.dsize[0] = int(self.zoom*self.osize[0])
        self.dsize[1] = int(self.zoom*self.osize[1])
        self.canvas.config(scrollregion=(0,0,self.dsize[0]-1,self.dsize[1]-1))
        self.drawImage()
        self.config(text=self.name+" - [" + str(int(self.zoom*100)) + "%]")
        
        # For a zoom of only one, the scrollbar is removed.
        if self.dsize[0] <= self.csize[0]:
            self.canvas_hb.grid_remove()
        else:
            self.canvas_hb.grid()
        if self.dsize[1] <= self.csize[1]:
            self.canvas_vb.grid_remove()
        else:
            self.canvas_vb.grid()
    def getZoom(self):
        # Returns the value of zoom
        return self.zoom
            
    def drawImage(self):
        # Draws the image inside the canvas.
        if self.pilImage:
            self.tkpi = ImageTk.PhotoImage(self.pilImage.resize(self.dsize, Image.NEAREST))
            if self.imid:
                self.canvas.delete(self.imid)
            self.imid = self.canvas.create_image(max((self.csize[0]-self.dsize[0])//2, 0),
                                                 max((self.csize[1]-self.dsize[1])//2, 0),
                                                 anchor=tk.NW,
                                                 image=self.tkpi)
        
    # Public interface functions ###############################################

    def display(self, im):
        # "Connects" the window to a mamba image.
        self.pilImage = im
        self.drawImage()
        
    def drawTarget(self, x, y):
        # Draws the target when the user moves the mouse while hold ctrl
        self.eraseTarget()
        esize = max(self.csize, self.dsize)
        x = (x*self.dsize[0])//self.osize[0] + max((self.csize[0]-self.dsize[0])//2,0)
        y = (y*self.dsize[1])//self.osize[1] + max((self.csize[1]-self.dsize[1])//2,0)
        id = self.canvas.create_line(x,0,x,esize[1]-1,fill="red")
        self.targetid.append(id)
        id = self.canvas.create_line(0,y,esize[0]-1,y,fill="red")
        self.targetid.append(id)
        
    def eraseTarget(self):
        # Erases the target upon releasing the ctrl button
        for id in self.targetid:
            self.canvas.delete(id)
        self.targetid = []

class Display3D_Proj(tk.Frame):
    
    # Constructor ##############################################################
    def __init__(self, master):
    
        # Window creation
        tk.Frame.__init__(self, master)

        self.master = master
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Local variables
        self.x = 0
        self.y = 0
        self.z = 0
        self.raw = ""
        self.im_ref = None
        
    # Events handling ##########################################################
    
    def movingEvent(self, u, v, plane, state):
        # When the mouse moves inside a plane
        if state&0x0004==0x0004:
            if plane=="plane Z":
                self.x = u
                self.y = v
                if self.raw:
                    self.planez.drawTarget(self.x, self.y)
                    self.setImagePlaneY()
                    self.setImagePlaneX()
            elif plane=="plane Y":
                self.x = u
                self.z = v
                if self.raw:
                    self.planey.drawTarget(self.x, self.z)
                    self.setImagePlaneZ()
                    self.setImagePlaneX()
            elif plane=="plane X":
                self.z = u
                self.y = v
                if self.raw:
                    self.planex.drawTarget(self.z, self.y)
                    self.setImagePlaneY()
                    self.setImagePlaneZ()
            value = self.im_ref().getPixel((self.x, self.y, self.z))
            self.posLabel.config(text="At (%d,%d,%d) = %d" % (self.x,self.y,self.z,value))
        else:
            self.planex.eraseTarget()
            self.planey.eraseTarget()
            self.planez.eraseTarget()
    
    def keyboardEvent(self, event):
        # Keyboard events handling
        if event.keycode==37 or event.keycode==105:
            self.planex.eraseTarget()
            self.planey.eraseTarget()
            self.planez.eraseTarget()
        
    # Display methods ##########################################################
    
    def setImagePlaneZ(self):
        # Extracts the image for plane Z
        start = self.z*self.W*self.H
        stop = (self.z+1)*self.W*self.H
        im = Image.frombytes("L", (self.W,self.H), self.raw[start:stop])
        if self.master.palname:
            im.putpalette(palette.getPalette(self.master.palname))
        self.planez.display(im)
        self.planez.drawTarget(self.x, self.y)
        
    def setImagePlaneY(self):
        # Extracts the image for plane Y
        data = b""
        for i in range(self.L):
            start = self.W*(self.y+self.H*i)
            data += self.raw[start:start+self.W]
        im = Image.frombytes("L", (self.W,self.L), data)
        if self.master.palname:
            im.putpalette(palette.getPalette(self.master.palname))
        self.planey.display(im)
        self.planey.drawTarget(self.x, self.z)
        
    def setImagePlaneX(self):
        # Extracts the image for plane X
        im = Image.frombytes("L", (self.H,self.L), self.raw[self.x::self.W])
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.ROTATE_270)
        if self.master.palname:
            im.putpalette(palette.getPalette(self.master.palname))
        self.planex.display(im)
        self.planex.drawTarget(self.z, self.y)
    
    # Public method : called by the display window #############################
    
    def connect(self, im_ref):
        # Connection of the 3D image to the display
        self.im_ref = im_ref
        self.W, self.H, self.L = self.im_ref().getSize()
        imsize = [self.W, self.H, self.L]
        zoom = 1.0
        while imsize[0]<constants._MIN or imsize[1]<constants._MIN or imsize[2]<constants._MIN:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            imsize[2] = imsize[2]*2
            zoom = zoom*2
        while imsize[0]>constants._MAX or imsize[1]>constants._MAX or imsize[2]>constants._MAX:
            imsize[0] = imsize[0]//2
            imsize[1] = imsize[1]//2
            imsize[2] = imsize[2]//2
            zoom = zoom/2
        self.columnconfigure(0, weight=int(100*(self.W/float(self.W+self.L))) )
        self.rowconfigure(0, weight=int(100*(self.L/float(self.W+self.L))) )
        self.columnconfigure(1, weight=int(100*(self.H/float(self.H+self.L))) )
        self.rowconfigure(1, weight=int(100*(self.L/float(self.H+self.L))) )
        self.planez = planeFrame(self, [self.W,self.H], "plane Z", zoom=zoom)
        self.planez.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.planey = planeFrame(self, [self.W,self.L], "plane Y", zoom=zoom)
        self.planey.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.planex = planeFrame(self, [self.L,self.H], "plane X", zoom=zoom)
        self.planex.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
        lb = ttk.LabelFrame(self, text="Information", labelanchor=tk.NW)
        lb.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
        self.volLabel = ttk.Label(lb, text="Volume : 0")
        self.volLabel.grid(row=0, column=0, sticky=tk.W)
        self.posLabel = ttk.Label(lb, text="At (0,0,0) = 0")
        self.posLabel.grid(row=1, column=0, sticky=tk.W)
        self.planeLabel = ttk.Label(lb, text="")
        self.planeLabel.grid(row=2, column=0, sticky=tk.W)
        
    def updateim(self):
        # Updates the display (perform a rendering)
        depth = self.im_ref().getDepth()
        volume = 0
        if depth==1:
            # binary 3D image
            self.planeLabel.config(text="")
            im8 = mamba.imageMb(self.W, self.H, 8)
            self.raw = b""
            for im2D in self.im_ref():
                mamba.convert(im2D, im8)
                self.raw += im8.extractRaw()
                volume += mamba.computeVolume(im2D)
        elif depth==32:
            # 32-bit 3D image
            if self.master.bplane==4:
                self.planeLabel.config(text="Plane : all")
                im3D_8 = m3D.image3DMb(self.im_ref(), 8)
                m3D.convert3D(self.im_ref(), im3D_8)
                self.raw = im3D_8.extractRaw()
                volume = m3D.computeVolume3D(self.im_ref())
            else:
                self.planeLabel.config(text="Plane : %d" % (self.master.bplane))
                im8 = mamba.imageMb(self.W, self.H, 8)
                self.raw = b""
                for im2D in self.im_ref():
                    mamba.copyBytePlane(im2D, self.master.bplane, im8)
                    self.raw += im8.extractRaw()
                    volume += mamba.computeVolume(im2D)
        else:
            # Greyscale image
            self.planeLabel.config(text="")
            self.raw = self.im_ref().extractRaw()
            volume = m3D.computeVolume3D(self.im_ref())
        self.setImagePlaneZ()
        self.setImagePlaneY()
        self.setImagePlaneX()
        self.planex.eraseTarget()
        self.planey.eraseTarget()
        self.planez.eraseTarget()
        self.volLabel.config(text="Volume : %d" % (volume))
        value = self.im_ref().getPixel((self.x, self.y, self.z))
        self.posLabel.config(text="At (%d,%d,%d) = %d" % (self.x,self.y,self.z,value))

    def onHide(self):
        pass
    def onShow(self):
        pass
    def onRestore(self):
        imsize = [self.W, self.H, self.L]
        zoom = 1.0
        while imsize[0]<constants._MIN or imsize[1]<constants._MIN or imsize[2]<constants._MIN:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            imsize[2] = imsize[2]*2
            zoom = zoom*2
        while imsize[0]>constants._MAX or imsize[1]>constants._MAX or imsize[2]>constants._MAX:
            imsize[0] = imsize[0]//2
            imsize[1] = imsize[1]//2
            imsize[2] = imsize[2]//2
            zoom = zoom/2
        self.planez.setZoom(zoom)
        self.planey.setZoom(zoom)
        self.planex.setZoom(zoom)
