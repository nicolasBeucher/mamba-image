/* Mamba Parallel API SWIG wrapper for python
 * 
 * Copyright (c) <2011>, <Nicolas BEUCHER>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation files
 * (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish, 
 * distribute, sublicense, and/or sell copies of the Software, and to permit 
 * persons to whom the Software is furnished to do so, subject to the following 
 * conditions: The above copyright notice and this permission notice shall be 
 * included in all copies or substantial portions of the Software.
 *
 * Except as contained in this notice, the names of the above copyright 
 * holders shall not be used in advertising or otherwise to promote the sale, 
 * use or other dealings in this Software without their prior written 
 * authorization.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

%module mambaPLCore

/* Inclusion inside the c file wrapper created by swig*/
%{
#include "mambaPLApi.h"
%}

/* standard value typedefs */
/** Unsigned 8 bit value type */
typedef uint8_t Uint8;
/** Unsigned 16 bit value type */
typedef uint16_t Uint16;
/** Unsigned 32 bit value type*/
typedef uint32_t Uint32;
/** Unsigned 64 bit value type */
typedef uint64_t Uint64;
/** Signed 8 bit value type */
typedef int8_t Sint8;
/** Signed 16 bit value type */
typedef int16_t Sint16;
/** Signed 32 bit value type */
typedef int32_t Sint32;
/** Signed 64 bit value type */
typedef int64_t Sint64;

/** grey-scale pixels value type */
typedef uint8_t PIX8;
/** Pixels line pointers type */
typedef PIX8 *PLINE;

/** Signed 32-bit pixels value type */
typedef uint32_t PIX32;
/** 32-bit pixels line pointers type */
typedef PIX32 *PLINE32;

/* Typemaps definition */
%include <typemaps.i>
%include <stdint.i>
%include <exception.i>

%typemap(in) PIX8 * {
    if(PyString_Check($input)) {
        $1 = (PIX8 *) PyString_AsString($input);
    }
    else {
        PyErr_SetString(PyExc_TypeError,"not a string");
        return NULL;
    }
}

%typemap(in,numinputs=0) (PIX8 **outdata, Uint32 *len) (PIX8 * temp, Uint32 len) {
    $1 = &temp;
    $2 = &len;
}
%typemap(argout) (PIX8 **outdata, Uint32 *len) {
    PyObject *o, *o2, *o3;
    
    o = PyString_FromStringAndSize((char *) *$1,*$2);//MB_h*MB_w*4);
    if ((!$result) || ($result == Py_None)) {
        $result = o;
    } else {
        if (!PyTuple_Check($result)) {
            PyObject *o2 = $result;
            $result = PyTuple_New(1);
            PyTuple_SetItem($result,0,o2);
        }
        o3 = PyTuple_New(1);
        PyTuple_SetItem(o3,0,o);
        o2 = $result;
        $result = PySequence_Concat(o2,o3);
        Py_DECREF(o2);
        Py_DECREF(o3);
    }
    /* The data extracted is free*/
    free((Uint32 *) *$1);
}

%apply unsigned long long *OUTPUT {Uint64 *pVolume};

/* the functions and variables wrapped */
%include "MBPL_error.h"
%include "mambaPLApi.h"

/* extending the MB_Image structure with creator and destructor */
%extend MBPL_Image {
    
    /* Image destructor */
    ~MBPL_Image() {
        MBPL_Destroy($self);
    }    
}





