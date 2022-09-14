import array
import os
import sys
import time
import xml.etree.ElementTree as ET
import win32api
import win32com.client
import win32con
import win32gui

S_OK                    = 0
S_FALSE                 = 1
FALSE                   = 0
TRUE                    = 1

TestContinue            = 0
TestAbort               = 1
TestSkipped             = 2
TestLoopBreak           = 3
TestLoopContinue        = 4

_TestPASS               = 0
_TestFAIL               = 1
_TestABORT              = 2 
_TestSKIPPED            = 3

_Error                  = 1      # 1..N
_noError                = 0
_Skipped                = -1
_noTest                 = -2

trDefault               = -1
trForcePass             = 0
trTestResult            = 1
trForceFail             = 2
trForceSkip             = 3
trIgnoreResult          = 4

mvNone                  = 0

_pkUnknown              = 0
_pkString               = 1
_pkNumber               = 2
_pkPinlist              = 3

_intParameterType       = 0
_doubleParameterType    = 1
_stringParameterType    = 2
_pinlistParameterType   = 3

_sERRUnit               = "ERR"

Add                     = 0
Remove                  = 1

DontSet                 = -1
No                      = 0
Yes                     = 1

Off                     = 0
On                      = 1

_NoChannelMode          = -1
_4L_INC_O               = 0
_4L_INC_C               = 1
_4L_IMM_OC              = 2
_8L_INC_O               = 3
_8L_INC_C               = 4
_8L_IMM_OC              = 5
_2L_INC_O               = 6
_2L_INC_C               = 7
_2L_IMM_OC              = 8
_NC_OC                  = 0x40000000

_FirstPermissions       = 1
_SecondPermissions      = 2
_ParallelMode           = 0x00002000

_dbIDUnknown            = 0

_ICTRead                = 0x00100000
_ICTAutoLearn           = 0x00200000
_ICTValid               = 0x00400000
_ICTAutodebug           = 0x00800000
_ICTAutoAdjustment      = 0x04000000

_RCNoError              = 0
_RCParameterError       = 1
_RCSectionNotFound      = 2
_RCComponentNotFound    = 3
_RCMacroNotFound        = 4
_RCLabelNotFound        = 5
_RCComponentNotEnabled  = 6
_RCMacroNotEnabled      = 7

_sTwinnedBoards         = "TwinnedBoards"
_sTwinnedComponents     = "TwinnedComponents"
_sTwinnedChannels       = "TwinnedChannels"
_sBoardsFailed          = "BoardsFailed"
_sBoardsBarcodes        = "BoardCodes"

def TRACE( sMsg ):
    win32api.OutputDebugString( sMsg )

def MessageBox( sTitle, sMsg ):
    win32gui.MessageBox( 0, sMsg, sTitle, win32con.MB_OK )

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CFileIni:
#{
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ctor - CFileIni
    #'
    def __init__( self, IniFile ):
    #{
        try:
        #{
            self._ComObj = win32com.client.Dispatch( "Lcx.IniHelper" )
            self._IniFile = IniFile
        #}
        except:
        #{
            MessageBox( "Error", "CFileIni:__init__" )
        #}
        finally:
        #{
            pass
        #}
    #}

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ~ctor - CFileIni
    #
    def __del__( self ):
    #{
        self._ComObj
    #}

    def Write( self, Section, Entry, Value ):
    #{
        R = self._ComObj.Write( Section, Entry, Value, self._IniFile )

        if ( 0 == R ):
        #{
            MessageBox( "Error", "Write Failed" )
        #)
    #}

    def Read( self, Section, Entry, DefaultValue ):
    #{
        Value = ""
        R = self._ComObj.Read( Section, Entry, DefaultValue, self._IniFile, Value )

        if ( 0 == R ):
        #{
            MessageBox( "Error", "Read Failed" )
        #)
        return R[ 1 ]
    #}

    def Wait( self, Section, Entry, DefaultValue ):
    #{
        Value = 0
        R = self._ComObj.Wait( Section, Entry, DefaultValue, self._IniFile, Value )

        if ( 0 == R ):
        #{
            MessageBox( "Error", "Wait Failed" )
        #)
        return R[ 1 ]
    #}
#}
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CViva:
#{
    _MaxNumTimers = 10

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ctor - CViva
    #
    def __init__( self, COMStoreName ):
    #{
        try:
        #{
            self.fInitOK    = False
            self.COMStore   = None
            if ( COMStoreName != "" ):
            #{
                self.COMStore       = win32com.client.Dispatch( "LCX.IUS" )
                self.VivaSystem     = self.COMStore.GetInterface( "S2K.System" + COMStoreName )
                self.VivaTest       = self.COMStore.GetInterface( "S2K.Test" + COMStoreName )
                self.VivaDB         = self.COMStore.GetInterface( "S2K.Database" + COMStoreName )
            #}
            else:
            #{
                self.VivaSystem     = win32com.client.Dispatch( "S2K.System" )
                self.VivaTest       = win32com.client.Dispatch( "S2K.Test" )
                self.VivaDB         = win32com.client.Dispatch( "S2K.Database" )
            #}
            self.VivaDir                = self.VivaSystem.VivaPath          # Retrieve The Viva Path
            self.BdPath                 = self.VivaSystem.DefaultWorkPath  # Retrieve The Current Path
            self.BdName                 = self.VivaSystem.CurrentBoard     # Retrieve The Current Board
            self.KITName                = self.VivaSystem.KITName
            self.PanelCode              = str( self.VivaSystem.BoardCode )
            if ( self.PanelCode == " " ):
            #{
                self.PanelCode = ""
            #}
            self.BoardCode              = str( self.VivaSystem.BoardSubCode )

            self.nNumBoards             = self.GetNumBoards()
            self.nCurrentBoardNumber    = self.GetCurrentBoardNumber()
            if ( self.nCurrentBoardNumber == -1 ):
            #{
                return
            #}
            self.sComponentName         = ""
            self.sMacroName             = ""
            self.sInstrName             = ""
            self.nSequence              = -1
            self.GetComponentInfo()
            self.GetMacroInfo()

            self.ClearReport()
            self.GetEmulation()
            self.GetTestSettings()
            self.VivaHelper = win32com.client.Dispatch( "Seica.VivaHelper" )
            self.dTimer  = [ 0 ] * self._MaxNumTimers
            self.fInitOK = True
        #}
        except Exception as e:
        #{
            MessageBox( "Error", "CViva.__init__ Exception : %s" % str( e ) )
        #}
        finally:
        #{
            pass
        #}
    #}

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ~ctor - CViva
    #
    def __del__( self ):
    #{
        if ( self.COMStore != None ):
        #{
            del self.COMStore
        #}
        else:
        #{
            del self.VivaSystem
            del self.VivaTest
            del self.VivaDB
        #}
        del self.VivaHelper
    #}

    def IsFlying( self ):
    #{
        sFlying = self.VivaSystem.FixtureType
        if ( ( sFlying == "Flying" ) or ( sFlying == "Mobile Fixture" ) ):
        #{
            self.fFlying = True
        #}
        else:
        #{
            self.fFlying = False
        #}
    #}

    def ClearReport( self ):
    #{
        if ( self.nSequence == -1 ):
        #{
            return True
        #}
        Response = self.VivaTest.Execute( "ResetInstrCookie", None )
        return int( Response[ 0 ] )
    #}

    def CheckStopProgram( self ):
    #{
        # Check if Stop Test is pressed
        Params = "<R><MSG SyncAbort=\"N\" /></R>"
        Response = self.VivaTest.Execute( "CheckStopProgram", Params )
        return int( Response[ 0 ] )
    #}

    def GetEmulation( self ):
    #{
        Response = self.VivaTest.Execute( "GetEmulationEnabled", None )
        self.fEmulation = int( Response[ 0 ] )
    #}

    def GetTestSettings( self ):
    #{
        self.fAutoDebug = self.VivaSystem.Autodebug
        self.fAutoLearn = self.VivaSystem.Autolearn
        self.fAutoAdjust = self.VivaSystem.AutoAdjustment
    #}

    def DisableVivaOscilloscope( self ):
    #{
        Response = self.VivaSystem.Execute( "DisableVivaOscilloscope", None )
        return int( Response[ 0 ] )
    #}

    def SetView( self, fView ):
    #{
        Params = int( fView )
        Response = self.VivaSystem.Execute( "SetView", Params )
        return int( Response[ 0 ] )
    #}

    def GetNumBoards( self ):
    #{
        Response = self.VivaTest.Execute( "GetNumBoards", None )
        return 0 if ( Response[ 0 ] == FALSE ) else int( Response[ 1 ] )
    #}

    def GetCurrentBoardNumber( self ):
    #{
        Response = self.VivaTest.Execute( "GetCurrentBoardNumber", None )
        return -1 if ( Response[ 0 ] == FALSE ) else int( Response[ 1 ] )
    #}

    def IsBoardEnabled( self, nBoard ):
    #{
        return self.VivaTest.BoardEnabled( int( nBoard ) )
    #}

    def GetComponentInfo( self ):
    #{
        self.sComponentName = ""
        Response = self.VivaDB.Execute( "GetCurrentComponentName", None )
        if ( Response[ 0 ] == TRUE ):
        #{
            self.sComponentName = str( Response[ 1 ] )
        #}
    #}

    def GetMacroInfo( self ):
    #{
        self.nSequence = -1
        if ( self.sComponentName != "" ):
        #{
            Response = self.VivaDB.Execute( "GetCurrentMacroInfo", None )
            if ( Response[ 0 ] == TRUE ):
            #{
                root = ET.fromstring( Response[ 1 ] )
                self.sMacroName = root.find( 'MSG' ).get( 'MacroName' )
                self.sInstrName = root.find( 'MSG' ).get( 'InstrName' )
                self.nSequence  = int( root.find( 'MSG' ).get( 'Sequence' ) )
            #}
        #}
    #}

    def GetMacroParameter( self, sParameterName, ParameterType ):
    #{
        ParameterValues = self.VivaDB.GetCurMacroParameter( str( sParameterName ) )
        if ( ParameterType == _intParameterType ):
        #{
            return int( ParameterValues[ 0 ] )
        #}
        elif ( ParameterType == _doubleParameterType ):
        #{
            return float( ParameterValues[ 0 ] )
        #}
        elif ( ParameterType == _stringParameterType ):
        #{
            return str( ParameterValues[ 2 ] )
        #}
        elif ( ParameterType == _pinlistParameterType ):
        #{
            sPinlist = str( ParameterValues[ 2 ] ).split( "-" )
            nPinlist = []
            for sPin in sPinlist:
            #{
                nPinlist.append( int( sPin ) )
            #}
            return nPinlist
        #}
    #}

    def SetMacroParameter( self, sParameterName, Value ):
    #{
        Response = self.VivaDB.SetCurMacroParameter( str( sParameterName ), Value )
        return False if ( Response == FALSE ) else True
    #}

    def GetMacroMemoParameter( self, sSectionName, sParameterName, DefaultValue, ParameterType, fConvert = True ):
    #{
        if ( ParameterType == _intParameterType ):
        #{
            ParameterValue = self.VivaTest.GetSectionParN( str( sSectionName ), str( sParameterName ), DefaultValue )
            return int( ParameterValue )
        #}
        elif ( ParameterType == _doubleParameterType ):
        #{
            ParameterValue = self.VivaTest.GetSectionParN( str( sSectionName ), str( sParameterName ), DefaultValue )
            return float( ParameterValue )
        #}
        elif ( ParameterType == _stringParameterType ):
        #{
            ParameterValue = self.VivaTest.GetSectionParS( str( sSectionName ), str( sParameterName ), DefaultValue )
            if ( fConvert ):
            #{
                if ( ( str( ParameterValue[ 0 ] ) == "Y" ) or ( str( ParameterValue[ 0 ] ) == "y" ) ):
                #{
                    return True
                #}
                elif ( ( str( ParameterValue[ 0 ] ) == "N" ) or ( str( ParameterValue[ 0 ] ) == "n" ) ):
                #{
                    return False
                #}
                else:
                #{
                    return str( ParameterValue )
                #}
            #}
            else:
            #{
                return str( ParameterValue )
            #}
        #}
    #}

    def SetMacroMemoParameter( self, sSectionName, sParameterName, ParameterType, Value ):
    #{
        if ( ParameterType == _intParameterType ):
        #{
            self.VivaTest.SetSectionParN( str( sSectionName ), str( sParameterName ), Value )
        #}
        elif ( ParameterType == _doubleParameterType ):
        #{
            self.VivaTest.SetSectionParN( str( sSectionName ), str( sParameterName ), Value )
        #}
        elif ( ParameterType == _stringParameterType ):
        #{
            self.VivaTest.SetSectionParS( str( sSectionName ), str( sParameterName ), Value )
        #}
    #}

    def GetMacroPermissions( self, PermissionsType ):
    #{
        Params = "<R><MSG Request=\"Permissions\" Item=\"Macro\" Action=\"Read\" PermissionsType=\"" + str( PermissionsType ) + "\" /></R>"
        Response = self.VivaSystem.Execute( "Permissions", Params )
        if ( Response[ 0 ] == FALSE ):
        #{
            return 0
        #}
        root = ET.fromstring( Response[ 1 ] )
        return int( root.find( 'MSG' ).get( 'Value' ) )
    #}

    def GetMacroState( self ):
    #{
        Params = "<R><MSG Request=\"State\" Item=\"Macro\" Action=\"Read\" /></R>"
        Response = self.VivaSystem.Execute( "State", Params )
        if ( Response[ 0 ] == FALSE ):
        #{
            return 0
        #}
        root = ET.fromstring( Response[ 1 ] )
        return int( root.find( 'MSG' ).get( 'Value' ) )
    #}

    def SetMacroState( self, nState ):
    #{
        Params = "<R><MSG Request=\"State\" Item=\"Macro\" Action=\"Write\" Value=\"" + str( nState ) + "\" DefaultValue=\"" + str( nState ) + "\" /></R>"
        Response = self.VivaSystem.Execute( "State", Params )
        return False if ( Response[ 0 ] == FALSE ) else True
    #}

    def GetGlobalVariable( self, sGlobalVariableName, GlobalVariableType ):
    #{
        Response = self.VivaDB.GetGlobalVariable( sGlobalVariableName )
        if ( GlobalVariableType == _intParameterType ):
        #{
            return int( Response[ 0 ] ) if ( Response[ 1 ] == _pkNumber ) else sys.maxsize
        #}
        elif ( GlobalVariableType == _doubleParameterType ):
        #{
            return float( Response[ 0 ] ) if ( Response[ 1 ] == _pkNumber ) else sys.float_info.max
        #}
        elif ( GlobalVariableType == _stringParameterType ):
        #{
            return str( Response[ 2 ] ) if ( Response[ 1 ] == _pkString ) else ""
        #}
    #}

    def SetGlobalVariable( self, sGlobalVariableName, vValue ):
    #{
        Response = self.VivaDB.SetGlobalVariable( sGlobalVariableName, vValue )
        return False if ( Response == FALSE ) else True
    #}

    def GetMacroParameterValue( self, sComponent, sMacro, nMacroNumber, nMacroID, sParameterName ):
    #{
        return self.VivaTest.GetMacroParameterValue( sComponent, sMacro, nMacroNumber, nMacroID, sParameterName )
    #}

    def SetMacroParameterValue( self, sComponent, sMacro, nMacroNumber, nMacroID, sParameterName, Value ):
    #{
        return self.VivaTest.SetMacroParameterValue( sComponent, sMacro, nMacroNumber, nMacroID, sParameterName, Value )
    #}

    def GetTwinnedChannel( self, nBoard, nChannel ):
    #{
        Params = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" BoardNumber=\"" + str( nBoard ) + "\" VirtualPin=\"Y\" /></R>"
        Response = self.VivaSystem.Execute( "SetPinMode", Params )
        if ( Response[ 0 ] == FALSE ):
        #{
            return 0
        #}
        else:
        #{
            root = ET.fromstring( Response[ 1 ] )
            nTwinnedChannel = int( root.find( 'MSG' ).get( 'Channel' ) )
            return nTwinnedChannel
        #}
    #}

    def MoveChannels( self, nChannels, Mode, Locked = No ):
    #{
        sLocked = "Y" if ( Locked == Yes ) else "N"
        Params = "<R><MSG Mode=\"" + str( _8L_IMM_OC ) + "\" Connect=\"" + ( "Y" if ( Mode == Add ) else "N" ) + "\" CloseLines=\"0\" ExtLines=\"0\" Locked=\"" + ( str( Locked ) if ( Locked != DontSet ) else "-1" ) + "\" Channels=\""
        for nChannel in nChannels:
        #{
            if ( ( Mode == Add ) and ( Locked != DontSet ) ):
            #{
                Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" LockPin=\"" + sLocked +"\" /></R>"
                Response = self.VivaSystem.Execute( "SetPinMode", Params1 )
                if ( Response[ 0 ] == FALSE ):
                #{
                    return FALSE
                #}
            #}
            Params = Params + str( nChannel ) + ";"
        #}
        Params = Params + "\" /></R>"
        Response = self.VivaSystem.Execute( "Connect", Params )
        if ( Mode == Remove ):
        #{
            for nChannel in nChannels:
            #{
                if ( Locked != DontSet ):
                #{
                    Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" LockPin=\"" + sLocked if ( Locked != DontSet ) else "" + "\" /></R>"
                #}
                else:
                #{
                    Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" /></R>"
                #}
                Response1 = self.VivaSystem.Execute( "ResetPinMode", Params1 )
                if ( Response1[ 0 ] == FALSE ):
                #{
                    return FALSE
                #}
            #}
        #}
        if ( Response[ 0 ] == FALSE ):
        #{
            return FALSE
        #}
        else:
        #{
            root = ET.fromstring( Response[ 1 ] )
            if ( int( root.find( 'MSG' ).get( 'ConnectStatus' ) ) == FALSE ):
            #{
                TRACE( "Return Code = " + root.find( 'MSG' ).get( 'ReturnCode' ) + "\n" )
                return FALSE
            #}
            else:
            #{
                return TRUE
            #}
        #}
    #}

    def WriteMessage( self, sMessage ):
    #{
        self.VivaTest.WriteMessage( sMessage )
    #}
    
    def SetTestResult( self, sTestErroInfo, sUnit, ReadValue, LowLimit, ExpectedValue, HighLimit, eTestResult, nBoard, sComponentName, sInstrName, nSequence ):
    #{
        Params =    "<R><MSG Request=\"SetTestResult\""                         + \
                            " Board=\"" + str( nBoard )                 + "\""  + \
                            " ComponentName=\"" + sComponentName        + "\""  + \
                            " InstrName=\"" + sInstrName                + "\""  + \
                            " Sequence=\"" + str( nSequence )           + "\""  + \
                            " Unit=\"" + sUnit                          + "\""  + \
                            " Value=\"" + str( ReadValue )              + "\""  + \
                            " Low=\"" + str( LowLimit )                 + "\""  + \
                            " Expected=\"" + str( ExpectedValue )       + "\""  + \
                            " High=\"" + str( HighLimit )               + "\""  + \
                            " TestResult=\"" + str( eTestResult )       + "\""  + \
                            " ResetCookies=\"Y\""                               + \
                            " Cookies=\"" + sTestErroInfo               + "\""  + \
                    " /></R>"
        #TRACE( "\n" + Params + "\n" )
        bRet, dummy = self.VivaTest.Execute( "SetTestResult", Params )
        if ( bRet == FALSE ):
        #{
            return False
        #}
        return True
    #}
    
    def SetTestInfo( self,                      \
                     sTestErroInfo,             \
                     sUnit,                     \
                     ReadValue,                 \
                     LowLimit,                  \
                     ExpectedValue,             \
                     HighLimit,                 \
                     eTestResult,               \
                     nBoard = -1,               \
                     sComponentName = "",       \
                     sInstrName = "",           \
                     nMacroNumber = -1,         \
                     nMacroID = _dbIDUnknown,   \
                     nSequence = -1,            \
                     sLabelName = "",           \
                     nLabelNumber = -1,         \
                     nLabelID = _dbIDUnknown,   \
                     sValueName = "",           \
                     dValue = 0 ):
    #{
        #TRACE( "\n nBoard : " + str( nBoard ) + \
        #        " sUnit : " + str( sUnit ) + \
        #        " ReadValue : " + str( ReadValue ) + \
        #        " LowLimit : " + str( LowLimit ) + \
        #        " ExpectedValue : " + str( ExpectedValue ) + \
        #        " HighLimit : " + str ( HighLimit ) + \
        #        " eTestResult : " + str( eTestResult ) + "\n" + \
        #        " sTestErroInfo : " + str( sTestErroInfo ) + "\n" )
        if ( self.fEmulation ):
        #{
            ReadValue = ExpectedValue
        #}
        fResultPass = True
        if ( eTestResult == trTestResult ):
        #{
            if ( ( ReadValue < LowLimit ) or ( ReadValue > HighLimit ) ):
            #{
                fResultPass = False
            #}
        #}
        elif ( eTestResult == trForceFail ):
        #{
            fResultPass = False
        #}
        elif ( eTestResult == trForcePass ):
        #{
            if ( ( ReadValue < LowLimit ) or ( ReadValue > HighLimit ) ):
            #{
                sTestErroInfo = ""
            #}
        #}
        if ( nBoard == -1 ):
        #{
            nBoard = self.nCurrentBoardNumber
        #}
        if ( nBoard == self.nCurrentBoardNumber ):
        #{
            if ( sComponentName == "" ):
            #{
                self.ClearReport()
                self.VivaTest.Clear()
                self.VivaTest.Set( sUnit, LowLimit, ExpectedValue, HighLimit )
                self.VivaTest.Measure( ReadValue, eTestResult, mvNone )
                if ( sTestErroInfo != "" ):
                #{
                    self.VivaTest.WriteReport( sTestErroInfo )
                #}
            #}
            else:
            #{
                if ( _RCNoError != self.VivaTest.SetValue( sComponentName, sInstrName, nMacroNumber, nMacroID, sLabelName, nLabelNumber, nLabelID, sValueName, dValue ) ):
                #{
                    return False, fResultPass
                #}
            #}
        #}
        else:
        #{
            if ( sComponentName == "" ):
            #{
                if ( not self.SetTestResult( sTestErroInfo, sUnit, ReadValue, LowLimit, ExpectedValue, HighLimit, eTestResult, nBoard, self.sComponentName, self.sInstrName, self.nSequence ) ):
                #{
                    return False, fResultPass
                #}
            #}
            else:
            #{
                if ( not self.SetTestResult( sTestErroInfo, sUnit, ReadValue, LowLimit, ExpectedValue, HighLimit, eTestResult, nBoard, sComponentName, sInstrName, nSequence ) ):
                #{
                    return False, fResultPass
                #}
            #}
        #}
        return True, fResultPass
    #}

    def ReportFail( self, sTestErroInfo, eTestResult, nBoard = -1 ):
    #{
        return self.SetTestInfo( sTestErroInfo, _sERRUnit, 1.0, 0.0, 0.0, 0.0, eTestResult, nBoard )
    #}

    def StartTimer( self, dStartTimer = 0, nTimer = 0 ):
    #{
        if ( ( nTimer < 0 ) or ( nTimer >= self._MaxNumTimers ) ):
        #{
            return False
        #}
        self.dTimer[ nTimer ] = float( dStartTimer )
        if ( self.dTimer[ nTimer ] == 0 ):
        #{
            self.dTimer[ nTimer ] = time.clock()
        #}
        return True
    #}

    def TimerExpired( self, dTimeout, nTimer = 0 ):
    #{
        if ( ( nTimer < 0 ) or ( nTimer >= self._MaxNumTimers ) ):
        #{
            return True
        #}
        if ( self.dTimer[ nTimer ] == 0 ):
        #{
            return True
        #}
        if ( ( time.clock() - self.dTimer[ nTimer ] ) > dTimeout ):
        #{
            self.dTimer[ nTimer ] = 0
            return True
        #}
        return False
    #}

    def IsBoardFailed( self, BoardsFailed, nBoard ):
    #{
        if ( BoardsFailed == "" ):
        #{
            return False
        #}
        for BoardFailed in BoardsFailed:
        #{
            if ( int( BoardFailed ) == int ( nBoard ) ):
            #{
                return True
            #}
        #}
        return False
    #}

    def GetBoardBarcode( self, BoardsBarcodes, nBoard ):
    #{
        if ( len( BoardsBarcodes ) >= int ( nBoard ) ):
        #{
            if ( BoardsBarcodes[ int ( nBoard ) - 1 ] != "" ):
            #{
                return str( BoardsBarcodes[ int ( nBoard ) - 1 ] )
            #}
            elif( self.BoardCode != "" ):
            #{
                return str( self.BoardCode )
            #}
            elif( self.PanelCode != "" ):
            #{
                return str( self.PanelCode )
            #}
            else:
            #{
                return ""
            #}
        #}
        elif( self.BoardCode != "" ):
        #{
            return str( self.BoardCode )
        #}
        elif( self.PanelCode != "" ):
        #{
            return str( self.PanelCode )
        #}
        else:
        #{
            return ""
        #}
    #}
    
    def GetSectionComponents( self, sSectionName ):
    #{
        nRet, sComponentsName = self.VivaTest.GetSectionComponents( sSectionName )
        return nRet, sComponentsName
    #}

    def GetComponentMacros( self, sComponent ):
    #{
        nRet, sMacrosName, nMacrosID = self.VivaTest.GetComponentMacros( sComponent )
        return nRet, sMacrosName, nMacrosID
    #}

    def GetMacroIDLabels( self, sComponent, nMacroID ):
    #{
        nRet, sLabelsName = self.VivaTest.GetMacroLabels( sComponent, "", -1, nMacroID )
        return nRet, sLabelsName
    #}
#}
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CSeicaACL:
#{
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ctor - CSeicaACL
    #
    def __init__( self, Viva, COMStoreName ):
    #{
        try:
        #{
            self.fInitOK    = False
            self.Viva       = Viva
            if ( self.Viva.COMStore != None ):
            #{
                self.SeicaACL   = self.Viva.COMStore.GetInterface( "ACLAM" + COMStoreName )
                self.AGND       = self.Viva.COMStore.GetInterface( "ACL_AGND" + COMStoreName )
                self.DRA        = self.Viva.COMStore.GetInterface( "ACL_DRA" + COMStoreName )
                self.DRB        = self.Viva.COMStore.GetInterface( "ACL_DRB" + COMStoreName )
                self.DRC        = self.Viva.COMStore.GetInterface( "ACL_DRC" + COMStoreName )
            #}
            else:
            #{
                self.SeicaACL   = win32com.client.Dispatch( "Seica.ACLAM" )
                self.AGND       = win32com.client.Dispatch( "Seica.AGND" )
                self.DRA        = win32com.client.Dispatch( "Seica.DRA" )
                self.DRB        = win32com.client.Dispatch( "Seica.DRB" )
                self.DRC        = win32com.client.Dispatch( "Seica.DRC" )
            #}
            self.fInitOK    = True
        #}
        except:
        #{
            MessageBox( "Error", "CSeicaACL:__init__" )
        #}
        finally:
        #{
            pass
        #}
    #}

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ~ctor - CSeicaACL
    #
    def __del__( self ):
    #{
        if ( self.Viva.COMStore == None ):
        #{
            del self.SeicaACL
            del self.AGND
            del self.DRA
            del self.DRB
            del self.DRC
        #}
    #}
#}
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
