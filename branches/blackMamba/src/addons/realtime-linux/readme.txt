Mamba Realtime for Linux

Release 1.1.1

====================================================================
Mamba Realtime
====================================================================

Contents
--------

+ Introduction
+ History
+ License information
+ Build instructions and know how

--------------------------------------------------------------------
Introduction
--------------------------------------------------------------------

The Mamba Realtime module is an extension to the Mamba library for Python that 
allows you to test your algorithms in realtime images.

Realtime images acquisition or production can be done with any supported webcam
using video 4 linux 2 or either with a movie file (via the FFmpeg API). The 
display is done with the SDL library.

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

Currently two versions of this module exist. One for Windows platform and 
another for Linux platform. This document is related to the Linux platform 
version.
  
--------------------------------------------------------------------
License
--------------------------------------------------------------------

WARNING : Previous version (0.1) of the realtime module was released under a x11
like license, starting with 0.2 this is NO LONGER the case. New versions of the
module uses some FFmpeg library functions that are released under the GPL
license. The  mamba realtime module is thus "contaminated" with the GPL.

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
