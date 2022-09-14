# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def %function%( COMStoreName ):
    try:
        # Get Macro Parameters
        res, ParType, oParam = GetCurMacroParameter( "UserParam" )
        
        # Add your code here
        Value = 1
        
        # Set The Results
        if res:
            SetTestInfo( "V", Value, Value - 1, Value, Value + 1, TestResult.TestResult )
        else:
            SetTestInfo( "V", -1, Value - 1, -1, Value + 1, TestResult.ForceFail )
        
        return ScriptResult.TestContinue
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return ScriptResult.TestAbort
