"""
A popup label used in the displays.
"""

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    try:
        import Tkinter as tk
        import ttk
    except ImportError:
        print("Missing Tkinter library")
        raise

import time

class Popup(ttk.Label):

    def __init__(self, master):
        ttk.Label.__init__(self, master)
        self.timeout = 0

        self.style = ttk.Style()
        self.style.configure("popupInfo.TLabel", background="yellow")
        self.style.configure("popupWarn.TLabel", background="orange")
        self.style.configure("popupErr.TLabel", background="red", foreground="white")

    def endPopupEvent(self):
        t = int(time.time())
        if t>= self.timeout:
            self.grid_remove()
        else:
            self.after(1000, self.endPopupEvent)

    def info(self, info):
        self.config(text=info, style="popupInfo.TLabel")
        self.timeout = int(time.time())+5
        self.grid()
        self.after(1000, self.endPopupEvent)

    def warn(self, warning):
        self.config(text=warning, style="popupWarn.TLabel")
        self.timeout = int(time.time())+5
        self.grid()
        self.after(1000, self.endPopupEvent)

    def err(self, error):
        self.config(text=error, style="popupErr.TLabel")
        self.timeout = int(time.time())+5
        self.grid()
        self.after(1000, self.endPopupEvent)

