# setup.py
# This is the distutils setup function of Mamba Image library
import distutils
import os
import re
from distutils.core import setup, Extension
import platform

# Functions to extract meta-data
def getVersion(filename):
    for line in open(filename).readlines():
        m = re.search("VERSION\s*=\s*\"([^\"]+)\"", line)
        if m:
            return m.group(1)

################################################################################
# Extension modules and Packages
################################################################################
EXTENSIONS = []
PACKAGES = []

# platform specific compilation defines
if platform.architecture()[0] == '64bit':
    DEF_MACROS = [('BINARY64', None)]
    SWIGDEF64 = ['-DBINARY64']
else:
    DEF_MACROS = []
    SWIGDEF64 = []

# Parallel module and associated packages
#""""""""""""""""""""""""""""""""""""""""

# List of source files
MBPL_API_SWIG = os.path.join("swig","mambaPLApi.i")

MBPL_API_SRC = [
    "MBPL_Context", "MBPL_Create", "MBPL_Transfer", "MBPL_error", "MBPL_Utils",
    "MBPL_LoadExtract", "MBPL_Add", "MBPL_Copy", "MBPL_Volume", "MBPL_ConSet",
    "MBPL_Kernels", "MBPL_InfNb8", "MBPL_And", "MBPL_Inf",
    ]
MBPL_API_SRC.sort() #Compilation in alphabetic order 

files = []
files.append(MBPL_API_SWIG)
for s in MBPL_API_SRC:
    files.append(os.path.join("c", s+".c"))
    
# compiler options
INC_DIRS = ['/usr/local/cuda/include','./cl','./include','./include-private','../../commons']
# swig options
PL_SWIG_OPTS = SWIGDEF64 + ['-I'+v for v in INC_DIRS] + ['-outdir','python/mambaParallel','-threads']

# add it to extensions
EXTENSIONS.append(
        Extension("mambaParallel._mambaPLCore",
                  files, 
                  swig_opts=PL_SWIG_OPTS,
                  include_dirs=INC_DIRS,
                  define_macros=DEF_MACROS,
                  libraries=['OpenCL'])
                 )
PACKAGES = PACKAGES+['mambaParallel']

    
################################################################################
# Meta-data
################################################################################

NAME = "Mamba Parallel"
VERSION = getVersion(os.path.join("python",os.path.join("mambaParallel","parallel.py")))
DESCRIPTION = "An OpenCL implementation of the mamba library"
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
      package_dir = {'': 'python'}
      )
