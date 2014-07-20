"""
Volume rendering display for 3D images.
"""

# Contributors : Nicolas BEUCHER

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

# VTK imports
try:
    _vtk_lib_present = True
    import vtk
    from vtk import vtkImageImport
    from vtk.util.vtkConstants import *
    from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
except ImportError:
    _vtk_lib_present = False

import constants

# Mamba imports
import mamba3D as m3D
import mamba

################################################################################
# Volume rendering display

class Display3D_VolRen(tk.Frame):

    def __init__(self, master):
        global _vtk_lib_present
        if not _vtk_lib_present:
            raise ValueError("no VTK")
    
        # Window creation
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Renderer and associated widget
        self.im_ref = None
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
        self.infos[2].set("Hit Tab for control <-")
            
        # Events bindings
        master.bind("<KeyPress-Tab>", self.displayControlEvent)
        
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
            self.infos[2].set("Hit Tab to hide control ->")
        else:
            self.controlbar.grid_remove()
            self.controlbar.state = "hidden"
            self.infos[2].set("Hit Tab for control <-")
        
    # Display update and connection ############################################
    def _convertIntoVTKImage(self):
        # Converts the associated sequence into a VTK image
        # structure to be able to display it using the rendering
        # mechanisms of VTK
        W, H = self.im_ref().getSize()
        L = self.im_ref().getLength()
        depth = self.im_ref().getDepth()
    
        if depth==8:
            # 8-bit 3D image
            raw_data = self.im_ref().extractRaw()
            volume = m3D.computeVolume3D(self.im_ref())
            self.vtk_im.CopyImportVoidPointer(raw_data, len(raw_data))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
        elif depth==32:
            # 32-bit 3D image
            raw_data = self.im_ref().extractRaw()
            volume = m3D.computeVolume3D(self.im_ref())
            raw_data2 = raw_data[0::4]+raw_data[1::4]+raw_data[2::4]+raw_data[3::4]
            L = L*4
            self.vtk_im.CopyImportVoidPointer(raw_data2, len(raw_data2))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
        else:
            # binary 3D image
            im8 = mamba.imageMb(W, H, 8)
            raw_data = b""
            for im2D in self.im_ref():
                mamba.convert(im2D, im8)
                raw_data += im8.extractRaw()
                volume += mamba.computeVolume(im2D)
            
            self.vtk_im.CopyImportVoidPointer(raw_data, len(raw_data))
            self.vtk_im.SetDataScalarType(VTK_UNSIGNED_CHAR)
            
        self.vtk_im.SetNumberOfScalarComponents(1)
        extent = self.vtk_im.GetDataExtent()
        self.vtk_im.SetDataExtent(extent[0], extent[0] + W - 1,
                                  extent[2], extent[2] + H - 1,
                                  extent[4], extent[4] + L - 1)
        self.vtk_im.SetWholeExtent(extent[0], extent[0] + W - 1,
                                   extent[2], extent[2] + H - 1,
                                   extent[4], extent[4] + L - 1)
        self.volLabel.config(text="Volume = %d" % (volume))
    
    # Public method : called by the display window #############################
        
    def connect(self, im_ref):
        # Connection of the 3D image to the display
        self.im_ref = im_ref
        W, H = self.im_ref().getSize()
        L = self.im_ref().getLength()
        depth = self.im_ref().getDepth()
        self.dimLabel.config(text="Dimensions = %dx%dx%d" % (W, H, L))
        if depth==1:
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
        
    def updateim(self):
        # Update the display (perform a rendering)
        self.infos[0].set("Updating ...")
        self._convertIntoVTKImage()
        self._renWidget.Render()
        self.infos[0].set("")

