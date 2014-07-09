"""
Module defining the classes used to display and generate output for the
Mamba Test Platform.
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


################################################################################
# Definition for test ending notification
################################################################################
Failure = -1
Error = -2
Success = 0

################################################################################
# Classes interface
################################################################################
class MambaTestOutput:
    """
    Dummy class used to define the interface to a test output generator.
    This class defines methods and attributes that are generic to all the 
    output generator class
    """
    
    def __init__(self, descriptions=1, verbosity=0):
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        
    def notifyModuleTestStart(self, moduleInfo):
        """Notifies the beginnig of a module test."""
        pass
        
    def notifyTestStart(self, test):
        """Notifies the beginning of a test."""
        pass
        
    def notifyTestEnd(self, test, result):
        """Notifies the end of a test with its result."""
        pass
        
    def printModuleReport(self, moduleInfo, moduleResult):
        """
        Produces a report for the played module. 
        'moduleInfo' contains the name, description and time taken for the tests.
        'moduleResult' is an instance of MambaTestResult produced for the given 
        module.
        """
        pass
        
    def printGeneralReport(self, playedModules, cov=None, morfs=[]):
        """
        Produces a complete report associated with a MambaTestRunner instance.
        All the modules played, their results and other information are displayed.
        A coverage instance can be given to process code coverage stats.
        """
        pass
        
class ModuleInfo:

    def __init__(self, name, desc):
        """
        Completes information regarding a test module.
        """
        self.name = name
        self.desc = desc
        self.timeTaken = 0
        
    def __hash__(self):
        # Making sure the module info could be used as a key for a dictionary
        return hash(self.name)
