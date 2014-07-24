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

import constants
import display3D_proj
import display3D_volren
import display3D_player

class Display3D(tk.Toplevel):
    
    # Constructor ##############################################################
    def __init__(self, master):
    
        # Window creation
        tk.Toplevel.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.projFrame = display3D_proj.Display3D_Proj(self)
        self.projFrame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.playFrame = display3D_player.Display3D_Player(self)
        self.playFrame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.playFrame.grid_remove()
        try:
            self.volrenFrame = display3D_volren.Display3D_VolRen(self)
            self.volrenFrame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
            self.volrenFrame.grid_remove()
        except ValueError as err:
            print err
            self.volrenFrame = None
        self.selectedFrame = self.projFrame

        self.std_geometry = ""
        self.palactive = True
        self.bplane = 4

        # Event binding
        self.bind("<KeyPress-F1>", self.selectProjection)
        self.bind("<KeyPress-F2>", self.selectVolRen)
        self.bind("<KeyPress-F3>", self.selectPlayer)
        self.bind("<KeyPress-F5>", self.displayUpdateEvent)

        self.bind("<KeyRelease>", self.keyboardEvent)
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

    # Events ###################################################################

    def keyboardEvent(self, event):
        # Keyboard events handling
        if event.char == "p":
            # PALETTE ACTIVATION
            self.palactive = not self.palactive
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
        self.selectedFrame = self.projFrame
        self.selectedFrame.updateim()
        self.selectedFrame.grid()
    def selectVolRen(self, event):
        if self.volrenFrame:
            self.selectedFrame.grid_remove()
            self.selectedFrame = self.volrenFrame
            self.selectedFrame.updateim()
            self.selectedFrame.grid()
    def selectPlayer(self, event):
        self.selectedFrame.grid_remove()
        self.selectedFrame = self.playFrame
        self.selectedFrame.updateim()
        self.selectedFrame.grid()
    
    def displayUpdateEvent(self, event):
        # Called when the user wants to update the display
        self.selectedFrame.updateim()

    # Public method : called by the image3DMb class ############################
    
    def connect(self, im_ref):
        # Connection of the 3D image to the display
        depth = im_ref().getDepth()
        self.title(im_ref().getName()+" - "+str(depth))
        self.projFrame.connect(im_ref)
        self.playFrame.connect(im_ref)
        if self.volrenFrame:
            self.volrenFrame.connect(im_ref)
        self.updateim()
        
    def updateim(self):
        # Update the display (perform a rendering)
        if self.state()=="normal":
            self.selectedFrame.updateim()
        
    def hide(self):
        # Hide the display
        self.withdraw()
        
    def show(self):
        # Show the display
        if self.state()!="normal":
            self.deiconify()
        self.updateim()
        
    def freeze(self):
        pass
    def unfreeze(self):
        pass
