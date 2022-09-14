# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

_ActionToDo_FAIL    = "FAIL"
_ActionToDo_TEST    = "TEST"
_ActionToDo_SKIP    = "SKIP"

def BeginBoard( CurrentBoard, Barcode, Diversities, COMStoreName ):
    try:
        #*******   Initialize Constant and Variables   *******
        RequestedInfo = ""
        if( Barcode == "" ):
            return 1, Diversities, Barcode, _ActionToDo_FAIL, RequestedInfo
        #TODO: Add your code here
        return 0, Diversities, Barcode, _ActionToDo_TEST, RequestedInfo
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return 1, Diversities, Barcode, _ActionToDo_FAIL, RequestedInfo
