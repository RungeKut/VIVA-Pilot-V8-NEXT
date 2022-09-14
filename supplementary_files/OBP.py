# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

# Macro Version Info
#
# Description :         Implementation of the OBP Macro.
# Version :             3.0.0
# Created :             31/07/2019
#
# Revision History :
#
#        1.0   - 31/07/2019 : First Release
#        2.0   - 12/11/2019 : dynamic commands management
#        2.0.1 - 15/01/2020 : new message & 10 Retry connections
#        2.0.2 - 06/05/2020 : bug fixed about master board
#        3.0.0 - 11/06/2020 : Python 3.x and FNTools
#        3.1   - 26/06/2020 : OBP Seica DEVICECLIP + SMH FR20 
#
# Macro Version Info

import collections
from collections import namedtuple
import ctypes
import logging
import os
import socket
import sys
import time

from FNtools import *

class eProgrammerType( Enum ):
    _SMH20              = "SMH_FR20"
    _SEICA              = "SEICA_DC"

SMH_OBP_Cmd             = "#%d*%s"
SMH_OBP_PrjNameExt      = ".prj"
SMH_OBP_GetEngStatus    = "GETENGSTATUS"
SMH_OBP_ClearErr        = "CLRERR"
SMH_OBP_Sping           = "SPING"
SMH_OBP_SetRelays       = ""
SMH_OBP_Run             = "RUN "
SMH_OBP_GetError        = "SGETERR"
SMH_OBP_Error           = "ERR"
SMH_OBP_SEND_EOL        = "\n"
SMH_OBP_RECV_EOL        = "\n"
SMH_OBP_RECV_PASS       = ">"
SMH_OBP_RECV_FAIL       = "!"
SMH_OBP_RECV_FAIL1      = ""
SMH_OBP_RECV_FAIL2      = ""
SMH_OBP_MasterChannel   = 55

OBP_Cmd                 = SMH_OBP_Cmd         
OBP_PrjNameExt          = SMH_OBP_PrjNameExt     
OBP_GetEngStatus        = SMH_OBP_GetEngStatus
OBP_ClearErr            = SMH_OBP_ClearErr    
OBP_Sping               = SMH_OBP_Sping 
OBP_SetRelays           = SMH_OBP_SetRelays      
OBP_Run                 = SMH_OBP_Run         
OBP_GetError            = SMH_OBP_GetError    
OBP_Error               = SMH_OBP_Error       
OBP_SEND_EOL            = SMH_OBP_SEND_EOL
OBP_RECV_EOL            = SMH_OBP_RECV_EOL
OBP_RECV_PASS           = SMH_OBP_RECV_PASS
OBP_RECV_FAIL           = SMH_OBP_RECV_FAIL         
OBP_RECV_FAIL1          = SMH_OBP_RECV_FAIL1         
OBP_RECV_FAIL2          = SMH_OBP_RECV_FAIL2        

_nAnswerTimeout         = 1000
_nProgramAnswerTimeout  = 30000

_SysCfgFileName         = "OBP_SysConfig.ini"
_BrdCfgFileName         = "OBP_BrdConfig.ini"
_MaxNumProjects         = 20
_SettingsSectionKey     = "Settings"
_ProgrammerInterfaceKey = "ProgrammerInterface"
_ProgrammerTypeKey      = "ProgrammerType"
_OBP_Cmd_Key            = "OBP_Cmd"         
_OBP_PrjNameExt_Key     = "OBP_PrjNameExt"     
_OBP_GetEngStatus_Key   = "OBP_GetEngStatus"
_OBP_ClearErr_Key       = "OBP_ClearErr"    
_OBP_Sping_Key          = "OBP_Sping"       
_OBP_SetRelays_Key      = "OBP_SetRelays"
_OBP_Run_Key            = "OBP_Run"         
_OBP_GetError_Key       = "OBP_GetError"    
_OBP_Error_Key          = "OBP_Error"       
_OBP_SEND_EOL_Key       = "OBP_SEND_EOL"     
_OBP_RECV_EOL_Key       = "OBP_RECV_EOL"     
_OBP_RECV_PASS_Key      = "OBP_RECV_PASS"     
_OBP_RECV_FAIL_Key      = "OBP_RECV_FAIL"     
_OBP_RECV_FAIL1_Key     = "OBP_RECV_FAIL1"     
_OBP_RECV_FAIL2_Key     = "OBP_RECV_FAIL2"     
_OBP_MasterChannel_Key  = "OBP_MasterChannel"  
_OBPSectionKey          = "OBP"
_IPKey                  = "IP"
_PortKey                = "Port"
_ChannelsKey            = "Channels"
_EmulatedKey            = "Emulated"
_WriteMessageErrorKey   = "WriteMessageError"
_LogFileNameKey         = "LogFileName"
_LoggingKey             = "Logging"
_SendDynamicCMDKey      = "SendDynamic"
_ProjectsSectionKey     = "PROJECTS"
_DynamicSectionKey      = "DYNAMICS"
_BoardSectionKey        = "B%d"
_OBPKey                 = "OBP"
_ChannelKey             = "Channel"
_MasterKey              = "Master"
_BrothersKey            = "Brothers"
_ProjectKey             = "P%d"
_DynamicKey             = "DYNAMIC%d"
_CMDKey                 = "CMD%d"

_sOBPLoopGV             = "OBP_Loop"               

OBPInfo_t               = namedtuple( 'OBPInfo_t', [ 'sProgrammerName', 'eProgrammerType', 'sProgrammerInterface', 'sIP', 'sPort', 'nNumChannels', 'nMasterChannel', 'fEmulated', 'nBoards', 'nChannels', 'sProjectsName', 'sDynamicCMDsFileNames', 'DynamicCMDs' ] )

global g_fWriteMessageError
g_fWriteMessageError    = False
global g_fLogging
g_fLogging              = False

def Log( sMsg ):
#{
    global g_fLogging
    if ( g_fLogging ):
    #{
        logging.error( sMsg )
    #}
#}

class COBP:
#{
    _Master                 = -1
    _InvalidHandle          = 0
    _MaxAnswerSize          = 4096

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ctor - COBP
    #
    def __init__( self, OBPInfo, nTimeout, nRecycles, eTestResult ):
    #{
        try:
        #{
            self.fInitOK            = False
            self.OBPInfo            = OBPInfo
            self.nTimeout           = nTimeout
            self.nRecycles          = nRecycles
            self.eTestResult        = eTestResult
            self.vcChannelsStatus   = [ '-' ] * len( self.OBPInfo.nChannels )
            self.fBoardsProgramming = [ False ] * len( self.OBPInfo.nBoards )
            self.fBoardsFailed      = [ False ] * len( self.OBPInfo.nBoards )
            self.OBP_Handle         = self._InvalidHandle
            self.vcAnswer           = None
            self.sResponse          = ""
            self.MsgChErr           = [ "" ] * len( self.OBPInfo.nChannels )  # Error Message for each channel

            if ( ( self.OBPInfo.sIP == "" ) or ( self.OBPInfo.sPort == "" ) ):
            #{
                OBPReportFail( "%s Invalid IP Configuration" % self.OBPInfo.sProgrammerName, TestResult.ForceFail )
                return
            #}
            if ( self.OBPInfo.sProgrammerInterface != "" ):
            #{
                if ( not os.access( self.OBPInfo.sProgrammerInterface, os.R_OK ) ):
                #{
                    OBPReportFail( "%s DLL Error %s" % ( self.OBPInfo.sProgrammerName, self.OBPInfo.sProgrammerInterface ), TestResult.ForceFail )
                    return
                #}
                self.OBP_Dll = ctypes.WinDLL( self.OBPInfo.sProgrammerInterface )
                if ( self.OBP_Dll == None ):
                #{
                    OBPReportFail( "%s DLL Error %s" % ( self.OBPInfo.sProgrammerName, self.OBPInfo.sProgrammerInterface ), TestResult.ForceFail )
                    return
                #}
                self.vcAnswer = ctypes.create_unicode_buffer( self._MaxAnswerSize )
                if ( self.vcAnswer == None ):
                #{
                    OBPReportFail( "%s Answer Allocation Error" % self.OBPInfo.sProgrammerName, TestResult.ForceFail )
                    return
                #}
                ctypes.memset( ctypes.addressof( self.vcAnswer ), 0, ctypes.sizeof( self.vcAnswer ) )
            #}
            else:
            #{
                pass
            #}
            WriteMessage( r"Connecting To %s..." % self.OBPInfo.sProgrammerName )
            if ( not self.OBPInfo.fEmulated ):
            #{
                for nRecycle in range( 0, 2, 1 ):
                #{
                    if ( self.OBPInfo.sProgrammerInterface != "" ):
                    #{
                        self.OBP_Handle = self.OBP_Dll.FR_OpenCommunicationW( "LAN", str( "%s:%s" % ( self.OBPInfo.sIP, self.OBPInfo.sPort ) ) )
                        if ( self.OBP_Handle != self._InvalidHandle ):
                        #{
                            break
                        #}
                    #}
                    else:
                    #{
                        try:
                        #{
                            self.OBP_Handle = socket.socket()
                            self.OBP_Handle.settimeout( 1.0 )  # seconds
                            self.OBP_Handle.connect( ( self.OBPInfo.sIP, int( self.OBPInfo.sPort ) ) ) 
                            #if ( not self.SendCommand( OBP_Cmd %( self.OBPInfo.nMasterChannel, OBP_GetEngStatus ), self._Master ) ):
                            ##{
                            #    return
                            ##}
                            break
                        #}
                        except Exception as e:
                        #{
                            OBPReportFail( "%s Communication Error : Exception %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
                            if ( self.OBP_Handle != self._InvalidHandle ):
                            #{
                                self.OBP_Handle.close()
                            #}
                        #}
                    #}
                    CheckStopProgram()
                    Delay( 1 )
                    WriteMessage( r"Retry #%d Connection to %s (%s:%s) ..." % ( nRecycle + 1, self.OBPInfo.sProgrammerName, self.OBPInfo.sIP, self.OBPInfo.sPort ) )
                #}
                if ( self.OBP_Handle == self._InvalidHandle ):
                #{
                    OBPReportFail( "Error Connecting to %s (%s:%s)" % (self.OBPInfo.sProgrammerName, self.OBPInfo.sIP, self.OBPInfo.sPort), TestResult.ForceFail )
                    return
                #}
            #}
            WriteMessage( r"Connected To %s" % self.OBPInfo.sProgrammerName )
            if ( not self.SendCommand( OBP_Cmd %( self.OBPInfo.nMasterChannel, OBP_Sping ), self._Master ) ):
            #{
                return
            #}
            if ( OBP_SetRelays != "" ):
            #{
                for nChannel in range( 0, self.OBPInfo.nChannels, 1 ):
                #{
                    if ( not self.SendCommand( OBP_SetRelays % ( nChannel, Switch.Off ), self._Master ) ):
                    #{
                        return
                    #}
                #}
            #}
            self.fInitOK = True
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s __init__() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
        #}
        finally:
        #{
            pass
        #}
    #}

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ~ctor - COBP
    #
    def __del__( self ):
    #{
        try:
        #{
            if ( self.vcAnswer != None ):
            #{
                del self.vcAnswer
            #}
            if ( self.OBP_Handle != self._InvalidHandle ):
            #{
                if ( self.OBPInfo.sProgrammerInterface != "" ):
                #{
                    self.OBP_Dll.FR_CloseCommunicationW( self.OBP_Handle )
                #}
                else:
                #{
                    self.OBP_Handle.close()
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s __del__() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
        #}
        finally:
        #{
            pass
        #}
    #}

    def Programs( self, nRecycle ):
    #{
        try:
        #{
            fCleaError = False
            for nIdx in range( len( self.OBPInfo.nBoards ) ):
            #{
                if ( ( self.OBPInfo.sProjectsName[ nIdx ] != "" ) and ( ( nRecycle == 0 ) or self.fBoardsFailed[ nIdx ] ) ):
                #{
                    fCleaError = True
                    break
                #}
            #}
            if ( fCleaError and ( OBP_ClearErr != "" ) ):
            #{
                if ( not self.SendCommand( OBP_Cmd %( self.OBPInfo.nMasterChannel, OBP_ClearErr ), self._Master ) ):
                #{
                    for nIdx in range( len( self.OBPInfo.nBoards ) ):
                    #{
                        self.fBoardsFailed[ nIdx ] = True
                    #}
                    return False
                #}
            #}
            for nIdx in range( len( self.OBPInfo.nBoards ) ):
            #{
                if ( ( self.OBPInfo.sProjectsName[ nIdx ] != "" ) and ( ( nRecycle == 0 ) or self.fBoardsFailed[ nIdx ] ) ):
                #{
                    self.fBoardsFailed[ nIdx ] = False
                    # Send Dynamic Commands
                    if ( len ( self.OBPInfo.DynamicCMDs ) and ( int( self.OBPInfo.nBoards[ nIdx ] ) in self.OBPInfo.DynamicCMDs ) ):
                    #{
                        sDynamicCMDs = self.OBPInfo.DynamicCMDs[ self.OBPInfo.nBoards[ nIdx ] ]
                        if ( len( sDynamicCMDs ) ):
                        #{
                            WriteMessage( r"UUT%d(%s:%s) Sending %s..." % ( self.OBPInfo.nBoards[ nIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nIdx ], self.OBPInfo.sDynamicCMDsFileNames[ nIdx ] ) )
                            for sDynamicCMD in sDynamicCMDs:
                            #{
                                if ( not self.SendCommand( OBP_Cmd % ( self.OBPInfo.nChannels[ nIdx ], str( sDynamicCMD ) ), nIdx, True, self.nTimeout ) ):
                                #{
                                    self.fBoardsFailed[ nIdx ] = True
                                    break
                                #}
                            #}
                        #}
                    #}
                    if ( not self.fBoardsFailed[ nIdx ] ):
                    #{
                        if ( nRecycle == 0 ):
                        #{
                            WriteMessage( r"UUT%d(%s:%s) Programming %s ..." % ( self.OBPInfo.nBoards[ nIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nIdx ], self.OBPInfo.sProjectsName[ nIdx ] ) )
                        #}
                        else:
                        #{
                            WriteMessage( r"UUT%d(%s:%s) Retry #%d Program %s ..." % ( self.OBPInfo.nBoards[ nIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nIdx ], nRecycle, self.OBPInfo.sProjectsName[ nIdx ] )  )
                        #}
                        self.fBoardsProgramming[ nIdx ] = True
                        # 
                        if ( not self.SendCommand( OBP_Cmd % ( self.OBPInfo.nChannels[ nIdx ], OBP_Run ) + str( self.OBPInfo.sProjectsName[ nIdx ] ), nIdx, True if ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ) else False, self.nTimeout ) ):
                        #{
                            # TODO : devo mettere self.fInitOK = False per non fargli fare il ciclo GetStatus() . Altimenti :
                            # 1] lancio uno script che non esiste (0000 script_run eee)
                            # 2] fa il ciclo di  GetStatus() a cui risponde sempre BUSY (0000 K B)
                            self.fInitOK = False if ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ) else self.fInitOK
                            self.fBoardsFailed[ nIdx ] = True
                            return False
                        #}
                    #}
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s Programs( %d ) Exception : %s" % ( self.OBPInfo.sProgrammerName, nRecycle, str( e ) ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
        return True
    #}

    def GetResults( self ):
    #{
        try:
        #{
            fProgramming = False
            for nIdx in range( len( self.OBPInfo.nBoards ) ):
            #{
                if ( self.fBoardsProgramming[ nIdx ] ):
                #{
                    fProgramming = True
                    break
                #}
            #}
            if ( not fProgramming ):
            #{
                return True
            #}
            #bRet, bFail = self.GetResponse( False, self.nTimeout ) # if (  self.nTimeout < 1000 ) else 1000 )
            bFail = False
            if ( bFail  ):
            #{
                for nIdx in range( len( self.OBPInfo.nBoards ) ):
                #{
                    if ( self.fBoardsProgramming[ nIdx ] ):
                    #{
                        self.fBoardsProgramming[ nIdx ] = False
                        self.fBoardsFailed[ nIdx ]      = True
                    #}
                #}
                return False
            #}
            elif ( not self.GetStatus( self.nTimeout ) ):
            #{
                for nIdx in range( len( self.OBPInfo.nBoards ) ):
                #{
                    if ( self.fBoardsProgramming[ nIdx ] ):
                    #{
                        self.fBoardsProgramming[ nIdx ] = False
                        self.fBoardsFailed[ nIdx ]      = True
                    #}
                #}
                return False
            #}
            else:
            #{
                for nIdx in range( len( self.OBPInfo.nBoards ) ):
                #{
                    if ( self.fBoardsProgramming[ nIdx ] ):
                    #{
                        self.fBoardsProgramming[ nIdx ] = False
                        if ( self.vcChannelsStatus[ nIdx ] == 'F' ):
                        #{
                            self.fBoardsFailed[ nIdx ] = True
                            if ( not self.GetError( nIdx, self.nTimeout ) ):
                            #{
                                return False
                            #}
                        #}
                        else:
                        #{
                            SetTestInfoEx( "PASS", "N", 1, 0, 1, 2, self.eTestResult, TestView.tvNone, True, self.OBPInfo.nBoards[ nIdx ] )
                        #}
                    #}
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s GetResults() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
        return True
    #}

    def GetBoardsFailed( self ):
    #{
        try:
        #{
            _BoardsFailed = ""
            for nIdx in range( len( self.OBPInfo.nBoards ) ):
            #{
                if ( self.fBoardsFailed[ nIdx ] ):
                #{
                    _BoardsFailed = str( self.OBPInfo.nBoards[ nIdx ] ) if ( _BoardsFailed == "" ) else _BoardsFailed + ",%d" % self.OBPInfo.nBoards[ nIdx ]
                #}
            #}
            return _BoardsFailed
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s GetBoardsFailed() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
            return ""
        #}
        finally:
        #{
            pass
        #}
        return ""
    #}
    
    def SendCommand( self, sCommand, nBoardIdx, fWaitAnswer = True, nTimeout = _nAnswerTimeout ):
    #{
        try:
        #{
            if ( not self.OBPInfo.fEmulated ):
            #{
                Log( "UUT%d( %s:%d ) SendCommand( %s )" % ( self.OBPInfo.nBoards[ nBoardIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], sCommand ) )
                if ( self.OBPInfo.sProgrammerInterface != "" ):
                #{
                    if ( self.OBP_Dll.FR_SendCommandW( self.OBP_Handle, sCommand ) != 0 ):
                    #{
                        ctypes.memset( ctypes.addressof( self.vcAnswer ), 0, ctypes.sizeof( self.vcAnswer ) )
                        self.OBP_Dll.FR_GetLastErrorMessageW( self.vcAnswer, self._MaxAnswerSize )
                        OBPReportFail( "%s SendCommand( %s ) Error : %s" % ( self.OBPInfo.sProgrammerName, sCommand, self.vcAnswer.value ), 
                                         TestResult.ForceFail, 
                                         "UUT%d( %s:%d ) SendCommand( %s ) Error : %s" % ( self.OBPInfo.nBoards[ nBoardIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], sCommand, self.vcAnswer.value ), 
                                         self.OBPInfo.nBoards[ nBoardIdx ] )
                        return False
                    #}
                #}
                else:
                #{
                    if ( self.OBP_Handle.send( bytes( sCommand + OBP_SEND_EOL, 'utf-8' ) ) == 0 ):
                    #{
                        OBPReportFail( "%s SendCommand( %s ) Error : %s" % ( self.OBPInfo.sProgrammerName, sCommand, self.vcAnswer.value ), 
                                         TestResult.ForceFail, 
                                         "UUT%d( %s:%d ) SendCommand( %s ) Error : %s" % ( self.OBPInfo.nBoards[ nBoardIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], sCommand, self.vcAnswer.value ), 
                                         self.OBPInfo.nBoards[ nBoardIdx ] )
                        return False
                    #}
                #}
            #}
            if ( fWaitAnswer ):
            #{
                bRet, bFail = self.GetResponse( True, nTimeout )
                if ( not bRet or bFail  ):
                #{
                    self.GetError( nBoardIdx, nTimeout )
                    return False
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s SendCommand( %s ) Exception : %s" % ( self.OBPInfo.sProgrammerName, sCommand, str( e ) ), 
                             TestResult.ForceFail, 
                             "UUT%d( %s:%d ) SendCommand( %s ) Exception : %s" % ( self.OBPInfo.nBoards[ nBoardIdx ], self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], sCommand, str( e ) ),
                             self.OBPInfo.nBoards[ nBoardIdx ] )
            return False
        #}
        finally:
        #{
            pass
        #}
        return True
    #}

    def GetResponse( self, fTimeoutError = True, nTimeout = _nAnswerTimeout ):
    #{
        global OBP_RECV_PASS
        global OBP_RECV_FAIL
        global OBP_RECV_FAIL1
        global OBP_RECV_FAIL2
        try:
        #{
            if ( not self.OBPInfo.fEmulated ):
            #{
                if ( self.OBPInfo.sProgrammerInterface != "" ):
                #{
                    ctypes.memset( ctypes.addressof( self.vcAnswer ), 0, ctypes.sizeof( self.vcAnswer ) )
                    if ( self.OBP_Dll.FR_GetAnswerW( self.OBP_Handle, self.vcAnswer, self._MaxAnswerSize, int( nTimeout ) ) != 0 ):
                    #{
                        if ( fTimeoutError ):
                        #{
                            ctypes.memset( ctypes.addressof( self.vcAnswer ), 0, ctypes.sizeof( self.vcAnswer ) )
                            self.OBP_Dll.FR_GetLastErrorMessageW( self.vcAnswer, self._MaxAnswerSize )
                            OBPReportFail( "%s GetResponse() Error : %s" % ( self.OBPInfo.sProgrammerName, self.vcAnswer.value ), TestResult.ForceFail )
                            return False, True
                        #}
                        else:
                        #{
                            return False, False
                        #}
                    #}
                #}
                else:
                #{
                    self.vcAnswer = ""
                    Timer = CTimer()
                    Timer.StartTimer()
                    while not Timer.TimerExpired( nTimeout ):
                    #{
                        try:
                        #{
                            data = self.OBP_Handle.recv( self._MaxAnswerSize ).decode( 'utf-8' )
                        #}
                        except socket.timeout as e:
                        #{
                            CheckStopProgram()
                            continue
                        #}
                        except Exception as e:
                        #{
                            raise e
                        #}
                        self.vcAnswer = self.vcAnswer + data
                        if ( self.OBPInfo.eProgrammerType == eProgrammerType._SMH20 ):
                        #{
                            if ( ( OBP_RECV_PASS in self.vcAnswer ) or ( OBP_RECV_FAIL in self.vcAnswer ) ):
                            #{
                                break
                            #}
                        #}
                        elif ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ):
                        #{                    
                            if ( OBP_RECV_EOL in self.vcAnswer ):
                            #{
                                break
                            #}
                        #}
                    #}
                    if ( Timer.TimerExpired( nTimeout ) ):
                    #{
                        if ( fTimeoutError ):
                        #{
                            OBPReportFail( "%s GetResponse() Error : Timeout" % self.OBPInfo.sProgrammerName, TestResult.ForceFail, "%s GetResponse() Error : Timeout( %d )" % ( self.OBPInfo.sProgrammerName, nTimeout ) )
                            return False, True
                        #}
                        else:
                        #{
                            return False, False
                        #}
                    #}
                #}
                self.TrimResponse()
                Log( "%s GetResponse() : %s" % ( self.OBPInfo.sProgrammerName, self.sResponse ) )
                if ( self.OBPInfo.eProgrammerType == eProgrammerType._SMH20 ):
                #{
                    if ( OBP_RECV_FAIL in self.sResponse ):
                    #{
                        OBPReportFail( "%s Error : %s" % ( self.OBPInfo.sProgrammerName, self.sResponse ), self.eTestResult )
                        return True, True
                    #}
                    return True, False
                #}
                elif ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ):
                #{                    
                    # bisogna ritornare fail se ho 'K E'  'K S'  'E *' 
                    sChannelsStatus = str( self.sResponse ).split( " " )
                    StatusError = False
                    if ( len( sChannelsStatus ) > 2 ):
                    #{
                        if ( ( sChannelsStatus[ 2 ] == OBP_RECV_FAIL ) or ( sChannelsStatus[ 2 ] == OBP_RECV_FAIL1 ) ):
                        #{
                            StatusError = True
                        #}
                    #}    
                    return True, True if ( StatusError or ( sChannelsStatus[ 1 ] == OBP_RECV_FAIL ) ) else False
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s GetResponse() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
            return False, False
        #}
        finally:
        #{
            pass
        #}
        return True, False
    #}

    def GetStatus( self, nTimeout = _nAnswerTimeout ):
    #{
        try:
        #{
            if ( not self.OBPInfo.fEmulated ):
            #{
                Timer = CTimer()
                Timer.StartTimer()
                while not Timer.TimerExpired( nTimeout ):
                #{
                    if ( not self.SendCommand( OBP_Cmd %( self.OBPInfo.nMasterChannel, OBP_GetEngStatus ), self._Master, True, nTimeout ) ):
                    #{
                        return False
                    #}
                    sChannelsStatus = str( self.sResponse ).split( "|" )
                    if ( len( sChannelsStatus ) < 3 ):
                    #{
                        return False
                    #}
                    if ( int( sChannelsStatus[ 0 ] ) == self.OBPInfo.nMasterChannel ):
                    #{
                        bBusy = False
                        for nIdx in range( len( self.OBPInfo.nChannels ) ):
                        #{
                            self.vcChannelsStatus[ nIdx ] = sChannelsStatus[ 1 ][ self.OBPInfo.nChannels[ nIdx ] - 1 ]
                            if ( ( self.vcChannelsStatus[ nIdx ] == 'B' ) or ( self.vcChannelsStatus[ nIdx ] == 'R' ) ):
                            #{
                                bBusy = True
                                break
                            #}
                        #}
                        if ( not bBusy ):
                        #{
                            break
                        #}
                    #}
                    CheckStopProgram()
                    Delay( 0.05 )
                #}
                if ( Timer.TimerExpired( nTimeout ) ):
                #{
                    OBPReportFail( "%s GetStatus() Error : Timeout" % self.OBPInfo.sProgrammerName, TestResult.ForceFail, "%s GetStatus() Error : Timeout( %d )" % ( self.OBPInfo.sProgrammerName, nTimeout ) )
                    return False
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s GetStatus() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
        return True
    #}

    def GetError( self, nBoardIdx, nTimeout = _nAnswerTimeout ):
    #{
        try:
        #{
            if ( not self.OBPInfo.fEmulated ):
            #{
                if ( self.OBPInfo.eProgrammerType == eProgrammerType._SMH20 ):
                #{
                    sGetErr = str( OBP_Cmd % ( self.OBPInfo.nChannels[ nBoardIdx ], OBP_GetError ) )
                    if ( not self.SendCommand( sGetErr, nBoardIdx, False, nTimeout ) ):
                    #{
                        return False
                    #}
                    bRet, bFail = self.GetResponse( True, nTimeout )
                    if ( not bRet or bFail  ):
                    #{
                        return False
                    #}
                    self.TrimResponse()
                    if ( OBP_Error in str( self.sResponse ) ):
                    #{
                        sTestErrorInfo = self.TrimResponse()
                    
                        #MessageBox ("togliere le righe ripetute", sTestErrorInfo)
                        # togliere le righe ripetute 
                    
                        OBPReportFail( "%s:%d Error : %s\n%s" % ( self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], self.OBPInfo.sProjectsName[ nBoardIdx ], str( sTestErrorInfo ) ), self.eTestResult, int( self.OBPInfo.nBoards[ nBoardIdx ] ) )
                        return True
                    #}
                #}
                elif ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ):
                #{
                    OBPReportFail( self.MsgChErr[ nBoardIdx ], self.eTestResult, int( self.OBPInfo.nBoards[ nBoardIdx ] ) )
                    # TODO : log_get
                    return True
                #}
            #}
        #}
        except Exception as e:
        #{
            OBPReportFail( "%s GetError() Exception : %s" % ( self.OBPInfo.sProgrammerName, str( e ) ), 
                             TestResult.ForceFail, 
                             "UUT%d( %s:%d ) GetError() Exception : %s" % ( int( self.OBPInfo.nBoards[ nBoardIdx ] ), self.OBPInfo.sProgrammerName, self.OBPInfo.nChannels[ nBoardIdx ], str( e ) ),
                             int( self.OBPInfo.nBoards[ nBoardIdx ] ) )
            return False
        #}
        finally:
        #{
            pass
        #}
        return True
    #}

    def TrimResponse( self ):
    #{
        self.sResponse = ""
        if ( self.OBPInfo.eProgrammerType == eProgrammerType._SMH20 ):
        #{
            self.sResponse = str( self.vcAnswer.value if ( self.OBPInfo.sProgrammerInterface != "" ) else self.vcAnswer )
            nStartIdx = str( self.sResponse ).find( OBP_RECV_PASS )
            if ( nStartIdx != -1 ):
            #{
                self.sResponse = str( self.sResponse[ :nStartIdx ] )
            #}
        #}
        elif ( self.OBPInfo.eProgrammerType == eProgrammerType._SEICA ):
        #{
            self.sResponse = str( self.vcAnswer )
            nStartIdx = str( self.sResponse ).find( OBP_RECV_EOL )
            if ( nStartIdx != -1 ):
            #{
                self.sResponse = str( self.sResponse[ :nStartIdx ] )
            #}
        #}
        else:
        #{
            self.sResponse = str( self.vcAnswer )
        #}
        return self.sResponse
    #}
#}

def OBPReportFail( TestErroInfo : str,
                   Tresult : TestResult,
                   LogErrorInfo : str = None, 
                   Board : int = -1
                   ):              
#{
    ReportFail( TestErroInfo, Tresult )
    global g_fWriteMessageError
    if ( g_fWriteMessageError ):
    #{
        WriteMessage( TestErroInfo )
    #}
    Log( LogErrorInfo if ( ( LogErrorInfo is not None ) and ( LogErrorInfo != "" ) ) else TestErroInfo )
#}

def LoadDynamicCMDs( eTestResult, BoardCfgFile, nBoard, nLoopCounter ):
#{
    try:
    #{
        sBoardPath          = GetBoardPath()
        sBoardName          = GetBoardName()
        sDynamicCMDs        = []
        sDynamicCMDsFileName = BoardCfgFile.Read( _DynamicSectionKey, _DynamicKey % nLoopCounter,         "" )
        if ( sDynamicCMDsFileName == "" ):
        #{
            return True, sDynamicCMDsFileName, sDynamicCMDs
        #}
        if ( ( sDynamicCMDsFileName != "" ) and not os.access( sBoardPath + sBoardName + "\\" + sDynamicCMDsFileName, os.R_OK ) ):
        #{
            OBPReportFail( "%s Not Found!" % ( sBoardPath + sBoardName + "\\" + sDynamicCMDsFileName ), TestResult.ForceFail )
            return False, sDynamicCMDsFileName, sDynamicCMDs
        #}
        DynamicCMDFile = CFileIni( sBoardPath + sBoardName + "\\" + sDynamicCMDsFileName )

        nCmd = 1
        while( True ):
        #{
            sCmd = ""
            sCmd = DynamicCMDFile.Read( _BoardSectionKey % int( nBoard ), _CMDKey % nCmd, "" )
            if ( sCmd == "" ):
            #{
                break
            #}
            sDynamicCMDs.append( sCmd )
            nCmd += 1
        #}
        return True, sDynamicCMDsFileName, sDynamicCMDs
    #}
    except Exception as e:
    #{
        OBPReportFail( "LoadDynamicCMDs() Exception : %s" % str( e ), TestResult.ForceFail )
        return False, "", ""
    #}
    finally:
    #{
        pass
    #}
    return False, "", ""
#}

def GetParallelInfo( sProjectName, OBPsInfo, eTestResult ):
#{
    global OBP_Cmd          
    global OBP_PrjNameExt      
    global OBP_GetEngStatus 
    global OBP_ClearErr     
    global OBP_Sping    
    global OBP_SetRelays    
    global OBP_Run            
    global OBP_GetError     
    global OBP_Error        
    global OBP_SEND_EOL         
    global OBP_RECV_EOL         
    global OBP_RECV_PASS         
    global OBP_RECV_FAIL
    global OBP_RECV_FAIL1
    global OBP_RECV_FAIL2
    try:
    #{
        sVivaPath           = GetVivaPath()
        sBoardPath          = GetBoardPath()
        sBoardName          = GetBoardName()
        nCurrentBoardNumber = GetCurrentBoardNumber()
        BoardsFailed = ""
        bRet, nParType, Value = GetGlobalVariable( GVParallelMode._sBoardsFailed )
        if ( bRet and ( nParType == ParVarType.string ) and ( Value != "" ) ):
        #{
            BoardsFailed = str( Value ).split( "," )
        #}
        # Get Parallel Test Mode Present
        if ( not os.access( sVivaPath + _SysCfgFileName, os.R_OK ) ):
        #{
            OBPReportFail( "%s Not Found!" % ( sVivaPath + _SysCfgFileName ), TestResult.ForceFail )
            return 0
        #}
        if ( not os.access( sBoardPath + sBoardName + "\\" + _BrdCfgFileName, os.R_OK ) ):
        #{
            OBPReportFail( "%s Not Found!" % ( sBoardPath + sBoardName + "\\" + _BrdCfgFileName ), TestResult.ForceFail )
            return 0
        #}
        SystemCfgFile           = CFileIni( sVivaPath + _SysCfgFileName )
        ProgrammerType          = eProgrammerType( SystemCfgFile.Read(  _SettingsSectionKey,                    _ProgrammerTypeKey,         eProgrammerType._SMH20.value )  )
        nMasterChannel          = int( SystemCfgFile.Read(              ProgrammerType.value,                   _OBP_MasterChannel_Key,     str( SMH_OBP_MasterChannel ) )  )
        BoardCfgFile            = CFileIni( sBoardPath + sBoardName + "\\" + _BrdCfgFileName )
        global g_fWriteMessageError
        g_fWriteMessageError    = True if ( BoardCfgFile.Read(          _SettingsSectionKey,                    _WriteMessageErrorKey,      "" ) == "Y" ) else False
        sLogFileName            = BoardCfgFile.Read(                    _SettingsSectionKey,                    _LogFileNameKey,            "" )
        global g_fLogging
        g_fLogging              = True if ( ( BoardCfgFile.Read(        _SettingsSectionKey,                   _LoggingKey,                 "" ) == "Y" ) and ( sLogFileName != "" ) ) else False
        if ( g_fLogging ):
        #{
            if ( not os.path.isabs( sLogFileName ) ):
            #{
                sLogFileName = sBoardPath + sBoardName + "\\" + sLogFileName
            #}
            logging.basicConfig( filename = sLogFileName, format = "%(asctime)-15s %(message)s" )
        #}
        sMaster                 = BoardCfgFile.Read( _BoardSectionKey % nCurrentBoardNumber,    _MasterKey,                 "" )
        nMaster                 = 0 if ( sMaster == "" ) else int( sMaster )
        sBrothers               = BoardCfgFile.Read( _BoardSectionKey % nCurrentBoardNumber,    _BrothersKey,               "" )
        fParallelMode           = True
        if ( ( nMaster == 0 ) or ( sBrothers == "" ) ):
        #{
            fParallelMode = False
        #}
        else:
        #{
            if ( str( sBrothers ).upper() != "ALL" ):
            #{
                Boards = str( sBrothers ).split( "," )
            #}
            else:
            #{
                Boards = []
                for nBoard in range( GetNumBoards() ):
                #{
                    Boards.append( nBoard + 1 )
                #}
            #}
            nBoardsEnabled = 0
            for nBoard in range( len( Boards ) ):
            #{
                if ( ( Boards[ nBoard ] != "" ) and IsBoardEnabled( int( Boards[ nBoard ] ) ) ):
                #{
                    nBoardsEnabled += 1
                #}
            #}
            if ( nBoardsEnabled <= 1 ):
            #{
                fParallelMode = False
            #}
            elif ( nMaster != nCurrentBoardNumber ):
            #{
                if ( not IsBoardEnabled( nMaster ) or IsBoardFailed( BoardsFailed, nMaster ) ):
                #{
                    fParallelMode = False
                    for nBoard in range( len( Boards ) - 1, 0, -1 ):
                    #{
                        if ( ( Boards[ nBoard ] != "" ) and IsBoardEnabled( Boards[ nBoard ] ) and not IsBoardFailed( BoardsFailed, Boards[ nBoard ] ) ):
                        #{
                            if ( int( Boards[ nBoard ] ) != nCurrentBoardNumber ):
                            #{
                                SetTestInfoEx( "", "N", 1, 0, 1, 2, eTestResult )
                                return 0
                            #}
                            else:
                            #{
                                fParallelMode = True
                                break
                            #}
                        #}
                    #}
                #}
                else:
                #{
                    SetTestInfoEx( "", "N", 1, 0, 1, 2, eTestResult )
                    return 0
                #}
            #}
        #}
        if ( not fParallelMode ):
        #{
            if ( not IsBoardFailed( BoardsFailed, nCurrentBoardNumber ) ):
            #{
                Boards = []
                Boards.append( str( nCurrentBoardNumber ) )
            #}
            else:
            #{
                OBPReportFail( "UUT%d NOT PROGRAMMED for a previous ICT/OBP FAIL" % nCurrentBoardNumber, eTestResult )
                return 0
            #}
        #}
        nLoopCounter = 0
        bRet    = False
        Value   = ""
        bRet, nParType, Value = GetGlobalVariable( _sOBPLoopGV )
        if ( bRet and ( nParType == ParVarType.string ) and ( Value != "" ) ):
        #{
            nLoopCounter = int( Value )
        #}
        else:
        #{
            bRet, nLoopCounter = GetLoopCounter()
            if ( not bool( bRet ) ):
            #{
                OBPReportFail( "GetLoopCounter Error!", TestResult.ForceFail )
                return 0
            #}
            nLoopCounter += 1
        #}
        if ( nLoopCounter == 0 ):
        #{
            OBPReportFail( "Viva Variable OBP_Loop = 0   FixRelConfID = 0", eTestResult )
            return 0
        #}
        sProgrammerInterface    = SystemCfgFile.Read(                   _SettingsSectionKey,                    _ProgrammerInterfaceKey,        "" )
        if ( sProgrammerInterface == "" ):
        #{
            sProgrammerInterface = SystemCfgFile.Read(                  ProgrammerType.value,                       _ProgrammerInterfaceKey,    "" )
        #}
        OBP_Cmd                 = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_Cmd_Key,               "" )
        OBP_PrjNameExt          = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_PrjNameExt_Key,        "" )
        OBP_GetEngStatus        = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_GetEngStatus_Key,      "" )
        OBP_ClearErr            = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_ClearErr_Key,          "" )
        OBP_Sping               = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_Sping_Key,             "" )
        OBP_SetRelays           = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_SetRelays_Key,         "" )
        OBP_Run                 = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_Run_Key,               "" )
        OBP_GetError            = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_GetError_Key,          "" )
        OBP_Error               = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_Error_Key,             "" )
        OBP_SEND_EOL            = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_SEND_EOL_Key,          "" )
        OBP_SEND_EOL = OBP_SEND_EOL.replace( "\\n", "\n" )
        OBP_SEND_EOL = OBP_SEND_EOL.replace( "\\r", "\r" )
        OBP_SEND_EOL = OBP_SEND_EOL.replace( "\\0", "\0" )
        OBP_RECV_EOL            = SystemCfgFile.Read(                   ProgrammerType.value,                       _OBP_RECV_EOL_Key,          "" )
        OBP_RECV_EOL = OBP_RECV_EOL.replace( "\\n", "\n" )
        OBP_RECV_EOL = OBP_RECV_EOL.replace( "\\r", "\r" )
        OBP_RECV_EOL = OBP_RECV_EOL.replace( "\\0", "\0" )
        OBP_RECV_PASS       = SystemCfgFile.Read(                       ProgrammerType.value,                       _OBP_RECV_PASS_Key,         "" )
        OBP_RECV_PASS = OBP_RECV_PASS.replace( "\\n", "\n" )
        OBP_RECV_PASS = OBP_RECV_PASS.replace( "\\r", "\r" )
        OBP_RECV_PASS = OBP_RECV_PASS.replace( "\\0", "\0" )
        OBP_RECV_FAIL       = SystemCfgFile.Read(                       ProgrammerType.value,                       _OBP_RECV_FAIL_Key,         "" )
        OBP_RECV_FAIL = OBP_RECV_FAIL.replace( "\\n", "\n" )
        OBP_RECV_FAIL = OBP_RECV_FAIL.replace( "\\r", "\r" )
        OBP_RECV_FAIL = OBP_RECV_FAIL.replace( "\\0", "\0" )
        OBP_RECV_FAIL1      = SystemCfgFile.Read(                       ProgrammerType.value,                       _OBP_RECV_FAIL1_Key,        "" )
        OBP_RECV_FAIL1 = OBP_RECV_FAIL1.replace( "\\n", "\n" )
        OBP_RECV_FAIL1 = OBP_RECV_FAIL1.replace( "\\r", "\r" )
        OBP_RECV_FAIL1 = OBP_RECV_FAIL1.replace( "\\0", "\0" )
        OBP_RECV_FAIL2      = SystemCfgFile.Read(                       ProgrammerType.value,                       _OBP_RECV_FAIL2_Key,        "" )
        OBP_RECV_FAIL2 = OBP_RECV_FAIL2.replace( "\\n", "\n" )
        OBP_RECV_FAIL2 = OBP_RECV_FAIL2.replace( "\\r", "\r" )
        OBP_RECV_FAIL2 = OBP_RECV_FAIL2.replace( "\\0", "\0" )
        for nBoard in range( len( Boards ) ):
        #{
            if ( ( Boards[ nBoard ] != "" ) and IsBoardEnabled( Boards[ nBoard ] ) and not IsBoardFailed( BoardsFailed, Boards[ nBoard ] ) ):
            #{
                sOBP                    = BoardCfgFile.Read(            _BoardSectionKey % int( Boards[ nBoard ] ), _OBPKey,                    "" )
                sChannel                = BoardCfgFile.Read(            _BoardSectionKey % int( Boards[ nBoard ] ), _ChannelKey,                "" )
                nChannel                = 0 if ( sChannel == "" ) else int( sChannel )
                sIP                     = SystemCfgFile.Read(           sOBP,                                       _IPKey,                     "" )
                sPort                   = SystemCfgFile.Read(           sOBP,                                       _PortKey,                   "" )
                sNumChannels            = SystemCfgFile.Read(           sOBP,                                       _ChannelsKey,               "" )
                nNumChannels            = 0 if ( sNumChannels == "" ) else int( sNumChannels )
                fEmulated               = True if ( GetEmulation() ) else True if ( SystemCfgFile.Read( sOBP,       _EmulatedKey,               "" ) == "Y" ) else False
                if ( sOBP == "" ):
                #{
                    OBPReportFail( "Programmer Name Not Defined in %s / Section: [B%s] / Key: %s=" % (_BrdCfgFileName, Boards[ nBoard ], _OBPKey), TestResult.ForceFail )
                    return 0
                #}
                elif ( ( sIP == "" ) or ( sPort == "" ) or ( nNumChannels == 0 ) ):
                #{
                    OBPReportFail( "Invalid IP,Port,Channels in %s / section [%s] " % (_SysCfgFileName, sOBP), TestResult.ForceFail )
                    return 0
                #}
                elif ( ( nChannel == 0 ) or ( nChannel > nNumChannels ) ):
                #{
                    OBPReportFail( "Invalid Channel : %s /[B%s] /%s=%d  > %s / [B%s]/%s=%d" % (_BrdCfgFileName, Boards[ nBoard ], _ChannelKey, nChannel, _SysCfgFileName, sOBP, _ChannelsKey, nNumChannels), TestResult.ForceFail )
                    return 0
                #}
                _sProjectName = sProjectName
                if ( _sProjectName == "" ):
                #{
                    _sProjectName = BoardCfgFile.Read( _ProjectsSectionKey, BoardCfgFile.Read( _BoardSectionKey % int( Boards[ nBoard ] ), _ProjectKey % nLoopCounter, "" ), "" )
                    _sProjectName = ( "%s%s" % ( _sProjectName, OBP_PrjNameExt ) ) if ( not ( OBP_PrjNameExt in _sProjectName ) ) else _sProjectName
                #}
                if ( sOBP in OBPsInfo ):
                #{
                    OBPInfo = OBPsInfo[ sOBP ]
                    OBPInfo.nBoards.append( int( Boards[ nBoard ] ) )
                    OBPInfo.nChannels.append( nChannel )
                    OBPInfo.sProjectsName.append( _sProjectName ) 
                    bRet, sDynamicCMDsFileName, sDynamicCMDs = LoadDynamicCMDs( eTestResult, BoardCfgFile, Boards[ nBoard ], nLoopCounter )
                    if ( not bRet ):
                    #{
                        return 0
                    #}
                    OBPInfo.sDynamicCMDsFileNames.append( sDynamicCMDsFileName )
                    OBPInfo.DynamicCMDs[ int( Boards[ nBoard ] ) ] = sDynamicCMDs
                    OBPsInfo[ sOBP ] = OBPInfo
                #}
                else:
                #{
                    nBoards                 = []
                    nChannels               = []
                    sProjectsName           = []
                    sDynamicCMDsFileNames   = []
                    DynamicCMDs             = dict()
                    nBoards.append( int( Boards[ nBoard ] ) )
                    nChannels.append( nChannel )
                    sProjectsName.append( _sProjectName ) 
                    bRet, sDynamicCMDsFileName, sDynamicCMDs = LoadDynamicCMDs( eTestResult, BoardCfgFile, Boards[ nBoard ], nLoopCounter )
                    if ( not bRet ):
                    #{
                        return 0
                    #}
                    sDynamicCMDsFileNames.append( sDynamicCMDsFileName )
                    DynamicCMDs[ int( Boards[ nBoard ] ) ] = sDynamicCMDs
                    OBPsInfo[ sOBP ] = OBPInfo_t( sOBP, ProgrammerType, sProgrammerInterface, sIP, sPort, nNumChannels, nMasterChannel, fEmulated, nBoards, nChannels, sProjectsName, sDynamicCMDsFileNames, DynamicCMDs )
                #}
            #}
        #}
        if ( len( OBPsInfo ) == 0 ):
        #{
            OBPReportFail( "No Boards Enabled", eTestResult )
            return 0
        #}
        return len( OBPsInfo )
    #}
    except Exception as e:
    #{
        OBPReportFail( "GetParallelInfo() Exception : %s" % str( e ), TestResult.ForceFail )
        return 0
    #}
    finally:
    #{
        pass
    #}
    return 0
#}

def OBPRun( OBPsInfo, nTimeout, nRecycles, eTestResult ):
#{
    try:
    #{
        if ( len( OBPsInfo ) == 0  ):
        #{
            return True
        #}
        OBPs = []
        for sOBPInfo in sorted( OBPsInfo.keys() ):
        #{
            OBP = COBP( OBPsInfo[ sOBPInfo ], nTimeout, nRecycles, eTestResult )
            OBPs.append( OBP )
        #}
        for nRecycle in range( nRecycles ):
        #{
            BoardsFailed = ""
            for OBP in OBPs:
            #{
                if ( OBP.fInitOK ):
                #{
                    if ( not OBP.Programs( nRecycle ) ):
                    #{
                        break
                    #}
                #}
            #}
            Delay( 0.5 )
            for OBP in OBPs:
            #{
                if ( OBP.fInitOK ):
                #{
                    if ( not OBP.GetResults() ):
                    #{
                        break
                    #}
                #}
            #}
            for OBP in OBPs:
            #{
                _BoardsFailed = OBP.GetBoardsFailed()
                if ( _BoardsFailed != "" ):
                #{
                    BoardsFailed = _BoardsFailed if ( BoardsFailed == "" ) else  BoardsFailed + "," + _BoardsFailed
                #}
            #}
            if ( BoardsFailed == "" ):
            #{
                break
            #}
        #}
        for OBP in OBPs:
        #{
            del OBP
        #}
        if ( BoardsFailed != "" ):
        #{
            SetGlobalVariable( GVParallelMode._sBoardsFailed, BoardsFailed )
            return False
        #}
    #}
    except Exception as e:
    #{
        OBPReportFail( "OBPRun() Exception : %s" % str( e ), TestResult.ForceFail )
        return False
    #}
    finally:
    #{
        pass
    #}
    return True
#}

def OBP( COMStoreName ):
#{
    #TODO: Add your code here
    OBPReportFail( "", TestResult.ForceFail )
    # Get Macro Parameters
    bRet, nParType, sProjectName    = GetCurMacroParameter( "ProjectName" )
    if ( not bRet ):
    #{
        OBPReportFail( "Parameter \"ProjectName\" Error", TestResult.ForceFail )
        return ScriptResult.TestContinue
    #}
    bRet, nParType, Value           = GetCurMacroParameter( "Time" )
    if ( not bRet ):
    #{
        OBPReportFail( "Parameter \"Time\" Error", TestResult.ForceFail )
        return ScriptResult.TestContinue
    #}
    nTime                           = float( Value ) * 1000
    bRet, nParType, Value           = GetCurMacroParameter( "Recycle" )
    if ( not bRet ):
    #{
        OBPReportFail( "Parameter \"Recycle\" Error", TestResult.ForceFail )
        return ScriptResult.TestContinue
    #}
    nRecycles                       = int( Value ) + 1
    bRet, nParType, Value           = GetCurMacroParameter( "TestResult" )
    if ( not bRet ):
    #{
        OBPReportFail( "Parameter \"TestResult\" Error", TestResult.ForceFail )
        return ScriptResult.TestContinue
    #}
    eTestResult                     = TestResult( Value )
    eTestResult                     = eTestResult if ( eTestResult != TestResult.Default ) else TestResult.TestResult

    OBPsInfo = dict()
    if ( GetParallelInfo( sProjectName, OBPsInfo, eTestResult ) == 0 ):
    #{
        return ScriptResult.TestContinue
    #}
    if ( not OBPRun( OBPsInfo, nTime, nRecycles, eTestResult ) ):
    #{
        return ScriptResult.TestContinue
    #}
    return ScriptResult.TestContinue
#}
