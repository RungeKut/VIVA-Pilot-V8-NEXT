# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

_ActionToDo_FAIL    = "FAIL"
_ActionToDo_TEST    = "TEST"
_ActionToDo_SKIP    = "SKIP"

def BeginPanel( MultiPanelName, BoardName, Batch, Barcode, TestSetting, WizardSetting, COMStoreName ):
    try:
        #*******   Initialize Constant and Variables   *******
        if( Barcode == "" ):
            return 1, Barcode, _ActionToDo_FAIL
        #TODO: Add your code here
        return 0, Barcode, _ActionToDo_TEST
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) ) 
        return 1, Barcode, _ActionToDo_FAIL
