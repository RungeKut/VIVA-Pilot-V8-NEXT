# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def BarcodeReaderAndVerifier( Barcode, Diversities, COMStoreName ):
    try:
        if( Barcode == "" ):
             return 1, Barcode, Diversities
        #TODO: Add your code here
        return 0, Barcode, Diversities
        
    except Exception as inst:
        MessageBox( "PYTHON SCRIPT ERROR", "Exception: \n" + str( inst ) )
        return 1, Barcode, Diversities
