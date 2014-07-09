
__version__ = "$Revision: 599 $"

# setup.py
# This is the distutils setup function of Mamba Image library realtime module
import distutils
import os
import re
import glob
import shutil
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

DEF_MACROS = [('__STDC_CONSTANT_MACROS',None),('_CRT_SECURE_NO_WARNINGS',None)]
SWIGDEF64 = []

# Realtime module and associated package
#"""""""""""""""""""""""""""""""""""""""

# This version of the module works only for Windows platform

# List of source files for realtime module
MBRT_API_SWIG = os.path.join("swig","mambaRTApi.i")

MBRT_API_SRC = [
    "MBRT_VideoAcq", "MBRT_VideoAcq_dshow", "MBRT_VideoAcq_avc",
    "MBRT_error",
    "MBRT_Display",
    "MBRT_Context", "MBRT_Record"
    ]
MBRT_API_SRC.sort() #Compilation in alphabetic order 

filesRT = []
filesRT.append(MBRT_API_SWIG)
for s in MBRT_API_SRC:
    filesRT.append(os.path.join("c", s + ".cpp"))
    
# swig options
RT_SWIG_OPTS = SWIGDEF64+['-I./include',
                          '-I./include-private',
                          '-I../../commons',
                          '-c++',
                          '-outdir','python/mambaRealtime/']

# adding it to extensions
EXTENSIONS.append(
    Extension("mambaRealtime._mambaRTCore",
                filesRT,
                swig_opts=RT_SWIG_OPTS,
                include_dirs=['./include',
                            '../../commons',
                            'D:/SDL-1.2.14/include', #<-modify this line accordingly
                            'D:/ffmpeg-r26400-swscale-r32676-mingw32-shared-dev/include', #<-modify this line accordingly
                            './include-private'],
                libraries=["kernel32","user32","gdi32","winspool","comdlg32",
                           "advapi32","shell32","ole32","oleaut32","uuid",
                           "odbc32","odbccp32","strmiids","SDL","SDLmain",
                           "avcodec","avutil","avformat","swscale"],
                library_dirs=['./lib'],
                define_macros=DEF_MACROS)
                )
PACKAGES = PACKAGES+['mambaRealtime']

# Copying all the DLLs found in the lib directory into the mambaRealtime package
list_dll = glob.glob('lib/*.dll')
packages_data_dll = []
for dll in list_dll:
    shutil.copyfile(dll, 'python/mambaRealtime/'+os.path.basename(dll))
    packages_data_dll.append(os.path.basename(dll))

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
      package_dir = {'mambaRealtime': 'python/mambaRealtime'},
      package_data = {'mambaRealtime': packages_data_dll}
      )
