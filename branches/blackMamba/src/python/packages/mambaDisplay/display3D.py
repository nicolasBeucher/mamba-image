"""
This module defines a 3D data displayer for mamba based on the VTK library.
This displayer is not fast and thus does not behave similarly to the display
embedded in mamba for 2D images (more remarkably it is not updated after
each operation).
"""

# Contributors : Nicolas BEUCHER

# VTK imports
try:
    _vtk_lib_present = True
    import vtk
    from vtk import vtkImageImport
    from vtk.util.vtkConstants import *
    from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
except ImportError:
    _vtk_lib_present = False

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import colorchooser
except ImportError:
    import Tkinter as tk
    import ttk
    import tkColorChooser as colorchooser

import time
from PIL import Image
from PIL import ImageTk

import constants

# Mamba imports
import mamba3D as m3D
import mamba
import mamba.core as core

################################################################################
# VTK Display 

# This class is not public and is accessed through the appropriate methods
# of the image3DMb class.
class _image3DVTKDisplay(tk.Toplevel):

    def __init__(self, name):
    
        # Window creation
        tk.Toplevel.__init__(self)
        self.title(name)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # ttk style
        self.style = ttk.Style()
        if 'xpnative' in self.style.theme_names():
            self.style.theme_use('xpnative')
        else:
            self.style.theme_use('classic')
        
        # Renderer and associated widget
        self._renWidget = vtkTkRenderWidget(self)
        self._ren = vtk.vtkRenderer()
        self._renWidget.GetRenderWindow().AddRenderer(self._ren)
        self._renWidget.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        
        # Transfer functions and volume display options and properties
        self.vtk_im = vtkImageImport()
        self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
        self.im_flipy = vtk.vtkImageFlip()
        self.im_flipy.SetFilteredAxis(1)
        self.im_flipy.SetInputConnection(self.vtk_im.GetOutputPort());
        self.im_flipz = vtk.vtkImageFlip()
        self.im_flipz.SetFilteredAxis(2)
        self.im_flipz.SetInputConnection(self.im_flipy.GetOutputPort());
        self.opaTF = vtk.vtkPiecewiseFunction()
        self.colTF = vtk.vtkColorTransferFunction()
        self.volProp = vtk.vtkVolumeProperty()
        self.volProp.SetColor(self.colTF)
        self.volProp.SetScalarOpacity(self.opaTF)
        self.volProp.ShadeOn()
        self.volProp.SetInterpolationTypeToLinear()
        self.compoFun = vtk.vtkVolumeRayCastCompositeFunction()
        self.isosfFun = vtk.vtkVolumeRayCastIsosurfaceFunction()
        self.isosfFun.SetIsoValue(0)
        self.mipFun = vtk.vtkVolumeRayCastMIPFunction()
        self.volMap = vtk.vtkVolumeRayCastMapper()
        self.volMap.SetVolumeRayCastFunction(self.compoFun)
        self.volMap.SetInputConnection(self.im_flipz.GetOutputPort())
        self.volume = vtk.vtkVolume()
        self.volume.SetMapper(self.volMap)
        self.volume.SetProperty(self.volProp)
        self.outlineData = vtk.vtkOutlineFilter()
        self.outlineData.SetInputConnection(self.im_flipz.GetOutputPort())
        self.mapOutline = vtk.vtkPolyDataMapper()
        self.mapOutline.SetInputConnection(self.outlineData.GetOutputPort())
        self.outline = vtk.vtkActor()
        self.outline.SetMapper(self.mapOutline)
        self.outline.GetProperty().SetColor(1, 1, 1)
        self._ren.AddVolume(self.volume)
        self._ren.AddActor(self.outline)
        self._ren.SetBackground(116/255.0,214/255.0,220/255.0)
        
        # Control widget
        self.controlbar = ttk.Frame(self)
        self.controlbar.grid(row=0, column=1,
                             sticky=tk.E+tk.W+tk.N+tk.S)
        self.drawControlBar()
        self.controlbar.grid_remove()
        self.controlbar.state = "hidden"
        
        # Creates the info status bar.
        statusbar = ttk.Frame(self)
        statusbar.columnconfigure(0, weight=1)
        statusbar.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.infos = []
        for i in range(3):
            v = tk.StringVar(self)
            ttk.Label(statusbar, anchor=tk.W, textvariable=v).grid(row=0, column=i, sticky=tk.E+tk.W)
            self.infos.append(v)
        self.infos[2].set("Hit F1 for control <-")
            
        # Events bindings
        self.bind("<KeyPress-F1>", self.displayControlEvent)
        self.bind("<KeyPress-F5>", self.displayUpdateEvent)
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        
    def drawControlBar(self):
        # Draw all the widgets inside the control bar
        lf = ttk.LabelFrame(self.controlbar,
                           text="Transfer controls",
                           labelanchor=tk.NW)
        lf.grid(row=0, column=0,
                padx=4, pady=4, 
                sticky=tk.E+tk.W+tk.N+tk.S)
        l = ttk.Label(lf, text="Color")
        l.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.colorCan = tk.Canvas(lf, bg="white", bd=2, relief=tk.RIDGE)
        self.colorCan.config(width=256, height=20, scrollregion=(0,0,255,19))
        self.colorCan.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.drawColTF()
        l = ttk.Label(lf, text="Transparency")
        l.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.opaCan = tk.Canvas(lf, bg="white", bd=2, relief=tk.RIDGE)
        self.opaCan.config(width=256, height=20, scrollregion=(0,0,255,19))
        self.opaCan.grid(row=3, column=0, sticky=tk.E+tk.W)
        self.drawOpaTF()
        self.opaCan.bind("<Button-1>", self.changeOpa)
        l = ttk.Label(lf, text="Background")
        l.grid(row=4, column=0, sticky=tk.E+tk.W)
        self.bgCan = tk.Canvas(lf, bg="white", bd=2, relief=tk.RIDGE)
        self.bgCan.config(width=256, height=20, scrollregion=(0,0,255,19))
        self.bgCan.grid(row=5, column=0, sticky=tk.E+tk.W)
        self.bgCan.bind("<Button-1>", self.changeBg)
        self.drawBg()
        lf = ttk.LabelFrame(self.controlbar,
                           text="Raycast function controls",
                           labelanchor=tk.NW)
        lf.grid(row=1, column=0, 
                padx=4, pady=4, sticky=tk.E+tk.W+tk.N+tk.S)
        RC_FUN = [
            ("Composite", 0),
            ("Isosurface", 1),
            ("Maximum Intensity Pixel", 2)
        ]
        self.funSelected = tk.IntVar()
        self.funSelected.set(0)
        for i,(text,value) in enumerate(RC_FUN):
            ttk.Radiobutton(lf, 
                                text=text,
                                value=value,
                                variable=self.funSelected,
                                command=self.changeRCFunction).grid(row=i, column=0, sticky=tk.W)
            if text=="Isosurface":
                 self.isoValueSpin = tk.Spinbox(lf, width=4,
                                                from_=0, to=255, increment=1,
                                                command=self.changeIsoValue)
                 self.isoValueSpin.grid(row=i, column=1, sticky=tk.E)
                 self.isoValueSpin.bind("<KeyPress-Return>", self.changeIsoValue)
        lf = ttk.LabelFrame(self.controlbar,
                           text="Image properties",
                           labelanchor=tk.NW)
        lf.grid(row=2, column=0, 
                padx=4, pady=4, sticky=tk.E+tk.W+tk.N+tk.S)
        self.dimLabel = ttk.Label(lf)
        self.dimLabel.grid(row=0, sticky=tk.W)
        self.volLabel = ttk.Label(lf)
        self.volLabel.grid(row=1, sticky=tk.W)
    
    # Functions to draw the widget inside the control bar
    def drawColTF(self):
        for i in range(256):
            color = [int(v*255) for v in self.colTF.GetColor(i)]
            fill = "#%02x%02x%02x" % (color[0], color[1], color[2])
            self.colorCan.create_line(i,0,i,20,fill=fill)
    def drawOpaTF(self):
        for i in range(256):
            color = int(255*self.opaTF.GetValue(i))
            fill = "#%02x%02x%02x" % (color, color, color)
            self.opaCan.create_line(i,0,i,20,fill=fill)
    def drawBg(self):
        color = [int(v*255) for v in self._ren.GetBackground()]
        fill = "#%02x%02x%02x" % (color[0], color[1], color[2])
        self.bgCan.config(bg=fill)
        
    # Functions associated with the control widgets
    def changeBg(self, event):
        # Change the background color
        new_color = colorchooser.askcolor(event.widget.cget("bg"))
        if new_color[0]==None:
            return
        self.bgCan.config(bg=new_color[1])
        bg = [v/255.0 for v in new_color[0]]
        self._ren.SetBackground(*bg)
        self.updateim()
    def changeOpa(self, event):
        # Change the opacity function
        v = self.opaCan.canvasx(event.x)
        self.opaTF.RemoveAllPoints()
        self.opaTF.AddPoint(0, 0.0)
        self.opaTF.AddPoint(v-1, 0.0)
        self.opaTF.AddPoint(v, 1.0)
        self.opaTF.AddPoint(256, 1.0)
        self.drawOpaTF()
        self.updateim()
    def changeIsoValue(self, event=None):
        # Change of the iso value used by the isosurface function
        # This impacts the display only if the current function used
        # is isosurface.
        value = self.isoValueSpin.get()
        try:
            self.isosfFun.SetIsoValue(float(value))
            fun = self.funSelected.get()
            if fun==1:
                self.updateim()
        except:
            pass
    def changeRCFunction(self):
        # Change of the raycast function
        fun = self.funSelected.get()
        if fun==1:
            self.volProp.SetInterpolationTypeToNearest()
            self.volMap.SetVolumeRayCastFunction(self.isosfFun)
        elif fun==2:
            self.volProp.SetInterpolationTypeToLinear()
            self.volMap.SetVolumeRayCastFunction(self.mipFun)
        else:
            self.volProp.SetInterpolationTypeToLinear()
            self.volMap.SetVolumeRayCastFunction(self.compoFun)
        self.updateim()
        
    # Events handling methods ##################################################
    def displayControlEvent(self, event):
        if self.controlbar.state=="hidden":
            self.controlbar.grid()
            self.controlbar.state = "displayed"
            self.infos[2].set("Hit F1 to hide control ->")
        else:
            self.controlbar.grid_remove()
            self.controlbar.state = "hidden"
            self.infos[2].set("Hit F1 for control <-")
        
    def displayUpdateEvent(self, event):
        # Upon hitting key F5 the display is updated in order to avoid
        # having to call the appropriate function every time
        self.updateim()
        
    # Display update and connection ############################################
    def _convertIntoVTKImage(self):
        # Converts the associated sequence into a VTK image
        # structure to be able to display it using the rendering
        # mechanisms of VTK
        w = self._seq[0].width
        h = self._seq[0].height
        l = len(self._seq)
        volume = 0
    
        if self._seq[0].depth==8:
            # 8-bit 3D image
            raw_data = ""
            for mbIm in self._seq:
                err,s = core.MB_Extract(mbIm)
                mamba.raiseExceptionOnError(err)
                err, vol = core.MB_Volume(mbIm)
                mamba.raiseExceptionOnError(err)
                volume += vol
                raw_data += s
            
            self.vtk_im.CopyImportVoidPointer(raw_data, len(raw_data))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
        elif self._seq[0].depth==32:
            # 32-bit 3D image
            raw_data = ""
            for mbIm in self._seq:
                err,s = core.MB_Extract(mbIm)
                mamba.raiseExceptionOnError(err)
                err, vol = core.MB_Volume(mbIm)
                mamba.raiseExceptionOnError(err)
                volume += vol
                raw_data += s
            raw_data2 = raw_data[0::4]+raw_data[1::4]+raw_data[2::4]+raw_data[3::4]
            l = l*4
            
            self.vtk_im.CopyImportVoidPointer(raw_data2, len(raw_data2))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
        else:
            # binary 3D image
            im8 = mamba.imageMb(self._seq[0].width, self._seq[0].height, 8)
            raw_data = ""
            for mbIm in self._seq:
                err = core.MB_Convert(mbIm, im8.mbIm)
                mamba.raiseExceptionOnError(err)
                err,s = core.MB_Extract(im8.mbIm)
                mamba.raiseExceptionOnError(err)
                err, vol = core.MB_Volume(mbIm)
                mamba.raiseExceptionOnError(err)
                volume += vol
                raw_data += s
            
            self.vtk_im.CopyImportVoidPointer(raw_data, len(raw_data))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
            
        self.vtk_im.SetNumberOfScalarComponents(1)
        extent = self.vtk_im.GetDataExtent()
        self.vtk_im.SetDataExtent(extent[0], extent[0] + w - 1,
                                  extent[2], extent[2] + h - 1,
                                  extent[4], extent[4] + l - 1)
        self.vtk_im.SetWholeExtent(extent[0], extent[0] + w - 1,
                                   extent[2], extent[2] + h - 1,
                                   extent[4], extent[4] + l - 1)
        self.volLabel.config(text="Volume = %d" % (volume))
        
    def connect(self, sequence, name=""):
        # Connect a sequence to the display (gives the
        # reference).
        self._name = name
        self._seq = sequence
        self.dimLabel.config(text="Dimensions = %dx%dx%d" % (self._seq[0].width, self._seq[0].height, len(self._seq)))
        if self._seq[0].depth==1:
            self.opaTF.AddPoint(0, 0.0)
            self.opaTF.AddPoint(127, 0.0)
            self.opaTF.AddPoint(128, 1.0)
            self.opaTF.AddPoint(256, 1.0)
            self.colTF.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
            self.colTF.AddRGBPoint(127.0, 0.0, 0.0, 0.0)
            self.colTF.AddRGBPoint(128.0, 1.0, 1.0, 1.0)
            self.colTF.AddRGBPoint(256.0, 1.0, 1.0, 1.0)
        else:
            self.opaTF.AddPoint(0, 0.0)
            self.opaTF.AddPoint(255, 1.0)
            self.colTF.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
            self.colTF.AddRGBPoint(255.0, 1.0, 1.0, 1.0)
        self.drawOpaTF()
        self.drawColTF()
        self.updateim()
        
    def setColorPalette(self, pal):
        # Called when the color palette is changed
        self.colTF.RemoveAllPoints()
        for i in range(256):
            self.colTF.AddRGBPoint(i, pal[i*3]/255.0, pal[i*3+1]/255.0, pal[i*3+2]/255.0)
        self.drawColTF()
        self.updateim()
        
    def setOpacityPalette(self, pal):
        # Called when the opacity palette is changed
        self.opaTF.RemoveAllPoints()
        for i in range(256):
            self.opaTF.AddPoint(i, pal[i]/255.0)
        self.drawOpaTF()
        self.updateim()
        
    def updateim(self):
        # Update the display (perform a rendering)
        if self.state()=="normal":
            self.infos[0].set("Updating ...")
            self.title(self._name+" - "+str(self._seq[0].depth))
            self._convertIntoVTKImage()
            self._renWidget.Render()
            self.infos[0].set("")
        
    def show(self):
        # Show the display
        if self.state()!="normal":
            self.deiconify()
        self.updateim()
        
    def hide(self):
        # Hide the display
        self.withdraw()
        
    def destroy(self):
        # Destroy the display
        del self._seq
        tk.Toplevel.destroy(self)
        
################################################################################
# Projection display

class _planeFrame(ttk.LabelFrame):

    def __init__(self,root,size,name,zoom=-1):
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
        if zoom<0:
            self.zoom = 1.0
            while  imsize < [constants._MINW, constants._MINH]:
                imsize[0] = imsize[0]*2
                imsize[1] = imsize[1]*2
                self.zoom = self.zoom*2
            while imsize > [constants._MAXW, constants._MAXH]:
                imsize[0] = imsize[0]//2
                imsize[1] = imsize[1]//2
                self.zoom = self.zoom//2
        else:
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
        self.depth = 0
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
        if event.state&0x0004==0x0004:
            self.root.movingEvent(x,y,self.name)
        else:
            self.eraseTarget()
        
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
                    zoom = self.zoom//2
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
                        zoom = self.zoom//2
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
        # returns the value of zoom
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
        
    def setDepth(self, depth):
        # Sets the depth of the displayed data
        self.depth = depth
        
    def drawTarget(self, x, y):
        # Draw the target when the user moves the mouse while hold ctrl
        self.eraseTarget()
        esize = max(self.csize, self.dsize)
        x = (x*self.dsize[0])//self.osize[0] + max((self.csize[0]-self.dsize[0])//2,0)
        y = (y*self.dsize[1])//self.osize[1] + max((self.csize[1]-self.dsize[1])//2,0)
        id = self.canvas.create_line(x,0,x,esize[1]-1,fill="red")
        self.targetid.append(id)
        id = self.canvas.create_line(0,y,esize[0]-1,y,fill="red")
        self.targetid.append(id)
        
    def eraseTarget(self):
        # Erase the target upon releasing the ctrl button
        for id in self.targetid:
            self.canvas.delete(id)
        self.targetid = []

class Display3D(tk.Toplevel):
    
    # Constructor ##############################################################
    # destroy method is inherited from Toplevel
    def __init__(self, master, name):
    
        # Window creation
        tk.Toplevel.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # ttk style
        self.style = ttk.Style()
        if 'xpnative' in self.style.theme_names():
            self.style.theme_use('xpnative')
        else:
            self.style.theme_use('classic')
        
        # Local variables
        self.x = 0
        self.y = 0
        self.z = 0
        self.raw = ""
        self.icon = None
        self._seq = []
        self.palette = None
        self.palactive = False
        self.name = name
        self.std_geometry = ""
        
        # Event binding
        self.bind("<KeyRelease>", self.keyboardEvent)
        self.bind("<KeyPress-F5>", self.displayUpdateEvent)
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        
    # Events handling ##########################################################
    
    def movingEvent(self, u, v, plane):
        # When the mouse moves inside a plane
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
        err, value = core.MB_GetPixel(self._seq[self.z], self.x, self.y)
        mamba.raiseExceptionOnError(err)
        self.posLabel.config(text="At (%d,%d,%d) = %d" % (self.x,self.y,self.z,value))
    
    def keyboardEvent(self, event):
        # Keyboard events handling
        if event.keycode==37 or event.keycode==105:
            self.planex.eraseTarget()
            self.planey.eraseTarget()
            self.planez.eraseTarget()
        elif event.char == "p":
            # PALETTE ACTIVATION
            self.palactive = not self.palactive
            self.updateim()
            
    def displayUpdateEvent(self, event):
        # Called when the user wants to update the display
        self.updateim()
        
    # Display methods ##########################################################
    
    def setImagePlaneZ(self):
        # Extract the image for plane Z
        if self._seq[0].depth==32:
            # 32-bit images
            start = self.z*self.W*self.H*4
            stop = (self.z+1)*self.W*self.H*4
            lpilim = []
            for i in range(4):
                pilim = Image.frombytes("L", (self.W,self.H), self.raw[start+i:stop+i:4])
                lpilim.append(pilim)
            im = Image.new("L", (self.W*2,self.H*2))
            for i,pilim in enumerate(lpilim):
                im.paste(pilim, (self.W*(i%2),self.H*(i//2)))
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planez.display(im)
            self.planez.setDepth(self._seq[0].depth)
            self.planez.drawTarget(self.x, self.y)
            if not self.icon:
                start = self.L*self.W*self.H*2
                stop = (self.L//2+1)*self.W*self.H*4
                lpilim = []
                for i in range(4):
                    # Creating the PIL image 
                    pilim = Image.frombytes("L", (self.W,self.H), self.raw[start+i:stop+i:4])
                    lpilim.append(pilim)
                im = Image.new("L", (self.W*2,self.H*2))
                for i,pilim in enumerate(lpilim):
                    im.paste(pilim, (self.W*(i%2),self.H*(i//2)))
                m = max(self.H, self.W)
                icon_size = ((constants._icon_max_size*self.W)//m,
                             (constants._icon_max_size*self.H)//m)
                self.icon = ImageTk.PhotoImage(im.resize(icon_size, Image.NEAREST))
                self.tk.call('wm','iconphoto', self._w, self.icon)
        else:
            # 1 or 8 bit images
            start = self.z*self.W*self.H
            stop = (self.z+1)*self.W*self.H
            im = Image.frombytes("L", (self.W,self.H), self.raw[start:stop])
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planez.display(im)
            self.planez.setDepth(self._seq[0].depth)
            self.planez.drawTarget(self.x, self.y)
            if not self.icon:
                start = self.L//2*self.W*self.H
                stop = (self.L//2+1)*self.W*self.H
                im = Image.frombytes("L", (self.W,self.H), self.raw[start:stop])
                m = max(self.H, self.W)
                icon_size = ((constants._icon_max_size*self.W)//m,
                             (constants._icon_max_size*self.H)//m)
                self.icon = ImageTk.PhotoImage(im.resize(icon_size, Image.NEAREST))
                self.tk.call('wm','iconphoto', self._w, self.icon)
        
    def setImagePlaneY(self):
        # Extract the image for plane Y
        if self._seq[0].depth==32:
            # 32-bit images
            lpilim = []
            for j in range(4):
                data = b""
                for i in range(self.L):
                    start = self.W*(self.y+self.H*i)*4
                    data += self.raw[start+j:start+self.W*4+j:4]
                pilim = Image.frombytes("L", (self.W,self.L), data)
                lpilim.append(pilim)
            im = Image.new("L", (self.W*2,self.L*2))
            for i,pilim in enumerate(lpilim):
                im.paste(pilim, (self.W*(i%2),self.L*(i//2)))
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planey.display(im)
            self.planey.setDepth(self._seq[0].depth)
            self.planey.drawTarget(self.x, self.z)
        else:
            # 1 or 8 bit images
            data = b""
            for i in range(self.L):
                start = self.W*(self.y+self.H*i)
                data += self.raw[start:start+self.W]
            im = Image.frombytes("L", (self.W,self.L), data)
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planey.display(im)
            self.planey.setDepth(self._seq[0].depth)
            self.planey.drawTarget(self.x, self.z)
        
    def setImagePlaneX(self):
        # Extract the image for plane X
        if self._seq[0].depth==32:
            # 32-bit images
            lpilim = []
            for j in range(4):
                pilim = Image.frombytes("L", (self.H,self.L), self.raw[self.x*4+j::self.W*4])
                pilim = pilim.transpose(Image.FLIP_TOP_BOTTOM)
                pilim = pilim.transpose(Image.ROTATE_270)
                lpilim.append(pilim)
            im = Image.new("L", (self.L*2,self.H*2))
            for i,pilim in enumerate(lpilim):
                im.paste(pilim, (self.L*(i%2),self.H*(i//2)))
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planex.display(im)
            self.planex.setDepth(self._seq[0].depth)
            self.planex.drawTarget(self.z, self.y)
        else:
            # 1 or 8 bit images
            im = Image.frombytes("L", (self.H,self.L), self.raw[self.x::self.W])
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
            im = im.transpose(Image.ROTATE_270)
            if self.palette and self.palactive:
                im.putpalette(self.palette)
            self.planex.display(im)
            self.planex.setDepth(self._seq[0].depth)
            self.planex.drawTarget(self.z, self.y)
    
    # Public method : called by the image3DMb class ############################
    
    def connect(self, sequence, pal=None, opa=None):
        # Connection of the 3D image to the display
        self.palette = pal
        self.palactive = True
        self.W = sequence[0].width
        self.H = sequence[0].height
        self.L = len(sequence)
        imsize = [self.W, self.H, self.L]
        zoom = 1.0
        while imsize[0]<constants._MINW or imsize[1]<constants._MINH or imsize[2]<constants._MINH:
            imsize[0] = imsize[0]*2
            imsize[1] = imsize[1]*2
            imsize[2] = imsize[2]*2
            zoom = zoom*2
        while imsize[0]>constants._MAXW or imsize[1]>constants._MAXH or imsize[2]>constants._MAXH:
            imsize[0] = imsize[0]//2
            imsize[1] = imsize[1]//2
            imsize[2] = imsize[2]//2
            zoom = zoom//2
        self.columnconfigure(0, weight=int(100*(self.W/float(self.W+self.L))) )
        self.rowconfigure(0, weight=int(100*(self.L/float(self.W+self.L))) )
        self.columnconfigure(1, weight=int(100*(self.H/float(self.H+self.L))) )
        self.rowconfigure(1, weight=int(100*(self.L/float(self.H+self.L))) )
        self._seq = sequence
        self.title(self.name+" - "+str(self._seq[0].depth))
        if self._seq[0].depth==32:
            mul = 2
            zoom = zoom//2
        else:
            mul = 1
        self.planez = _planeFrame(self, [self.W*mul,self.H*mul], "plane Z", zoom=zoom)
        self.planez.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.planey = _planeFrame(self, [self.W*mul,self.L*mul], "plane Y", zoom=zoom)
        self.planey.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.planex = _planeFrame(self, [self.L*mul,self.H*mul], "plane X", zoom=zoom)
        self.planex.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
        volume = 0
        if self._seq[0].depth==1:
            # binary 3D image
            im8 = mamba.imageMb(self.W, self.H, 8)
            self.raw = b""
            for mbIm in self._seq:
                err = core.MB_Convert(mbIm, im8.mbIm)
                mamba.raiseExceptionOnError(err)
                err,s = core.MB_Extract(im8.mbIm)
                mamba.raiseExceptionOnError(err)
                self.raw += s
                err, vol = core.MB_Volume(mbIm)
                mamba.raiseExceptionOnError(err)
                volume += vol
        else:
            self.raw = b""
            for mbIm in self._seq:
                err,s = core.MB_Extract(mbIm)
                mamba.raiseExceptionOnError(err)
                self.raw += s
                err, vol = core.MB_Volume(mbIm)
                mamba.raiseExceptionOnError(err)
                volume += vol
        self.setImagePlaneZ()
        self.setImagePlaneY()
        self.setImagePlaneX()
        self.planex.eraseTarget()
        self.planey.eraseTarget()
        self.planez.eraseTarget()
        
        lb = ttk.LabelFrame(self, text="Information", labelanchor=tk.NW)
        lb.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
        self.volLabel = ttk.Label(lb, text="Volume : %d" % (volume))
        self.volLabel.grid(row=0, column=0, sticky=tk.W)
        err, value = core.MB_GetPixel(self._seq[self.z], self.x, self.y)
        mamba.raiseExceptionOnError(err)
        self.posLabel = ttk.Label(lb, text="At (0,0,0) = %d" % (value))
        self.posLabel.grid(row=1, column=0, sticky=tk.W)
        
    def updateim(self):
        # Update the display (perform a rendering)
        if self.state()=="normal":
            volume = 0
            if self._seq[0].depth==1:
                # binary 3D image
                im8 = mamba.imageMb(self.W, self.H, 8)
                self.raw = b""
                for mbIm in self._seq:
                    err = core.MB_Convert(mbIm, im8.mbIm)
                    mamba.raiseExceptionOnError(err)
                    err,s = core.MB_Extract(im8.mbIm)
                    mamba.raiseExceptionOnError(err)
                    self.raw += s
                    err, vol = core.MB_Volume(mbIm)
                    mamba.raiseExceptionOnError(err)
                    volume += vol
            else:
                self.raw = b""
                for mbIm in self._seq:
                    err,s = core.MB_Extract(mbIm)
                    mamba.raiseExceptionOnError(err)
                    self.raw += s
                    err, vol = core.MB_Volume(mbIm)
                    mamba.raiseExceptionOnError(err)
                    volume += vol
            self.icon = None
            self.setImagePlaneZ()
            self.setImagePlaneY()
            self.setImagePlaneX()
            self.planex.eraseTarget()
            self.planey.eraseTarget()
            self.planez.eraseTarget()
            self.volLabel.config(text="Volume : %d" % (volume))
            err, value = core.MB_GetPixel(self._seq[self.z], self.x, self.y)
            mamba.raiseExceptionOnError(err)
            self.posLabel.config(text="At (%d,%d,%d) = %d" % (self.x,self.y,self.z,value))
        
    def hide(self):
        # Hide the display
        self.withdraw()
        
    def show(self):
        # Show the display
        if self.state()!="normal":
            self.deiconify()
        self.updateim()
        
    def colorize(self, pal, opa):
        # Called when the color palette is changed
        # Called when the opacity palette is changed
        self.palette = pal
        self.palactive = True
        self.updateim()
        
    def freeze(self):
        pass
    def unfreeze(self):
        pass
        
    def retitle(self, name):
        # Changing the name of the image
        self.name = name
        self.title(self.name+" - "+str(self._seq[0].depth))
        
    def destroy(self):
        # Destroy the display
        del self._seq
        tk.Toplevel.destroy(self)


