# Python API quick reference generating script
#
# This script generates the python API quick reference for the Mamba library.
# It produces a tex file which is then compiled by pdflatex to produce a PDF
# document.
#
# To make it work, you will need to install a latex distribution on your 
# computer (such as Miktex for Windows users) and make sure pdflatex program can
# be found in the PATH on your system (try calling it on any command line to make
# sure this is the case). The tool also use the pydoc script.
#
# The script must be launched in its correct position inside the mamba source tree.
# Mamba needs to be installed on your system for the script to work.

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
import glob
import pydoc

################################################################################
# Latex predefined beginning and ending
################################################################################
begin = r"""
\documentclass[a4paper,10pt,oneside]{article}
\usepackage[top=2.5cm, bottom=3cm, left=0.5cm, right=0.5cm]{geometry}
\usepackage{setspace}
\usepackage{multirow}
\usepackage{multicol}
\usepackage{pifont}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{tikz}

\setlength{\headheight}{2cm}
\setlength{\topmargin}{-2.35cm}
\setlength{\headsep}{0.35cm}
\setlength{\textheight}{730pt}
\setlength{\parskip}{0.15cm}
\newlength{\nodewidth}
\setlength{\nodewidth}{0.95\textwidth}

\def\mambaVersion{%s}

\definecolor{mambaLightBg}{HTML}{6FADE9}
\definecolor{mambaBg}{HTML}{408AD2}
\definecolor{mambaTextFg}{HTML}{FFC640}
\definecolor{modfg}{HTML}{408AD2}
\definecolor{modfgspe}{HTML}{802080}
\definecolor{parts}{HTML}{0040A0}
\definecolor{partsspe}{HTML}{701070}
\definecolor{classfg}{HTML}{E78F05}
\definecolor{deffg}{HTML}{8D1405}
\definecolor{lightb}{HTML}{A0A0FF}
\definecolor{purple}{HTML}{802080}

\usetikzlibrary{calc}
\tikzstyle{module}=[minimum width=\textwidth, text width=\nodewidth, rectangle, fill=white, rounded corners]
\tikzstyle{modulespe}=[minimum width=\textwidth, text width=\nodewidth, rectangle, fill=purple, rounded corners]

\fancypagestyle{mambaQuickPageStyle}{
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
    \pagecolor{mambaLightBg}
    \fancyhead[C]{
        \begin{tikzpicture}[overlay, remember picture]
        \draw ($(current page.north west)$)
          node[below right, minimum width=\paperwidth, minimum height=2.3cm, anchor=north west, rectangle, fill=mambaBg, text width=\paperwidth-2cm]
        {\includegraphics[height=1.7cm]{mamba_logo.pdf}};
        \end{tikzpicture}
        \begin{tabular*}{\textwidth}{ @{ \extracolsep{\fill} } lr}
        & \textcolor{mambaTextFg}{\large{\textbf{mamba API quick reference}}} \\
        & \textcolor{mambaTextFg}{for version \mambaVersion}
        \end{tabular*}
    }
    \fancyfoot[C]{
        \begin{tikzpicture}[overlay, remember picture]
        \draw ($(current page.south west)$)
          node[above right, minimum width=\paperwidth, minimum height=1cm, anchor=south west, rectangle, fill=mambaBg]
        {\begin{tabular*}{\textwidth}{ @{ \extracolsep{\fill} } lr}
        \textcolor{white}{\textbf{\thepage}} & \textcolor{white}{\textbf{www.mamba-image.org}}
        \end{tabular*}};
        \end{tikzpicture}
    }
}

\pagestyle{mambaQuickPageStyle}

\newcommand{\modName}[1]{
    \textcolor{modfg}{
        \rule{1ex}{1ex}\hspace{1ex}\textsc{Module : }\textbf{#1}
    }
    \vspace{0.2cm}
}

\newcommand{\modNameSpe}[1]{
    \textcolor{modfgspe}{
        \rule{1ex}{1ex}\hspace{1ex}\textsc{Module : }\textbf{#1}
    }
    \vspace{0.2cm}
}

\newcommand{\pkgName}[1]{
    \textcolor{modfg}{
        \rule{1ex}{1ex}\hspace{1ex}\textsc{Package : }\textbf{#1}
    }
    \vspace{0.2cm}
}

\newcommand{\pkgNameSpe}[1]{
    \textcolor{modfgspe}{
        \rule{1ex}{1ex}\hspace{1ex}\textsc{Package : }\textbf{#1}
    }
    \vspace{0.2cm}
}

\newcommand{\className}[1]{
    \textcolor{classfg}{
        \footnotesize{\textbf{#1}}
    }
}

\newcommand{\defp}{\textcolor{deffg}{\textbf{def }}}

\newenvironment{modDesc}
{\scriptsize\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.3cm}}

\newenvironment{classSec}
{\small\textcolor{parts}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Class :}}\\\vspace{0.1cm}\scriptsize\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.2cm}}

\newenvironment{classSecSpe}
{\small\textcolor{partsspe}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Class :}}\\\vspace{0.1cm}\scriptsize\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.2cm}}

\newenvironment{methodList}
{\tiny\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.1cm}}

\newenvironment{funcSec}
{\small\textcolor{parts}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Functions :}}\\\vspace{0.1cm}\scriptsize\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.2cm}}

\newenvironment{funcSecSpe}
{\small\textcolor{partsspe}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Functions :}}\\\vspace{0.1cm}\scriptsize\begin{spacing}{0}}
{\end{spacing}\normalsize\vspace{0.2cm}}

\begin{document}
\begin{center}

"""

general_infos = r"""

\begin{tikzpicture}
\node[module] {
\begin{minipage}{\nodewidth}
\begin{multicols}{2}
\begin{flushleft}

\textcolor{modfg}{\rule{1ex}{1ex}\hspace{1ex}\textsc{General}}\vspace{0.2cm}

\small\textcolor{parts}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Grid and Edge:}}

\scriptsize
Mamba can work with two grids : \textbf{HEXAGONAL} and \textbf{SQUARE}.

The \textbf{DEFAULT\_GRID} is used by the function when no other grid is
specified. Its value, HEXAGONAL at start, can be changed with the appropriate 
function.

Mamba3D can work with three grids : \textbf{CUBIC}, \textbf{FACE\_CENTER\_CUBIC}
and \textbf{CENTER\_CUBIC}. Only the first two are supported by the C 
operators.

The \textbf{DEFAULT\_GRID3D} is used by the function when no other grid is
specified. Its value, FACE\_CENTER\_CUBIC at start, can be changed with the
appropriate function.

Two edge behaviors are defined : \textbf{EMPTY} and \textbf{FILLED}.

\small\textcolor{parts}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Directions/Neighbors:}}

\scriptsize
Here is the encoding used for Mamba grids:
\begin{center}
\begin{tabular}{cc}
hexagonal grid & square grid \\
\includegraphics[width=0.3\columnwidth]{../mamba-um/figures/hexa_grid.pdf} &
\includegraphics[width=0.3\columnwidth]{../mamba-um/figures/square_grid.pdf} \\
\end{tabular}
\end{center}
\normalsize

\small\textcolor{parts}{\rule{1ex}{1ex}\hspace{1ex}\textsc{Structuring elements:}}

\scriptsize
By default Mamba defines seven structuring elements:
\begin{center}
\includegraphics[width=0.6\columnwidth]{../mamba-um/figures/se.pdf}
\end{center}

\scriptsize
By default Mamba3D defines four structuring elements:

\textbf{CUBOCTAHEDRON} which is based on the FACE\_CENTER\_CUBIC grid,
\textbf{CUBE2X2X2} and \textbf{CUBE3X3X3} both based on the CUBIC grid,
and finally \textbf{CUBOCTAHEDRON\_BIS} which is based on the 
CENTER\_CUBIC grid.

\vspace{1cm}

\end{flushleft}
\end{multicols}
\end{minipage}
};
\end{tikzpicture}

\pagebreak

"""

end = r"""

\begin{tikzpicture}
\node[modulespe] {
\begin{minipage}{\nodewidth}
\begin{multicols}{2}
\begin{flushleft}

\color{white}

\rule{1ex}{1ex}\hspace{1ex}\textsc{Displays shortcuts}\vspace{0.2cm}

\small\rule{1ex}{1ex}\hspace{1ex}\textsc{Keyboard:}

\scriptsize

\begin{itemize}
\item \textbf{P}: will circle through all the available palettes.
\item \textbf{Z} and \textbf{A}: will zoom in/out in 2D displays (basic, 
projection, player ...)
\item \textbf{B} and \textbf{N}: With 32-bit images, these keys will allow you
to move through byte planes or to show the complete image downscaled.
\item \textbf{Control-F}: will freeze/unfreeze the display. See the freeze() 
method.
\item \textbf{Control-R}: will reset the display to its original size and
zoom value.
\item \textbf{Control-V}: will copy any image stored inside the clipboard 
in your image (only works on 2D images on Windows platforms).
\item \textbf{F1}: on a 3D image display, will switch to mode PROJECTION.
\item \textbf{F2}: on a 3D image display, will switch to mode VOLUME
RENDERING if you have VTK python bindings available on your computer.
\item \textbf{F3}: on a 3D image display, will switch to mode PLAYER.
\item \textbf{F5}: on a 3D image display, will update the display with
the image content. Similar to the method update.
\item \textbf{Space} : will start/stop the player in the 3D image display
PLAYER mode.
\item \textbf{Page-Up} : will display the next image in the sequence in the
3D image display PLAYER mode.
\item \textbf{Page-Down} : will display the previous image in the sequence
in the 3D image display PLAYER mode.
\end{itemize}

\small\rule{1ex}{1ex}\hspace{1ex}\textsc{Mouse:}

\scriptsize

\begin{itemize}
\item \textbf{scrolling} : will zoom in/out in 2D displays (basic, 
projection, player ...)
\item \textbf{motion+Control} : will allow to move through the image
in the 3D image display PROJECTION mode.
\end{itemize}

\end{flushleft}
\end{multicols}
\end{minipage}
};
\end{tikzpicture}


\end{center}
\end{document}
"""

################################################################################
# Global variables
################################################################################
VERSION = "Undef"
PROVDOC = 'doc.txt'
OUTDOC = 'mamba-pyquickref.tex'

################################################################################
# Data representation
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
            
################################################################################
# The module information extraction
################################################################################
# The function parses the pydoc output and produces a tex format of it.
# In the case of the quick reference, this format is particular (only the
# function names and signature are used)
def extractModule(path, special=False):
    f = open(path)
    lines = f.readlines()
    f.close()

    sections = {
                "TYPE" : '',
                "NAME" : '',
                "FILE" : '',
                "SHORT_DESCRIPTION" : '',
                "DESCRIPTION" : '',
                "CLASSES" : [],
                "FUNCTIONS" : [],
                "DATA" : []
                }
        
    in_section = ""
    in_klass = False
    in_klass_method_list = False
    in_klass_method_inherited = False
    for i,l in enumerate(lines):
        l = l.replace('\n','')
        if l!='':
            if i>0 and l[0]!=' ':
                in_section = l
            elif not sections["TYPE"] and l.find("Help on ")>=0:
                sections["TYPE"] = l.split(" ")[2]
            else:
                if in_section=="NAME" and not sections["NAME"]:
                    # sections NAME can contain name and short description
                    names = l[4:].split(' - ')
                    sections[in_section] = names[0]
                    if len(names)>1:
                        sections["SHORT_DESCRIPTION"] = names[1].replace('_','\\_')
                elif in_section=="FILE":
                    # section FILE contains only one information
                    sections[in_section] = l[4:]
                elif in_section=="DESCRIPTION":
                    # The DESCRIPTION can be spreaded along multiple lines
                    # here we concatened all of them
                    sections[in_section] += ' '+l[4:].replace('_','\\_')
                elif in_section=="CLASSES":
                    # The CLASSES section lists all the classes and their methods
                    sl = l[4:].split(' ')
                    if sl[0]=="class":
                        k = klass(sl[1])
                        sections[in_section].append(k)
                        in_klass = True
                        in_klass_method_list = False
                        in_klass_method_inherited = False
                        m = ''
                    elif in_klass and len(sl)<1:
                        in_klass = False
                    elif in_klass:
                        if l.find("Methods defined here")>=0:
                            in_klass_method_list = True
                        elif l.find("Methods inherited from")>=0:
                            in_klass_method_inherited = True
                        elif not in_klass_method_list and not in_klass_method_inherited:
                            k.fillDesc(l[8:])
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
    s = "\\begin{tikzpicture}\n"
    linesout.append(s)
    s = "\\node[module] { \n"
    linesout.append(s)
    s = "\\begin{minipage}{\\nodewidth}\n"
    linesout.append(s)
    s = "\\begin{multicols}{2}\n"
    linesout.append(s)
    s = "\\begin{flushleft}\n\n"
    linesout.append(s)
    
    if sections["TYPE"]=="package" and special:
        s = "\\pkgNameSpe{"+sections["NAME"]+"}\n\n"
    elif sections["TYPE"]=="package":
        s = "\\pkgName{"+sections["NAME"]+"}\n\n"
    elif special:
        s = "\\modNameSpe{"+sections["NAME"]+"}\n\n"
    else:
        s = "\\modName{"+sections["NAME"]+"}\n\n"
    linesout.append(s)
    
    s = "\\begin{modDesc}\n"
    linesout.append(s)
    s = "\\textbf{"+sections["SHORT_DESCRIPTION"].strip()+"}\n"
    linesout.append(s)
    s = sections["DESCRIPTION"].strip()+"\n"
    linesout.append(s)
    s = "\\end{modDesc}\n\n"
    linesout.append(s)

    # Classes
    if sections["CLASSES"]!=[]:

        if special:
            s = "\\begin{classSecSpe}\n\n"
        else:
            s = "\\begin{classSec}\n\n"
        linesout.append(s)
        for k in sections["CLASSES"]:
            s = "\\className{"+k.name+"}\n"
            linesout.append(s)
            s = "\\begin{methodList}\n"
            linesout.append(s)
            meths = k.methods.keys()
            meths.sort()
            for m in meths:
                s = "\\ding{70} "+m+"\\newline\n"
                linesout.append(s)
            s = "\\end{methodList}\n\n"
            linesout.append(s)
        if special:
            s = "\\end{classSecSpe}\n\n"
        else:
            s = "\\end{classSec}\n\n"
        linesout.append(s)

    # Functions
    if sections["FUNCTIONS"]!=[]:

        if special:
            s = "\\begin{funcSecSpe}\n"
        else:
            s = "\\begin{funcSec}\n"
        linesout.append(s)
        for fn in sections["FUNCTIONS"]:
            s = "\defp "+fn.name+":\\newline\n"
            linesout.append(s)
        if special:
            s = "\\end{funcSecSpe}\n\n"
        else:
            s = "\\end{funcSec}\n\n"
        linesout.append(s)
    
    s = "\\end{flushleft}\n"
    linesout.append(s)
    s = "\\end{multicols}\n"
    linesout.append(s)
    s = "\\end{minipage}\n"
    linesout.append(s)
    s = "};\n"
    linesout.append(s)
    s = "\\end{tikzpicture}\n\n"
    linesout.append(s)
    
    return linesout

################################################################################
# Main script
################################################################################
# First moving to where the sources can be found
# Listing all the interesting Python sourcesand returning to the original directory
cwd = os.getcwd()
os.chdir('../../src/python/packages')
mod_mb = glob.glob(os.path.join('mamba','[!_]*.py')) # __init__.py is not catch
mod_mb.remove(os.path.join('mamba','utils.py'))
mod_mb.remove(os.path.join('mamba','error.py'))
mod_mb.sort()
mod_mb3D = glob.glob(os.path.join('mamba3D','[!_]*.py')) # __init__.py is not catch
mod_mb3D.sort()
os.chdir(cwd)
# The file to document
pyfile_list = mod_mb + mod_mb3D
# getting the version
os.system('%s -c "import mamba; print(mamba.VERSION)" > %s' %(sys.executable, PROVDOC) )
VERSION = open(PROVDOC).readlines()[0].strip()
# Creating the tex file (all the lines)
lines = [begin % (VERSION)]
for f in pyfile_list:
    os.system(sys.executable+' '+pydoc.__file__+' '+f.split('.')[0].replace('/','.').replace('\\','.')+' > '+PROVDOC)
    lines = lines+extractModule(PROVDOC)
lines.append(general_infos)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay > '+PROVDOC)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay.palette >> '+PROVDOC)
lines = lines+extractModule(PROVDOC, special=True)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay.extra > '+PROVDOC)
lines = lines+extractModule(PROVDOC, special=True)
lines.append(end)
# Removing byproducts
os.remove(PROVDOC)
# writing the final tex file
f = open(OUTDOC,'w')
f.writelines(lines)
f.close()
#creating the pdf
for i in range(5):
    os.system('pdflatex '+OUTDOC)
