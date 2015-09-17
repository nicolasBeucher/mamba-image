# IDLE specific startup script to create a Mamba Shell

# This file serves two purposes: creating an IDLE shell that is correctly working
# with Mamba (no subprocess) and starting a basic workspace more easily

# You can edit it to fit your own needs
try:
    # Add your import here
    from mamba import *
    from mamba3D import *
    from mambaDisplay import *
except ImportError as excpt:
    print("Error : Mamba could not be imported on your computer")
    print("Please check you have correctly installed it")
    raise ImportError(excpt)

################################################################################
# Demo
################################################################################
# Importing the demo string and defining the demo running function
# Do not modify this part unless you know what you are doing
import mambaShell.demo
from time import sleep
import os
def _runDemo(demo, askGo):
    demoLines = demo.split('\n')
    prevLineWasExec = False
    
    for l in demoLines:
        if l.find(">>>")==0:
            print(l)
            # Code to be executed (waiting a bit after it)
            retval =  eval(l[3:])
            if retval:
                print(retval)
            prevLineWasExec = True
        else:
            if prevLineWasExec:
                if askGo:
                    order = raw_input('#> Press enter to continue (or q then enter to quit)')
                    if order=='q':
                        return
                else:
                    for i in range(2000):
                        sleep(0.001)
            # The line must be displayed
            print(l)
            if not askGo:
                for i in range(len(l)*35):
                    sleep(0.001)
            prevLineWasExec = False
                
def Demo1():
    """
    This is a demo function for the mamba python library.
    """
    f_path = os.path.dirname(getInitFile())+"/demo.bmp"
    _runDemo(mambaShell.demo.demo1 % (f_path), True)

################################################################################
# Some utility functions
################################################################################
# Do not modify this part unless you know what you are doing
def getVersion():
    """
    Returns the version (in a string) of Mamba.
    """
    import mamba as mb
    return mb.VERSION

def getInitFile():
    """
    Returns the file where the default behaviour for mambaShell is defined.
    """
    import mambaShell as mbs
    return mbs.__file__

################################################################################
# Modifiable part
################################################################################

# Modify your welcome message here
print(" ! Welcome to Mamba Image ! ")
print("Version : "+ getVersion())
print("    more information : www.mamba-image.org")
print("")
print("This is an adapted IDLE shell, change in configuration here will")
print("affect your normal IDLE shell.")
print("")
print("This script automatically imports Mamba. Here is the complete")
print("imports performed:")
print("    from mamba import *")
print("    from mamba3D import *")
print("    from mambaDisplay import *")
print("")
print("The following images were created (the [d] indicates that they are")
print("displayed). All these images have the default size (256x256).")
print("    binary    : imbin1[d], imbin2, imbin3, imbin4")
print("    greyscale : im1[d], im2[d], im3, im4")
print("    32-bit    : im32_1[d], im32_2")
print("")
print("A demo tour is accessible by calling : Demo1()")
print("Warning ! This demo will modify im1 and im2")
print("")
print("To modify the default behavior of this program, edit file:")
print("    "+ getInitFile())
print("Feel free to adapt it to your own needs")

# Add your default images here

# Binary images
imbin1 = imageMb(1)
imbin1.show()
imbin1.setName('imbin1')
imbin2 = imageMb(1)
imbin2.setName('imbin2')
imbin3 = imageMb(1)
imbin3.setName('imbin3')
imbin4 = imageMb(1)
imbin4.setName('imbin4')

# Greyscale (8-bit)
im1 = imageMb()
im1.show()
im1.setName('im1')
im2 = imageMb()
im2.show()
im2.setName('im2')
im3 = imageMb()
im3.setName('im3')
im4 = imageMb()
im4.setName('im4')

# 32-bit
im32_1 = imageMb(32)
im32_1.show()
im32_1.setName('im32_1')
im32_2 = imageMb(32)
im32_2.setName('im32_2')

# Tidying the display (ordering the created image to ensure most of them are visible)
tidyDisplays()

