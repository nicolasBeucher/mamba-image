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
# The compilation is heavily platform dependant.
# Almost nothing in the C code is common between windows and linux

if platform.system()=='Linux':

    MBRT_DEF_MACROS = []

    MBRT_API_SRC = [
        "MBRT_VideoAcq",
        "MBRT_VideoAcq_v4l2",
        "MBRT_VideoAcq_avc",
        "MBRT_error",
        "MBRT_Display",
        "MBRT_Context",
        "MBRT_Record"
    ]
    MBRT_SRC_DIR = "c-linux"
    MBRT_SRC_EXT = ".c"
    MBRT_SWIG_OPTS = ['-I./include',
                      '-I/usr/include/ffmpeg',
                      '-outdir','python/mambaRealtime']
    MBRT_INC_DIRS = ['./include',
                     '/usr/include/ffmpeg']
    MBRT_LIBS = ['SDL','v4l2','v4l1','avformat','avcodec','swscale']
    MBRT_LIB_DIRS = []
    MBRT_PACKAGE_DATA = {}

elif platform.system()=='Windows':

    MBRT_DEF_MACROS = [('MBRT_WIN',None),
                       ('__STDC_CONSTANT_MACROS',None),
                       ('_CRT_SECURE_NO_WARNINGS',None)]
    MBRT_API_SRC = [
        "MBRT_VideoAcq",
        "MBRT_VideoAcq_dshow",
        "MBRT_VideoAcq_avc",
        "MBRT_error",
        "MBRT_Display",
        "MBRT_Context",
        "MBRT_Record"
    ]
    MBRT_SRC_DIR = "c-win"
    MBRT_SRC_EXT = ".cpp"
    MBRT_SWIG_OPTS = ['-I./include',
                      '-DMBRT_WIN',
                      '-c++',
                      '-outdir','python/mambaRealtime/']
    MBRT_INC_DIRS = ['./include',
                     '../../include',
                     # modify the following lines accordingly
                     'D:/SDL2-2.0.3/include', 
                     'D:/ffmpeg-20141115-git-933eca9-win32-dev/include']
    MBRT_LIBS = ["avcodec","avutil","avformat","swresample","swscale",
                 "ole32","strmiids",
                 "SDL2"]
    MBRT_LIB_DIRS = ["./lib"]
    # Copying all the DLLs found in the lib directory into the mambaRealtime package
    list_dll = glob.glob('lib/*.dll')
    packages_data_dll = []
    for dll in list_dll:
        shutil.copyfile(dll, 'python/mambaRealtime/'+os.path.basename(dll))
        packages_data_dll.append(os.path.basename(dll))
    MBRT_PACKAGE_DATA = {"mambaRealtime":packages_data_dll}

# List of source files for realtime module
MBRT_API_SWIG = os.path.join("swig","mambaRTApi.i")

filesRT = []
filesRT.append(MBRT_API_SWIG)
for s in MBRT_API_SRC:
    filesRT.append(os.path.join(MBRT_SRC_DIR, s + MBRT_SRC_EXT))

# add it to extensions
EXTENSIONS = [
    Extension("mambaRealtime._core",
              filesRT,
              swig_opts=MBRT_SWIG_OPTS,
              include_dirs=MBRT_INC_DIRS,
              define_macros=MBRT_DEF_MACROS,
              libraries=MBRT_LIBS,
              library_dirs=MBRT_LIB_DIRS,
             )
]

PACKAGES = ['mambaRealtime']

################################################################################
# Meta-data
################################################################################

NAME = "Mamba Realtime"
VERSION = getVersion(os.path.join("python",os.path.join("mambaRealtime","__init__.py")))
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
      license = "GPLv3",
      long_description = DESCRIPTION,
      ext_modules = EXTENSIONS,
      packages = PACKAGES,
      package_dir = {'': 'python'},
      package_data = MBRT_PACKAGE_DATA
)
