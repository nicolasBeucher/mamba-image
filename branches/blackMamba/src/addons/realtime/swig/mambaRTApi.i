/* Mamba API SWIG wrapper for Python
 *
 *
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

/* Inclusion inside the C file wrapper created by swig*/
%{
#include "mambaRTApi.h"
%}

/* Typemaps definition */
%include <typemaps.i>
%include <stdint.i>

%typemap(in) Uint32 *icon {
    if (PyList_Check($input)) {
        int size = PyList_Size($input);
        int i = 0;
        $1 = (Uint32 *) malloc((size)*sizeof(Uint32));
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyLong_Check(o)) {
                $1[i] = (Uint32) PyLong_AsUnsignedLong(PyList_GetItem($input,i));
            } else if(PyInt_Check(o)) {
                $1[i] = (Uint32) PyInt_AsLong(PyList_GetItem($input,i));
            }else {
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

%typemap(freearg) Uint32 *icon {
    free((Uint32 *) $1);
}

%typemap(in) Uint8 *palette {
    if (PyList_Check($input)) {
        int size = PyList_Size($input);
        int i = 0;
        if (size!=768) {
            PyErr_SetString(PyExc_ValueError,"Expecting a list of 768 integer");
            return NULL;
        }
        $1 = (Uint8 *) malloc((size)*sizeof(Uint8));
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyInt_Check(o))
                $1[i] = (Uint8) PyInt_AsLong(PyList_GetItem($input,i));
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

%typemap(freearg) Uint8 *palette {
    free((Uint8 *) $1);
}

%typemap(in,numinputs=0) MBRT_eventcode *event_code(MBRT_eventcode event_code) {
    $1 = &event_code;
}
%typemap(argout) MBRT_eventcode *event_code {
    PyObject *o, *o2, *o3;
    
    o = PyInt_FromLong((long) *$1);
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

%apply int *OUTPUT {int *acq_w, int *acq_h};
%apply double *OUTPUT {double *ofps};

/* the functions and variables wrapped */
%include "mambaRTApi.h"

%init %{
    if(MBRT_Initialize() != MBRT_NO_ERR)
    {
        PyErr_SetString(PyExc_ImportError, "Initialization of MBRT failed.");
        return;
    }
%}

