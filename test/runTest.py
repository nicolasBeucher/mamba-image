#!/usr/bin/env python
"""
This is the Mamba Test Platform main entry.

This script can be used to launch the unitary test for Mamba.
This tool uses the Python module unittest to run tests

Usage:
    python runTest.py <options>
    options :
        -h or --help displays this short description
        -v <n> selects the verbosity level of the output 
        (0 to 2 (most), default is 0)
        -c activates code coverage (needs package coverage)
        -t <testModule> plays the specified test module.
        If not specified, the script will play all the tests.
        -d <directory> specifies the test directory to be used. Several 
        directories can be specified by repeating this option.
        If not specified, all the tests will be performed.
        -o or --output <file> specifies the file in which the report will be
        written (by default on the standard output)
        
visit www.mamba-image.org for more.
    
Copyright (c) <2009>, <Nicolas BEUCHER>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Softwared, and to permit 
persons to whom the Software is furnished to do so, subject to the following 
conditions: The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

Except as contained in this notice, the names of the above copyright 
holders shall not be used in advertising or otherwise to promote the sale, 
use or other dealings in this Software without their prior written 
authorization.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import sys
import getopt
import glob

from tools.MambaTestRunner import MambaTestRunner
from tools.MambaTestOutputText import MambaTestOutputText
from tools.MambaTestOutputHtml import MambaTestOutputHtml

version = 0.1

################################################################################
# Global variables
################################################################################
_mb_runner = None
_mb_output = None
_testModule = None
_coverageOn = False
_verbose = 0
_fpath = ''
_ftype = ''

DEFAULT_TEST_DIRECTORIES = ['testmamba', 'testmamba3D', 'testmambaDisplay']
TEST_DIRECTORIES = []

################################################################################
# Functions
################################################################################

def playAllTests():
    """
    Play all the tests defined for the Mamba Test Platform.
    """
    global _mb_runner
    
    script_files = {}
    
    if _mb_runner:
        for directory in TEST_DIRECTORIES:
            file_list = os.listdir(directory)
            file_list.sort()
            script_files[directory] = file_list

        for directory, file_list in script_files.items():
            for f in file_list:
                name, ext = os.path.splitext(f)
                if name!='__init__' and ext=='.py':
                    _mb_runner.runModule(directory+'.'+name)

def playSelectedTest(testModule):
    """
    Play the tests given by its name in 'testModule'.
    
    If the module is not found directly, the function will search for it
    inside the test directories.
    """
    global _mb_runner
    
    if _mb_runner:
        try:
            _mb_runner.runModule(testModule)
            return
        except ImportError:
            pass

        # In case of an import error, we will try to 
        # search for the modules inside the test directories
        found = False
        for directory in TEST_DIRECTORIES:
            try:
                td = __import__(directory+'.'+testModule)
            except ImportError:
                pass
            else:
                # Test module found
                found = True
                print("Found test module \"%s\" in %s ! " % (testModule, directory))
                del(td)
                _mb_runner.runModule(directory+'.'+testModule)
                break
            
        if not found:
            print("test module %s not found !" % (testModule))
            sys.exit(1)

################################################################################
# Parsing the command line options and running the test
################################################################################
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hcv:t:o:d:', ["help","output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(str(err)) # will print something like "option -a not recognized"
    print(__doc__)
    sys.exit(2)
    
for o, a in opts:
    if o == "-v":
        # verbose option must be an integer
        try:
            _verbose = int(a)
        except ValueError:
            print("verbose parameter incorrect (must be an integer): fall back to 0")
            _verbose = 0
    elif o in ("-o", "--output"):
        # An output is specified
        _fpath = a
        _ftype = os.path.splitext(_fpath)[-1]
    elif o in ("-h", "--help"):
        print(__doc__)
        sys.exit()
    elif o == "-c":
        # Coverage is activated (only if package coverage can be activated)
        try:
            from coverage import coverage
            _cov = coverage(cover_pylib=True)
            _coverageOn = True
        except ImportError:
            print("Package coverage cannot be found : disabling code coverage")
            _coverageOn = False
    elif o == "-t":
        _testModule = a
    elif o == "-d":
        TEST_DIRECTORIES.append(a)
    else:
        print(__doc__)
        sys.exit()
        
# Falling back to default directories if no one was provided
if TEST_DIRECTORIES==[]:
    TEST_DIRECTORIES = DEFAULT_TEST_DIRECTORIES

# The output generator is selected accordingly to the given options
if _fpath and _ftype=='.txt':
    _mb_output = MambaTestOutputText(stream=_fpath, verbosity=_verbose)
elif _fpath and _ftype=='.html':
    _mb_output = MambaTestOutputHtml(_fpath, verbosity=_verbose)
else:
    _mb_output = MambaTestOutputText(verbosity=_verbose)

# Running the Mamba Test Runner with selected verbosity on the selected tests
if _coverageOn:
    _cov.start()
    
# Verifying that the mamba module is present and selecting the file to 
# "cover"
_morfs = []
try:
    
    if 'testmamba' in TEST_DIRECTORIES:
        import mamba as mb
        dirname = os.path.dirname(mb.__file__)
        _morfs += glob.glob(os.path.join(dirname, '*.py'))
        _morfs.remove(os.path.join(dirname, 'core.py'))
        del(mb)
    if 'testmamba3D' in TEST_DIRECTORIES:
        import mamba3D as mb3D
        dirname = os.path.dirname(mb3D.__file__)
        _morfs += glob.glob(os.path.join(dirname, '*.py'))
        del(mb3D)
except ImportError:
    print("mamba module not found !")
    sys.exit(1)
    
# Launching the tests
_mb_runner = MambaTestRunner(_mb_output)
if _testModule:
    playSelectedTest(_testModule)
else:
    playAllTests()
if _coverageOn:
    _cov.stop()
    _mb_runner.produceReport(_cov, _morfs)
else:
    _mb_runner.produceReport()
