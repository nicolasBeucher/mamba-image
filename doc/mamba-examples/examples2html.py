#!/usr/bin/env python

# This script automatically generates html source file from examples found
# in the examples directory of the sources.

#Copyright (c) <2011>, <Nicolas BEUCHER>

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
from PIL import Image
import shutil

################################################################################
# The difficulty dictionary
################################################################################
dif_dict = {
    "E" : "Easy",
    "M" : "Moderate",
    "A" : "Advanced"
}

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

    _py_keywords = ["and", "del", "for", "is", "raise", "as",
                    "assert", "elif", "from", "lambda", "return",
                    "break", "else", "global", "not", "try",
                    "class", "except", "if", "or", "while",
                    "continue", "exec", "import", "pass", "yield",
                    "def", "finally", "in", "print"]

    def __init__(self, path):
        self.file = os.path.basename(path)
        self.dir = os.path.relpath(os.path.dirname(path),"../../examples")
        sp = os.path.split(self.dir)
        self.name = sp[1].replace("_"," ")
        self.id = sp[1]
        self.title = ""
        self.desc = ""
        self.src = ""
        self.inIm = []
        self.outIm = []
        self.pyparse_inStr1 = False
        self.pyparse_inStr2 = False
        self.pyparse_inStr3 = False
        self.pyparse_inStr4 = False
        
    def _tidy(self, text):
        # Correcting all the mishap in text that can be digest by latex
        text = text.replace("<","&lt;")
        return text
    def setTitle(self, title):
        self.title += self._tidy(title)
    def setDesc(self, desc):
        self.desc += self._tidy(desc)
    def setSrc(self, src):
        self.src += src.replace('\r','')
    def inImage(self, inImage):
        self.inIm.append(inImage)
    def outImage(self, outImage):
        self.outIm.append(outImage)
        
    def processCodeLine(self, line):
        # Parse a python line code to add syntax color
        line = self._tidy(line)
        outLine = ""
        word = ""
        inComment = False
        fun_name_exp = False
        
        if self.pyparse_inStr1:
            outLine += '<span class="st">'
        if self.pyparse_inStr2:
            outLine += '<span class="st">'
        if self.pyparse_inStr3:
            outLine += '<span class="st">'
        if self.pyparse_inStr4:
            outLine += '<span class="st">'
            
        for i,c in enumerate(line):
            if not inComment and not self.pyparse_inStr1 and not self.pyparse_inStr2 and not self.pyparse_inStr3:
                if c=='#':
                    inComment = True
                    outLine += '<span class="c">'
                    word = ""
                elif c=='"':
                    if line[i-2:i+1]=='"""':
                        self.pyparse_inStr3 = True
                    else:
                        self.pyparse_inStr1 = True
                    outLine += '<span class="st">'
                    word = ""
                elif c=="'":
                    if line[i-2:i+1]=="'''":
                        self.pyparse_inStr4 = True
                    else:
                        self.pyparse_inStr2 = True
                    outLine += '<span class="st">'
                    word = ""
                elif c==' ' or c==':':
                    if self._py_keywords.count(word)>0:
                        outLine = outLine[:-len(word)]+'<span class="kw">'+word+'</span>'
                    if word=="def":
                        fun_name_exp = True
                    word = ""
                elif c=='(' and fun_name_exp:
                    outLine = outLine[:-len(word)]+'<span class="fn">'+word+'</span>'
                    word = ""
                    fun_name_exp = False
                else:
                    word += c
                
                    
            elif self.pyparse_inStr1:
                if c=='"':
                    self.pyparse_inStr1 = False
                    c += '</span>'
                    
            elif self.pyparse_inStr2:
                if c=="'":
                    self.pyparse_inStr2 = False
                    c += '</span>'
                    
            elif self.pyparse_inStr3:
                if line[i-2:i+1]=='"""':
                    self.pyparse_inStr3 = False
                    c += '</span>'
                    
            elif self.pyparse_inStr4:
                if line[i-2:i+1]=="'''":
                    self.pyparse_inStr4 = False
                    c += '</span>'
                    
            outLine += c
            
        if inComment:
            outLine += '</span>'
        if self.pyparse_inStr1:
            outLine += '</span>'
        if self.pyparse_inStr2:
            outLine += '</span>'
        if self.pyparse_inStr3:
            outLine += '</span>'
        if self.pyparse_inStr4:
            outLine += '</span>'
        
        return outLine
        
    def generateHTML(self):
        s  = '<h1>'+self.title+'</h1>\n'
        s += '<p>'+self.desc+' '
        sp = os.path.join(self.dir,self.file)
        s += '(<a href="./examples/'+sp+'">script</a>)</p>\n'
        if self.inIm:
            s += '<table class="images_in">\n'
            tl1 = '<tr>\n'
            tl2 = '<tr>\n'
            for im in self.inIm:
                imp = os.path.join(self.dir,im)
                tl1 += '    <td><a href="./examples/'+imp+'">'
                tl1 += '    <img class="img_ex_in" alt="'+self.name+'" src="./examples/'+imp+'" /></a></td>\n'
                tl2 += '    <td class="legend">'+im+'</td>\n'
            s += tl1+'</tr>\n'+tl2+'</tr>\n</table>\n'
        if self.outIm:
            s += '<table class="images_out">\n'
            tl1 = '<tr>\n'
            tl2 = '<tr>\n'
            for index, im in enumerate(self.outIm):
                imp = os.path.join(self.dir,im)
                tl1 += '    <td><a href="./examples/'+imp+'">'
                tl1 += '<img class="img_ex_out" alt="'+self.name+'" src="./examples/'+imp+'" /></a></td>\n'
                tl2 += '    <td class="legend">'+im+'</td>\n'
                if index%3==2:
                    s += tl1+'</tr>\n'+tl2+'</tr>\n'
                    tl1 = '<tr>\n'
                    tl2 = '<tr>\b'
            if index%3!=2:
                s += tl1+'</tr>\n'+tl2+'</tr>\n'
            s += '</table>\n'
        s += '<div class="python">\n'
        s += '<pre>\n'
        lines = self.src.split('\n')
        for i,l in enumerate(lines):
            s += '<span class="no">%3d</span> %s\n' % (i+1,self.processCodeLine(l))
        s += '</pre>\n'
        s += '</div>\n'
        return s.replace("'","\\'")
        
################################################################################
# HTML header and footer
################################################################################
# header 

_html_header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="fr" xml:lang="fr">
<head>
    <title>Mamba Image : Examples</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="./mamba.css" />
    <script src="./javascripts/jquery.js" type="text/javascript"></script>
    
<script language="JavaScript" type="text/javascript">
<!--
"""

_html_body = """

function selectExample(level)
{
    var j=0;
    
    s = "<table><tr>";
    for(var i=0; i<exampleList.length; i++) {
        
        if ((exampleList[i][0]==level) || (level<0)) {
            j++;
            s = s + '<td><a class="Erequest" id="'+exampleList[i][1]+'">';
            if (exampleList[i][3]!='') {
                s = s + '<img class="expreview" title="'
                s = s + exampleList[i][2]
                s = s + '" alt="'+exampleList[i][2]+'" src="'+exampleList[i][3]+'" />';
            } else {
                s = s + '<div class="expreview" ';
                s = s + 'title="'+exampleList[i][2]+'"></div>';
            }
            s = s + '</a></td>';
            if (j==8) {
                s = s+'</tr><tr>';
                j = 0;
            }
        }
    }
    s = s + '</tr></table>';
    
    $( "#exlist" ).html( s );
}

function requestExample(exname) {
    var jqxhr = $.ajax( "./examples_list.php?example="+exname )
      .done(function( msg ) {
        $( "#exbox" ).html(msg);
        $( "html,body" ).animate({scrollTop: $("#exbox").offset().top}, 'slow');
      })
      .fail(function() {
      })
      .always(function() {
      });
}

$( document ).ready(function() {
    $( "#exmenu").html("<ul><li><a id='EX'>Easy</a></li><li><a id='MX'>Moderate</a></li><li><a id='AX'>Advanced</a></li><li><a id='ALL'>All</a></li></ul>");
    $( "a#EX" ).click(function() {
        selectExample(0);
    });
    $( "a#MX" ).click(function() {
        selectExample(1);
    });
    $( "a#AX" ).click(function() {
        selectExample(2);
    });
    $( "a#ALL" ).click(function() {
        selectExample(-1);
    });
    selectExample(-1);
    $( "a.Erequest" ).click(function() {
        requestExample($(this).attr("id"));
    });
});

// -->
</script>
</head>

<body>

<div id="content">

<div id="header">
</div> <!-- header -->

<div id="menu">
   <ul>
      <li><a id="index" href="./index.html"></a></li>
      <li><a href="./examples.html">Examples</a></li>
      <li><a href="./doc.html">Documentation</a></li>
      <li><a href="./download.html">Download</a></li>
   </ul>
</div> <!-- menu -->

<div id="main">

<div id="exinfo"> <!-- info regarding examples -->
    <h1><a name="top"></a>Regarding examples</h1>
    <p>All the examples in this section are meant to give you an overview of the 
       possibilities given by the Mamba Library. They can be used as a starting 
       point for coding your own applications.<br />
       To understand them, we strongly recommand you to read the user manual which
       is available in the <a href="./doc.html">documentation page</a>.</p>
    <p>Examples can also be downloaded in <a href="./docs/2.0/mamba-examples.pdf">pdf format</a>.</p>
    <p>There are three types of examples :</p>
    <ul>
        <li> <b>Easy</b>: These are mainly intended for beginners so they could refer
            to some basic examples to start their own code.</li>
        <li> <b>Moderate</b>: In these examples, more elaborated actions are performed
            and presented. They cover usage that may not be difficult to do provided that you
            read the documentation, but are more easily explained and understood with an
            example.</li>
        <li> <b>Advanced</b>: These are more complex examples that should be considered
            as demonstrators of the capabilities of the Mamba library.</li>
    </ul>

    <p>Examples presented here may not correctly work. We tried to put a wide 
       range of examples and produced this small selection after some efforts 
       (some of them are non-trivial) but we may have broken them in the process
       of publishing them. If it so happens, try to see this as an exercise or
       e-mail us.
    </p>
</div>

<div id="exmenu">
    <noscript>
    <p>To be able to see the examples, you must have javascript enabled in your
       browser.
    </p>
    </noscript>
</div> <!-- exmenu -->

<div id="exlist">
</div> <!-- exlist -->

<div id="exbox" class="example"></div>

</div> <!-- main -->

</div> <!-- content -->
</body>
</html>
"""

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

# For each example, reading its header info
#  - Title
#  - Description
#  - Images IN and OUT if there are ones
exaInfList = []
for diff,exampleList in examples:
    for example in exampleList:
        print(example)
        exaInf = ExampleInfo(example)
        exaInf.difficulty = diff
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
        exaInfList.append(exaInf)
    
# Generating the list of examples and the icon images
try:
    os.mkdir("examples_icons")
except:
    shutil.rmtree("examples_icons")
    os.mkdir("examples_icons")
diff_level = {"Easy" : 0, "Moderate":1, "Advanced":2}
jsdata= []
for exaInf in exaInfList:
    im = Image.open(os.path.join("..","..","examples",exaInf.dir,exaInf.outIm[-1]))
    im = im.resize((100,100), Image.ANTIALIAS)
    im.save("examples_icons/"+exaInf.id+".jpg")
    jsdata.append([diff_level[exaInf.difficulty], exaInf.id, exaInf.title, "./examples_icons/"+exaInf.id+".jpg"])

# the output files
# html
htmlOutput = _html_header
htmlOutput += "var exampleList = "+repr(jsdata)+"\n"
htmlOutput += _html_body
f = open("examples.html","w")
f.write(htmlOutput)
f.close()
# php
phpOutput = "<?php\n\n";
for exaInf in exaInfList:
    phpOutput += "$examples['"+exaInf.id+"'] = '\n"+exaInf.generateHTML()+"';\n\n"
phpOutput += "echo $examples[$_GET['example']];\n"
phpOutput += "\n"
phpOutput += "?>\n"
f = open("examples_list.php","w")
f.write(phpOutput)
f.close()
