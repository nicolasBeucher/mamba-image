# Python API reference generating script
#
# This script generates the python API reference for the Mamba library.
# It produces a tex file which is then compiled by pdflatex to produce a PDF
# document.
#
# To make it work, you will need to install a Latex distribution on your 
# computer (such as Miktex for Windows users) and make sure pdflatex program can
# be found in the PATH on your system (try calling it on any command line to make
# sure this is the case). The tool also uses the pydoc script.
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
begin = """\\documentclass[a4paper,10pt,oneside]{article}
\\usepackage{mamba}

\\title{Mamba Image Library Python Reference}
\\author{Automatically generated using pydoc}
\\date\\today

\\begin{document}

\\mambaCover
\\mambaContent

\\section{Introduction}

This document is the Mamba library Python reference.

It applies to version %s.

It gives information regarding all the classes, functions and exceptions defined
in the Python part of the Mamba library. This extends to all the functions
defined in the mamba and mamba3D packages.

The document also gives information regarding the mambaDisplay peripheral module.

This document is intended for reference only. To learn more about Mamba, start
with the Mamba User Manual.
"""

end = "\\end{document}"

################################################################################
# Global variables
################################################################################
VERSION = "Undef"
PROVDOC = 'doc.txt'
OUTDOC = 'mamba-pyref.tex'

################################################################################
# Data representation and utility functions
################################################################################
# Here we stored the information collected in the Python source code (docstring)
# into   a workable class
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
    # Will replace the example using a Python lstset
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
            elif ls=="":
                tidy_desc += "\\end{itemize}\n\n"+ls+"\n"
                in_list = False
            else:
                tidy_desc += ls+"\n"
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
            
    # last line was in an example
    if in_example:
        tidy_desc += "\\end{lstlisting}\n\n"
        
    return tidy_desc

################################################################################
# The module information extraction
################################################################################
# The function parses the pydoc output and produces a tex format of it.
def extractModule(path):
    f = open(path)
    lines = f.readlines()
    f.close()

    sections = {
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
            else:
                if in_section=="NAME" and not sections["NAME"]:
                    # Sections NAME can contain name and short description
                    names = l[4:].split(' - ')
                    sections[in_section] = names[0]
                    if len(names)>1:
                        sections["SHORT_DESCRIPTION"] = names[1].replace('_','\\_')
                elif in_section=="FILE":
                    # Section FILE contains only one information
                    sections[in_section] = l[4:]
                elif in_section=="DESCRIPTION":
                    # The DESCRIPTION can be spreaded along multiple lines
                    # here we concatened all of them
                    sections[in_section] = sections[in_section]+' '+l[4:].replace('_','\\_')
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
    s = "\\section{"+sections["NAME"]+"}\n"
    linesout.append(s)
    s = "\\textbf{"+sections["SHORT_DESCRIPTION"].strip()+"}\n"
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
            meths = k.methods.keys()
            meths.sort()
            for m in meths:
                s = "\\paragraph{"+m+"}\n\n"
                linesout.append(s)
                s = adaptAndtidyDesc(k.methods[m].strip())+"\n\n"
                linesout.append(s)
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
            s = "\\label{fun:"+fn.name.split('(')[0].replace('\\_','')+"}\n"
            linesout.append(s)
            s = adaptAndtidyDesc(fn.desc.strip())+"\n\n"
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
# Getting the version
os.system('%s -c "import mamba; print(mamba.VERSION)" > %s' %(sys.executable, PROVDOC) )
VERSION = open(PROVDOC).readlines()[0].strip()
# Creating the tex file (all the lines)
lines = [begin % (VERSION)]
for f in pyfile_list:
    os.system(sys.executable+' '+pydoc.__file__+' '+f.split('.')[0].replace('/','.').replace('\\','.')+' > '+PROVDOC)
    lines = lines+extractModule(PROVDOC)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay > '+PROVDOC)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay.palette >> '+PROVDOC)
lines = lines+extractModule(PROVDOC)
os.system(sys.executable+' '+pydoc.__file__+' mambaDisplay.extra > '+PROVDOC)
lines = lines+extractModule(PROVDOC)
lines.append(end)
print cwd
# Removing byproducts
os.remove(PROVDOC)
# Writing the final tex file
f = open(OUTDOC,'w')
f.writelines(lines)
f.close()
#Creating the pdf
for i in range(5):
    os.system('pdflatex '+OUTDOC)
