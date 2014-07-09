/* Mamba API SWIG wrapper for python*/
 
/*
 * Copyright (c) <2009>, <Nicolas BEUCHER and ARMINES for the Centre de 
 * Morphologie Mathématique(CMM), common research center to ARMINES and MINES 
 * Paristech>
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

%module core

/* Inclusion inside the c file wrapper created by swig*/
%{
#include "mamba/mamba.h"
%}

/* Typemaps definition */
%include <typemaps.i>
%include <stdint.i>
%include <exception.i>

%typemap(in) PIX8 * {

    if(PyBytes_Check($input)) {
        $1 = (PIX8 *) PyBytes_AsString($input);
    }
    else {
        PyErr_SetString(PyExc_TypeError,"not a bytes string");
        return NULL;
    }
}

%typemap(in) Uint32 *ptab {
    if (PyList_Check($input)) {
        int size = PyList_Size($input);
        int i = 0;
        if (size!=256) {
            PyErr_SetString(PyExc_ValueError,"Expecting a list of 256 integer");
            return NULL;
        }
        $1 = (Uint32 *) malloc((size)*sizeof(Uint32));
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyInt_Check(o))
                $1[i] = (Uint32) PyInt_AsLong(PyList_GetItem($input,i));
            else {
                PyErr_SetString(PyExc_TypeError,"list must contain integer");
                free($1);
                return NULL;
            }
        }
    } else {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
    }
}

%typemap(freearg) Uint32 *ptab {
    free((Uint32 *) $1);
}

%typemap(in,numinputs=0) (PIX8 **outdata, Uint32 *len) (PIX8 * temp, Uint32 len) {
    $1 = &temp;
    $2 = &len;
}
%typemap(argout) (PIX8 **outdata, Uint32 *len) {
    PyObject *o, *o2, *o3;
    
    if (*$2>0) {
        o = PyBytes_FromStringAndSize((char *) *$1,*$2);//MB_h*MB_w*4);
        /* The data extracted is free*/
        free((Uint32 *) *$1);
    } else {
        o = Py_None;
    }
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
}

%typemap(in) Uint32 *phisto {
    int i;
    
    if (PyList_Check($input)) {
        int size = PyList_Size($input);
        if (size!=256) {
            PyErr_SetString(PyExc_ValueError,"Expecting a list of 256 integer");
            return NULL;
        }
        i = 0;
        $1 = (Uint32 *) malloc((size)*sizeof(Uint32));
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyInt_Check(o))
                $1[i] = (Uint32) PyInt_AsLong(PyList_GetItem($input,i));
            else {
                PyErr_SetString(PyExc_TypeError,"list must contain integer");
                free($1);
                return NULL;
            }
        }
    } else {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
    }
}

%typemap(argout) Uint32 *phisto {
    PyObject *o, *o1, *o2, *o3;
    int i;
    
    o = PyList_New(256);
    for(i=0;i<256;i++) {
        o1 = PyInt_FromLong((long) $1[i]);
        PyList_SetItem(o,i,o1);
    }
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
}

%apply int *OUTPUT {Sint32 *px, Sint32 *py};
%apply unsigned int *OUTPUT {Uint32 *min, Uint32 *max};
%apply unsigned long long *OUTPUT {Uint64 *pVolume};
%apply unsigned int *OUTPUT {Uint32 *isEmpty};
%apply unsigned int *OUTPUT {Uint32 *pNbobj};
%apply unsigned int *OUTPUT {Uint32 *pixVal};
%apply unsigned int *OUTPUT {Uint32 *ulx, Uint32 *uly, Uint32 *brx, Uint32 *bry};

/* the functions and variables wrapped */
%include "mamba/mamba.h"
%include "mamba/MB_Common.h"
%include "mamba/MB_Error.h"
%include "mamba/MB_Image.h"
%include "mamba/MB_Api.h"
%include "mamba/MB_Api_3D.h"
%include "mamba/MB_Api_neighbors.h"
%include "mamba/MB_Api_hierarchical.h"

/* extending the MB_Image structure with creator and destructor */
%extend MB_Image {
    
    /* Image destructor */
    ~MB_Image() {
        MB_Destroy($self);
    }    
}

/* extending the MB3D_Image structure with creator and destructor */
%extend MB3D_Image {
    
    /* 3D Image destructor */
    ~MB3D_Image() {
        MB3D_Destroy($self);
    }    
}




