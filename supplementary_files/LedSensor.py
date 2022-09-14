# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

# Macro Version Info
#
# Description :         Implementation of the Led Sesor Macro.
# Version :             2.0.0
# Created :             31/07/2019
#
# Revision History :
#
#        1.0.0   - 31/07/2019 : First Release
#        2.0.0   - 11/06/2020 : Python 3.x and FNTools
#
# Macro Version Info

import collections
from collections import namedtuple
import subprocess
import sys
import xml.etree.ElementTree as ET

from FNtools import *

class eCaptureType( IntEnum ):
#{
    _ctNone                         = 0
    _ctRange                        = 1
    _ctFactorPWM                    = 2
#}

class eRange( IntEnum ):
#{
    _rNone                          = 0
    _rLow                           = 1
    _rMedium                        = 2
    _rHigh                          = 3
    _rSuper                         = 4
    _rUltra                         = 5
    _rUser                          = 6
    _rNumRange                      = 6
#}

class eTableRef( IntEnum ):
#{
    _tblrOFF                        = 0
    _tblrRed                        = 1
    _tblrGreen                      = 2
    _tblrBlue                       = 3
    _tblrYellow                     = 4
    _tblrOrange                     = 5
    _tblrWhite                      = 6
#}

class eUser( IntEnum ):
#{
    _uNone                          = 0
    _uUserGains                     = 1
    _uUserSoftware                  = 2
    _uUserXYOffsets                 = 1
#}

class eMeasureView( IntEnum ):
#{
    _mvHUE                          = 1
    _mvSaturation                   = 2
    _mvIntensity                    = 3
    _mvx                            = 4
    _mvy                            = 5
    _mvWatt                         = 6
    _mvWaveLength                   = 7
    _mvCCT                          = 8
    _mvDeltaEDistance               = 9
    _mvRGB                          = 10
    _mvRed                          = 11
    _mvGreen                        = 12
    _mvBlue                         = 13
    _mvXYZ                          = 14
    _mvX                            = 15
    _mvY                            = 16
    _mvZ                            = 17
#}

class ePowerMode( IntEnum ):
#{
    _pStandard                      = 0
    _pExtHV                         = 1
    _pNone                          = 2
#}

_FeasaINIFile                   = "Feasa.ini"
_FeasaLAUserGains               = r"C:\Program Files (x86)\FEASA Led Analyser\UserGains\UserGains.exe"
_FeasaLAUserSoftware            = r"C:\Program Files (x86)\FEASA Led Analyser\UserSoftware\UserSoftware.exe"
_FeasaLAUserXYOffsets           = r"C:\Program Files (x86)\FEASA Led Analyser\UserXYOffsets\UserXYOffsets.exe"

_FeasaSUserGains               = r"C:\Program Files (x86)\FEASA Spectrometer\Spectrometer\Spectrometer.exe"
_FeasaSUserSoftware            = r"C:\Program Files (x86)\FEASA Spectrometer\Spectrometer\Spectrometer.exe"
_FeasaSUserXYOffsets           = r"C:\Program Files (x86)\FEASA Spectrometer\Spectrometer\Spectrometer.exe"

_sHUEUnit                       = "HUE"
_sSaturationUnit                = "SAT"
_sIntensityUnit                 = "INT"
_sRedUnit                       = "R"
_sGreenUnit                     = "G"
_sBlueUnit                      = "B"
_sxUnit                         = "x"
_syUnit                         = "y"
_sWattUnit                      = "W"
_sWaveLengthUnit                = "nm"
_sCCTUnit                       = "K"
_sDeltaEDistanceUnit            = "K"
_sXUnit                         = "X"
_sYUnit                         = "Y"
_sZUnit                         = "Z"

_dHUEDefaultTolPos              = 20
_dHUEDefaultTolNeg              = 20
_nSaturationDefaultTolPos       = 20
_nSaturationDefaultTolNeg       = 20
_nIntensityDefaultTolPos        = 40
_nIntensityDefaultTolNeg        = 40

_nRedDefaultTolPos              = 20
_nRedDefaultTolNeg              = 20
_nGreenDefaultTolPos            = 20
_nGreenDefaultTolNeg            = 20
_nBlueDefaultTolPos             = 20
_nBlueDefaultTolNeg             = 20

_dxDefaultTolPos                = 20
_dxDefaultTolNeg                = 20
_dyDefaultTolPos                = 20
_dyDefaultTolNeg                = 20

_nWaveLengthDefaultTolPos       = 20
_nWaveLengthDefaultTolNeg       = 20

_nCCTDefaultTolPos              = 20
_nCCTDefaultTolNeg              = 20

_dXDefaultTolPos                = 20
_dXDefaultTolNeg                = 20
_dYDefaultTolPos                = 20
_dYDefaultTolNeg                = 20
_dZDefaultTolPos                = 20
_dZDefaultTolNeg                = 20

_sHSIDataLogFileName            = "HSI_Datalog.csv"
_sxyDataLogFileName             = "xy_Datalog.csv"
_sRGBDataLogFileName            = "RGB_Datalog.csv"
_sRedDataLogFileName            = "RED_Datalog.csv"
_sGreenDataLogFileName          = "GREEN_Datalog.csv"
_sBlueDataLogFileName           = "BLUE_Datalog.csv"
_sWLDataLogFileName             = "WaveLength_Datalog.csv"
_sCCTDataLogFileName            = "CCT_Datalog.csv"
_sXYZDataLogFileName            = "XYZ_Datalog.csv"
_sXDataLogFileName              = "X_Datalog.csv"
_sYDataLogFileName              = "Y_Datalog.csv"
_sZDataLogFileName              = "Z_Datalog.csv"
_sDataLogFieldSeparator         = ";"

_DefaultTimeout                 = 50

class eErrorCode( IntEnum ):
#{
    _NoError                          = 0
    _InvalidParameters                = 1
    _DeviceNotPresent                 = 2
    _ConfigurationNotPresent          = 3
    _InvalidManufacturerID            = 4
    _InvalidHwID                      = 5
    _InvalidMaxFiberNr                = 6
    _CommandNotSupported              = 7
    _InvalidCommunicationPort         = 8
    _CommunicationDeviceNotPresent    = 9
    _CommunicationOpenError           = 10
    _CommunicationError               = 11
    _CommunicationTimeout             = 12
    _CommandError                     = 13
#}

# Global Variables
_sLS_CaptureType                = "LS_CaptureType"
_sLS_Range                      = "LS_Range"
_sLS_FactorPWM                  = "LS_FactorPWM"
_sLS_TestResult                 = "LS_TestResult"
_sLS_ResetStoreData             = "LS_ResetStoreData"

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CLedSensor:
#{
    _eInstrumentUnknown = -1
    _eLedAnalyser       = 0
    _eSpectrometer      = 1
    BoardInfo_t         = namedtuple( 'BoardInfo_t', [ 'nBoard', 'sBarcode', 'nSensorPin' ] )
    LedSensorInfo_t     = namedtuple( 'LedSensorInfo_t', [ 'sComponentName', 'nSensorPin', 'nLedSensorNumber', 'eInstrumentType', 'sHwID', 'nMaxFiberNr', 'nFiberChannel', 'dxOffset', 'dyOffset', 'nWaveLengthOffset', 'fFailed' ] )

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ctor - CLedSensor
    #
    def __init__( self, COMStoreName : str ):
    #{
        try:
        #{
            self.fInitOK                                        = False
            self.fMove                                          = False
            self.sComponentsName                                = []
            self.nChannels                                      = 0
            self.fLearn                                         = False
            self.sComponentName                                 = GetComponentName()
            self.sMacroName, self.sInstrName, self.nSequence    = GetMacroInfo()
            self.nCurrentBoardNumber                            = GetCurrentBoardNumber()
            self.BoardCode                                      = GetBoardCode()
            self.fEmulation                                     = GetEmulation()
            fAutoDebug, fAutoLearn, fAutoAdjust                 = GetTestSettings()
            self.fLearn                                         = fAutoLearn or fAutoDebug
            self.fResetStoreData                                = False
            self.fInitOK                                        = True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "__init__() Exception : %s" % str( e ), TestResult.ForceFail )
        #}
        finally:
        #{
            pass
        #}
    #}

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #    ~ctor - CLedSensor
    #
    def __del__( self ):
    #{
        try:
        #{
            if ( self.fMove and ( self.nChannels != 0 ) ):
            #{
                if ( self.ePowerMode == ePowerMode._pNone ):
                #{
                    MoveChannels( self.nChannels, MC_Mode.Remove )
                #}
                elif ( not self.fDisableSwitchOff ):
                #{
                    MoveChannels( self.nChannels, MC_Mode.Remove )
                #}
                else:
                #{
                    MoveChannels( self.nSensorPin, MC_Mode.Remove )
                #}
            #}
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "__del__() Exception : %s" % str( e ), TestResult.ForceFail )
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetSensorsInfo( self ):
    #{
        try:
        #{
            self.LedSensorsInfo = dict()
            if ( self.nSensorPin[ 0 ] != 0 ):
            #{
                for nSensorPin in range( 0, len( self.nSensorPin ) ):
                #{
                    nRet, sVivaXMLMsg = GetLedSensorInfo( int( self.nSensorPin[ nSensorPin ] ) )
                    if ( nRet == BOOL.FALSE ):
                    #{
                        self.ReportFail( None, "GetLedSensorInfo() Error", TestResult.ForceFail )
                        return False
                    #}
                    VivaRoot = ET.fromstring( sVivaXMLMsg )
                    self.LedSensorsInfo[ self.nSensorPin[ nSensorPin ] ] = self.LedSensorInfo_t( str( self.sComponentsName[ nSensorPin ] ), \
                                                                                                int ( self.nSensorPin[ nSensorPin ] ), \
                                                                                                int( VivaRoot.find( 'MSG' ).get( 'ModuleNumber' ) ), \
                                                                                                int( VivaRoot.find( 'MSG' ).get( 'InstrumentType' ) ), \
                                                                                                str( VivaRoot.find( 'MSG' ).get( 'HwID' ) ), \
                                                                                                int( VivaRoot.find( 'MSG' ).get( 'MaxFiberNr' ) ), \
                                                                                                int( VivaRoot.find( 'MSG' ).get( 'FiberChannel' ) ),
                                                                                                float( VivaRoot.find( 'MSG' ).get( 'xOffset' ) ), \
                                                                                                float( VivaRoot.find( 'MSG' ).get( 'yOffset' ) ), \
                                                                                                int( VivaRoot.find( 'MSG' ).get( 'WaveLengthOffset' ) ), \
                                                                                                False )
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetSensorsInfo() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetSensorInfo( self, nSensorPin : int ):
    #{
        try:
        #{
            if ( nSensorPin == 0 ):
            #{
                return None
            #}
            if ( len( self.LedSensorsInfo ) == 0 ):
            #{
                return None
            #}
            return self.LedSensorsInfo[ nSensorPin ]
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetSensorInfo() Exception : %s" % str( e ), TestResult.ForceFail )
            return None
        #}
        finally:
        #{
            pass
        #}
    #}

    def SetSensorInfoStatus( self, nSensorPin : int, fFail : bool ):
    #{
        try:
        #{
            LedSensorInfo = self.LedSensorsInfo[ nSensorPin ]._replace( fFailed = fFail )
            self.LedSensorsInfo[ nSensorPin ] = LedSensorInfo
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SetSensorInfoStatus() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def SetHSIDefault( self ):
    #{
        try:
        #{
            if ( ( self.dHUE == 0.0 ) and ( self.nSaturation == 0 ) and ( self.nIntensity == 0 ) ):
            #{
                if ( self.eTableRef == eTableRef._tblrOFF ):
                #{
                    # default value WHITE
                    self.dHUE                   = 100
                    self.dHUELowLimit           = 20
                    self.dHUEHighLimit          = 180
                    self.nSaturation            = 50
                    self.nSaturationLowLimit    = 30
                    self.nSaturationHighLimit   = 70
                #}
                elif ( self.eTableRef == eTableRef._tblrRed ):
                #{
                    self.dHUE                   = 2
                    self.dHUELowLimit           = 0
                    self.dHUEHighLimit          = 3
                    self.nSaturation            = 100
                    self.nSaturationLowLimit    = 85
                    self.nSaturationHighLimit   = 100
                #}
                elif ( self.eTableRef == eTableRef._tblrGreen ):
                #{
                    self.dHUE                   = 120
                    self.dHUELowLimit           = 85
                    self.dHUEHighLimit          = 155
                    self.nSaturation            = 100
                    self.nSaturationLowLimit    = 85
                    self.nSaturationHighLimit   = 100
                #}
                elif ( self.eTableRef == eTableRef._tblrBlue ):
                #{
                    self.dHUE                   = 238
                    self.dHUELowLimit           = 200
                    self.dHUEHighLimit          = 280
                    self.nSaturation            = 100
                    self.nSaturationLowLimit    = 85
                    self.nSaturationHighLimit   = 100
                #}
                elif ( self.eTableRef == eTableRef._tblrYellow ):
                #{
                    self.dHUE                   = 75
                    self.dHUELowLimit           = 50
                    self.dHUEHighLimit          = 100
                    self.nSaturation            = 100
                    self.nSaturationLowLimit    = 90
                    self.nSaturationHighLimit   = 100
                #}
                elif ( self.eTableRef == eTableRef._tblrOrange ):
                #{
                    self.dHUE                   = 10
                    self.dHUELowLimit           = 5
                    self.dHUEHighLimit          = 30
                    self.nSaturation            = 100
                    self.nSaturationLowLimit    = 85
                    self.nSaturationHighLimit   = 100
                #}
                elif ( self.eTableRef == eTableRef._tblrWhite ):
                #{
                    self.dHUE                   = 100
                    self.dHUELowLimit           = 20
                    self.dHUEHighLimit          = 180
                    self.nSaturation            = 50
                    self.nSaturationLowLimit    = 30
                    self.nSaturationHighLimit   = 70
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SetHSIDefault() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GeMacroParameters(self ):
    #{
        try:
        #{
            # Get Macro Parameters
            bRet    = False
            Value   = ""
            bRet, nParType, self.nPositivePin   = GetCurMacroParameter( "PositivePin" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"PositivePin\" Error" )
            #}
            bRet, nParType, self.nNegativePin   = GetCurMacroParameter( "NegativePin" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"NegativePin\" Error" )
            #}
            bRet, nParType, nSensorPin          = GetCurMacroParameter( "SensorPin" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"SensorPin\" Error" )
            #}
            self.nSensorPin                     = list( nSensorPin )
            bRet, nParType, Value               = GetCurMacroParameter( "Time" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"Time\" Error" )
            #}
            self.nTime                          = float( Value )
            bRet, nParType, Value               = GetGlobalVariable( _sLS_CaptureType )
            if ( not bRet ):
            #{
                bRet, nParType, Value           = GetCurMacroParameter( "CaptureType" )
                if ( not bRet ):
                #{
                    raise Exception( "Parameter \"CaptureType\" Error" )
                #}
            #}
            self.eCaptureType                   = eCaptureType( Value )
            bRet, nParType, Value               = GetGlobalVariable( _sLS_Range )
            if ( not bRet ):
            #{
                bRet, nParType, Value           = GetCurMacroParameter( "Range" )
                if ( not bRet ):
                #{
                    raise Exception( "Parameter \"Range\" Error" )
                #}
            #}
            self.eRange                         = int( Value )
            bRet, nParType, Value               = GetGlobalVariable( _sLS_FactorPWM )
            if ( not bRet ):
            #{
                bRet, nParType, Value           = GetCurMacroParameter( "FactorPWM" )
                if ( not bRet ):
                #{
                    raise Exception( "Parameter \"FactorPWM\" Error" )
                #}
            #}
            self.nFactorPWM                     = int( Value )
            bRet, nParType, Value               = GetCurMacroParameter( "MeasureView" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"MeasureView\" Error" )
            #}
            self.eMeasureView                   = eMeasureView( Value )
            bRet, nParType, Value               = GetGlobalVariable( _sLS_TestResult )
            if ( not bRet ):
            #{
                bRet, nParType, Value           = GetCurMacroParameter( "TestResult" )
                if ( not bRet ):
                #{
                    raise Exception( "Parameter \"TestResult\" Error" )
                #}
            #}
            self.eTestResult                    = TestResult( Value )
            self.eTestResult                    = self.eTestResult if ( self.eTestResult != TestResult.Default ) else TestResult.TestResult
            bRet, nParType, Value               = GetGlobalVariable( _sLS_ResetStoreData )
            if ( bRet ):
            #{
                self.fResetStoreData            = True if ( int( Value ) == BOOL.TRUE ) else False
                SetGlobalVariable( _sLS_ResetStoreData, BOOL.FALSE )
            #}
            bRet, nParType, Value               = GetCurMacroParameter( "PowerMode" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"PowerMode\" Error" )
            #}
            self.ePowerMode                     = ePowerMode( Value )
            bRet, nParType, Value               = GetCurMacroParameter( "User" )
            if ( not bRet ):
            #{
                raise Exception( "Parameter \"User\" Error" )
            #}
            self.eUser                          = eUser( Value )

            # Get Macro Memo Parameters
            bRet, self.fAcquire                 = GetCurMacroMemoParameter( "Measures",             "Acquire",                  "",                             ParVarType.string )
            #if ( self.fAcquire == "" ):
            ##{
            #    self.fAcquire = True
            #    SetCurMacroMemoParameter( "Measures", "Acquire", ParVarType.string, "Y" )
            ##}
            bRet, self.fAcquire                 = GetCurMacroMemoParameter( "Measures",             "Acquire",                  "Y",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures Acquire\" Error" )
            #}
            if ( self.fLearn ):
            #{
                self.fAcquire = True
            #}
            bRet, self.fHSIMeasure              = GetCurMacroMemoParameter( "Measures",             "HSI",                      "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures HSI\" Error" )
            #}
            bRet, self.fxyMeasure               = GetCurMacroMemoParameter( "Measures",             "xy",                       "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures xy\" Error" )
            #}
            bRet, self.fRGBMeasure              = GetCurMacroMemoParameter( "Measures",             "RGB",                      "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures RGB\" Error" )
            #}
            bRet, self.fWaveLengthMeasure       = GetCurMacroMemoParameter( "Measures",             "WaveLength",               "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures WaveLength\" Error" )
            #}
            bRet, self.fCCTMeasure              = GetCurMacroMemoParameter( "Measures",             "CCT",                      "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures CCT\" Error" )
            #}
            bRet, self.fXYZMeasure              = GetCurMacroMemoParameter( "Measures",             "XYZ",                      "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Measures XYZ\" Error" )
            #}

            bRet, self.dHUE                     = GetCurMacroMemoParameter( "HUE",                  "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"HUE Value\" Error" )
            #}
            bRet, self.dHUELowLimit             = GetCurMacroMemoParameter( "HUE",                  "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"HUE LowLimit\" Error" )
            #}
            bRet, self.dHUEHighLimit            = GetCurMacroMemoParameter( "HUE",                  "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"HUE HighLimit\" Error" )
            #}

            bRet, Value                         = GetCurMacroMemoParameter( "Saturation",           "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Saturation Value\" Error" )
            #}
            self.nSaturation                    = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "Saturation",           "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Saturation LowLimit\" Error" )
            #}
            self.nSaturationLowLimit            = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "Saturation",           "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Saturation HighLimit\" Error" )
            #}
            self.nSaturationHighLimit           = int( Value )

            bRet, Value                         = GetCurMacroMemoParameter( "Intensity",            "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Intensity Value\" Error" )
            #}
            self.nIntensity                     = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "Intensity",            "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Intensity LowLimit\" Error" )
            #}
            self.nIntensityLowLimit             = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "Intensity",            "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Intensity HighLimit\" Error" )
            #}
            self.nIntensityHighLimit            = int( Value )

            bRet, self.dx                       = GetCurMacroMemoParameter( "xy",                   "x",                        0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"xy x\" Error" )
            #}
            bRet, self.dxOffset                 = GetCurMacroMemoParameter( "xy",                   "xOffset",                  0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"xy xOffset\" Error" )
            #}
            bRet, self.dy                       = GetCurMacroMemoParameter( "xy",                   "y",                        0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"xy y\" Error" )
            #}
            bRet, self.dyOffset                 = GetCurMacroMemoParameter( "xy",                   "yOffset",                  0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"xy yOffset\" Error" )
            #}
            bRet, self.sxyEdges                 = GetCurMacroMemoParameter( "xy",                   "xyEdges",                  "",                             ParVarType.string )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"xy xyEdges\" Error" )
            #}
            if ( self.fLearn ):
            #{
                self.dxOffset = 0
                self.dyOffset = 0
            #}

            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "RedValue",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB RedValue\" Error" )
            #}
            self.nRed                           = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "RedLowLimit",              0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB RedLowLimit\" Error" )
            #}
            self.nRedLowLimit                   = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "RedHighLimit",             0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB RedHighLimit\" Error" )
            #}
            self.nRedHighLimit                  = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "GreenValue",               0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB GreenValue\" Error" )
            #}
            self.nGreen                         = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "GreenLowLimit",            0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB GreenLowLimit\" Error" )
            #}
            self.nGreenLowLimit                 = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "GreenHighLimit",           0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB GreenHighLimit\" Error" )
            #}
            self.nGreenHighLimit                = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "BlueValue",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB BlueValue\" Error" )
            #}
            self.nBlue                          = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "BlueLowLimit",             0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB BlueLowLimit\" Error" )
            #}
            self.nBlueLowLimit                  = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "RGB",                  "BlueHighLimit",            0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"RGB BlueHighLimit\" Error" )
            #}
            self.nBlueHighLimit                 = int( Value )

            bRet, Value                         = GetCurMacroMemoParameter( "WaveLength",           "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"WaveLength Value\" Error" )
            #}
            self.nWaveLength                    = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "WaveLength",           "Offset",                   0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"WaveLength Offset\" Error" )
            #}
            self.nWaveLengthOffset              = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "WaveLength",           "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"WaveLength LowLimit\" Error" )
            #}
            self.nWaveLengthLowLimit            = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "WaveLength",           "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"WaveLength HighLimit\" Error" )
            #}
            self.nWaveLengthHighLimit           = int( Value )
            if ( self.fLearn ):
            #{
                self.nWaveLengthOffset = 0
            #}

            bRet, Value                         = GetCurMacroMemoParameter( "CCT",                  "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"CCT Value\" Error" )
            #}
            self.nCCT                           = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "CCT",                  "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"CCT LowLimit\" Error" )
            #}
            self.nCCTLowLimit                   = int( Value )
            bRet, Value                         = GetCurMacroMemoParameter( "CCT",                  "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"CCT HighLimit\" Error" )
            #}
            self.nCCTHighLimit                  = int( Value )

            bRet, dValue                        = GetCurMacroMemoParameter( "DeltaEDistance",       "Value",                    1000000.0,                      ParVarType.double )
            if ( dValue == 1000000 ):
            #{
                SetCurMacroMemoParameter( "DeltaEDistance", "Value",     ParVarType.double, 0.0 )
                SetCurMacroMemoParameter( "DeltaEDistance", "LowLimit",  ParVarType.double, 0.0 )
                SetCurMacroMemoParameter( "DeltaEDistance", "HighLimit", ParVarType.double, 0.0 )
            #}
            bRet, self.dDeltaEDistance          = GetCurMacroMemoParameter( "DeltaEDistance",       "Value",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"DeltaEDistance Value\" Error" )
            #}
            bRet, self.dDeltaEDistanceLowLimit  = GetCurMacroMemoParameter( "DeltaEDistance",       "LowLimit",                 0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"DeltaEDistance LowLimit\" Error" )
            #}
            bRet, self.dDeltaEDistanceHighLimit = GetCurMacroMemoParameter( "DeltaEDistance",       "HighLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"DeltaEDistance HighLimit\" Error" )
            #}

            bRet, self.dX                       = GetCurMacroMemoParameter( "XYZ",                  "XValue",                   0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ XValue\" Error" )
            #}
            bRet, self.dXLowLimit               = GetCurMacroMemoParameter( "XYZ",                  "XLowLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ XLowLimit\" Error" )
            #}
            bRet, self.dXHighLimit              = GetCurMacroMemoParameter( "XYZ",                  "XHighLimit",               0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ XHighLimit\" Error" )
            #}
            bRet, self.dY                       = GetCurMacroMemoParameter( "XYZ",                  "YValue",                   0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ YValue\" Error" )
            #}
            bRet, self.dYLowLimit               = GetCurMacroMemoParameter( "XYZ",                  "YLowLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ YLowLimit\" Error" )
            #}
            bRet, self.dYHighLimit              = GetCurMacroMemoParameter( "XYZ",                  "YHighLimit",               0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ YHighLimit\" Error" )
            #}
            bRet, self.dZ                       = GetCurMacroMemoParameter( "XYZ",                  "ZValue",                   0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ ZValue\" Error" )
            #}
            bRet, self.dZLowLimit               = GetCurMacroMemoParameter( "XYZ",                  "ZLowLimit",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ ZLowLimit\" Error" )
            #}
            bRet, self.dZHighLimit              = GetCurMacroMemoParameter( "XYZ",                  "ZHighLimit",               0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"XYZ ZHighLimit\" Error" )
            #}

            bRet, self.fPowerCheck              = GetCurMacroMemoParameter( "Power",                "PowerCheck",               "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power PowerCheck\" Error" )
            #}
            bRet, self.dCurrent                 = GetCurMacroMemoParameter( "Power",                "Current",                  0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power Current\" Error" )
            #}
            bRet, self.dVolt                    = GetCurMacroMemoParameter( "Power",                "Volt",                     0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power Volt\" Error" )
            #}
            bRet, self.dWatt                    = GetCurMacroMemoParameter( "Power",                "Watt",                     0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power Watt\" Error" )
            #}
            bRet, self.nDelay                   = GetCurMacroMemoParameter( "Power",                "Delay",                    0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power Delay\" Error" )
            #}
            bRet, self.nTol                     = GetCurMacroMemoParameter( "Power",                "Tolerance",                0.0,                            ParVarType.double )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"Power Tolerance\" Error" )
            #}

            bRet, self.fDisableSwitchOff        = GetCurMacroMemoParameter( "OptionalParameters",   "DisableSwitchOff",         "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"OptionalParameters DisableSwitchOff\" Error" )
            #}
            bRet, self.fStayToWorkingDistance   = GetCurMacroMemoParameter( "OptionalParameters",   "StayToWorkingDistance",    "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"OptionalParameters StayToWorkingDistance\" Error" )
            #}
            bRet, self.fStoreData               = GetCurMacroMemoParameter( "OptionalParameters",   "EnableStoreData",          "N",                            ParVarType.string, True )
            if ( not bRet ):
            #{
                raise Exception( "Memo Parameter \"OptionalParameters EnableStoreData\" Error" )
            #}
            bRet, self.fParallelModeDisabled    = GetCurMacroMemoParameter( "OptionalParameters",   "DisableParallelMode",      "N",                            ParVarType.string, True )
            bRet, Value                         = GetCurMacroMemoParameter( "OptionalParameters",   "TableRef",                 "",                             ParVarType.string )
            if ( Value != "" ):
            #{
                bRet, Value                     = GetCurMacroMemoParameter( "OptionalParameters",   "TableRef",                 float( eTableRef._tblrOFF ),    ParVarType.double )
                self.eTableRef                  = eTableRef( Value )
                self.SetHSIDefault()
            #}
            bRet = SystemExecute( "LedSensorStayToWorkingDistance", "Y" if ( self.fStayToWorkingDistance ) else "N" )
            return False if ( bRet == BOOL.FALSE ) else True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GeMacroParameters() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def SeMacroParameters(self ):
    #{
        try:
        #{
            # Set Macro Parameters

            # Set Macro Memo Parameters
            SetCurMacroMemoParameter( "HUE",             "Value",                ParVarType.double,      self.dHUE                       )
            SetCurMacroMemoParameter( "HUE",             "LowLimit",             ParVarType.double,      self.dHUELowLimit               )
            SetCurMacroMemoParameter( "HUE",             "HighLimit",            ParVarType.double,      self.dHUEHighLimit              )

            SetCurMacroMemoParameter( "Saturation",      "Value",                ParVarType.double,         self.nSaturation                )
            SetCurMacroMemoParameter( "Saturation",      "LowLimit",             ParVarType.double,         self.nSaturationLowLimit        )
            SetCurMacroMemoParameter( "Saturation",      "HighLimit",            ParVarType.double,         self.nSaturationHighLimit       )

            SetCurMacroMemoParameter( "Intensity",       "Value",                ParVarType.double,         self.nIntensity                 )
            SetCurMacroMemoParameter( "Intensity",       "LowLimit",             ParVarType.double,         self.nIntensityLowLimit         )
            SetCurMacroMemoParameter( "Intensity",       "HighLimit",            ParVarType.double,         self.nIntensityHighLimit        )

            SetCurMacroMemoParameter( "xy",              "x",                    ParVarType.double,      self.dx                         )
            SetCurMacroMemoParameter( "xy",              "xOffset",              ParVarType.double,      self.dxOffset                   )
            SetCurMacroMemoParameter( "xy",              "y",                    ParVarType.double,      self.dy                         )
            SetCurMacroMemoParameter( "xy",              "yOffset",              ParVarType.double,      self.dyOffset                   )

            SetCurMacroMemoParameter( "RGB",             "RedValue",             ParVarType.double,         self.nRed                       )
            SetCurMacroMemoParameter( "RGB",             "RedLowLimit",          ParVarType.double,         self.nRedLowLimit               )
            SetCurMacroMemoParameter( "RGB",             "RedHighLimit",         ParVarType.double,         self.nRedHighLimit              )

            SetCurMacroMemoParameter( "RGB",             "GreenValue",           ParVarType.double,         self.nGreen                     )
            SetCurMacroMemoParameter( "RGB",             "GreenLowLimit",        ParVarType.double,         self.nGreenLowLimit             )
            SetCurMacroMemoParameter( "RGB",             "GreenHighLimit",       ParVarType.double,         self.nGreenHighLimit            )

            SetCurMacroMemoParameter( "RGB",             "BlueValue",            ParVarType.double,         self.nBlue                      )
            SetCurMacroMemoParameter( "RGB",             "BlueLowLimit",         ParVarType.double,         self.nBlueLowLimit              )
            SetCurMacroMemoParameter( "RGB",             "BlueHighLimit",        ParVarType.double,         self.nBlueHighLimit             )

            SetCurMacroMemoParameter( "WaveLength",      "Value",                ParVarType.double,         self.nWaveLength                )
            SetCurMacroMemoParameter( "WaveLength",      "Offset",               ParVarType.double,         self.nWaveLengthOffset          )

            SetCurMacroMemoParameter( "CCT",             "Value",                ParVarType.double,         self.nCCT                       )
            SetCurMacroMemoParameter( "CCT",             "LowLimit",             ParVarType.double,         self.nCCTLowLimit               )
            SetCurMacroMemoParameter( "CCT",             "HighLimit",            ParVarType.double,         self.nCCTHighLimit              )

            SetCurMacroMemoParameter( "DeltaEDistance",  "Value",                ParVarType.double,      self.dDeltaEDistance            )
            SetCurMacroMemoParameter( "DeltaEDistance",  "LowLimit",             ParVarType.double,      self.dDeltaEDistanceLowLimit    )
            SetCurMacroMemoParameter( "DeltaEDistance",  "HighLimit",            ParVarType.double,      self.dDeltaEDistanceHighLimit   )

            SetCurMacroMemoParameter( "XYZ",             "XValue",               ParVarType.double,      self.dX                         )
            SetCurMacroMemoParameter( "XYZ",             "XLowLimit",            ParVarType.double,      self.dXLowLimit                 )
            SetCurMacroMemoParameter( "XYZ",             "XHighLimit",           ParVarType.double,      self.dXHighLimit                )
            SetCurMacroMemoParameter( "XYZ",             "YValue",               ParVarType.double,      self.dY                         )
            SetCurMacroMemoParameter( "XYZ",             "YLowLimit",            ParVarType.double,      self.dYLowLimit                 )
            SetCurMacroMemoParameter( "XYZ",             "YHighLimit",           ParVarType.double,      self.dYHighLimit                )
            SetCurMacroMemoParameter( "XYZ",             "ZValue",               ParVarType.double,      self.dZ                         )
            SetCurMacroMemoParameter( "XYZ",             "ZLowLimit",            ParVarType.double,      self.dZLowLimit                 )
            SetCurMacroMemoParameter( "XYZ",             "ZHighLimit",           ParVarType.double,      self.dZHighLimit                )
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SeMacroParameters() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreData( self, LedSensorInfo : LedSensorInfo_t, sStoreName : str, sData : str ):
    #{
        try:
        #{
            sFullStoreName = self.GetFullStoreFileName( LedSensorInfo, sStoreName )
            if ( sFullStoreName == "" ):
            #{
                return False
            #}
            FileStoreData = open( sFullStoreName, 'a' if ( not self.fResetStoreData ) else 'w' )
            if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ):
            #{
                sData = LedSensorInfo.sComponentName + _sDataLogFieldSeparator + LedSensorInfo.sHwID + _sDataLogFieldSeparator + str( LedSensorInfo.nFiberChannel ) + _sDataLogFieldSeparator + sData + "\n"
            #}
            else:
            #{
                sData = LedSensorInfo.sComponentName + _sDataLogFieldSeparator + LedSensorInfo.sHwID + _sDataLogFieldSeparator + sData + "\n"
            #}
            FileStoreData.writelines( sData )
            FileStoreData.close()
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( LedSensorInfo, "StoreData() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetFullStoreFileName( self, LedSensorInfo : LedSensorInfo_t, sStoreName : str ):
    #{
        try:
        #{
            sFullStoreName = ""
            BoardInfo = self.BoardsInfo[ LedSensorInfo.nSensorPin ]
            if ( BoardInfo.sBarcode != "" ):
            #{
                sBarcode = BoardInfo.sBarcode + "_"
            #}
            else:
            #{
                sBarcode = GetBoardCode()
                if ( sBarcode != "" ):
                #{
                    sBarcode = sBarcode + "_"
                #}
            #}
            if ( sBarcode != "" ):
            #{
                sFullStoreName = str( GetBoardPath() + GetBoardName() + "\\" + sBarcode + "B" + str( BoardInfo.nBoard ) + "_" + sStoreName )
            #}
            else:
            #{
                sFullStoreName = str( GetBoardPath() + GetBoardName() + "\\" + "B" + str( BoardInfo.nBoard ) + "_" + sStoreName )
            #}
            return sFullStoreName
        #}
        except Exception as e:
        #{
            self.ReportFail( LedSensorInfo, "GetFullStoreFileName() Exception : %s" % str( e ), TestResult.ForceFail )
            return sFullStoreName
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetLedSensorChannel( self, sComponent ):
    #{
        try:
        #{
            if ( sComponent == "" ):
            #{
                return 0
            #}
            nRet, sInstrsName, nMacrosID = GetComponentMacros( sComponent )
            if ( nRet != ReturnCode._RCNoError ):
            #{
                return 0
            #}
            for nMacroIdx in range( len( nMacrosID ) ):
            #{
                nRet, Value = GetMacroParameterValue( sComponent, "", -1, nMacrosID[ nMacroIdx ], "SensorPin" )
                if ( nRet == ReturnCode._RCNoError ):
                #{
                    return int( Value )
                #}
            #}
            return 0
        #}
        except Exception as e:
        #{
            MessageBox( "Error", "GetLedSensorChannel() Exception : %s" % str( e ) )
            return 0
        #}
    #}

    def GetFriendSensorPin( self ):
    #{
        try:
        #{
            bRet, ParType, Value = GetGlobalVariable( GVParallelMode._sTwinnedComponents.value )
            if ( bRet and ( ParType == ParVarType.string ) and ( Value != "" ) ):
            #{
                sTwinnedComponents = str( Value ).split( "," )
                if ( len( sTwinnedComponents ) ):
                #{
                    for sTwinnedComponent in sTwinnedComponents:
                    #{
                        sComponents = str( sTwinnedComponent ).split( "-" )
                        if ( len( sComponents ) > 1 ):
                        #{
                            for nComponent in range( len( sComponents ) ):
                            #{
                                if ( sComponents[ nComponent ] == self.sComponentName ):
                                #{
                                    nComponent = nComponent - ( 1 if ( nComponent == ( len( sComponents ) - 1 ) ) else -1 )
                                    return sComponents[ nComponent ], self.GetLedSensorChannel( sComponents[ nComponent ] )
                                #}
                            #}
                        #}
                    #}
                #}
            #}
            return self.sComponentName, self.nSensorPin[ 0 ]
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetFriendSensorPin() Exception : %s" % str( e ), TestResult.ForceFail )
            return 0
        #}
        finally:
        #{
            pass
        #}
    #}

    def MoveLedSensors( self ):
    #{
        try:
        #{
            self.BoardsInfo     = dict()
            self.nChannels      = []
            self.fMove          = False
            self.fTwinnedBoards = False
            for nSensorPin in self.nSensorPin:
            #{
                self.BoardsInfo[ nSensorPin ] = self.BoardInfo_t( int( self.nCurrentBoardNumber ), str( self.BoardCode ), nSensorPin )
                self.sComponentsName.append( self.sComponentName )
                self.nChannels.append( nSensorPin )
            #}
            if ( len( self.nChannels ) == 1 ):
            #{
                # Get Macro Parallel Test Mode Option Supported
                bRet, Permissions = GetMacroPermissions( PermType._SecondPermissions )
                if ( bRet and ( ( Permissions != 0 ) and ( ( Permissions & PermType._ParallelMode ) == PermType._ParallelMode ) ) ):
                #{
                    bRet, ParType, Value = GetGlobalVariable( GVParallelMode._sTwinnedBoards.value )
                    if ( bRet and ( ParType == ParVarType.string ) and ( Value != "" ) ):
                    #{
                        TwinnedBoards = str( Value ).split( "," )
                        if ( len( TwinnedBoards ) ):
                        #{
                            BoardsBarcodes = ""
                            bRet, ParType, Value = GetGlobalVariable( GVParallelMode._sBoardsBarcodes.value )
                            if ( bRet and ( ParType == ParVarType.string ) and ( Value != "" ) ):
                            #{
                                BoardsBarcodes = str( Value ).split( "," )
                            #}
                            fFound = False
                            for TwinnedBoard in TwinnedBoards:
                            #{
                                Boards = str( TwinnedBoard ).split( "-" )
                                nBoards = len( Boards )
                                for nBoard in range( nBoards ):
                                #{
                                    if ( int( Boards[ nBoard ] ) == self.nCurrentBoardNumber ):
                                    #{
                                        fFound = True
                                        _sBarcode = GetBoardBarcode( BoardsBarcodes, int( Boards[ nBoard ] ) )
                                        BoardInfo = self.BoardsInfo[ self.nSensorPin[ 0 ] ]._replace( sBarcode = _sBarcode )
                                        self.BoardsInfo[ self.nSensorPin[ 0 ] ] = BoardInfo
                                        if ( nBoards > 1 ):
                                        #{
                                            if ( nBoard == ( nBoards - 1 ) ):
                                            #{
                                                if ( self.ePowerMode == ePowerMode._pNone ):
                                                #{
                                                    if ( IsBoardEnabled( int( Boards[ nBoard - 1 ] ) ) ):
                                                    #{
                                                        sComponentName, nFriendSensorPin = self.GetFriendSensorPin()
                                                        if ( nFriendSensorPin != 0 ):
                                                        #{
                                                            bRet, nTwinnedChannel = GetTwinnedChannel( int( Boards[ nBoard - 1 ] ), nFriendSensorPin )
                                                            if ( bRet and ( nTwinnedChannel != 0 ) ):
                                                            #{
                                                                self.sComponentsName.append( sComponentName )
                                                                self.nChannels.append( nTwinnedChannel )
                                                                self.nSensorPin.append( nTwinnedChannel )
                                                                _sBarcode = GetBoardBarcode( BoardsBarcodes, int( Boards[ nBoard - 1 ] ) )
                                                                self.BoardsInfo[ self.nSensorPin[ 1 ] ] = self.BoardInfo_t( int( Boards[ nBoard - 1 ] ), _sBarcode, nTwinnedChannel )
                                                                self.fTwinnedBoards = True
                                                            #}
                                                        #}
                                                    #}
                                                    self.fMove = True
                                                #}
                                            #}
                                            else:
                                            #{
                                                if ( not IsBoardEnabled( int( Boards[ nBoard + 1 ] ) ) ):
                                                #{
                                                    self.fMove = True
                                                #}
                                            #}
                                        #}
                                        else:
                                        #{
                                            self.fMove = True
                                        #}
                                        break
                                    #}
                                #}
                                if ( fFound ):
                                #{
                                    break
                                #}
                            #}
                            if ( fFound ):
                            #{
                                if ( self.fMove ):
                                #{
                                    if ( len( self.nChannels ) > 1 ):
                                    #{
                                        if ( self.nChannels[ 1 ] == 0 ):
                                        #{
                                            self.ReportFail( None, "MoveLedSensors() Error", TestResult.ForceFail )
                                            return TestResult.ForceFail
                                        #}
                                    #}
                                #}
                                elif ( self.fParallelModeDisabled ):
                                #{
                                    self.fMove = True
                                #}
                                else:
                                #{
                                    self.SetTestInfo( None, "", "", 0, 0, 0, 0, TestResult.ForcePass )
                                    return TestResult.ForceSkip
                                #}
                            #}
                            else:
                            #{
                                self.ReportFail( None, "MoveLedSensors() Error", TestResult.ForceFail )
                                return TestResult.ForceFail
                            #}
                        #}
                        else:
                        #{
                            self.fMove = True
                        #}
                    #}
                    else:
                    #{
                        self.fMove = True
                    #}
                #}
                else:
                #{
                    self.fMove = True
                #}
            #}
            if ( not self.fTwinnedBoards ):
            #{
                if ( self.ePowerMode != ePowerMode._pNone ):
                #{
                    self.nChannels.append( self.nPositivePin[0] )
                    self.nChannels.append( self.nNegativePin[0] )
                #}
                self.fMove = True
            #}
            if ( self.fMove ):
            #{
                bRet, sSignalsFromProbes, sChannelsFromProbes = MoveChannels( self.nChannels, MC_Mode.Add, MC_Locked.Yes )
                if ( bRet ):
                #{
                    if ( not self.GetSensorsInfo() ):
                    #{
                        return TestResult.ForceFail
                    #}
                #}
                else:
                #{
                    self.ReportFail( None, "MoveChannels() Error", TestResult.ForceFail )
                    return TestResult.ForceFail
                #}
                if ( self.nTime ):
                #{
                    bRet, nParType, Value = GetGlobalVariable( "StartTimer" )
                    if ( bRet and ( ParType == ParVarType.double ) ):
                    #{
                        Timer = CTimer()
                        Timer.StartTimer( Value )
                        while( not Timer.TimerExpired( self.nTime ) ):
                        #{
                            pass
                        #}
                    #}
                #}
                return TestResult.ForcePass
            #}
            else:
            #{
                self.SetTestInfo( None, "", "", 0, 0, 0, 0, TestResult.ForcePass )
                return TestResult.ForceSkip
            #}
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "MoveLedSensors() Exception : %s" % str( e ), TestResult.ForceFail )
            return TestResult.ForceFail
        #}
        finally:
        #{
            pass
        #}
    #}

    def SetPower( self, fPowerOn : bool ):
    #{
        try:
        #{
            if ( self.ePowerMode == ePowerMode._pNone ):
            #{
                return True
            #}
            elif ( self.ePowerMode == ePowerMode._pStandard ):
            #{
                if ( fPowerOn ):
                #{
                    if ( ( self.dVolt > 100 ) or ( self.dCurrent > 0.100 ) ):
                    #{
                        self.ReportFail( None, "Current or Voltage values exceeded limits ( max 100 mA and 100 V )", TestResult.ForceFail )
                    #}
                    else:
                    #{
                        LINE_Set( MODE = LINEMODE._8L )                                             # set line out = close mode = 8L;
                        CHANNEL_Set( CHN = self.nPositivePin[0], LINEE = ELINE.L2 )
                        CHANNEL_Set( CHN = self.nPositivePin[0], LINEE = ELINE.L6 )                 # set channel chn = self.nPositivePin       linee = 34;        ! anodo su L2+L6
                        CHANNEL_Set( CHN = self.nNegativePin[0], LINEE = ELINE.L3 )
                        CHANNEL_Set( CHN = self.nNegativePin[0], LINEE = ELINE.L7 )                 # set channel chn = self.nNegativePin       linee = 68;        ! catodo su L3+L7 ( GND )
                        IMM_Set()                                                                   # set imm;
                        GND_Set( OUT = GNDLINE.L3 )                                                 # set agnd out=L3; ! gnd su linea 3
                        DRC_Set( VOLTAGE = self.dVolt, CURRENT = self.dCurrent, OUT = DRCOUT.L2 )   # set drc V = self.dVolt I = self.dCurrent out = 2;            ! set drc
                    #}
                #}
                elif ( not self.fDisableSwitchOff ):
                #{
                    DRC_Set( VOLTAGE = 0, CURRENT = self.dCurrent, OUT = DRCOUT.NONE )              # set drc V = 0 I = self.dCurrent out = 0;            ! set drc
                    GND_Clear()                                                                     # clear agnd;
                    IMM_Clear()
                    CHANNEL_Set( CHN = self.nPositivePin[0], LINEE = ELINE.NONE )
                    CHANNEL_Set( CHN = self.nPositivePin[0], LINEE = ELINE.NONE )                   # set channel chn = self.nPositivePin        linee = 0;   ! anodo su L2
                    CHANNEL_Set( CHN = self.nNegativePin[0], LINEE = ELINE.NONE )
                    CHANNEL_Set( CHN = self.nNegativePin[0], LINEE = ELINE.NONE )                   # set channel chn = self.nNegativePin       linee = 0;   ! catodo su L3 ( GND )
                #}
                return True
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SetPower() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def RunInteractiveProgram( self ):
    #{
        try:
        #{
            if ( self.eUser == eUser._uNone ):
            #{
                return True
            #}
            LedSensorInfo = self.GetSensorInfo( self.nSensorPin[ 0 ] )
            FeasaIniFile = CFileIni( GetVivaPath() + _FeasaINIFile )
            sSection = "FEASA"
            if ( FeasaIniFile.Read( "Spectrometer", "UserGains", "" ) != "" ):
            #{
                sSection = "LED Analyser" if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ) else "Spectrometer"
            #}
            sProgram = ""
            if ( self.eUser == eUser._uUserGains ):
            #{
                sProgram = FeasaIniFile.Read( sSection, "UserGains", _FeasaLAUserGains if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ) else _FeasaSUserGains )
            #}
            elif ( self.eUser == eUser._uUserSoftware ):
            #{
                sProgram = FeasaIniFile.Read( sSection, "UserSoftware", _FeasaLAUserSoftware if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ) else _FeasaSUserSoftware )
            #}
            elif ( self.eUser == eUser._uUserXYOffsets ):
            #{
                sProgram = FeasaIniFile.Read( "FEASA", "UserXYOffsets", _FeasaLAUserXYOffsets if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ) else _FeasaSUserXYOffsets )
            #}
            if ( sProgram != "" ):
            #{
                subprocess.call( "\"" + str( sProgram ) + "\"" )
            #}
            del FeasaIniFile
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "RunInteractiveProgram() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def Test( self ):
    #{
        try:
        #{
            if ( len( self.LedSensorsInfo ) == 0 ):
            #{
                return True
            #}
            if ( self.fLearn ):
            #{
                LedSensorInfo = self.GetSensorInfo( self.nSensorPin[ 0 ] )
                # TODO :
                if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ):
                #{
                    self.dxOffset           = LedSensorInfo.dxOffset
                    self.dyOffset           = LedSensorInfo.dyOffset
                    self.nWaveLengthOffset  = LedSensorInfo.nWaveLengthOffset
                    fAcquireWithOffsets     = False
                    while ( ( self.eRange > eRange._rNone ) and ( self.eRange < eRange._rNumRange ) ):
                    #{
                        eCurrentRange = self.eRange
                        if ( not self.SetOffsets( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                        if ( not self.Acquire( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                        if ( self.fHSIMeasure ):
                        #{
                            if ( not self.GetHSI( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( self.fRGBMeasure ):
                        #{
                            if ( not self.GetRGB( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( self.fxyMeasure ):
                        #{
                            if ( not self.Getxy( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( self.fWaveLengthMeasure ):
                        #{
                            if ( not self.GetWaveLength( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( self.fCCTMeasure ):
                        #{
                            if ( not self.GetCCT( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( self.fXYZMeasure ):
                        #{
                            if ( not self.GetXYZ( LedSensorInfo ) ):
                            #{
                                return False
                            #}
                            if ( eCurrentRange != self.eRange ):
                            #{
                                continue
                            #}
                        #}
                        if ( not fAcquireWithOffsets ):
                        #{
                            if ( ( self.dX != 0 ) or ( self.dY != 0 ) ):
                            #{
                                self.dXOffset = self.dX - self.dXValue
                                self.dYOffset = self.dY - self.dYValue
                                fAcquireWithOffsets = True
                                continue
                            #}
                        #}
                    #}
                #}
                else:
                #{
                    if ( not self.Acquire( LedSensorInfo ) ):
                    #{
                        return False
                    #}
                    if ( self.fxyMeasure ):
                    #{
                        if ( not self.Getxy( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                    #}
                    if ( self.fWaveLengthMeasure ):
                    #{
                        if ( not self.GetWaveLength( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                    #}
                    if ( self.fCCTMeasure ):
                    #{
                        if ( not self.GetCCT( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                    #}
                    if ( self.fXYZMeasure ):
                    #{
                        if ( not self.GetXYZ( LedSensorInfo ) ):
                        #{
                            return False
                        #}
                    #}
                #}
                if ( not self.fEmulation ):
                #{
                    self.SeMacroParameters()
                #}
            #}
            else:
            #{
                if ( self.fAcquire ):
                #{
                    for nLedSensor in self.LedSensorsInfo:
                    #{
                        LedSensorInfo = self.LedSensorsInfo[ nLedSensor ]
                        if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ):
                        #{
                            if ( not self.SetOffsets( LedSensorInfo ) ):
                            #{
                                self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                                continue
                            #}
                        #}
                        if ( not self.Acquire( LedSensorInfo, 0 ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                    for nLedSensor in self.LedSensorsInfo:
                    #{
                        LedSensorInfo = self.LedSensorsInfo[ nLedSensor ]
                        if ( not self.GetAcquireStatus( LedSensorInfo ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                #}
                for nLedSensor in self.LedSensorsInfo:
                #{
                    LedSensorInfo = self.LedSensorsInfo[ nLedSensor ]
                    if ( LedSensorInfo.eInstrumentType == self._eLedAnalyser ):
                    #{
                        if ( self.fHSIMeasure ):
                        #{
                            if ( not self.GetHSI( LedSensorInfo ) ):
                            #{
                                self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                                continue
                            #}
                        #}
                        if ( self.fRGBMeasure ):
                        #{
                            if ( not self.GetRGB( LedSensorInfo ) ):
                            #{
                                self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                                continue
                            #}
                        #}
                    #}
                    if ( self.fxyMeasure ):
                    #{
                        if ( not self.Getxy( LedSensorInfo ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                    if ( self.fWaveLengthMeasure ):
                    #{
                        if ( not self.GetWaveLength( LedSensorInfo ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                    if ( self.fCCTMeasure ):
                    #{
                        if ( not self.GetCCT( LedSensorInfo ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                    if ( self.fXYZMeasure ):
                    #{
                        if ( not self.GetXYZ( LedSensorInfo ) ):
                        #{
                            self.SetSensorInfoStatus( LedSensorInfo.nSensorPin, True )
                            continue
                        #}
                    #}
                    if ( not self.fTwinnedBoards ):
                    #{
                        break
                    #}
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "Test() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetLastErrorCode( self ):
    #{
        try:
        #{
            ErrorInfo = []
            nRet, ErrorInfo = LEDSENSOR_Execute( "GetLastError", None )
            if ( nRet == BOOL.FALSE ):
            #{
                return 1
            #}
            return int( ErrorInfo[ 0 ] )
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetLastErrorCode() Exception : %s" % str( e ), TestResult.ForceFail )
            return 1
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetLastError( self ):
    #{
        try:
        #{
            ErrorInfo = []
            nRet, ErrorInfo = LEDSENSOR_Execute( "GetLastError", None )
            if ( nRet == BOOL.FALSE ):
            #{
                return "Error"
            #}
            return str( ErrorInfo[ 1 ] )
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetLastError() Exception : %s" % str( e ), TestResult.ForceFail )
            return "Error"
        #}
        finally:
        #{
            pass
        #}
    #}

    def SetOffsets( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( LedSensorInfo.fFailed ):
            #{
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, self.dxOffset ]
            nRet = LEDSENSOR_Execute( "PutXOffset", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.ReportFail( LedSensorInfo, "PutXOffset Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            Params[ 2 ] = self.dyOffset
            nRet = LEDSENSOR_Execute( "PutYOffset", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.ReportFail( LedSensorInfo, "PutYOffset Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            Params[ 2 ] = self.nWaveLengthOffset
            nRet = LEDSENSOR_Execute( "PutWaveLengthOffset", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.ReportFail( LedSensorInfo, "PutWaveLengthOffset Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SetOffsets() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def Acquire( self, LedSensorInfo, nTimeout = _DefaultTimeout ):
    #{
        try:
        #{
            if ( LedSensorInfo.fFailed ):
            #{
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, self.eCaptureType, self.eRange, self.nFactorPWM, nTimeout ]
            nRet = LEDSENSOR_Execute( "Acquire", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.ReportFail( LedSensorInfo, "Acquire Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "Acquire() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetAcquireStatus( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( LedSensorInfo.fFailed ):
            #{
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber ]
            nRet = LEDSENSOR_Execute( "GetAcquireStatus", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.ReportFail( LedSensorInfo, "GetAcquireStatus Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetAcquireStatus() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetHSI( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            self.dHUEValue          = 0.0
            self.nSaturationValue   = 0
            self.nIntensityValue    = 0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataHSI( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            HSI = []
            nRet, HSI = LEDSENSOR_Execute( "GetHSI", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.StoreDataHSI( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetHSI Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            self.dHUEValue          = float( HSI[ 0 ] )
            self.nSaturationValue   = int( HSI[ 1 ] )
            self.nIntensityValue    = int( HSI[ 2 ] )
            if ( self.fEmulation ):
            #{
                self.dHUEValue          = 1
                self.nSaturationValue   = 1
                self.nIntensityValue    = 1
            #}
            if ( ( self.dHUEValue == 999.99 ) and ( self.nSaturationValue == 999 ) and ( self.nIntensityValue == 0 ) ):
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange - 1 ) <= eRange._rNone ):
                    #{
                        self.ReportFail( LedSensorInfo, "HSI : *** UNDER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange - 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataHSI( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "HSI : *** UNDER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( ( self.dHUEValue == 999.99 ) and ( self.nSaturationValue == 999 ) and ( self.nIntensityValue == 99999 ) ):
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange + 1 ) >= eRange._rNumRange ):
                    #{
                        self.ReportFail( LedSensorInfo, "HSI : *** OVER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange + 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataHSI( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "HSI : *** OVER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                if ( self.eTableRef == eTableRef._tblrOFF ):
                #{
                    self.dHUE           = self.dHUEValue
                    self.nSaturation    = self.nSaturationValue
                    self.nIntensity     = self.nIntensityValue
                    if ( self.dHUELowLimit == 0 ):
                    #{
                        self.dHUELowLimit = self.dHUE - ( ( self.dHUE * _dHUEDefaultTolNeg ) / 100 ) + 1.0
                        if ( self.dHUELowLimit < 0 ):
                        #{
                            self.dHUELowLimit = 0
                        #}
                    #}
                    if ( self.dHUEHighLimit == 0 ):
                    #{
                        self.dHUEHighLimit = self.dHUE + ( ( self.dHUE * _dHUEDefaultTolPos ) / 100 ) + 1.0
                        if ( self.dHUEHighLimit > 360 ):
                        #{
                            self.dHUEHighLimit = 360
                        #}
                    #}
                    if ( self.nSaturationLowLimit == 0 ):
                    #{
                        self.nSaturationLowLimit = self.nSaturation - ( ( self.nSaturation * _nSaturationDefaultTolNeg ) / 100 ) + 1
                        if ( self.nSaturationLowLimit < 0 ):
                        #{
                            self.nSaturationLowLimit = 0
                        #}
                    #}
                    if ( self.nSaturationHighLimit == 0 ):
                    #{
                        self.nSaturationHighLimit = self.nSaturation + ( ( self.nSaturation * _nSaturationDefaultTolPos ) / 100 ) + 1
                        if ( self.nSaturationHighLimit > 100 ):
                        #{
                            self.nSaturationHighLimit = 100
                        #}
                    #}
                    if ( self.nIntensityLowLimit == 0 ):
                    #{
                        self.nIntensityLowLimit = self.nIntensity - ( ( self.nIntensity * _nIntensityDefaultTolNeg ) / 100 ) + 1
                        if ( self.nIntensityLowLimit < 0 ):
                        #{
                            self.nIntensityLowLimit = 0
                        #}
                    #}
                    if ( self.nIntensityHighLimit == 0 ):
                    #{
                        self.nIntensityHighLimit = self.nIntensity + ( ( self.nIntensity * _nIntensityDefaultTolPos ) / 100 ) + 1
                        if ( self.nIntensityHighLimit > 99999 ):
                        #{
                            self.nIntensityHighLimit = 99999
                        #}
                    #}
                #}
            #}
            if ( not self.StoreDataHSI( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvHUE ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "HUE Error", _sHUEUnit, self.dHUEValue, self.dHUELowLimit, self.dHUE, self.dHUEHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvSaturation ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "Saturation Error", _sSaturationUnit, self.nSaturationValue, self.nSaturationLowLimit, self.nSaturation, self.nSaturationHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvIntensity ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "Intensity Error", _sIntensityUnit, self.nIntensityValue, self.nIntensityLowLimit, self.nIntensity, self.nIntensityHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetHSI() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataHSI( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sHSIStoreData = str( self.dHUEValue )           + _sDataLogFieldSeparator + \
                                str( self.nSaturationValue )    + _sDataLogFieldSeparator + \
                                str( self.nIntensityValue )
                if ( not self.StoreData( LedSensorInfo, _sHSIDataLogFileName, sHSIStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataHSI() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetRGB( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            self.nRedValue      = 0
            self.nGreenValue    = 0
            self.nBlueValue     = 0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataRGB( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            RGBI = []
            nRet, RGBI = LEDSENSOR_Execute( "GetRGBI", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.StoreDataRGB( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetRGB Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            self.nRedValue      = int( RGBI[ 0 ] )
            self.nGreenValue    = int( RGBI[ 1 ] )
            self.nBlueValue     = int( RGBI[ 2 ] )
            nIntensityValue     = int( RGBI[ 3 ] )
            if ( self.fEmulation ):
            #{
                self.nRedValue      = 1
                self.nGreenValue    = 1
                self.nBlueValue     = 1
            #}
            if ( ( self.nRedValue == 0 ) and ( self.nGreenValue == 0 ) and ( self.nBlueValue == 0 ) and ( nIntensityValue == 0 ) ):
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange - 1 ) <= eRange._rNone ):
                    #{
                        self.ReportFail( LedSensorInfo, "RGBI : *** UNDER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange - 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataRGB( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "RGBI : *** UNDER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                self.nRed   = self.nRedValue
                self.nGreen = self.nGreenValue
                self.nBlue  = self.nBlueValue
                if ( self.nRedLowLimit == 0 ):
                #{
                    self.nRedLowLimit = self.nRed - ( ( self.nRed * _nRedDefaultTolNeg ) / 100 ) + 1
                    if ( self.nRedLowLimit < 0 ):
                    #{
                        self.nRedLowLimit = 0
                    #}
                #}
                if ( self.nRedHighLimit == 0 ):
                #{
                    self.nRedHighLimit = self.nRed + ( ( self.nRed * _nRedDefaultTolPos ) / 100 ) + 1
                    if ( self.nRedHighLimit > 255 ):
                    #{
                        self.nRedHighLimit = 255
                    #}
                #}
                if ( self.nGreenLowLimit == 0 ):
                #{
                    self.nGreenLowLimit = self.nGreen - ( ( self.nGreen * _nGreenDefaultTolNeg ) / 100 ) + 1
                    if ( self.nGreenLowLimit < 0 ):
                    #{
                        self.nGreenLowLimit = 0
                    #}
                #}
                if ( self.nGreenHighLimit == 0 ):
                #{
                    self.nGreenHighLimit = self.nGreen + ( ( self.nGreen * _nGreenDefaultTolPos ) / 100 ) + 1
                    if ( self.nGreenHighLimit > 255 ):
                    #{
                        self.nGreenHighLimit = 255
                    #}
                #}
                if ( self.nBlueLowLimit == 0 ):
                #{
                    self.nBlueLowLimit = self.nBlue - ( ( self.nBlue * _nBlueDefaultTolNeg ) / 100 ) + 1
                    if ( self.nBlueLowLimit < 0 ):
                    #{
                        self.nBlueLowLimit = 0
                    #}
                #}
                if ( self.nBlueHighLimit == 0 ):
                #{
                    self.nBlueHighLimit = self.nBlue + ( ( self.nBlue * _nBlueDefaultTolPos ) / 100 ) + 1
                    if ( self.nBlueHighLimit > 255 ):
                    #{
                        self.nBlueHighLimit = 255
                    #}
                #}
            #}
            if ( not self.StoreDataRGB( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvRGB ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "RED Error", _sRedUnit, self.nRedValue, self.nRedLowLimit, self.nRed, self.nRedHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
                elif ( not self.SetTestInfo( LedSensorInfo, "GREEN Error", _sGreenUnit, self.nGreenValue, self.nGreenLowLimit, self.nGreen, self.nGreenHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
                elif ( not self.SetTestInfo( LedSensorInfo, "BLUE Error", _sBlueUnit, self.nBlueValue, self.nBlueLowLimit, self.nBlue, self.nBlueHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvRed ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "RED Error", _sRedUnit, self.nRedValue, self.nRedLowLimit, self.nRed, self.nRedHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvGreen ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "GREEN Error", _sGreenUnit, self.nGreenValue, self.nGreenLowLimit, self.nGreen, self.nGreenHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvBlue ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "BLUE Error", _sBlueUnit, self.nBlueValue, self.nBlueLowLimit, self.nBlue, self.nBlueHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetRGB() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataRGB( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sRGBStoreDataFileName = ""
                if ( self.eMeasureView == eMeasureView._mvRGB ):
                #{
                    sRGBStoreDataFileName = _sRGBDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvRed ):
                #{
                    sRGBStoreDataFileName = _sRedDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvGreen ):
                #{
                    sRGBStoreDataFileName = _sGreenDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvBlue ):
                #{
                    sRGBStoreDataFileName = _sBlueDataLogFileName
                #}
                else:
                #{
                    sRGBStoreDataFileName = _sRGBDataLogFileName
                #}
                sRGBStoreData = str( self.nRedValue )       + _sDataLogFieldSeparator + \
                                str( self.nGreenValue )     + _sDataLogFieldSeparator + \
                                str( self.nBlueValue )
                if ( not self.StoreData( LedSensorInfo, sRGBStoreDataFileName, sRGBStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataRGB() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def Getxy( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            self.dxValue = 0.0
            self.dyValue = 0.0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataxy( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            Response = LEDSENSOR_Execute( "GetXY", Params )
            if ( Response[ 0 ] == BOOL.FALSE ):
            #{
                self.StoreDataxy( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetXY Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            xy = []
            xy = Response[ 1 ]
            self.dxValue = float( xy[ 0 ] )
            self.dyValue = float( xy[ 1 ] )
            if ( self.fEmulation ):
            #{
                self.dxValue = 0.1
                self.dyValue = 0.1
            #}
            if ( ( self.dxValue == 0 ) and ( self.dyValue == 0 ) ):
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange + 1 ) >= eRange._rNumRange ):
                    #{
                        self.ReportFail( LedSensorInfo, "xy : *** OVER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange + 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataxy( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "xy : *** OVER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                if ( ( self.dx == 0 ) and ( self.dy == 0 ) ):
                #{
                    self.dx         = self.dxValue
                    self.dy         = self.dyValue
                    self.dxOffset   = 0
                    self.dyOffset   = 0
                #}
            #}
            self.dxLowLimit     = self.dx - ( ( self.dx * _dxDefaultTolNeg ) / 100 ) + 1.0
            self.dxHighLimit    = self.dx + ( ( self.dx * _dxDefaultTolPos ) / 100 ) + 1.0
            self.dyLowLimit     = self.dy - ( ( self.dy * _dyDefaultTolNeg ) / 100 ) + 1.0
            self.dyHighLimit    = self.dy + ( ( self.dy * _dyDefaultTolPos ) / 100 ) + 1.0
            if ( not self.StoreDataxy( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvx ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "x Error", _sXUnit, self.dxValue, self.dxLowLimit, self.dx, self.dxHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvy ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "y Error", _sYUnit, self.dyValue, self.dyLowLimit, self.dy, self.dyHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            if ( ( ( self.eMeasureView == eMeasureView._mvx ) or ( self.eMeasureView == eMeasureView._mvy ) ) and ( self.sxyEdges != "" ) ):
            #{
                Params = ( self.dxValue, self.dyValue, self.sxyEdges )
                Response = LEDSENSOR_Execute( "CheckXY", Params )
                if ( Response[ 0 ] == BOOL.FALSE ):
                #{
                    if ( self.GetLastErrorCode() != eErrorCode._NoError ):
                    #{
                        self.ReportFail( LedSensorInfo, "CheckXY Error : " + self.GetLastError(), TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.ReportFail( LedSensorInfo, "Point out of area" + " x : " + self.dxValue + " y : " + self.dyValue + " xyEdges : " + self.sxyEdges, self.eTestResult )
                    #}
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "Getxy() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataxy( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sxyStoreData = str( self.dxValue ) + _sDataLogFieldSeparator + str( self.dyValue )
                if ( not self.StoreData( LedSensorInfo, _sxyDataLogFileName, sxyStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataxy() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
#}

    def GetWaveLength( self, LedSensorInfo ):
    #{
        try:
        #{
            self.nWaveLengthValue = 0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataWaveLength( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            WaveLength = []
            nRet, WaveLength = LEDSENSOR_Execute( "GetWaveLength", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.StoreDataWaveLength( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetWaveLength Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            self.nWaveLengthValue = int( WaveLength[ 0 ] )
            if ( self.fEmulation ):
            #{
                self.nWaveLengthValue = 1
            #}
            if ( self.nWaveLengthValue == 0 ) :
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange - 1 ) <= eRange._rNone ):
                    #{
                        self.ReportFail( LedSensorInfo, "WaveLength : *** UNDER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange - 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataWaveLength( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "WaveLength : *** UNDER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                if ( self.nWaveLength == 0 ):
                #{
                    self.nWaveLength        = self.nWaveLengthValue
                    self.nWaveLengthOffset  = 0
                #}
                if ( self.nWaveLengthLowLimit == 0 ):
                #{
                    self.nWaveLengthLowLimit = self.nWaveLength - ( ( self.nWaveLength * _nWaveLengthDefaultTolNeg ) / 100 ) + 1
                    if ( self.nWaveLengthLowLimit < 0 ):
                    #{
                        self.nWaveLengthLowLimit = 0
                    #}
                #}
                if ( self.nWaveLengthHighLimit == 0 ):
                #{
                    self.nWaveLengthHighLimit = self.nWaveLength + ( ( self.nWaveLength * _nWaveLengthDefaultTolPos ) / 100 ) + 1
                    if ( self.nWaveLengthHighLimit > 999 ):
                    #{
                        self.nWaveLengthHighLimit = 999
                    #}
                #}
            #}
            if ( not self.StoreDataWaveLength( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvWaveLength ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "WaveLength Error", _sWaveLengthUnit, self.nWaveLengthValue, self.nWaveLengthLowLimit, self.nWaveLength, self.nWaveLengthHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetWaveLength() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataWaveLength( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sWaveLengthStoreData = str( self.nWaveLengthValue )
                if ( not self.StoreData( LedSensorInfo, _sWLDataLogFileName, sWaveLengthStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataWaveLength() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetCCT( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            self.nCCTValue              = 0
            self.dDeltaEDistanceValue   = 0.0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataCCT( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            CCT = []
            nRet, CCT = LEDSENSOR_Execute( "GetCCT", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.StoreDataCCT( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetCCT Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            self.nCCTValue              = int( CCT[ 0 ] )
            self.dDeltaEDistanceValue   = float( CCT[ 1 ] )
            if ( self.fEmulation ):
            #{
                self.nCCTValue = 1
            #}
            if ( self.nCCTValue == 0 ) :
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange - 1 ) <= eRange._rNone ):
                    #{
                        self.ReportFail( LedSensorInfo, "CCT : *** UNDER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange - 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataCCT( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "CCT : *** UNDER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                if ( self.nCCT == 0 ):
                #{
                    self.nCCT = self.nCCTValue
                #}
                self.dDeltaEDistance = self.dDeltaEDistanceValue
                if ( self.nCCTLowLimit == 0 ):
                #{
                    self.nCCTLowLimit = self.nCCT - ( ( self.nCCT * _nCCTDefaultTolNeg ) / 100 ) + 1
                    if ( self.nCCTLowLimit < 0 ):
                    #{
                        self.nCCTLowLimit = 0
                    #}
                #}
                if ( self.nCCTHighLimit == 0 ):
                #{
                    self.nCCTHighLimit = self.nCCT + ( ( self.nCCT * _nCCTDefaultTolPos ) / 100 ) + 1
                    if ( self.nCCTHighLimit > 99999 ):
                    #{
                        self.nCCTHighLimit = 99999
                    #}
                #}
            #}
            if ( not self.StoreDataCCT( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvCCT ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "CCT Error", _sCCTUnit, self.nCCTValue, self.nCCTLowLimit, self.nCCT, self.nCCTHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvDeltaEDistance ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "DeltaEDistance Error", _sDeltaEDistanceUnit, self.dDeltaEDistanceValue, self.dDeltaEDistanceLowLimit, self.dDeltaEDistance, self.dDeltaEDistanceHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetCCT() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataCCT( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sCCTStoreData = str( self.nCCTValue ) + _sDataLogFieldSeparator + str( self.dDeltaEDistanceValue )
                if ( not self.StoreData( LedSensorInfo, _sCCTDataLogFileName, sCCTStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataCCT() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def GetXYZ( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            self.dXValue    = 0.0
            self.dYValue    = 0.0
            self.dZValue    = 0.0
            if ( LedSensorInfo.fFailed ):
            #{
                self.StoreDataXYZ( LedSensorInfo )
                return True
            #}
            Params = [ LedSensorInfo.nLedSensorNumber, LedSensorInfo.nFiberChannel, _DefaultTimeout ]
            XYZ = []
            nRet, XYZ = LEDSENSOR_Execute( "GetXYZ", Params )
            if ( nRet == BOOL.FALSE ):
            #{
                self.StoreDataXYZ( LedSensorInfo )
                self.ReportFail( LedSensorInfo, "GetXYZ Error : " + self.GetLastError(), TestResult.ForceFail )
                return False
            #}
            self.dXValue    = float( XYZ[ 0 ] )
            self.dYValue    = float( XYZ[ 1 ] )
            self.dZValue    = float( XYZ[ 2 ] )
            if ( self.fEmulation ):
            #{
                self.dXValue    = 0.1
                self.dYValue    = 0.1
                self.dZValue    = 0.1
            #}
            if ( ( self.dXValue == 0 ) and ( self.dYValue == 0 ) and ( self.dZValue == 0 ) ):
            #{
                if ( self.fLearn ):
                #{
                    if ( ( self.eRange - 1 ) <= eRange._rNone ):
                    #{
                        self.ReportFail( LedSensorInfo, "XYZ : *** UNDER RANGE !!! ***", TestResult.ForceFail )
                        return False
                    #}
                    else:
                    #{
                        self.eRange = self.eRange - 1
                        return True
                    #}
                #}
                else:
                #{
                    self.StoreDataXYZ( LedSensorInfo )
                    self.ReportFail( LedSensorInfo, "XYZ : *** UNDER RANGE !!! ***", self.eTestResult )
                    return False
                #}
            #}
            elif ( self.fLearn ):
            #{
                self.dX = self.dXValue
                self.dY = self.dYValue
                self.dZ  = self.dZValue
                if ( self.dXLowLimit == 0 ):
                #{
                    self.dXLowLimit = self.dX - ( ( self.dX * _dXDefaultTolNeg ) / 100 ) + 1
                    if ( self.dXLowLimit < 0 ):
                    #{
                        self.dXLowLimit = 0
                    #}
                #}
                if ( self.dXHighLimit == 0 ):
                #{
                    self.dXHighLimit = self.dX + ( ( self.dX * _dXDefaultTolPos ) / 100 ) + 1
                    if ( self.dXHighLimit > 255 ):
                    #{
                        self.dXHighLimit = 255
                    #}
                #}
                if ( self.dYLowLimit == 0 ):
                #{
                    self.dYLowLimit = self.dY - ( ( self.dY * _dYDefaultTolNeg ) / 100 ) + 1
                    if ( self.dYLowLimit < 0 ):
                    #{
                        self.dYLowLimit = 0
                    #}
                #}
                if ( self.dYHighLimit == 0 ):
                #{
                    self.dYHighLimit = self.dY + ( ( self.dY * _dYDefaultTolPos ) / 100 ) + 1
                    if ( self.dYHighLimit > 255 ):
                    #{
                        self.dYHighLimit = 255
                    #}
                #}
                if ( self.dZLowLimit == 0 ):
                #{
                    self.dZLowLimit = self.dZ - ( ( self.dZ * _dZDefaultTolNeg ) / 100 ) + 1
                    if ( self.dZLowLimit < 0 ):
                    #{
                        self.dZLowLimit = 0
                    #}
                #}
                if ( self.dZHighLimit == 0 ):
                #{
                    self.dZHighLimit = self.dZ + ( ( self.dZ * _dZDefaultTolPos ) / 100 ) + 1
                    if ( self.dZHighLimit > 255 ):
                    #{
                        self.dZHighLimit = 255
                    #}
                #}
            #}
            if ( not self.StoreDataXYZ( LedSensorInfo ) ):
            #{
                return False
            #}
            if ( self.eMeasureView == eMeasureView._mvXYZ ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "X Error", _sXUnit, self.dXValue, self.dXLowLimit, self.dX, self.dXHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
                elif ( not self.SetTestInfo( LedSensorInfo, "Y Error", _sYUnit, self.dYValue, self.dYLowLimit, self.dY, self.dYHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
                elif ( not self.SetTestInfo( LedSensorInfo, "Z Error", _sZUnit, self.dZValue, self.dZLowLimit, self.dZ, self.dZHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvX ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "X Error", _sXUnit, self.dXValue, self.dXLowLimit, self.dX, self.dXHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvY ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "Y Error", _sYUnit, self.dYValue, self.dYLowLimit, self.dY, self.dYHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            elif ( self.eMeasureView == eMeasureView._mvZ ):
            #{
                if ( not self.SetTestInfo( LedSensorInfo, "Z Error", _sZUnit, self.dZValue, self.dZLowLimit, self.dZ, self.dZHighLimit, self.eTestResult ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "GetXYZ() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def StoreDataXYZ( self, LedSensorInfo : LedSensorInfo_t ):
    #{
        try:
        #{
            if ( self.fStoreData ):
            #{
                sXYZStoreDataFileName = ""
                if ( self.eMeasureView == eMeasureView._mvXYZ ):
                #{
                    sXYZStoreDataFileName = _sXYZDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvX ):
                #{
                    sXYZStoreDataFileName = _sXDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvY ):
                #{
                    sXYZStoreDataFileName = _sYDataLogFileName
                #}
                elif ( self.eMeasureView == eMeasureView._mvZ ):
                #{
                    sXYZStoreDataFileName = _sZDataLogFileName
                #}
                else:
                #{
                    sXYZStoreDataFileName = _sXYZDataLogFileName
                #}
                sXYZStoreData = str( self.dXValue )         + _sDataLogFieldSeparator + \
                                str( self.dYValue )         + _sDataLogFieldSeparator + \
                                str( self.dZValue )
                if ( not self.StoreData( LedSensorInfo, sXYZStoreDataFileName, sXYZStoreData ) ):
                #{
                    return False
                #}
            #}
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "StoreDataXYZ() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def SetTestInfo( self, LedSensorInfo : LedSensorInfo_t, sTest : str, sUnit : str, ReadValue, LowLimit, ExpectedValue, HighLimit, eTestResult ):
    #{
        try:
        #{
            SetTestInfoEx( sTest,
                            sUnit,
                            float( ReadValue ),
                            float( LowLimit ),
                            float( ExpectedValue ),
                            float( HighLimit ),
                            eTestResult,
                            TestView.tvNone,
                            False,
                            ( self.nCurrentBoardNumber if ( LedSensorInfo == None ) else self.BoardsInfo[ LedSensorInfo.nSensorPin ].nBoard ),
                            self.sComponentName,
                            self.sInstrName,
                            -1,
                            DB._dbIDUnknown,
                            self.nSequence
                            )
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "SetTestInfo() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}

    def ReportFail( self, LedSensorInfo : LedSensorInfo_t, sTestErroInfo : str, eTestResult : TestResult ):
    #{
        try:
        #{
            ReportFail( sTestErroInfo, eTestResult, ( self.nCurrentBoardNumber if ( LedSensorInfo == None ) else self.BoardsInfo[ LedSensorInfo.nSensorPin ].nBoard ) )
            return True
        #}
        except Exception as e:
        #{
            self.ReportFail( None, "ReportFail() Exception : %s" % str( e ), TestResult.ForceFail )
            return False
        #}
        finally:
        #{
            pass
        #}
    #}
#}
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def LedSensorTest( COMStoreName : str ):
#{
    LedSensor   = None
    try:
    #{
        #*******   Initialize Constant and Variables   *******
        LedSensor = CLedSensor( COMStoreName )
        if ( not LedSensor.fInitOK ):
        #{
            del LedSensor
            return ScriptResult.TestAbort
        #}
        if ( not LedSensor.GeMacroParameters() ):
        #{
            del LedSensor
            return ScriptResult.TestContinue
        #}
        nMoveResult = LedSensor.MoveLedSensors( )
        if ( nMoveResult != TestResult.ForcePass ):
        #{
            del LedSensor
            return ScriptResult.TestContinue
        #}
        if ( not LedSensor.SetPower( Switch.On ) ):
        #{
            del LedSensor
            return ScriptResult.TestContinue
        #}
        if ( LedSensor.eUser != eUser._uNone ):
        #{
            LedSensor.RunInteractiveProgram()
        #}
        else:
        #{
            LedSensor.Test()
        #}
        if ( not LedSensor.SetPower( Switch.Off ) ):
        #{
            del LedSensor
            return ScriptResult.TestContinue
        #}
        del LedSensor
        return ScriptResult.TestContinue
    #}
    except Exception as e:
    #{
        ReportFail( "LedSensorTest() Exception : %s" % str( e ), TestResult.ForceFail )
        if ( LedSensor is not None ):
        #{
            del LedSensor
        #}
        return ScriptResult.TestAbort
    #}
    finally:
    #{
        pass
    #}
#}
