"""
Display and palette functions.

mambaDisplay contains all the elements allowing to display mamba images
(2D and 3D). The documentation for this package is intended for advanced
users who wish to define their own display.
"""

from . import constants
from .palette import *

################################################################################
# Displayer interface
################################################################################

# Class created to handle the references to all the display windows. The mamba
# image actually don't use a direct call to the display but uses the Displayer
# class _MbDisplayer: instead.
class Displayer:
    """
    This generic class is provided to allow advanced users to define their own
    way to display mamba images. To do so, you must create your own displayer
    class inheriting this one. Then call the setDisplayer function from
    this package like this :
    
        setDisplayer(displayer=your_own_displayer_class)
    
    As an example, you can look into the mambaDisplay package to see the 
    standard displayer provided with mamba based on Tkinter.
    """

    def addWindow(self, im):
        """
        Creates a window for mamba or mamba3D image 'im' (imageMb or image3DMb).
        
        You can access name, palette information and other information related
        to the mamba image object.
        
        The function must return the id of the window (also called its key) 
        that the mamba image (imageMb) will store for later interaction with 
        the display. If an error occurred, returns an empty string.
        """
        return ''
        
    def showWindow(self, wKey, **options):
        """
        Method used to recall and redisplay a window that has been hidden,
        iconified or withdrawn from the screen. 'wKey' indicates the particular
        window to redisplay. 'options' can be used to control specific
        element of the windows. It depends on the displayer.
        
        The function is also called right after the creation of the window. It 
        can be called even if the window was not hidden, iconified or withdrawn.
        """
        pass
        
    def controlWindow(self, wKey, ctrl):
        """
        Method used to control the display of a window identified by 'wKey'. The
        'ctrl' parameter indicates the type of operation to perform. Here are 
        the value the displayer must support :
            - "FREEZE"   : freeze the display so that update will no longer be 
                           possible until the window is unfreezed.
            - "UNFREEZE" : unfreeze the display and automatically update it.
        
        Other controls must be ignored quietly.
        """
        pass
       
    def updateWindow(self, wKey):
        """
        If an event occurred that modified the mamba image associated to window
        'wKey', this method will be called.
        
        For optimization sake, it is advised to disregard calls to this function
        when the concerned window is hidden.
        """
        pass
       
    def hideWindow(self, wKey):
        """
        Method used to hide a window from the screen. 'wKey' indicates the 
        particular window to withdraw.
        
        The function can be called even if the window is already hidden, 
        iconified or withdrawn.
        """
        pass

    def destroyWindow(self, wKey):
        """
        Destroys the window identified by 'wKey'.
        """
        pass
        
    def tidyWindows(self):
        """
        Tidies the display to ensure that all the windows are visible.
        
        In particular, this method is called by the mamba tidyDisplays()
        function.
        """
        pass

###############################################################################
#  Functions for display management and handling

_global_displayer = None

def setDisplayer(displayer):
    """
    Will set the 'displayer' to use.
    Use this function to overrun the default display.
    This will have no effect if you have already displayed images.
    """
    global _global_displayer
    if not _global_displayer:
        _global_displayer = displayer

def getDisplayer():
    """
    Returns the reference to the displayer used by mamba images when they need to
    be displayed.
    """
    global _global_displayer
    if not _global_displayer:
        from . import dftDisplayer
        _global_displayer = dftDisplayer.DftDisplayer()
    return _global_displayer
    
def setMaxDisplay(size):
    """
    Set the maximum 'size' (tuple with w and h) above which the image
    is automatically downsized upon displaying.
    """
    
    constants._MAXW = size[0]
    constants._MAXH = size[1]
    
def setMinDisplay(size):
    """
    Set the minimum 'size' (tuple with w and h) below which the image
    is automatically upsized upon displaying.
    """
    
    constants._MINW = size[0]
    constants._MINH = size[1]
    
def tidyDisplays():
    """
    Tidies the displayed images.
    This function will try to optimize, given the actual screen size, the 
    position of the images so that every one may be visible (not always)
    possible if many images are displayed).
    """
    global _global_displayer
    if not _global_displayer:
        from . import dftDisplayer
        _global_displayer = dftDisplayer.DftDisplayer()
    _global_displayer.tidyWindows()

