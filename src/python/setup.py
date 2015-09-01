#! /usr/bin/env python
# setup.py
# This is the default distutils setup function of Mamba Image library

import distutils
from distutils.core import setup, Extension
import platform
import os
import glob
import re
import shutil

################################################################################
# Tool functions
################################################################################

# Functions to extract meta-data
def getVersion(filename):
    for line in open(filename).readlines():
        m = re.search("VERSION\s*=\s*\"([^\"]+)\"", line)
        if m:
            return m.group(1)
    return None

################################################################################
# Extension modules and Packages
################################################################################
EXTENSION = [
        Extension("mamba._core",
                  [os.path.join("swig","mambaApi.i")],
                  libraries=['mamba'])
            ]

# List of packages
PACKAGES = ['mamba','mamba3D','mambaShell','mambaDisplay']

# Other elements
package_data = {'mambaShell': ['*.ico','*.bmp']}

if platform.platform().find("Windows")>=0:
    scripts = ['scripts/mamba_post_install.py']
    shutil.copy('../lib/Release/mamba.dll', 'packages/mamba/')
    package_data['mamba'] = ['mamba.dll']
else:
    scripts = []

################################################################################
# Meta-data
################################################################################

NAME = "Mamba Image"
VERSION = getVersion(os.path.join("packages","mamba","__init__.py"))
DESCRIPTION = "A fast and simple mathematical morphology image analysis library for python"
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
      ext_modules = EXTENSION,
      packages = PACKAGES,
      package_dir = {'': 'packages'},
      package_data = package_data,
      scripts = scripts
      )
