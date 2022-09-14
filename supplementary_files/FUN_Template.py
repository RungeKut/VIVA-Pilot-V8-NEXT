# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def %function%( Value, Pinlist, COMStoreName ):
    try:
        # Add your code here
        nValue = int( Value )
        
        # Set The Results
        SetTestInfo( "V", nValue, nValue - 1, nValue, nValue + 1, TestResult.TestResult )
        
        return ScriptResult.TestContinue
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return ScriptResult.TestAbort
