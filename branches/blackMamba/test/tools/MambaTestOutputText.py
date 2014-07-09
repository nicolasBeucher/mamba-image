"""
Module defining the class used to display and generate output in text format
(either in the standard output or in a file) for the Mamba Test Platform.
"""

from .MambaTestOutput import *
import sys

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

# Some definition for readability
big_sep = 80*'#'
sml_sep = 80*'-'

################################################################################
# Class for text output
################################################################################
class MambaTestOutputText(MambaTestOutput):
    """
    This class implements a text output generator for the Mamba Test Platform.
    """
    
    def __init__(self, stream=sys.stdout, descriptions=1, verbosity=0):
        """
        Creator with level of verbosity, descriptions allowed, and file used
        to collect the produced output.
        
        By default, description are on and the output is not verbose. sys.stdout
        is used as default file.
        """
        MambaTestOutput.__init__(self, descriptions, verbosity)
        if isinstance(stream, str):
            self.selfOpenStream = True
            try:
                path = stream
                self.stream = open(path, 'w')
            except:
                self.selfOpenStream = False
                print("Cannot open %s : fall back to stdout" % (path))
                self.stream = sys.stdout
        else:
            self.selfOpenStream = False
            self.stream = stream
        
    def notifyModuleTestStart(self, moduleInfo):
        """Notifies the beginnig of a module test."""
        if self.showAll:
            self.stream.write("\n"+big_sep+"\n")
            self.stream.write(moduleInfo.name+" : \n")
            self.stream.write('\t'+moduleInfo.desc.split('\n')[0]+'\n')
            self.stream.write(big_sep+"\n")
        elif self.dots:
            self.stream.write("\n"+moduleInfo.name+" : \n")
        else:
            self.stream.write(moduleInfo.name+" : ")
        self.stream.flush()

    def _getDescription(self, test):
        # returns the descriptions associated with a test
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)
        
    def notifyTestStart(self, test):
        """Notifies the beginning of a test."""
        if self.showAll:
            self.stream.write(self._getDescription(test)+" ... ")
            self.stream.flush()
        
    def notifyTestEnd(self, test, result):
        """Notifies the end of a test with its result."""
        if result==Success:
            if self.showAll:
                self.stream.write("ok\n")
            elif self.dots:
                self.stream.write(".")
        elif result==Error:
            if self.showAll:
                self.stream.write("ERROR\n")
            elif self.dots:
                self.stream.write("E")
        elif result==Failure:
            if self.showAll:
                self.stream.write("FAIL\n")
            elif self.dots:
                self.stream.write("F")
        self.stream.flush()
                
    def _printErrors(self, moduleResult):
        # Prints all the errors and failures of a given result for the report
        if self.dots or self.showAll:
            self.stream.write("\n")
        for test, err in moduleResult.errors:
            self.stream.write("\n"+sml_sep+"\n")
            self.stream.write("ERROR: %s\n" % (self._getDescription(test)))
            self.stream.write("%s\n" % err)
        for test, err in moduleResult.failures:
            self.stream.write("\n"+sml_sep+"\n")
            self.stream.write("FAILURE: %s\n" % (self._getDescription(test)))
            self.stream.write("%s\n" % err)
        
    def printModuleReport(self, moduleInfo, moduleResult):
        """
        Produces a report for the played module. 
        'moduleInfo' contains the name, description and time taken for the tests.
        'moduleResult' is an instance of MambaTestResult produced for the given 
        module.
        """
        self._printErrors(moduleResult)
        run = moduleResult.testsRun
        if self.showAll:
            self.stream.write(sml_sep+"\n")
            self.stream.write("Ran %d test%s in %.3fs\n" % (run, run != 1 and "s" or "", moduleInfo.timeTaken))
            self.stream.write(sml_sep+"\n")
            if not moduleResult.wasSuccessful():
                self.stream.write("FAILED (")
                failed, errored = map(len, (moduleResult.failures, moduleResult.errors))
                if failed:
                    self.stream.write("failures=%d" % failed)
                if errored:
                    if failed: self.stream.write(", ")
                    self.stream.write("errors=%d" % errored)
                self.stream.write(")\n")
            else:
                self.stream.write("OK\n")
            self.stream.write(sml_sep+"\n")
        else:
            self.stream.write("Ran %d test%s in %.3fs" % (run, run != 1 and "s" or "", moduleInfo.timeTaken))
            if not moduleResult.wasSuccessful():
                self.stream.write(" - FAILED\n")
            else:
                self.stream.write(" - OK\n")
        
    def printGeneralReport(self, playedModules, cov=None, morfs=[]):
        """
        Produces a complete report associated with a MambaTestRunner instance.
        All the modules played, their results and other information are displayed.
        """
        if self.selfOpenStream:
            self.stream.close()
        if cov:
            cov.report(morfs=morfs)
