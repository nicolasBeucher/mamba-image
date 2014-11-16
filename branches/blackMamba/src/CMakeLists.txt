
# CMake file for the Mamba library

# Copyright (c) <2014>, <Nicolas BEUCHER and ARMINES for the Centre de 
# Morphologie Mathématique(CMM), common research center to ARMINES and MINES 
# Paristech>

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to permit 
# persons to whom the Software is furnished to do so, subject to the following 
# conditions: The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.

# Except as contained in this notice, the names of the above copyright 
# holders shall not be used in advertising or otherwise to promote the sale, 
# use or other dealings in this Software without their prior written 
# authorization.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
  message(FATAL_ERROR "You cannot build Mamba in its source tree, create a new
directory and run cmake from there")
endif()

cmake_minimum_required(VERSION 2.8)
project(Mamba C)

include("GNUInstallDirs")
include("FindPythonInterp")

################################################################################
# Core mamba library

# 64bit processor always support SSE2, no need to ask
# Restricting the option to 32 bit proc
if(CMAKE_SIZEOF_VOID_P EQUAL 4)
    option (USE_SSE2 
            "Compile using the SSE2 instruction set" ON)
    add_definitions(-DVECTOR_32BIT)

    if(${USE_SSE2})
        if(MSVC)
            add_definitions(-D__SSE2__)
        elseif(UNIX)
            add_definitions(-msse2)
        endif(MSVC)
    endif(${USE_SSE2})
endif()

add_definitions(-DMB_BUILD)

file(COPY ${PROJECT_SOURCE_DIR}/include
     DESTINATION ${PROJECT_BINARY_DIR})
include_directories("${PROJECT_BINARY_DIR}/include")

file(GLOB MAMBA_SRCS "${PROJECT_SOURCE_DIR}/c-std/*.c")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR})

add_library(mamba SHARED ${MAMBA_SRCS})

if(NOT WIN32)
    install(TARGETS mamba
            DESTINATION ${CMAKE_INSTALL_LIBDIR})
    install(DIRECTORY "${PROJECT_SOURCE_DIR}/include/mamba"
            DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endif(NOT WIN32)

################################################################################
# Python library
set( SELECTED_PYTHON_EXECUTABLE ${PYTHON_EXECUTABLE} CACHE FILEPATH "*Python executable to use")

file(COPY ${PROJECT_SOURCE_DIR}/python
     DESTINATION ${PROJECT_BINARY_DIR})
     
if(NOT WIN32)
    add_custom_target(python ALL ${SELECTED_PYTHON_EXECUTABLE} ${PROJECT_BINARY_DIR}/python/setup.py build_ext
                        --swig-opts=\"-I${PROJECT_BINARY_DIR}/include -outdir packages/mamba -threads\"
                        -lmamba
                        -L${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}
                        -I${PROJECT_BINARY_DIR}/include
                      DEPENDS mamba
                      WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/python
                      COMMENT "Generating the python packages")
    add_custom_target(python_install ${SELECTED_PYTHON_EXECUTABLE} ${PROJECT_BINARY_DIR}/python/setup.py install
                      DEPENDS python
                      WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/python
                      COMMENT "Installing the python packages")
    add_custom_target(python_clean ${SELECTED_PYTHON_EXECUTABLE} ${PROJECT_BINARY_DIR}/python/setup.py clean -a
                      WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/python
                      COMMENT "Cleaning the python packages")
else(NOT WIN32)
    add_custom_target(python ALL ${SELECTED_PYTHON_EXECUTABLE} ${PROJECT_BINARY_DIR}/python/setup.py build_ext
                        --swig-opts=\"-I${PROJECT_BINARY_DIR}/include -outdir packages/mamba -threads\"
                        -lmamba
                        -L${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}/Release
                        -I${PROJECT_BINARY_DIR}/include
                      bdist_wininst
                        --install-script=mamba_post_install.py
                        --bitmap=${PROJECT_SOURCE_DIR}/../doc/style/mamba_logo.bmp
                      DEPENDS mamba
                      WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/python
                      COMMENT "Generating the python installer")
endif(NOT WIN32)
