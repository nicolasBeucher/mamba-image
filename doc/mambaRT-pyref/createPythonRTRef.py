# Python Realtime API reference generating script
#
# This script generates the Python API reference for the Mamba Realtime library
# It produces a tex file which is then compiled by pdflatex to produce a PDF
# document.
#
# To make it work, you will need to install a latex distribution on your 
# computer (such as Miktex for Windows users) and make sure pdflatex program can
# be found in the PATH on your system (try calling it on any command line to make
# sure this is the case). The tool also use the pydoc script.
#
# The script must be launched in its correct position inside the mamba source tree
# after a complete build using the distutils setup was performed. The tool will
# use the generated files found in the created build directory (and not previous
# installation on your machine).

#Copyright (c) <2009>, <Nicolas BEUCHER>

#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation files
#(the "Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish, 
#distribute, sublicense, and/or sell copies of the Software, and to permit 
#persons to whom the Software is furnished to do so, subject to the following 
#conditions: The above copyright notice and this permission notice shall be 
#included in all copies or substantial portions of the Software.

#Except as contained in this notice, the names of the above copyright 
#holders shall not be used in advertising or otherwise to promote the sale, 
#use or other dealings in this Software without their prior written 
#authorization.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
# 
import os
import sys
import platform
import glob
import pydoc

################################################################################
# Latex predefined beginning and ending
################################################################################
# For this particular document, the generated tex file is a blend of 
# automatically generated documentation (using docstring and pydoc for the 
# reference part) and hand written documentation (user manual part) which 
# explains the long definitions here.
begin = """\\documentclass[a4paper,10pt,oneside]{article}
\\usepackage{mamba}

\\title{Mamba Realtime Python Reference - %s}
\\author{Automatically generated using pydoc}
\\date\\today

\\begin{document}

\\mambaCover
\\mambaContent

\\section{Introduction}

The Mamba Realtime module is an extension to the Mamba library for Python that 
allows you to test your algorithms in realtime. Images can be acquired dynamically
from your webcam (or any video capture device supported) using the directshow 
API on Windows or Video4Linux2 (with possible support for V4L) on Linux.
Alternatively you can use mambaRealtime to read any supported movie file and
process it with your algorithm. The module then displays the result on your 
screen using the SDL library.

This document gives you the Python functions reference along with the list of
dynamic commands available in the realtime window.

Be warned that, although we tried to make the functions system independent, there
are still some differences between Windows and Linux implementations of this
module (mainly with the initializing function). Make sure the documentation you
are currently reading refers to the system you planned to target, the title 
should provide this information.

See also the restrictions for Windows of this module (does not work on Win64 environment).

This document applies to version %s.

"""

start_tut1 = """
\\section{Getting started : a small example}

To start using the realtime, import the module:

\\lstset{language=Python}
\\begin{lstlisting}
#A from-import is the best way to use the realtime module.
#import works but is really painful to use since the name of the
# module is this long
from mambaRealtime import *
\\end{lstlisting}

The second step is to start the image acquisition and display by either 
capturing them with a supported device or extracting them out of a movie file.

"""
start_tutinit_lin = """
The linux version supports any Video4Linux2 API compatible device (the support 
for V4L is very limited and may not work). Supported movie files are extremely
various and depends on which version of the FFmpeg library is shipped on your 
system but the most commons are likely to be supported.

To launch acquisition and display from your V4L2 device:

\\lstset{language=Python}
\\begin{lstlisting}
# This is assuming your device is "/dev/video0", there are a wide range of
# possibilities here but you must always give the path to a V4L2 supported
# device.
launchRealtime("/dev/video0", V4L2)
\\end{lstlisting}

To launch acquisition and display from your V4L device:

\\lstset{language=Python}
\\begin{lstlisting}
# Again, this is assuming your device is "/dev/video0".
#
# V4L support in mambaRealtime is WEAK and not tested extensively!
# V4L should die anyways so we are not going to bother.
launchRealtime("/dev/video0", V4L)
\\end{lstlisting}

To start playing a movie:

\\lstset{language=Python}
\\begin{lstlisting}
# The tag is AVC because the FFmpeg library is called libavcodec
# You should give a valid path to your movie file as first argument
launchRealtime("/path/to/your/movie", AVC)
\\end{lstlisting}

"""
start_tutinit_win = """
On Windows, any directshow API compatible device will be supported. The 
directshow API is part of directX and should be present by default
on any modern updated 32-bit Windows (XP, Vista, ...). Supported movie files are extremely
various but the most commons are likely to be supported.

To initialize your directshow device:

\\lstset{language=Python}
\\begin{lstlisting}
# Directshow gives a number to each device, starting with 0. If you have 
# many devices, there is actually no possiblity to identify it clearly by a
# name (mambaRealtime lacks it) so you will have to try each number until you 
# reach the correct one. Please also note that unplugging one of your device
# may have the consequence to change the order ... (Yeah I know it sucks).
# The number must be written inside a string.
launchRealtime("0", DSHOW)
\\end{lstlisting}

To start playing a movie:

\\lstset{language=Python}
\\begin{lstlisting}
# The tag is AVC because the FFmpeg library is called libavcodec
# You should give a valid path to your movie file as first argument
launchRealtime("c:/path/to/your/movie", AVC)
\\end{lstlisting}

"""
start_tut2 = """
At this point the mambaRealime module is now working.

\\begin{figure}
\\centering
\\includegraphics[scale=0.4]{mambaRT_win.png}
\\caption{The Realtime window looking at herself (full display)}
\\label{fig:win}
\\end{figure}

This should have opened a new window like \\ref{fig:win} in which you can see 
what your device is actually acquiring such as your smiling face (come on!) in 
front of your webcam.

As you can see, there is no color. By default the mambaRealtime module
acquires and displays greyscale images. If activated, the color option will
enable the module to acquire and display color images.

Once the realtime is active, you can specify a process to apply to the acquired
images. Processes are Python functions with a specific prototype. Refer to the 
documentation of the function setProcessRealtime() (see \\ref{fun:setProcessRealtime}). 
Here are some examples using the mambaComposed gradient function (All these
examples work on greyscale image):

\\lstset{language=Python}
\\begin{lstlisting}
# First import the gradient function
from mambaComposed import gradient

# Setting up a simple gradient as the realtime process
setProcessRealtime(gradient, INSTANT)
\\end{lstlisting}

Here the gradient function was used in a very simple manner similar to this :

\\lstset{language=Python}
\\begin{lstlisting}
# A simple gradient
gradient(imIn, imOut)
\\end{lstlisting}

But we know that the gradient function can take an optional argument modifying
its thickness, like this :

\\lstset{language=Python}
\\begin{lstlisting}
# A 2 pixels thick gradient
gradient(imIn, imOut, 2)
\\end{lstlisting}

In the mambaRealtime module you can specify that optional argument as well :

\\lstset{language=Python}
\\begin{lstlisting}
# Setting up a thick gradient as the realtime process
setProcessRealtime(gradient, INSTANT, 2)
\\end{lstlisting}

Now you have a 2-pixels thick gradient applied to every image extracted from 
your selected source. Let's say you want to apply another algorithm to the
result, like whiteTopHatFilter with 2 as size parameter (not sure it does 
anything interesting but it's for the sake of demonstration):

\\lstset{language=Python}
\\begin{lstlisting}
# Setting up a whiteTopHatFilter on top of the gradient (assuming
# the function was imported previously)
addProcessRealtime(whiteTopHatFilter, 2)
\\end{lstlisting}

For more info on this function see \\ref{fun:addProcessRealtime}.

At one point you are likely to give the mambaRealtime module wrong process 
functions or unsupported ones. In this case, the process will be dismissed and
a small warning logo will be displayed in the top left corner. You can 
obtain the error info using the function:

\\lstset{language=Python}
\\begin{lstlisting}
# Prints the last error that occured in the realtime
print(getErrorRealtime())
\\end{lstlisting}

Eventually, you can close the realtime module by either pressing escape inside
the display window or by calling the function:

\\lstset{language=Python}
\\begin{lstlisting}
# Close the realtime
deactivateRealtime()
\\end{lstlisting}

At this point, you can call back the launch function with other parameters or
acquisition devices/files and it will start again.

There is a bunch of other functions, for recording, palette display and so on.
Check the reference at the end of this document.

"""

commands = """
\\section{Realtime commands}

Once the realtime window is active, you have access to commands that will 
display information, activate palette coloring, activate the process or allow
you to close the window.

\\begin{itemize}

\\item \\textbf{<esc>} closes the realtime acquisition. Once pressed, you must 
reinitialize and reactivate it with the correct functions. If you are
displaying in fullscreen, this command will only leaves the fullscreen mode.

\\item \\textbf{p} toggles the color palette. You should first specify one using
the appropriate function.

\\item \\textbf{c} toggles on/off the color for acquisition and display.

\\item \\textbf{o} toggles on/off the computation process. You should first 
specify one using the appropriate function.

\\item \\textbf{r} displays framerate information in a white bar at the bottom of
the display. If the bar is full, the framerate is equal to the one required (10
by default), half the bar is filled, then the framerate is half the one required
and so on... You can see an example in figure \\ref{fig:win}

\\item \\textbf{h} displays histogram of what is actually displayed. You can see 
an example in figure \\ref{fig:win}. This is only available in greyscale mode.

\\item \\textbf{f} toggles on/off the fullscreen display.

\\item \\textbf{<pause>} toggles on/off the pause.

\\end{itemize}

"""

end = "\\end{document}"

################################################################################
# Global variables
################################################################################
VERSION = "Undef"
PROVDOC = 'doc.txt'
OUTDOC = 'mambaRT-pyref-'+platform.system().lower()[0:3]+'.tex'

################################################################################
# Data representation and utility functions
################################################################################
# Here we stored the information collected in the Python source code (docstring)
# into a workable class
class klass:
    def __init__(self, name):
        self.name = name.replace('_','\\_')
        self.desc = ''
        self.methods = {}
    def fillDesc(self, d):
        self.desc = self.desc+' '+d.replace('_','\\_')
    def addMethod(self, m):
        if m!='':
            m = m.replace('_','\\_')
            self.methods[m] = ''
    def fillMethod(self, m, d):
        if m!='':
            m = m.replace('_','\\_')
            self.methods[m] = self.methods[m]+' '+d.replace('_','\\_')
    def __repr__(self):
        return self.name
        
class func:
    def __init__(self, name):
        self.name = name.replace('_','\\_')
        self.desc = ''
    def fillDesc(self, d):
        self.desc = self.desc+' '+d.replace('_','\\_')
    def __repr__(self):
        return self.name
        
def adaptAndtidyDesc(desc):
    # Will replace the line begining with a * by an itemize list
    # will replace the example using a Python lstset
    tidy_desc = ""
    lines = desc.split('\n')
    
    in_example = False
    in_list = False
    
    for l in lines:
        ls = l.strip()
        if in_example:
            if ls=='':
                tidy_desc += "\\end{lstlisting}\n\n"
                in_example = False
            else:
                tidy_desc += ls.replace("\\_","_") + '\n'
        elif in_list:
            if ls.find("*")==0:
                tidy_desc += "\\item "+ls[1:].strip()+"\n"
            else:
                tidy_desc += "\\end{itemize}\n\n"+ls+"\n"
                in_list = False
        elif ls.find("*")==0:
            tidy_desc += "\\begin{itemize}\n"
            tidy_desc += "\\item "+ls[1:].strip()+"\n"
            in_list = True
        elif ls.find(">>>")==0:
            tidy_desc += "\\lstset{language=Python}\n\\begin{lstlisting}\n"
            tidy_desc += ls.replace("\\_","_") + '\n'
            in_example = True
        else:
            tidy_desc += ls + '\n'
            
    # Last line was in an example
    if in_example:
        tidy_desc += "\\end{lstlisting}\n\n"
        
    return tidy_desc

################################################################################
# The module information extraction
################################################################################
# The function parses the pydoc output and produce a tex format of it.
def extractModule(path):
    f = open(path)
    lines = f.readlines()
    f.close()

    sections = {
                "NAME" : '',
                "FILE" : '',
                "DESCRIPTION" : '',
                "CLASSES" : [],
                "FUNCTIONS" : [],
                "DATA" : []
                }
        
    in_section = ""
    in_klass = False
    for i,l in enumerate(lines):
        l = l.replace('\n','')
        if l!='':
            if i>0 and l[0]!=' ':
                in_section = l
            else:
                if in_section=="NAME" or in_section=="FILE":
                    # Sections NAME and FILE contains only one information
                    sections[in_section] = l[4:]
                elif in_section=="DESCRIPTION":
                    # The DESCRIPTION can be spreaded along multiple lines
                    # here we concatenated all of them
                    sections[in_section] = sections[in_section]+' '+l[4:]
                elif in_section=="CLASSES":
                    # The CLASSES section lists all the classes and their methods
                    sl = l[4:].split(' ')
                    if sl[0]=="class":
                        k = klass(sl[1])
                        sections[in_section].append(k)
                        in_klass = True
                        in_klass_method_list = False
                        m = ''
                    elif in_klass and len(sl)<1:
                        in_klass = False
                    elif in_klass:
                        if l.find("Methods defined here")>=0:
                            in_klass_method_list = True
                        elif not in_klass_method_list:
                            k.fillDesc(l[8:]+'\n')
                        elif in_klass_method_list and len(sl)>3 and sl[3]!='' and l.find('(')>=0:
                            m=l[8:]
                            k.addMethod(m)
                        elif in_klass_method_list and m:
                            k.fillMethod(m, l[12:]+'\n')
                elif in_section=="FUNCTIONS":
                    # Handling the functions
                    if len(l)>4 and l[4]!=' ':
                        fn = func(l[4:])
                        sections[in_section].append(fn)
                    elif len(l)>=8:
                        fn.fillDesc(l[8:]+'\n')
        
    #Begin
    linesout = []

    # Module name and description
    s = "\\section{API Reference}\n"
    linesout.append(s)
    s = sections["DESCRIPTION"].strip()+"\n\n"
    linesout.append(s)

    # Classes
    if sections["CLASSES"]!=[]:
        s = "\\subsection{Classes}\n\n"
        linesout.append(s)
        for k in sections["CLASSES"]:
            s = "\\subsubsection{"+k.name+"}\n"
            linesout.append(s)
            s = adaptAndtidyDesc(k.desc.strip())+"\n\n"
            linesout.append(s)
#            meths = k.methods.keys()
#            meths.sort()
#            for m in meths:
#                s = "\\paragraph{"+m+"}\n\n"
#                linesout.append(s)
#                s = adaptAndtidyDesc(k.methods[m].strip())+"\n\n"
#                linesout.append(s)
            linesout.append('\n')
        linesout.append('\n')

    # Functions
    if sections["FUNCTIONS"]!=[]:
        s = "\\subsection{Functions}\n\n"
        linesout.append(s)
        linesout.append('\n')
        for fn in sections["FUNCTIONS"]:
            s = "\\subsubsection{"+fn.name+"}\n"
            linesout.append(s)
            s = "\\label{fun:"+fn.name.split('(')[0]+"}\n"
            linesout.append(s)
            s = adaptAndtidyDesc(fn.desc.strip())+"\n\n"
            linesout.append(s)
    
    return linesout

################################################################################
# Main script
################################################################################
# First moving to where the sources can be found
cwd = os.getcwd()
print(cwd)
if platform.system()=='Windows':
    os.chdir(glob.glob('../../src/mambaAddons-restricted/realtime-win/build/lib*/')[0])
    start_tut = start_tut1 + start_tutinit_win + start_tut2 
else:
    os.chdir(glob.glob('../../src/mambaAddons-restricted/realtime-linux/build/lib*/')[0])
    start_tut = start_tut1 + start_tutinit_lin + start_tut2 
# The file to document
pyfile_list = ['mambaRealtime/realtime.py']
# Setting up the python path to find mamba.py
os.environ["PYTHONPATH"] = glob.glob(cwd+'/../../src/mambaApi/build/lib*/')[0]
# Getting the version
os.system('%s -c "import mambaRealtime; print(mambaRealtime.VERSION)" > %s' %(sys.executable, PROVDOC) )
VERSION = open(PROVDOC).readlines()[0].strip()
# Creating the tex file (all the lines)
lines = [begin % (platform.system(), VERSION), start_tut, commands]
for f in pyfile_list:
    os.system(sys.executable+' '+pydoc.__file__+' '+f.split('.')[0].replace('/','.').replace('\\','.')+' > '+PROVDOC)
    lines = lines+extractModule(PROVDOC)
lines.append(end)
# Removing byproducts and returning to the original directory
os.remove(PROVDOC)
del(os.environ["PYTHONPATH"])
os.chdir(cwd)
# Writing the final tex file
f = open(OUTDOC,'w')
f.writelines(lines)
f.close()
# Creating the pdf
for i in range(5):
    os.system('pdflatex '+OUTDOC)
