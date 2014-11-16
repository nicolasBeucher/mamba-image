Mamba Realtime for Linux/Windows

Release 2.0

====================================================================
Mamba Realtime
====================================================================

Contents
--------

+ Introduction
+ History
+ License
+ Build instructions and know how

--------------------------------------------------------------------
Introduction
--------------------------------------------------------------------

The Mamba Realtime module is an extension to the Mamba library for Python that 
allows you to test your algorithms in realtime images.

Realtime images acquisition or production can be done with any supported webcam
(using video 4 linux 2 on Linux or directshow on Windows) or either with a
movie file (via the FFmpeg API). The display is done with the SDL library.

--------------------------------------------------------------------
History
--------------------------------------------------------------------

The Mamba library allows you to develop easily and rapidly applications based on 
mathematical morphology algorithms. 

Most of the time you will test and try your ideas on static images to make sure 
that your algorithm is working correctly and efficiently. However, as good as 
this approach might be, it still lacks something when you want to confront your 
algorithm to "dynamic real life situation", meaning noise, unpredictable 
movement, fast input, etc ... that your algorithm will have to handle to 
efficiently work in a realtime situation.

The Mamba Realtime was built to help you test these situations easily without 
having to recode your algorithm in another language.

--------------------------------------------------------------------
License
--------------------------------------------------------------------

WARNING : Previous version (0.1) of the realtime module was released under a x11
like license, this is NO LONGER the case. The new versions of the module uses
some FFmpeg library functions that are released under the GPL license. The 
Mamba realtime module is thus "contaminated" with the GPL.

The module code is still released under the X11 license (see sources) meaning 
that you can do pretty much what you want as long as you do not compile it with
the FFmpeg functions released under GPL. However we do not provide a list of
said functions as it is unclear for us.

You will find an example of the GPL v3 license in the file license.txt.

--------------------------------------------------------------------
Build instructions and know how
--------------------------------------------------------------------

Compilation is ensured by distutils.

You will need the following tools :

# Linux ############################################################

 * GNU C Compiler (GCC) version 4.4.4 or later
 * Swig version 1.3.33 or later.
 * SDL library version 1.2.13 (or later)
 * libv4l2 library version 0.7.91 (or later)
 * FFmpeg libraries (libavcodec, libavformat, libswscale, ...) : mambaRealtime
was compiled successfully using version 0.7.1. Some functions call or define
constant could be deprecated with newer version.

Type :

python setupRT.py build_ext bdist

it will compile and create a "dist" directory where you will find a package 
containing the newly build module. To install type :

python setupRT.py install

If it does not work, you may have to tamper with the include directories in the
Python setup script to replace the default value with the corresponding one on
your system.

# Windows #########################################################

 * Microsoft Visual C++ Express 2008 edition (free, only requires inscription)
 * Swig version 1.3.33 or later.
 * SDL library version 2.0.3(or later) for visual C++ (you can find it at 
 www.libsdl.org)
 * The stdint.h and inttypes.h header files for visual C++ (which is not 
 shipped by Microsoft, don't ask me why). You can find them at
 http://msinttypes.googlecode.com/
 * FFmpeg builds for Windows. you can find them at http://ffmpeg.zeranoe.com/builds/
 or visit www.ffmpeg.org (These builds are under GPL)

Make sure Python and Swig binaries are in your PATH environnement variable.

First step is to put the stdint.h and inttypes.h header files into you current
visual C++ include directory. Should be something like this :

C:\Program Files\Microsoft Visual Studio 9.0\VC\include

You should have obtained from the SDL website a zip package containing all the SDL 
libraries and header files built for visual C++. Unzip it anywhere on your PC. 
Then edit the file setup.py in the sources files and change the following lines
with the correct include path to your SDL files.

    MBRT_INC_DIRS = ['./include',
                     '../../include',
                     # modify the following lines accordingly
                     'C:/Devel/SDL2-devel-2.0.3-VC/SDL2-2.0.3/include', 
                     'C:/Devel/ffmpeg-20140829-git-4c92047-win64-dev/include']
                            
Now copy the content of the directory lib/x86 or lib/x64 of your SDL directory
(should look something like SDL2-2.0.3/lib) into the lib directory of the
mambaRealtime module sources.

From the FFmpeg build website, download the shared and dev 7z 
packages of the latest build for your architecture.
Extract them on your computer. As well as for the SDL library you will
need to edit the setup.py script to indicate where are the include files
of the FFmpeg library (the include directory is extracted 
from the dev package). Then you will need to copy inside the lib directory
of the mambaRealtime module some DLLs and lib files. The DLLs you will need 
are in the bin/ directory extracted from the shared package. You need the
avcodec, avformat, avutil, swresample and swscale DLLs (their name are
extended with the current version). Now produce the corresponding lib files
using the def found in the dev package and the procedure described in
https://www.ffmpeg.org/platform.html#Linking-to-FFmpeg-with-Microsoft-Visual-C_002b_002b.

Then to perform the compilation, open a command Window and browse to the 
directory where you put the realtime module sources files. Type :

python setup.py build_ext bdist_wininst

it will compile and create a "dist" directory where you will find an exe 
installer for the realtime module. Double click to install.

The installer created will contain all the DLLs and your new mambaRealtime module.
