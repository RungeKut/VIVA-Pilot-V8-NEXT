# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def %PPC_function%( COMStoreName ):
    try:
        #*******   Initialize Constant and Variables   *******
        res = True
        #TODO: Add your code here
        if( res ):
            ret = ScriptResult.TestContinue
        else:
            ret = ScriptResult.TestAbort
        return ret
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return ScriptResult.TestAbort
