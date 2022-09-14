# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import sys
from FNtools import *

def MoveProbes( COMStoreName ):
    # Get Macro Parameters
    
    R1, ParType, Ch   = GetCurMacroParameter( "PinList" )
    if ( not R1 or ParType != ParVarType.pinlist or len( Ch ) == 0 ):
        WriteReport( "Invalid Channels" )
        SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
        return ScriptResult.TestContinue
    else:
        nChannels = list( Ch )
    
    R2, ParType, Mode       = GetCurMacroParameter( "Mode" )
    if ( not R2 or ParType != ParVarType.double ):
        WriteReport( "Invalid Channels" )
        SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
        return ScriptResult.TestContinue
    else:
        Mode = MC_Mode( Mode )
    
    R3, ParType, Locked     = GetCurMacroParameter( "Locked" )
    if ( not R3 or ParType != ParVarType.double ):
        WriteReport( "Invalid Channels" )
        SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
        return ScriptResult.TestContinue
    else:
        Locked = MC_Locked( Locked )

    fMove = False
    if ( len( nChannels ) != 0 ):
        # Get Macro Parallel Test Mode Option Supported
        R, Permissions = GetMacroPermissions( PermType._SecondPermissions )
        if ( ( Permissions != 0 ) and ( ( Permissions & PermType._ParallelMode ) == PermType._ParallelMode ) ):
            R, ParType, Value = GetGlobalVariable( GVParallelMode._sTwinnedBoards.value )
            if ( R and ParType == ParVarType.string and Value != "" ):
                TwinnedBoards = str( Value ).split( "," )
                if ( len( TwinnedBoards ) ):
                    fFound = False
                    for TwinnedBoard in TwinnedBoards:
                        Boards = str( TwinnedBoard ).split( "-" )
                        nBoards = len( Boards )
                        for nBoard in range( nBoards ):
                            if ( int( Boards[ nBoard ] ) == GetCurrentBoardNumber() ):
                                fFound = True
                                if ( nBoards > 1 ):
                                    if ( nBoard == ( nBoards - 1 ) ):
                                        if ( IsBoardEnabled( Boards[ nBoard - 1 ] ) ):
                                            nNumChannels = len( nChannels )
                                            for nChannel in range( nNumChannels ):
                                                R, TwinnedChannel = GetTwinnedChannel( Boards[ nBoard - 1 ], nChannels[ nChannel ] )
                                                if( R ):
                                                    nChannels.append( TwinnedChannel )
                                                else:
                                                    WriteReport( "Twinned channel error" )
                                                    SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
                                                    return ScriptResult.TestContinue
                                        fMove = True
                                    else:
                                        if ( not IsBoardEnabled( Boards[ nBoard + 1 ] ) ):
                                            fMove = True
                                else:
                                    fMove = True
                                break             
                        if ( fFound ):
                            break
                    if ( fFound ):
                        if ( fMove ):
                            if ( len( nChannels ) > 1 ):
                                if ( nChannels[ 1 ] == 0 ):
                                    WriteReport( "Invalid Channels" )
                                    SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
                                    fMove = False
                        else:
                            SetTestInfo( "N", 1, 0, 1, 2, TestResult.ForcePass )
                            fMove = False
                    else:
                        WriteReport( "Invalid Channels" )
                        SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
                        fMove = False
                else:
                    fMove = True
            else:
                fMove = True
        else:
            fMove = True
    else:
        fMove = True
    
    if ( fMove ):
        Ret, sSignalsFromProbes, sChannelsFromProbes = MoveChannels( nChannels, Mode, Locked )
        if ( Ret ):
            SetTestInfo( "N", 1, 0, 1, 2, TestResult.ForcePass )
        else:
            WriteReport( "Move Error" )
            SetTestInfo( "ERR", 1.0, 0.0, 0.0, 0.0, TestResult.ForceFail )
    
    return ScriptResult.TestContinue
