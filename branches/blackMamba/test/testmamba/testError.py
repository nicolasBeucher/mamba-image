"""
Test cases for the error string function.

The error function allows to associate a small string explanation with an error
code.
    
Python function:
    Not Applicable
    
C function:
    MB_StrErr
"""

import mamba
import mamba.core as core
import unittest
import random

class TestError(unittest.TestCase):

    def testError(self):
        """Tests error function"""
        for i in range(core.MB_ERR_UNKNOWN+1):
            err_str = core.MB_StrErr(i)
            self.assertNotEqual(err_str, "")
            
        ref_str = core.MB_StrErr(core.MB_ERR_UNKNOWN)
        for i in range(core.MB_ERR_UNKNOWN+1,10):
            err_str = core.MB_StrErr(i)
            self.assertEqual(err_str, ref_str)
            
        self.assertEqual(core.MB_NO_ERR, 0)

    def testException(self):
        """Tests the exception"""
        excp = mamba.MambaError(0)
        self.assertNotEqual(str(excp), "")
