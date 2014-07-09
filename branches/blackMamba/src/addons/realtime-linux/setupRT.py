
# setup.py
# This is the distutils setup function of Mamba Image library realtime module
import distutils
import os
import re
from distutils.core import setup, Extension
import platform

# Functions to extract meta-data
# (svn revision used as a patch number definition)
def getVersion(filename):
    for line in open(filename).readlines():
        m = re.search("VERSION\s*=\s*\"([^\"]+)\"", line)
        if m:
            return m.group(1)
    return None
    
################################################################################
# Extension modules and Packages
################################################################################
EXTENSIONS = []
PACKAGES = []

DEF_MACROS = []
SWIGDEF64 = []

# Realtime module and associated package
#"""""""""""""""""""""""""""""""""""""""

# This is the realtime module for linux platforms

# List of source files for realtime module
MBRT_API_SWIG = os.path.join("swig","mambaRTApi.i")

MBRT_API_SRC = [
    "MBRT_VideoAcq","MBRT_VideoAcq_v4l","MBRT_VideoAcq_v4l2","MBRT_VideoAcq_avc",
    "MBRT_error","MBRT_Display","MBRT_Context","MBRT_Record"
    ]
MBRT_API_SRC.sort() #Compilation in alphabetic order 

filesRT = []
filesRT.append(MBRT_API_SWIG)
for s in MBRT_API_SRC:
    filesRT.append(os.path.join("c", s + ".c"))
    
# swig options
RT_SWIG_OPTS = SWIGDEF64+['-I./include',
                            '-I./include-private',
                            '-I../../commons',
                            '-I/usr/include/ffmpeg',
                            '-outdir','python/mambaRealtime']

# add it to extensions
EXTENSIONS.append(
    Extension("mambaRealtime._mambaRTCore",
                filesRT,
                swig_opts=RT_SWIG_OPTS,
                include_dirs=['./include','./include-private','/usr/include/ffmpeg','../../commons'],
                define_macros=DEF_MACROS,
                libraries=['SDL','v4l2','v4l1','avformat','avcodec','swscale'])
                )
PACKAGES = PACKAGES+['mambaRealtime']
    
################################################################################
# Meta-data
################################################################################

NAME = "Mamba Realtime"
VERSION = getVersion(os.path.join("python",os.path.join("mambaRealtime","realtime.py")))
DESCRIPTION = "A realtime module extension for the Mamba library"
AUTHOR = "Nicolas BEUCHER", "nicolas.beucher@ensta.org"
HOMEPAGE = "www.mamba-image.org"

################################################################################
# SETUP FUNCTION
################################################################################

setup(name = NAME,
      author = AUTHOR[0], author_email = AUTHOR[1],
      description = DESCRIPTION,
      version = VERSION,
      url = HOMEPAGE,
      license = "License X11",
      long_description = DESCRIPTION,
      ext_modules = EXTENSIONS,
      packages = PACKAGES,
      package_dir = {'': 'python'},
      )
