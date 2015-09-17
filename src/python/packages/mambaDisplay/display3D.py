"""
This module defines a 3D data displayer for mamba.
"""

# Contributors : Nicolas BEUCHER

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from . import constants
from . import popup
from . import palette
from . import display3D_proj
from . import display3D_volren
from . import display3D_player

class Display3D(tk.Toplevel):
    
    # Constructor ##############################################################
    def __init__(self, master):
    
        # Window creation
        tk.Toplevel.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.popup = popup.Popup(self)
        self.popup.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.popup.grid_remove()
        
        self.projFrame = display3D_proj.Display3D_Proj(self)
        self.projFrame.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.playFrame = display3D_player.Display3D_Player(self)
        self.playFrame.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.playFrame.grid_remove()
        try:
            self.volrenFrame = display3D_volren.Display3D_VolRen(self)
            self.volrenFrame.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
            self.volrenFrame.grid_remove()
        except ValueError as err:
            self.volrenFrame = None
        self.selectedFrame = self.projFrame

        self.std_geometry = ""
        self.palname = ""
        self.bplane = 4
        self.frozen = False
        self.im_ref = None

        # Event binding
        self.bind("<KeyPress-F1>", self.selectProjection)
        self.bind("<KeyPress-F2>", self.selectVolRen)
        self.bind("<KeyPress-F3>", self.selectPlayer)
        self.bind("<KeyPress-F5>", self.displayUpdateEvent)
        self.bind("<KeyRelease>", self.keyboardEvent)
        self.bind("<Control-f>", self.freezeEvent)
        self.bind("<Control-r>", self.restoreEvent)
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

    # Events ###################################################################

    def keyboardEvent(self, event):
        # Keyboard events handling
        if event.char == "p":
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
        elif event.char == "b":
            # BYTE PLANE MODIFICATION (next)
            self.bplane = (self.bplane+1)%5
            self.updateim()
        elif event.char == "n":
            # BYTE PLANE MODIFICATION (previous)
            self.bplane = (self.bplane-1)%5
            self.updateim()
        else:
            self.selectedFrame.keyboardEvent(event)

    def selectProjection(self, event):
        self.selectedFrame.grid_remove()
        self.selectedFrame.onHide()
        self.selectedFrame = self.projFrame
        self.selectedFrame.updateim()
        self.selectedFrame.grid()
        self.selectedFrame.onShow()
    def selectVolRen(self, event):
        if self.volrenFrame:
            self.selectedFrame.grid_remove()
            self.selectedFrame.onHide()
            self.selectedFrame = self.volrenFrame
            self.selectedFrame.updateim()
            self.selectedFrame.grid()
            self.selectedFrame.onShow()
    def selectPlayer(self, event):
        self.selectedFrame.grid_remove()
        self.selectedFrame.onHide()
        self.selectedFrame = self.playFrame
        self.selectedFrame.updateim()
        self.selectedFrame.grid()
        self.selectedFrame.onShow()
    
    def displayUpdateEvent(self, event):
        # Called when the user wants to update the display
        self.selectedFrame.updateim()
    
    def freezeEvent(self, event):
        # Freeze/Unfreeze event
        if self.frozen:
            self.unfreeze()
        else:
            self.freeze()

    def restoreEvent(self, event):
        # Restore original size event
        # The window size and parameter are reset.
        self.projFrame.onRestore()
        self.playFrame.onRestore()
        if self.volrenFrame:
            self.volrenFrame.onRestore()
        self.selectProjection(None)
        # Restoring the standard geometry.
        self.geometry(self.std_geometry)

    # Public method : called by the image3DMb class ############################
    
    def connect(self, im_ref):
        # Connection of the 3D image to the display
        self.im_ref = im_ref
        self.projFrame.connect(im_ref)
        self.playFrame.connect(im_ref)
        if self.volrenFrame:
            self.volrenFrame.connect(im_ref)
        self.updateim()
        
    def updateim(self):
        # Updates the display (perform a rendering)
        if self.im_ref() and self.state()=="normal" and not self.frozen:
            self.title((self.frozen and "Frozen - " or "") +
                       self.im_ref().getName() + 
                       " - "+str(self.im_ref().getDepth()))
            self.selectedFrame.updateim()
        
    def hide(self):
        # Hides the display
        self.withdraw()
        
    def show(self, **options):
        # Shows the display
        if self.state()!="normal":
            self.deiconify()
        if "palette" in options:
            self.palname = options["palette"]
            if self.palname:
                self.popup.info("palette set to "+self.palname)
            else:
                self.popup.info("No palette set")
        if "plane" in options:
            self.bplane = options["plane"]
        if "mode" in options:
            if options["mode"]=="PLAYER":
                self.selectPlayer(None)
            elif options["mode"]=="VOLUME":
                self.selectVolRen(None)
            else:
                self.selectProjection(None)
        self.updateim()
        
    def freeze(self):
        # freezes the display so that update has no effect
        self.frozen = True
        self.title((self.frozen and "Frozen - " or "") +
                   self.im_ref().getName() + 
                   " - "+str(self.im_ref().getDepth()))

    def unfreeze(self):
        # Unfreezes the display
        self.frozen = False
        self.updateim()
