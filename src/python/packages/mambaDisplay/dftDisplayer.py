"""
This module defines a displayer.
"""

import weakref

import mamba
import mamba3D

import mambaDisplay
from . import display2D
from . import display3D

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    try:
        import Tkinter as tk
        import ttk
    except ImportError:
        print("Missing Tkinter library")
        raise

################################################################################
# Default implementation
################################################################################

# Real displayer (inherits from the generic displayer)
class DftDisplayer(mambaDisplay.Displayer):
    
    def __init__(self):
        self.windows = {}
        self.root = tk.Tk()
        self.root.withdraw()
        self.screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        # mainloop hack
        self.root.mainloop = self._dummy_mainloop
        tk.mainloop = self._dummy_mainloop
        
        # ttk style
        self.style = ttk.Style()
        if 'xpnative' in self.style.theme_names():
            self.style.theme_use('xpnative')
        else:
            self.style.theme_use('clam')
        
    def _dummy_mainloop(self, n=0):
        # Dummy mainloop to replace the mainloop that must not be called
        pass
    
    def addWindow(self, im):
        # Creates a window for image 'im'.
        # Returns the id of the window (its key).
        skey = ''
        if isinstance(im, mamba.imageMb):
            im_ref = weakref.ref(im)
            imd = display2D.Display2D(self.root)
            skey = str(imd)
            self.windows[skey] = imd
            imd.connect(im_ref)
        elif isinstance(im, mamba3D.image3DMb):
            im_ref = weakref.ref(im)
            imd = display3D.Display3D(self.root)
            skey = str(imd)
            self.windows[skey] = imd
            imd.connect(im_ref)
        return skey
        
    def showWindow(self, wKey, **options):
        # Displays the window identified by 'key'.
        self.windows[wKey].show(**options)
        self.root.update()
        # Storing the standard geometry.
        if not self.windows[wKey].std_geometry:
            geo = self.windows[wKey].geometry()
            geo = geo.split("-")[0].split("+")[0]
            self.windows[wKey].std_geometry = geo
        
    def controlWindow(self, wKey, ctrl):
        # Controls the window
        if ctrl=="FREEZE":
            self.windows[wKey].freeze()
        elif ctrl=="UNFREEZE":
            self.windows[wKey].unfreeze()
        self.root.update()
       
    def updateWindow(self, wKey):
        # Updates the window identified by 'wkey'.
        self.windows[wKey].updateim()
        self.root.update()
       
    def hideWindow(self, wKey):
        # Hides the window identified by 'wkey'.
        self.windows[wKey].hide()
        self.root.update()

    def destroyWindow(self, wKey):
        # Destroys the window identified by 'wkey'.
        self.windows[wKey].destroy()
        del(self.windows[wKey])
        
    def tidyWindows(self):
        # Tidies the display to ensure that all the windows are visible.
        x = self.screen_size[0]//20
        y = (19*self.screen_size[1])//20
        maxw = 0
        for toplvlw in self.root.winfo_children():
            if isinstance(toplvlw, tk.Toplevel):
                geo = toplvlw.geometry()
                geo = geo.split("-")[0].split("+")[0]
                l = geo.split("x")
                w = int(l[0])+5
                h = int(l[1])+30 # for window decoration
                if y-h<(self.screen_size[1]//20):
                    x = x + maxw
                    if x>(19*self.screen_size[0])//20:
                        x = self.screen_size[0]//20
                    y = (19*self.screen_size[1])//20
                    maxw = 0
                    y = y - h
                    geo = geo+"+"+str(x)+"+"+str(y)
                else:
                    y = y - h
                    geo = geo+"+"+str(x)+"+"+str(y)
                toplvlw.geometry(geo)
                if w>maxw:
                    maxw=w

