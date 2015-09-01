"""
Module defining the result class used by the Mamba Test Platform.
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

import unittest

from .MambaTestOutput import Success, Failure, Error

class MambaTestResult(unittest.TestResult):
    """A test result class that is created to display specific Mamba test information.

    This class main objective is to wrap up TestResult class so that the
    MambaTestOutput instance could be notified for every result or test played.

    Used by MambaTestRunner.
    """

    def __init__(self, output):
        unittest.TestResult.__init__(self)
        self.mtoutput = output
        self.success = []

    def startTest(self, test):
        self.mtoutput.notifyTestStart(test)
        unittest.TestResult.startTest(self, test)

    def addSuccess(self, test):
        self.success.append(test)
        unittest.TestResult.addSuccess(self, test)
        self.mtoutput.notifyTestEnd(test, Success)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.mtoutput.notifyTestEnd(test, Error)

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.mtoutput.notifyTestEnd(test, Failure)
