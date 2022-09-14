# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def EndProgram( MultiPanelName, BoardName, Batch, Barcode, CurrentBoard, TestAborted, TestsFail, COMStoreName ):
    try:
        #*******   Initialize Constant and Variables   *******
        if( Barcode == "" ):
            return 1
        #TODO: Add your code here
        return 0
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return 1
