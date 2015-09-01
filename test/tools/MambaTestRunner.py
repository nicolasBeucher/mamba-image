"""
Module defining the test runner class used by the Mamba Test Platform.
"""

#Copyright (c) <2009>, <Nicolas BEUCHER>

#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation files
#(the "Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish, 
#distribute, sublicense, and/or sell copies of the Software, and to permit 
#persons to whom the Software is furnished to do so, subject to the following 
#conditions: The above copyright notice and this permission notice shall be 
#included in all copies or substantial portions of the Software.

#Except as contained in this notice, the names of the above copyright 
#holders shall not be used in advertising or otherwise to promote the sale, 
#use or other dealings in this Software without their prior written 
#authorization.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys
import time
import unittest

from .MambaTestResult import MambaTestResult
from .MambaTestOutput import ModuleInfo

class MambaTestRunner:
    """A test runner class.
    
    This class objective is to run test modules and store their results then
    allowing to produce a complete report.
    """
    def __init__(self, mtoutput):
        self.playedModules = {}
        self.mtoutput = mtoutput

    def _makeResult(self):
        return MambaTestResult(self.mtoutput)

    def _run(self, test):
        # Runs the given test case or test suite.
        result = self._makeResult()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        return result, timeTaken
        
    def runModule(self, module):
        "runs the tests integrated to the module given into argument"
        __import__(module)
        testMod = sys.modules[module]
        suite = unittest.defaultTestLoader.loadTestsFromModule(testMod)
        name = module #module.split('.')[-1]
        moduleinfo = ModuleInfo(name, testMod.__doc__.strip('\n'))
        self.mtoutput.notifyModuleTestStart(moduleinfo)
        result, moduleinfo.timeTaken = self._run(suite)
        self.mtoutput.printModuleReport(moduleinfo, result)
        self.playedModules[moduleinfo] = result
            
    def produceReport(self, cov=None, morfs=[]):
        """Produces the global report using stored results"""
        self.mtoutput.printGeneralReport(self.playedModules, cov, morfs)
            
