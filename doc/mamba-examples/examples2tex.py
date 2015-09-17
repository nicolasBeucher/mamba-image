#!/usr/bin/env python

# This script automatically generates latex source file from examples found
# in the examples directory of the sources.

#Copyright (c) <2014>, <Nicolas BEUCHER>

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
import glob
import re

################################################################################
# Human sorting
################################################################################
def alphanum_key(s): 
    """
    Key function for sort
    """
    return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s)]

################################################################################
# Data representation
################################################################################
# The example class is a storage facility for all the extracted info
class ExampleInfo:
    def __init__(self, path):
        self.path = os.path.dirname(path)
        sp = os.path.split(self.path)
        self.name = sp[1].replace("_"," ")
        self.title = ""
        self.desc = ""
        self.src = ""
        self.inIm = []
        self.outIm = []
    def _tidy(self, text):
        # Correcting all the mishap in text that can be digest by latex
        text = text.replace("_","\\_")
        return text
    def setTitle(self, title):
        self.title += self._tidy(title)
    def setDesc(self, desc):
        self.desc += self._tidy(desc)
    def setSrc(self, src):
        self.src += src
    def inImage(self, inImage):
        self.inIm.append(inImage)
    def outImage(self, outImage):
        self.outIm.append(outImage)
    def generateTex(self):
        s  = "\n"
        s += "\\subsection{"+self.title+"}\n"
        s += "\n"
        s += self.desc
        s += "\n"
        if self.inIm:
            s += "\\begin{figure}[h]\n"
            s += "\\centering\n"
            s += "\\begin{tabular}{"+len(self.inIm)*"c"+"}\n"
            imline = ""
            nameline = ""
            for im in self.inIm:
                imline += "\\includegraphics[width=0.25\\textwidth]{"+os.path.join(self.path,im).replace("\\","/")+"} &"
                nameline += self._tidy(im) + " &"
            s += imline.strip("&") + "\\\\ \n"
            s += nameline.strip("&") + "\\\\ \n"
            s += "\\end{tabular}\n"
            #s += "\\caption{Input image(s) of "+self.name+"}\n"
            s += "\\end{figure}\n"
            s += "\n"
        if self.outIm:
            s += "\\begin{figure}[h]\n"
            s += "\\centering\n"
            s += "\\begin{tabular}{"+len(self.outIm)*"c"+"}\n"
            imline = ""
            nameline = ""
            for index, im in enumerate(self.outIm):
                imline += "\\includegraphics[width=0.25\\textwidth]{"+os.path.join(self.path,im).replace("\\","/")+"} &"
                nameline += self._tidy(im) + " &"
                if index%3==2:
                    s += imline.strip("&") + "\\\\ \n"
                    s += nameline.strip("&") + "\\\\ \n"
                    imline = ""
                    nameline = ""
            if index%3!=2:
                s += imline.strip("&") + "\\\\ \n"
                s += nameline.strip("&") + "\\\\ \n"
            s += "\\end{tabular}\n"
            #s += "\\caption{Output image(s) of "+self.name+"}\n"
            s += "\\end{figure}\n"
            s += "\n"
        s += "Here is the source code for this example (can be found in "+self.name+"):\n"
        s += "\n"
        s += "\\lstset{language=Python}\n"
        s += "\\begin{lstlisting}\n"
        s += self.src
        s += "\\end{lstlisting}\n"
        s += "\n"
        s += "\\pagebreak\n"
        s += "\n"
        return s
        

################################################################################
# Main script
################################################################################
# Getting the example files list
exampleListEasy = glob.glob('../../examples/Easy/*/*.py')
exampleListEasy.sort(key=alphanum_key)
exampleListMod = glob.glob('../../examples/Moderate/*/*.py')
exampleListMod.sort(key=alphanum_key)
exampleListAdv = glob.glob('../../examples/Advanced/*/*.py')
exampleListAdv.sort(key=alphanum_key)
examples = [
    ("Easy", exampleListEasy),
    ("Moderate", exampleListMod),
    ("Advanced", exampleListAdv)
]

# the output tex file
texOutput = """
\\documentclass[a4paper,10pt,oneside]{article}
\\usepackage[table]{xcolor}
\\usepackage{mamba}

\\title{Mamba Image Examples}
\\author{Nicolas BEUCHER \\and Serge BEUCHER}
\\date{\\today}

\\begin{document}

\\mambaCover
\\mambaContent

\\section{Regarding examples}
\\label{cha:regarding}

This document presents some examples that you can retrieve in the examples
directory of the source files.

There are three types of examples regrouped in the following sections:
\\begin{enumerate}
\item \\textbf{easy}: These are mainly intended for beginners so they could refer
to some basic examples to start their own code.
\\item \\textbf{moderate}: In these examples, more elaborated actions are performed
and presented. They cover usage that may not be difficult to do provided that you
read the documentation, but are more easily explained and understood with an
example.
\\item \\textbf{advanced}: These are more complex examples that should be considered
as demonstrators of the capabilities of the Mamba library.
\\end{enumerate}

\\warnBox{
Examples presented here may not correctly work. We tried to put a wide range of
examples and produced this small selection after some efforts (some of them are
non-trivial) but we may have broke them in the process of publishing them. If
it so happens, try to see this as an exercise or e-mail us.
}

\\pagebreak
"""

# For each example, reading its header info
#  - Title
#  - Description
#  - Images IN and OUT if there are ones
for diff,exampleList in examples:
    texOutput += "\\section{"+diff+"}\n"
    for example in exampleList:
        print(example)
        exaInf = ExampleInfo(example)
        exaf = open(example)
        lines = exaf.readlines()
        exaf.close()
        inDesc = False
        inSrc = False
        inTitle = False
        for l in lines:
            lc = l.replace('\n','').strip()
            if lc=="" and not inSrc:
                inDesc = False
                inSrc = False
                inTitle = False
            elif inTitle:
                exaInf.setTitle(lc[2:])
            elif inDesc:
                exaInf.setDesc(l[2:])
            elif inSrc:
                exaInf.setSrc(l)
            elif lc[:4]=="# IN":
                for im in lc.split(' ')[2:]:
                    exaInf.inImage(im)
            elif lc[:5]=="# OUT":
                for im in lc.split(' ')[2:]:
                    exaInf.outImage(im)
            elif lc[:8]=="## TITLE":
                inTitle = True
            elif lc[:14]=="## DESCRIPTION":
                inDesc = True
            elif lc[:9]=="## SCRIPT":
                inSrc = True
        texOutput += exaInf.generateTex()

texOutput += "\\end{document}\n"

f = open("mamba-examples.tex","w")
f.write(texOutput)
f.close()
#Creating the pdf
for i in range(3):
    os.system('pdflatex mamba-examples.tex')
