# -----------------------------------------
# Seica template for Python - Version=3.0
# -----------------------------------------

import array
import os
import sys
import time
import xml.etree.ElementTree as ET
import win32.win32gui as win32gui
import win32.win32api as win32api
import win32.lib.win32con as win32con
import win32com.client
from ctypes import *

def TRACE( sMsg ):
    win32api.OutputDebugString( sMsg )

def MessageBox( sTitle, sMsg ):
    win32gui.MessageBox( 0, sMsg, sTitle, win32con.MB_OK )

#---------------------------------------------------------
# ENUM
#---------------------------------------------------------
from enum import Enum
from enum import IntEnum

# Enum
# ----------------------------
# --------  COMMON  ----------
# ----------------------------

class ScriptResult( IntEnum ):
    TestContinue = 0
    TestAbort = 1
    TestSkipped = 2
    TestLoopBreak = 3
    TestLoopContinue = 4

class BOOL( IntEnum ):
    FALSE = 0
    TRUE = 1

class DB( IntEnum ):
    _dbIDUnknown = 0

class Switch( IntEnum ):
    Off = 0
    On = 1

class TIME_RELE( IntEnum ):
    ON = 0,
    OFF = 1

class DOMAIN( IntEnum ):
    INSTRUMENT = 0,
    PC = 1,
    ALL = 2

class DRSTART( IntEnum ):
    IMMEDIATE = 0,
    CNT_START = 1,
    CNT_STOP = 2,
    CNT_COMP = 3,
    HW1 = 4,
    HW2 = 5,
    SW1 = 6,
    CLEAR = 7,
    STOP_EVOL = 8

class DRRANGE( IntEnum ):
    AUTO = 0,
    v1V = 1,
    i50uA = 1,
    v10V = 2,
    i500uA = 2,
    i5MA = 3,
    i50MA = 4,
    i500MA = 5,
    i500NA = 6,
    i5UA = 7

class ALL( IntEnum ):
    ON = 0,
    OFF = 1

class WIRE( IntEnum ):
    _2WIRE = 2,
    _3WIRE = 3,
    _4WIRE = 4,
    _6WIRE = 6

class OEB( IntEnum ):
    OFF = 0,
    ON = 1

class ELINE( IntEnum ):
    NONE = 0b00000000,
    L1 = 0b00000001,
    L2 = 0b00000010,
    L3 = 0b00000100,
    L4 = 0b00001000,
    L5 = 0b00010000,
    L6 = 0b00100000,
    L7 = 0b01000000,
    L8 = 0b10000000

class MEASURE( IntEnum ):
    V = 0,
    I = 1

# ----------------------------
# ----------  IMM  -----------
# ----------------------------

class MEAS( IntEnum ):
    IST_I = 0,
    IST_V2 = 0,
    IST_V = 1,
    MAX_V = 2,
    MIN_V = 3,
    AVERAGE_V = 4,
    RMS_V = 5,
    P_V = 6,
    PP_V = 7,
    OFFSET_V = 8,
    DV_DT = 9,
    MAX_I = 10,
    MIN_I = 11,
    AVERAGE_I = 12,
    RMS_I = 13,
    P_I = 14,
    PP_I = 15,
    OFFSET_I = 16,
    DI_DT = 17,
    MAX_V2 = 10,
    MIN_V2 = 11,
    AVERAGE_V2 = 12,
    RMS_V2 = 13,
    P_V2 = 14,
    PP_V2 = 15,
    OFFSET_V2 = 16,
    DV2_DT = 17,
    BUFFER_V = 18,
    BUFFER_I = 19,
    MODULE_V = 20,
    PHASE_V = 21,
    MODULE_I = 22,
    PHASE_I = 23,
    MODULE_V2 = 22,
    PHASE_V2 = 23,
    VECT_VF = 24,
    VECT_IF = 25,
    BUFFER_V2 = 26,
    PAR_DRA = 104,
    PAR_DRB = 105,
    PAR_DRC = 106,
    PAR_GND = 107,
    PAR_LINE_EXT = 108,
    PAR_LINE = 109,
    PAR_PULL = 110,
    PAR_MEAS = 111,
    REL_DRA = 200,
    REL_DRB = 201,
    REL_DRC = 202,
    REL_MESVP = 203,
    REL_MESVM = 204,
    REL_MESI = 205,
    REL_MESI_REF = 206,
    REL_GND = 207,
    REL_PULL = 208

class RANGE_V( IntEnum ):
    NONE = 0,
    _200MVG = 1,
    _500MVG = 2,
    _1VG = 3,
    _2VG = 4,
    _5VG = 5,
    _10VG = 6,
    _2V = 7,
    _5V = 8,
    _10V = 9,
    _20V = 10,
    _50V = 11,
    _100V = 12

class RANGE_I( IntEnum ):
    NONE = 80,
    _500MADC = 0,
    _250MADC = 1,
    _100MADC = 2,
    _50MADC = 16,
    _25MADC = 17,
    _10MADC = 18,
    _5MADC = 32,
    _2P5MADC = 33,
    _1MADC = 34,
    _500UADC = 48,
    _250UADC = 49,
    _100UADC = 50,
    _50UADC = 64,
    _25UADC = 65,
    _10UADC = 66,
    _5UADC = 67,
    _2P5UADC = 68,
    _1UADC = 69,
    _500MAAC = 0,
    _250MAAC = 1,
    _100MAAC = 2,
    _50MAAC = 3,
    _25MAAC = 4,
    _10MAAC = 5,
    _5MAAC = 19,
    _2P5MAAC = 20,
    _1MAAC = 21,
    _500UAAC = 35,
    _250UAAC = 36,
    _100UAAC = 37,
    _50UAAC = 51,
    _25UAAC = 52,
    _10UAAC = 53,
    _25A = 97,
    _10A = 98,
    _5A = 11,
    _2p5A = 11,
    _1A = 11,
    _500MA = 12,
    _250MA = 12,
    _100MA = 13,
    _50MA = 14,
    _25MA = 14,
    _10MA = 14,
    _5MA = 16,
    _2P5MA = 16,
    _1MA = 16,
    _500UA = 17,
    _250UA = 17,
    _100UA = 17,
    _50UA = 19,
    _25UA = 19,
    _10UA = 19,
    _5UA = 20,
    _2P5UA = 20,
    _1UA = 21,
    _60MV = 22

class FILTER( IntEnum ):
    NONE = 0,
    PB_BW = 1,
    PA_BW = 2,
    PB_C1 = 3,
    PA_C2 = 4,
    MM = 5,
    PB_FH = 6,
    PA_FH = 7,
    PBD_FH = 8,
    BR_FH = 9,
    PB_FB = 10,
    PA_FB = 11,
    PBD_FB = 12,
    BR_FB = 13

class INP_VPOS( IntEnum ):
    OPEN = 0,
    L1 = 1,
    L2 = 2,
    L4 = 4,
    L6 = 6,
    GND = 9,
    MONITOR = 10,
    IDRA = 11,
    IDRB = 12,
    IDRC = 13,
    TEMP = 14

class INP_VNEG( IntEnum ):
    OPEN = 0,
    L1 = 1,
    L2 = 2,
    L3 = 3,
    L4 = 4,
    L5 = 5,
    L7 = 7,
    GND = 9

class INP_I_V2( IntEnum ):
    NONE = 0,
    OPEN = 0,
    L1_I = 1,
    L1_V = 2,
    L2_AMP = 2,
    L3_AMP = 3,
    L4_AMP = 4,
    L6_AMP = 6,
    L8_AMP = 8,
    POD = 11,
    CON = 12

class SENSE_I( IntEnum ):
    INTERNAL = 0,
    L5 = 1

class REF_I( IntEnum ):
    GND = 0,
    L3 = 3,
    L7 = 7,
    L2_AMP = 2,
    L3_AMP = 3,
    L4_AMP = 4,
    L5_AMP = 5,
    L7_AMP = 7

class IMMSTART( IntEnum ):
    IMMEDIATE = 0,
    CNT_START = 1,
    CNT_STOP = 2,
    CNT_COMP = 3,
    HW1 = 4,
    HW2 = 5,
    SW1 = 6,
    DISABLE = 7

class TRIG_OUT( IntEnum ):
    NONE = 0,
    SW1 = 1,
    SW2 = 2

class MEAS_V( IntEnum ):
    BUFF_AUTO = 0
    DC = 1
    AC = 2
    DV_DT = 4
    RMS = 8
    FFT = 16

class MEAS_I( IntEnum ):
    BUFF_AUTO = 0,
    DC = 1,
    AC = 2,
    DV_DT = 4,
    RMS = 8,
    FFT = 16

class MODE( IntEnum ):
    NORMAL = 0,
    PROCES = 4,
    ONE_SHOT = 8,
    DEBUG = 16

class MOVEFP( IntEnum ):
    ON = 0,
    OFF = 1

# ----------------------------
# ----------  VIVA  ----------
# ----------------------------

class TestResult( IntEnum ):
    Default         = -1
    ForcePass       = 0
    TestResult      = 1
    ForceFail       = 2
    ForceSkip       = 3
    IgnoreResult    = 4

class TestView( IntEnum ):
    tvNone          = 0
    tvView          = 1
    tvRepeat        = 2
    tvViewRepeat    = 3

class ParVarType( IntEnum ):
    unknown         = 0
    string          = 1
    double          = 2
    pinlist         = 3

class OscChannel( IntEnum ):
    TR_1            = 1
    TR_2            = 2
    TR_3            = 3
    TR_4            = 4
    TR_5            = 5
    TR_6            = 6
    TR_7            = 7
    TR_8            = 8
    TR_9            = 9
    TR_10           = 10
    TR_11           = 11
    TR_12           = 12

class OscTrackMode( IntEnum ):
    Append          = 0
    Append_Draw     = 1
    Clear           = 2
    Clear_Draw      = 3
    Remove          = 4

class OscShMode( IntEnum ):
    Show            = 1
    Hide            = 2

class OscColor( IntEnum ):
    Green           = 0
    Red             = 1
    Blue            = 2
    White           = 3
    Cyan            = 4
    Orange          = 5
    Gray            = 6
    Brown           = 7
    Violet          = 8
    DarkGreen       = 9
    Pink            = 10
    Purple          = 11
    Yellow          = 12
    Black           = 13

class MC_Mode( IntEnum ):
    Add             = 0
    Remove          = 1

class MC_Locked( IntEnum ):
    DontSet         = -1
    No              = 0
    Yes             = 1

class MC_ChannelMode( IntEnum ):
    _NoChannelMode  = -1
    _4L_INC_O       = 0
    _4L_INC_C       = 1
    _4L_IMM_OC      = 2
    _8L_INC_O       = 3
    _8L_INC_C       = 4
    _8L_IMM_OC      = 5
    _2L_INC_O       = 6
    _2L_INC_C       = 7
    _2L_IMM_OC      = 8
    _NC_OC          = 0x40000000

class ICTState( IntEnum ):
    _ICTRead                = 0x00100000
    _ICTAutoLearn           = 0x00200000
    _ICTValid               = 0x00400000
    _ICTAutodebug           = 0x00800000
    _ICTAutoAdjustment      = 0x04000000

class ReturnCode( IntEnum ):
    _RCNoError              = 0
    _RCParameterError       = 1
    _RCSectionNotFound      = 2
    _RCComponentNotFound    = 3
    _RCMacroNotFound        = 4
    _RCLabelNotFound        = 5
    _RCComponentNotEnabled  = 6
    _RCMacroNotEnabled      = 7

class PermType( IntEnum ):
    _FirstPermissions       = 1
    _SecondPermissions      = 2
    _ParallelMode           = 0x00002000

class GVParallelMode( Enum ):
    _sTwinnedBoards         = "TwinnedBoards"
    _sTwinnedComponents     = "TwinnedComponents"
    _sTwinnedChannels       = "TwinnedChannels"
    _sBoardsFailed          = "BoardsFailed"
    _sBoardsBarcodes        = "BoardCodes"

class MeasureUnit( Enum ):
    _sERR                   = "ERR"

# ----------------------------
# --------  RAM_EXT  ---------
# ----------------------------

class SIZE( IntEnum ):
    S32 = 0,
    S24 = 1,
    S16 = 2

class TYPE( IntEnum ):
    INT = 0,
    FLOAT = 1

# ----------------------------
# ----------  GND  -----------
# ----------------------------

class GNDLINE( IntEnum ):
    NONE = 0b11111111,
    L1 = 0b11111110,
    L2 = 0b11111101,
    L3 = 0b11111011,
    L4 = 0b11110111,
    L5 = 0b11101111,
    L6 = 0b11011111,
    L7 = 0b10111111,
    L8 = 0b01111111

class SOURCE( IntEnum ):
    GND = 0,
    GEN_GND = 1

# ----------------------------
# ----------  DRA  -----------
# ----------------------------

class DRAMODE( IntEnum ):
    V = 0,
    I = 1

class WAVE( IntEnum ):
    DC = 0,
    SINE = 1,
    TRI = 2,
    RECT = 3,
    ARB1 = 4,
    ARB2 = 5,
    ARB3 = 6,
    ARB4 = 7,
    ARB5 = 8,
    ARB6 = 9,
    ARB7 = 10,
    ARB8 = 11,
    ARB9 = 12,
    ARB10 = 13,
    VECT1 = 14,
    VECT2 = 15,
    VECT3 = 16,
    VECT4 = 17,
    VECT5 = 18,
    VECT6 = 19,
    VECT7 = 20,
    VECT8 = 21,
    VECT9 = 22,
    VECT10 = 23

class COUPLING( IntEnum ):
    DC = 0,
    AC = 1

class DRAOUT( IntEnum ):
    NONE = 0,
    L1 = 1,
    L2 = 2,
    L8 = 8

# ----------------------------
# ----------  DRB  -----------
# ----------------------------

class DRBMODE( IntEnum ):
    V = 0,
    GUARD = 4,
    FOLLOWER = 5

class DRBSENSE( IntEnum ):
    INT = 0,
    L4 = 4,
    L5 = 5

class IN( IntEnum ):
    DAC = 0,
    L2 = 2,
    L4 = 4,
    L6 = 6,
    L8 = 8

class DRBOUT( IntEnum ):
    NONE = 0,
    L1 = 1,
    L2 = 2,
    L3 = 3,
    L4 = 4,
    L5 = 5,
    L7 = 7,
    L4HF = 9

# ----------------------------
# ----------  DRC  -----------
# ----------------------------

class DRCOUT( IntEnum ):
    NONE = 0,
    L1 = 1,
    L2 = 2,
    L4 = 4,
    L6 = 6

class DRCSTART( IntEnum ):
    IMMEDIATE = 0,
    SW1 = 1,
    DRB_FOLLOWER = 2

# ----------------------------
# ---------  ANABUS  ---------
# ----------------------------

class CHN_SET( IntEnum ):
    UNC = 0,
    CON = 1,
    LEAVE = 2

class L_MODE( IntEnum ):
    INC_O = 0,
    INC_C = 1,
    IMM = 2

class CL_MODE( IntEnum ):
    IMM = 2

# ----------------------------
# ----------  CAP  -----------
# ----------------------------

class CAPMODE( IntEnum ):
    DC_ACTIVE = 0,
    AC_PASSIVE = 2

# ----------------------------
# --------  CHANNEL  ---------
# ----------------------------

class BLINEE( IntEnum ):
    CLOSE = 0,
    OPEN = 1,
    AUTO = 2

class CHMODE( IntEnum ):
    _4L_INC_O = 0,
    _4L_INC_C = 1,
    _4L_IMM = 2,
    _8L_INC_O = 3,
    _8L_INC_C = 4,
    _8L_IMM = 5,
    _2L_INC_O = 6,
    _2L_INC_C = 7,
    _2L_IMM = 8

# ----------------------------
# --------  DISCAP  ----------
# ----------------------------

class DISCAPMODE( IntEnum ):
    DRC_OFF = 0,
    DRC_ON = 1

# ----------------------------
# --------  CONTACT  ---------
# ----------------------------

class CTCMODE( IntEnum ):
    EXECUTE = 0,
    SINGLE_EXEC = 1,
    FAMILY = 10,
    EXCLUDE = 20,
    CLEAR = 100

class CTCTYPE( IntEnum ):
    ALL_FLAGS = 1,
    ALL_VP = 2,
    ALL_VM = 3,
    FAIL_CH = 4,
    FAIL_VP = 5,
    FAIL_VM = 6,
    FAIL_NUM = 7

# ----------------------------
# ---------  FLASH  ----------
# ----------------------------

class SEGMENT( IntEnum ):
    ARB1 = 4,
    ARB2 = 5,
    ARB3 = 6,
    ARB4 = 7,
    ARB5 = 8,
    ARB6 = 9,
    ARB7 = 10,
    ARB8 = 11,
    ARB9 = 12,
    ARB10 = 13,
    VECT1 = 14,
    VECT2 = 15,
    VECT3 = 16,
    VECT4 = 17,
    VECT5 = 18,
    VECT6 = 19,
    VECT7 = 20,
    VECT8 = 21,
    VECT9 = 22,
    VECT10 = 22

class CONVERSION( IntEnum ):
    NONE = 0,
    AUTO = 1

class OUT_A_STATUS( IntEnum ):
    NONE = 0,
    SPARE = 1,
    GND = 2,
    PULLDOWN = 4,
    VBAT = 10

class OUT_B_STATUS( IntEnum ):
    NONE = 0,
    PULLDOWN = 1,
    GND = 2,
    PULLUP = 5,
    VBAT = 10

class OUTLOAD_ONOFF( IntEnum ):
    OFF = 0,
    ON = 1

class OUTOPTO_STATUS( IntEnum ):
    ON = 0,
    OFF = 1

# ----------------------------
# ---------  LINE  -----------
# ----------------------------

class OUT_LINES( IntEnum ):
    OPEN = 0,
    _1_4_CLOSE = 1,
    _5_8_CLOSE = 2,
    CLOSE = 3

class LINEMODE( IntEnum ):
    _8L = 0,
    _4L = 1

class INT_LINES( IntEnum ):
    MEAS_I = 0,
    L1_ALL = 1,
    L5_ALL = 2,
    ALL = 3

# ----------------------------
# --------  MONITOR  ---------
# ----------------------------

class MON_OUT( IntEnum ):
    IDRA = 0,
    LPDRA = 1,
    IDRB = 2,
    LDRB = 3,
    IDRC = 4,
    LDRC = 5,
    LNDRA = 6,
    TEMP = 7,
    REFP = 8,
    REFN = 9,
    TH_START = 10,
    TH_STOP = 11,
    VOL = 12,
    VOH = 13,
    THL = 14,
    THH = 15,
    VDRB = 16,
    VDRC = 17,
    VDRA = 18,
    SDRA = 19,
    SDRB = 20,
    SDRC = 21,
    GDRA = 22,
    GDRB = 23

# ----------------------------
# -------  POWERSCAN  --------
# ----------------------------

class POS_MODE( IntEnum ):
    MODE_0 = 0,
    MODE_1 = 1

# ----------------------------
# ----------  PULL  ----------
# ----------------------------

class VAL( IntEnum ):
    R_NONE = 0,
    R_100 = 1,
    R_1K = 2,
    R_10K = 3,
    R_100K = 4,
    R_1M = 5

class PUL_SOURCE( IntEnum ):
    NONE = 0,
    L2 = 1,
    GND = 2,
    VCC = 3

# ----------------------------
# -----------  HW  -----------
# ----------------------------

class RD_TYPE( IntEnum ):
    RT = 1,
    JT = 2,
    FX = 3

class WR_TYPE( IntEnum ):
    OC = 0,
    RT = 1,
    JT = 2,
    FX = 3

# ----------------------------
# ----------  RES  -----------
# ----------------------------

class RES_MODE( IntEnum ):
    DC_ACTIVE = 0,
    DC_PASSIVE = 1,
    AC_PASSIVE = 2

# ----------------------------
# ----------  SCAY  ----------
# ----------------------------

class SCY_MODE( IntEnum ):
    MODE_0 = 0,
    MODE_7 = 7

# ----------------------------
# --------  COUNTER  ---------
# ----------------------------

class CNT_MODE( IntEnum ):
    COUNT = 0,
    COUNT_B = 1,
    COUNT_GATE = 2,
    FREQ = 3,
    TINT_A = 4,
    TINT_AB = 5,
    PERIOD = 6

class INP_A( IntEnum ):
    NONE = 0,
    L4 = 4,
    L6 = 6

class INP_B( IntEnum ):
    NONE = 0,
    L2 = 2,
    L8 = 8

class SLOPE( IntEnum ):
    NEG = 0,
    POS = 1

class CNT_RANGE( IntEnum ):
    _10V = 1,
    _100V = 2,
    _10V_50 = 3

class CNT_START( IntEnum ):
    IMMEDIATE = 0,
    HW1 = 4,
    HW2 = 5,
    SW1 = 6,
    DISABLE = 7,
    DISARM = 8

class HISTERESIS( IntEnum ):
    AUTO = 0,
    H_10US = 1,
    H_300NS = 2,
    H_10NS = 3

# ----------------------------
# ---------  SHORT  ----------
# ----------------------------

class SHT_MODE( IntEnum ):
    EXECUTE = 0,
    SINGLE_EXEC = 1,
    FAMILY = 10,
    FAIL_RES = 5,
    FAIL_NUM = 7

class SHT_TYPE( IntEnum ):
    ALL_FLAGS = 1,
    ALL_RES = 2,
    FAIL_CH = 4,
    FAIL_RES = 5,
    FAIL_NUM = 7

# ----------------------------
# ---------  SCAEVO  ---------
# ----------------------------

class SCE_MODE( IntEnum ):
    MODE_F = 15,
    MODE_E = 14,
    MODE_9 = 9,
    MODE_4 = 4

# ----------------------------
# -----------  PW  -----------
# ----------------------------

class STATE( IntEnum ):
    ON = 0,
    OFF = 1

class PW_MODE( IntEnum ):
    INT = 0,
    EXT = 1

class SENSE( IntEnum ):
    ON = 0,
    OFF = 1

class OPERATION( IntEnum ):
    SET = 0,
    PREPARE = 1,
    ALL = 2

class READSTATUS( IntEnum ):
    PWS_O3_V = 1,                   # solo per ~meas = leggi volt
    PWS_O3_I = 2,                   # solo per ~meas = leggi corrente
    PWS_O3_INT = 4,                 # solo per ~meas LEGGI IN INTERNO
    PWS_O3_EXT = 8,                 # solo per ~meas LEGGI IN EXTERNO
    PWS_O3_USER_NOCLEAR = 16,       # COME USER MA NON LIBERA LI4 NON FA LA MISURA E RITORNA IL VALORE DI CONVERSIONE.
    PWS_O3_USER = 32,               # solo per ~meas LEGGI MANDA TENSIONE FEEDBACK UN USCITA PER POI LEGGERE CON l'aclam A CARICO USER
    PWS_O3_DIG = 64,                # solo per ~meas LEGGI INTERNO DIGITALE SOLO SERVIZI 3
    PWS_O3_AC = 128,                # solo per ~meas LEGGI INTERNO DIGITALE SOLO SERVIZI 3
    PWS_O3_USER_CLEAR = 256,        # da usare per liberale la li4
    PWS_O3_STATUS = 0,              # READ PWS STATUS 0 SPENTO 1 ACCESO
    PWS_O3_VMAX = 17,               # TENSIONE MASSIMA DI CONFIGURAZIONE
    PWS_O3_IMAX = 18,               # CORRENTE MASSIMA DI CONFIGURAZIONE
    PWS_O3_VPVMAX = 19,
    PWS_O3_VPIMAX  = 20,
    PWS_O3_VRVEMAX = 21,
    PWS_O3_VRIEMAX = 22,
    PWS_O3_VMIN = 23,
    PWS_O3_IMIN = 24,
    PWS_O3_VPVMIN = 25,
    PWS_O3_VPIMIN = 26,
    PWS_O3_VCOFF = 27,
    PWS_O3_VCGAIN = 28,
    PWS_O3_ICOFF = 29,
    PWS_O3_ICGAIN = 30,
    PWS_O3_VRESET = 31,
    PWS_O3_IRESET = 32,
    PWS_O3_CRESET = 33,
    PWS_O3_SRESET = 34,
    PWS_O3_VRVEMIN = 35,
    PWS_O3_VRIEMIN = 36,
    PWS_O3_VRCEOFF = 37,
    PWS_O3_VRCEGAIN = 38,
    PWS_O3_IRCEOFF = 39,
    PWS_O3_IRCEGAIN = 40,
    PWS_O3_VLEMAX = 41,             # TENSIONE MASSIMA MODO EXTERNO
    PWS_O3_VLEMIN = 42,
    PWS_O3_ILEMAX = 43,             # CORRENTE MASSIMA MODO INTERNO
    PWS_O3_ILEMIN = 44,
    PWS_O3_VQUADRANT = 45,
    PWS_O3_IQUADRANT = 46,
    PWS_O3_IMODE = 47,
    PWS_O3_VRVIMAX = 48,
    PWS_O3_VRIIMAX = 49,
    PWS_O3_VRVIMIN = 50,
    PWS_O3_VRIIMIN = 51,
    PWS_O3_VRCIOFF = 52,
    PWS_O3_VRCIGAIN = 53,
    PWS_O3_IRCIOFF = 54,
    PWS_O3_IRCIGAIN = 55,
    PWS_O3_VLIMAX = 56,             # TENSIONE MASSIMA MODI INTERNO
    PWS_O3_ILIMAX = 57,             # CORRENTE MASSIMA MODO INTERNO
    PWS_O3_ENABLERIS = 58,
    PWS_O3_NAME = 59,
    PWS_O3_CONMODE = 60,
    PWS_O3_FEEDBACK = 61,
    PWS_O3_VRLIOFF = 62,
    PWS_O3_VRLIGAIN = 63,
    PWS_O3_IRLIOFF = 64,
    PWS_O3_IRLIGAIN = 65,
    PWS_O3_VRLEOFF = 66,
    PWS_O3_VRLEGAIN = 67,
    PWS_O3_IRLEOFF = 68,
    PWS_O3_IRLEGAIN = 69,
    PWS_O3_DESCRIPTIONSER = 70,     #01.07.20187lau: Versione della servali VER0=0, VER1=1...VERn=N
    PWS_O3_KINDOFSERVICE = 71       #01.07.20187lau: Servizi : SE2=2 o SE4=4

# ----------------------------
# -----------  POWER  --------
# ----------------------------

class POWER_SELECT( IntEnum ):
    AUTO = 0,
    PW1 = 1,
    PW2 = 2,
    PW3 = 3,
    PW4 = 4,
    PW5 = 5,
    PW6 = 6,
    PW7 = 7,
    PW8 = 8,
    PWEXT = 9,
    PWALL = 10                      #questo solo per la POWER_REMOVE!

class APPLY_MODE( IntEnum ):
    ON = 0,
    PREPARE = 1,
    ALLON = 2

class POWER_CONN( IntEnum ):
    FIXED = 0,
    FLYING_Floating = 1,
    FLYINGPosRef = 2,
    FLYINGNegRef = 3

class APPLY_SENSE( IntEnum ):
    ON = 0,
    OFF = 1

# ----------------------------
# ---------  LOGIC  ----------
# ----------------------------

class CH( IntEnum ):
    IL = 0,
    IH = 1,
    ML = 4,
    MH = 5,
    OL = 2,
    OH = 3,
    OM = 6

class BURST( IntEnum ):
    OFF = 0,
    ON = 1

class OUT_CH1( IntEnum ):
    NONE = 0,
    L1 = 1

class OUT_CH2( IntEnum ):
    NONE = 0,
    L2 = 2

class OUT_CH3( IntEnum ):
    NONE = 0,
    L3 = 3,
    L5 = 5

class OUT_CH4( IntEnum ):
    NONE = 0,
    L4 = 4,
    L8 = 8

class INP_CH1_3( IntEnum ):
    DSP = 0,
    RAM = 1,
    CLK_IMM = 2,
    JTAG = 3

class INP_CH2_4( IntEnum ):
    DSP = 0,
    RAM = 1,
    CLK_PLL = 2,
    JTAG = 3

# ----------------------------
# --------  FEMTO  -----------
# ----------------------------

class FMT_MODE( IntEnum ):
    _ModeNotMounted = -1,
    _ModeNone = 0,
    _ModeOpenProbe = 1,
    _ModeCAP = 2,
    _ModeFrequency = 3,
    _ModeHIZ = 4,
    _ModeUpGND = 5,
    _ModeLineHV = 6,
    _ModePeriod = 7,
    _ModeHIZG = 8,
    _ModeReadVector = 9,
    _ModeCAPAverage = 12,
    _ModeCAPTimeout = 13,
    _ModeCalibrate = 14,
    _ModePrepare = 15,
    _ModeWriteBoard = 16,
    _ModeWriteByte = 17,
    _ModeOpenProbeOld = 18,
    _ModeAcquire = 19,
    _ModeReadData = 20,
    _ModeCapLV = 21,
    _ModeHWReset = 22,
    _ModeDCForHALL = 24

class TODO( IntEnum ):
    _FemtoNone = 0,
    _FemtoRead = 0x1,
    _FemtoWrite = 0x2,
    _FemtoWriteRead = 0x3,
    _FemtoNumAcquisition = 1024

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CFileIni:
    def __init__( self, IniFile ):
        try:
            self._ComObj = win32com.client.Dispatch( "Lcx.IniHelper" )
            self._IniFile = IniFile
        except Exception as e:
            MessageBox( "Error", "CFileIni.__init__ Exception : %s" % str( e ) )
        finally:
            pass

    def __del__( self ):
        self._ComObj

    def Write( self, Section, Entry, Value ):
        R = self._ComObj.Write( Section, Entry, Value, self._IniFile )

        if ( 0 == R ):
            MessageBox( "Error", "Write Failed" )

    def Read( self, Section, Entry, DefaultValue ):
        Value = ""
        R = self._ComObj.Read( Section, Entry, DefaultValue, self._IniFile, Value )

        if ( 0 == R ):
            MessageBox( "Error", "Read Failed" )

        return R[ 1 ]

    def Wait( self, Section, Entry, DefaultValue ):
        Value = 0
        R = self._ComObj.Wait( Section, Entry, DefaultValue, self._IniFile, Value )

        if ( 0 == R ):
            MessageBox( "Error", "Wait Failed" )

        return R[ 1 ]

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class CTimer:
    _MaxNumTimers = 10
    def __init__( self ):
        try:
            self.dTimer  = [ 0 ] * self._MaxNumTimers
        except Exception as e:
            MessageBox( "Error", "CTimer.__init__ Exception : %s" % str( e ) )
        finally:
            pass

    def __del__( self ):
        pass

    def StartTimer( self, dStartTimer = 0, nTimer = 0 ):
        if ( ( nTimer < 0 ) or ( nTimer >= self._MaxNumTimers ) ):
            return False
        self.dTimer[ nTimer ] = float( dStartTimer )
        if ( self.dTimer[ nTimer ] == 0 ):
            self.dTimer[ nTimer ] = time.clock()
        return True

    def TimerExpired( self, dTimeout, nTimer = 0 ):
        if ( ( nTimer < 0 ) or ( nTimer >= self._MaxNumTimers ) ):
            return True
        if ( self.dTimer[ nTimer ] == 0 ):
            return True
        if ( ( time.clock() - self.dTimer[ nTimer ] ) > dTimeout ):
            self.dTimer[ nTimer ] = 0
            return True
        if ( GetEmulation() ):
            _dTimeout = 0.01 if ( dTimeout >= 0.01 ) else dTimeout
            if ( ( time.clock() - self.dTimer[ nTimer ] ) > _dTimeout ):
                self.dTimer[ nTimer ] = 0
                return True
        return False

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def Delay( dSeconds : float ):
    if ( not GetEmulation() ):
        time.sleep( dSeconds )
    else:
        SetEmulationTime( dSeconds * 1000000.0 ) # us

#---------------------------------------------------------
# INSTRUMENTS MANAGEMENT
#---------------------------------------------------------
class CFNtools:
    def __init__( self ):
        # Get SVIL from COM store
        self.COMStore = None
        COMStoreName = ".0"
        self.COMStore = win32com.client.Dispatch( "LCX.IUS" )
        self.Factory = self.COMStore.GetInterface( "SVIL" + COMStoreName )

        self.Aclam = self.Factory.GetACLAM()
        self.IMM = self.Factory.GetDMM()
        self.Viva = self.Factory.GetVIVA()
        self.Channel = self.Factory.GetCHANNEL()
        self.Line = self.Factory.GetLINE()
        self.Dra = self.Factory.GetDRASource()
        self.Drb = self.Factory.GetDRBSource()
        self.Drc = self.Factory.GetDRCSource()
        self.Counter = self.Factory.GetCOUNTER()
        self.RamExt = self.Factory.GetRAM_EXT()
        self.Gnd = self.Factory.GetAGND()
        self.Anabus = self.Factory.GetANABUS()
        self.Cap = self.Factory.GetCAP()
        self.Discap = self.Factory.GetDISCAP()
        self.Contact = self.Factory.GetCONTACT()
        self.Flash = self.Factory.GetFLASH()
        self.IOV5Load = self.Factory.GetIOV5LOAD()
        self.LineExt = self.Factory.GetLINE_EXT()
        self.Monitor = self.Factory.GetMONITOR()
        self.Powerscan = self.Factory.GetPOWERSCAN()
        self.Pull = self.Factory.GetPULL()
        self.HW = self.Factory.GetHW()
        self.Res = self.Factory.GetRES()
        self.ScaY = self.Factory.GetSCAY()
        self.Short = self.Factory.GetSHORT()
        self.ScaEvo = self.Factory.GetSCAEVO()
        self.PW = self.Factory.GetPW()
        self.Guapoint = self.Factory.GetGUAPOINT()
        self.Logic = self.Factory.GetLOGIC()
        self.Femto = self.Factory.GetFEMTO()
        self.Ipy = self.Factory.GetIPY()
        self.IctCtrl = self.Factory.GetICTCTRL()
        self.TestSvil = self.Factory.GetTestSvil()
        self.POWER = self.Factory.GetPOWER()
        self.VDT = self.Factory.GetVDT()
        self.LedSensor = self.Factory.GetLedSensor()

    def __del__( self ):
        del self.Factory
        del self.Aclam
        del self.IMM
        del self.Viva
        del self.Channel
        del self.Line
        del self.Dra
        del self.Drb
        del self.Drc
        del self.Counter
        del self.RamExt
        del self.Gnd
        del self.Anabus
        del self.Cap
        del self.Discap
        del self.Contact
        del self.Flash
        del self.IOV5Load
        del self.Monitor
        del self.Pull
        del self.HW
        del self.Res
        del self.ScaY
        del self.Short
        del self.ScaEvo
        del self.PW
        del self.Guapoint
        del self.Logic
        del self.Femto
        del self.Ipy
        del self.IctCtrl
        del self.TestSvil
        del self.POWER
        del self.VDT
        del self.LedSensor
        if ( self.COMStore != None ):
            del self.COMStore

# creates FNtools object (and executes the __init__).
# Before garbage collect the object will be executed the __del__
SVILinstruments = CFNtools()

# ----------------------------
# ----------  VIVA  ----------
# ----------------------------

def CheckLimits(
    ReadValue : float,
    LowLimit : float,
    ExpectedValue : float ,
    HighLimit : float,
    Unit : str = "",
    Tresult : TestResult = TestResult.TestResult
    ):
    return SVILinstruments.Viva.CheckLimits(
        Unit,
        ReadValue,
        LowLimit,
        ExpectedValue,
        HighLimit,
        Tresult
        )

def WriteReport(
    TestErroInfo : str
    ):
    return SVILinstruments.Viva.WriteReport(
        TestErroInfo
        )

def SetTestInfo(
    Unit : str,
    ReadValue : float,
    LowLimit : float,
    ExpectedValue : float,
    HighLimit : float,
    Tresult : TestResult,
    Tview : TestView = TestView.tvNone
    ):
    return SVILinstruments.Viva.SetTestInfo(
        Unit,
        ReadValue,
        LowLimit,
        ExpectedValue,
        HighLimit,
        Tresult,
        Tview
        )

def SetTestInfoEx(
    TestErroInfo : str,
    Unit : str,
    ReadValue : float,
    LowLimit : float,
    ExpectedValue : float,
    HighLimit : float,
    Tresult : TestResult,
    Tview : TestView = TestView.tvNone,
    AlwaysWriteReport : bool = False,
    Board : int = -1,
    ComponentName : str = "",
    InstrName : str = "",
    MacroNumber : int = -1,
    MacroID : DB = DB._dbIDUnknown,
    Sequence : int = -1,
    LabelName : str = "",
    LabelNumber : int = -1,
    LabelID : DB = DB._dbIDUnknown,
    ValueName : str = "",
    Value : float = 0
    ):
    return SVILinstruments.Viva.SetTestInfoEx(
        TestErroInfo,
        Unit,
        ReadValue,
        LowLimit,
        ExpectedValue,
        HighLimit,
        Tresult,
        Tview,
        AlwaysWriteReport,
        Board,
        ComponentName,
        InstrName,
        MacroNumber,
        MacroID,
        Sequence,
        LabelName,
        LabelNumber,
        LabelID,
        ValueName,
        Value
        )

def ReportFail(
    TestErroInfo : str,
    Tresult : TestResult,
    Board : int = -1
    ):
    return SetTestInfoEx( TestErroInfo, MeasureUnit._sERR.value, 1.0, 0.0, 0.0, 0.0, Tresult, TestView.tvNone, False, Board )

def TestClear():
    return SVILinstruments.Viva.TestClear()

def TestSet(
    Unit : str,
    LowLimit : str,
    ExpectedValue : float,
    HighLimit : float
    ):
    return SVILinstruments.Viva.TestSet(
        Unit,
        LowLimit,
        ExpectedValue,
        HighLimit
        )

def TestMeasure(
    ReadValue : float,
    Tresult : TestResult = TestResult.TestResult,
    Tview : TestView = TestView.tvNone
    ):
    return SVILinstruments.Viva.TestMeasure(
        ReadValue,
        Tresult,
        Tview
        )

def GetAteConf():
    R, AteConf = SVILinstruments.Viva.GetAteConf( "" )
    return R, AteConf

def GetGlobalVariable(
    GlobalVariableName : str
    ):
    R, Kind, Value = SVILinstruments.Viva.GetGlobalVariable(
        GlobalVariableName
        )
    return R, ParVarType( Kind ), Value

def SetGlobalVariable(
    GlobalVariableName : str,
    Value : object
    ):
    R = SVILinstruments.Viva.SetGlobalVariable(
        GlobalVariableName,
        Value
        )
    return R

def GetCurMacroParameter(
    ParameterName : str
    ):
    R, ParType, Value = SVILinstruments.Viva.GetCurMacroParameter(
        ParameterName,
        )
    return R, ParVarType( ParType ), Value

def SetCurMacroParameter(
    ParameterName : str,
    Value : object
    ):
    R = SVILinstruments.Viva.SetCurMacroParameter(
        ParameterName,
        Value
        )
    return R

def GetMacroParameterValue(
    ComponentName : str,
    InstrName : str,
    MacroNumber : int,
    MacroID : DB,
    ParameterName :str
    ):
    return SVILinstruments.Viva.GetMacroParameterValue( ComponentName, InstrName, MacroNumber, MacroID, ParameterName )

def SetMacroParameterValue(
    ComponentName : str,
    InstrName : str,
    MacroNumber : int,
    MacroID : DB,
    ParameterName :str,
    Value : object
    ):
    return SVILinstruments.Viva.SetMacroParameterValue( ComponentName, InstrName, MacroNumber, MacroID, ParameterName, Value )

def SystemExecute(
    Service : str,
    Params : object
    ):
    if ( ( Params is not None ) and ( type( Params ) == str ) ):
        R, Response = SVILinstruments.Viva.SystemExecute(
                                                        Service,
                                                        Params,
                                                        ""
                                                        )
        return R, Response
    else:
        R, Response = SVILinstruments.Viva.SystemExecuteRAW(
                                                            Service,
                                                            Params,
                                                            ""
                                                            )
        return R, Response

def TestExecute(
    Service : str,
    Params : object
    ):
    if ( ( Params is not None ) and ( type( Params ) == str ) ):
        R, Response = SVILinstruments.Viva.TestExecute(
                                                        Service,
                                                        Params,
                                                        ""
                                                        )
        return R, Response
    else:
        R, Response = SVILinstruments.Viva.TestExecuteRAW(
                                                        Service,
                                                        Params,
                                                        ""
                                                        )
        return R, Response

def DBExecute(
    Service : str,
    Params : object
    ):
    if ( ( Params is not None ) and ( type( Params ) == str ) ):
        R, Response = SVILinstruments.Viva.DBExecute(
                                                    Service,
                                                    Params,
                                                    ""
                                                    )
        return R, Response
    else:
        R, Response = SVILinstruments.Viva.DBExecuteRAW(
                                                        Service,
                                                        Params,
                                                        ""
                                                        )
        return R, Response

def SetViewInfo(
    Comp : str = "",
    Macro : str = "",
    Label : str = "",
    Val : float = 2,
    Unit : str = "V",
    vAtt : float = 2,
    perc : float = 10,
    vMin : float = 1,      # low
    vMax : float = 3,      # high
    Min : float = 0,       # tachimetro min
    Max : float = 4        # tachimetro max
    ):
    R = SVILinstruments.Viva.SetViewInfo(
        Comp,
        Macro,
        Label,
        Val,
        Unit,
        vAtt,
        perc,
        vMin,      # low
        vMax,      # high
        Min,       # tachimetro min
        Max        # tachimetro max
        )
    return R

def TerminalColor(
    Background : int = 0,     # Black
    Foreground : int = 15     # White
    ):
    R = SVILinstruments.Viva.TerminalColor(
        Background,
        Foreground
        )
    return R

def TerminalCursor(
    Row : int = 1,
    Column : int = 1
    ):
    R = SVILinstruments.Viva.TerminalCursor(
        Row,
        Column
        )
    return R

def TerminalPause():
    R = SVILinstruments.Viva.TerminalPause()
    return R

def TerminalWrite(
    Message : str
    ):
    R = SVILinstruments.Viva.TerminalWrite(
        Message
        )
    return R

def OSC_Disable():
    return SVILinstruments.Viva.OscDisable()

def OSC_Clear():
    return SVILinstruments.Viva.OscClear()

def OSC_SetTrack(
    SCOPE : float = 1,
    TRACK : OscChannel = OscChannel.TR_1,
    NAME : str = "",
    SCALE_Y : float = 1,
    OFFSET_Y : float = 0,
    MODE : OscTrackMode = OscTrackMode.Append,
    COLOR : OscColor = OscColor.Green
    ):
    return SVILinstruments.Viva.OscSetTrack(
        SCOPE,
        TRACK,
        NAME,
        SCALE_Y,
        OFFSET_Y,
        MODE,
        COLOR
        )

def OSC_Show(
    MODE : OscShMode = OscShMode.Show
    ):
    return SVILinstruments.Viva.OscShow(
        MODE
        )

def OSC_Set(
    SCOPE : float = 1,
    NAME_X : str = "",
    MIN_X : float = 0,
    MAX_X : float = 100,
    NAME_Y : str = "",
    MIN_Y : float = 0,
    MAX_Y : float = 100,
    TIME_DIV : float = 0
    ):
    return SVILinstruments.Viva.OscSet(
        SCOPE,
        NAME_X,
        MIN_X,
        MAX_X,
        NAME_Y,
        MIN_Y,
        MAX_Y,
        TIME_DIV
        )

def OSC_Draw(
    SCOPE : float = 1
    ):
    return SVILinstruments.Viva.OscDraw(
        SCOPE
        )

def OSC_Write(
    DATA : [float] = [],
    SCOPE : float = 1,
    TRACK : OscChannel = OscChannel.TR_1,
    ACQUISITION : float = 0
    ):
    return SVILinstruments.Viva.OscWrite(
        DATA,
        SCOPE,
        TRACK,
        ACQUISITION
        )

def IsFlying():
    sFlying = SVILinstruments.Viva.GetSystemProperty( "FixtureType" )
    if ( ( sFlying == "Flying" ) or ( sFlying == "Mobile Fixture" ) ):
        fFlying = True
    else:
        fFlying = False
    return fFlying

def ClearReport():
    R, sResponse = SVILinstruments.Viva.TestExecute(
        "ResetInstrCookie",
        "",
        ""
        )
    return R

def CheckStopProgram():
    # Check if Stop Test is pressed
    Params = "<R><MSG SyncAbort=\"N\" /></R>"
    fStop, sResponse = SVILinstruments.Viva.TestExecute(
        "CheckStopProgram",
        Params,
        ""
        )
    return fStop

def GetEmulation():
    fEmul, sResponse = SVILinstruments.Viva.TestExecute(
        "GetEmulationEnabled",
        "",
        ""
        )
    return fEmul

def GetVivaPath():
    return SVILinstruments.Viva.GetSystemProperty( "VivaPath" )

def GetBoardPath():
    return SVILinstruments.Viva.GetSystemProperty( "DefaultWorkPath" )

def GetKITName():
    return SVILinstruments.Viva.GetSystemProperty( "KITName" )

def GetBoardName():
    return SVILinstruments.Viva.GetSystemProperty( "CurrentBoard" )

def GetPanelCode():
    return SVILinstruments.Viva.GetSystemProperty( "BoardCode" )

def GetBoardCode():
    return SVILinstruments.Viva.GetSystemProperty( "BoardSubCode" )

def GetTestSettings():
    fAutoDebug = SVILinstruments.Viva.GetSystemProperty( "Autodebug" )
    fAutoLearn = SVILinstruments.Viva.GetSystemProperty( "Autolearn" )
    fAutoAdjust = SVILinstruments.Viva.GetSystemProperty( "AutoAdjustment" )
    return fAutoDebug, fAutoLearn, fAutoAdjust

def GetScannerBoards():
    sScannerBoards = SVILinstruments.Viva.GetSystemProperty( "ScannerBoards" )
    return sScannerBoards

def SetView(
    fView : bool
    ):
    Params = int( fView )
    R, Response = SVILinstruments.Viva.SystemExecute(
        "SetView",
        Params,
        ""
        )
    return R

def GetNumBoards():
    R, nBoards = SVILinstruments.Viva.TestExecute(
        "GetNumBoards",
        "",
        ""
        )
    return -1 if ( not R ) else int( nBoards )

def GetCurrentBoardNumber():
    R, Response = SVILinstruments.Viva.TestExecute(
        "GetCurrentBoardNumber",
        "",
        ""
        )
    return -1 if ( not R ) else int( Response )

def IsBoardEnabled(
    nBoard
    ):
    return SVILinstruments.Viva.BoardEnabled( int( nBoard ) )

def GetComponentName():
    sComponentName = ""
    R, Response = SVILinstruments.Viva.DBExecute(
        "GetCurrentComponentName",
        "",
        ""
        )
    if ( R ):
        sComponentName = str( Response )
    return sComponentName

def GetMacroInfo():
    nSequence   = -1
    sMacroName  = ""
    sInstrName  = ""
    nSequence   = 0
    R, Response = SVILinstruments.Viva.DBExecute(
        "GetCurrentMacroInfo",
        "",
        ""
        )
    if ( R ):
        root = ET.fromstring( Response )
        sMacroName = root.find( 'MSG' ).get( 'MacroName' )
        sInstrName = root.find( 'MSG' ).get( 'InstrName' )
        nSequence = int( root.find( 'MSG' ).get( 'Sequence' ) )
    return sMacroName, sInstrName, nSequence

def GetCurMacroMemoParameter(
    sSectionName : str = "",
    sParameterName : str = "",
    DefaultValue : object = None,
    ParameterType : ParVarType = ParVarType.string,
    fConvertToBool : bool = False
    ):
    R, Value = SVILinstruments.Viva.GetCurMacroMemoParameter(
        sSectionName,
        sParameterName,
        DefaultValue,
        ParameterType
        )
    if ( R and ( ( ParameterType == ParVarType.string ) and fConvertToBool ) ):
        if ( ( str( Value ) == "Y" ) or ( str( Value ) == "y" ) ):
            return R, True
        elif ( ( str( Value ) == "N" ) or ( str( Value ) == "n" ) ):
            return R, False
    return R, Value

def SetCurMacroMemoParameter(
    sSectionName : str = "",
    sParameterName : str = "",
    ParameterType : ParVarType = ParVarType.string,
    Value : object = None
    ):
    R = SVILinstruments.Viva.SetCurMacroMemoParameter(
        sSectionName,
        sParameterName,
        ParameterType,
        Value
        )
    return R

def GetMacroPermissions(
    PermissionsType : PermType = PermType._SecondPermissions
    ):
    Permissions = 0
    Params = "<R><MSG Request=\"Permissions\" Item=\"Macro\" Action=\"Read\" PermissionsType=\"" + str( int ( PermissionsType ) ) + "\" /></R>"
    R, Response = SVILinstruments.Viva.SystemExecute(
        "Permissions",
        Params,
        ""
        )
    if ( R ):
        root = ET.fromstring( Response )
        Permissions = int( root.find( 'MSG' ).get( 'Value' ) )
    return R, Permissions

def GetMacroState():
    State = 0
    Params = "<R><MSG Request=\"State\" Item=\"Macro\" Action=\"Read\" /></R>"
    R, Response = SVILinstruments.Viva.SystemExecute(
        "State",
        Params,
        ""
        )
    if ( R ):
        root = ET.fromstring( Response )
        State = int( root.find( 'MSG' ).get( 'Value' ) )
    return R, State

def SetMacroState(
    nState : int
    ):
    Params = "<R><MSG Request=\"State\" Item=\"Macro\" Action=\"Write\" Value=\"" + str( nState ) + "\" DefaultValue=\"" + str( nState ) + "\" /></R>"
    R = SVILinstruments.Viva.SystemExecute(
        "State",
        Params,
        ""
        )
    return True if ( R[0] ) else False

def GetTwinnedChannel(
    nBoard : int,
    nChannel : int
    ):
    TwinnedChannels = 0
    Params = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" BoardNumber=\"" + str( nBoard ) + "\" VirtualPin=\"Y\" /></R>"
    R, Response = SVILinstruments.Viva.SystemExecute(
        "SetPinMode",
        Params,
        ""
        )
    if ( R ):
        root = ET.fromstring( Response )
        TwinnedChannels = int( root.find( 'MSG' ).get( 'Channel' ) )
    return R, TwinnedChannels

def MoveChannels(
    nChannels : [int],
    Mode : MC_Mode,
    Locked : MC_Locked = MC_Locked.No
    ):
    sSignalsFromProbes = ""
    sChannelsFromProbes = ""
    Ret = False
    sLocked = "Y" if ( Locked == MC_Locked.Yes ) else "N"
    Params = "<R><MSG Mode=\"" + str( MC_ChannelMode._8L_IMM_OC ) + "\" Connect=\"" + ( "Y" if ( Mode == MC_Mode.Add ) else "N" ) + "\" CloseLines=\"0\" ExtLines=\"0\" Locked=\"" + str( int( Locked ) ) + "\" Channels=\""
    for nChannel in nChannels:
        if ( ( Mode == MC_Mode.Add ) and ( Locked != MC_Locked.DontSet ) ):
            Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" LockPin=\"" + sLocked +"\" /></R>"
            R, Response = SVILinstruments.Viva.SystemExecute(
                "SetPinMode",
                Params1,
                ""
                )
            if ( not R ):
                return Ret, sSignalsFromProbes, sChannelsFromProbes
        Params = Params + str( nChannel ) + ";"
    Params = Params + "\" /></R>"
    R, Response = SVILinstruments.Viva.SystemExecute(
        "Connect",
        Params,
        ""
        )
    if ( Mode == MC_Mode.Remove ):
        for nChannel in nChannels:
            if ( Locked != MC_Locked.DontSet ):
                Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" LockPin=\"" + sLocked if ( Locked != MC_Locked.DontSet ) else "" + "\" /></R>"
            else:
                Params1 = "<R><MSG Mode=\"None\" Channel=\"" + str( nChannel ) + "\" /></R>"
            R1, Response1 = SVILinstruments.Viva.SystemExecute(
                "ResetPinMode",
                Params1,
                ""
                )
            if ( not R1 ):
                return Ret, sSignalsFromProbes, sChannelsFromProbes
    if ( not R ):
        return Ret, sSignalsFromProbes, sChannelsFromProbes
    else:
        root = ET.fromstring( Response )
        if ( int( root.find( 'MSG' ).get( 'ConnectStatus' ) ) == 0 ):
            TRACE( "Return Code = " + root.find( 'MSG' ).get( 'ReturnCode' ) + "\n" )
            return Ret, sSignalsFromProbes, sChannelsFromProbes
        else:
            sSignalsFromProbes = ( root.find( 'MSG' ).get( 'Signals', '' ) )
            sChannelsFromProbes = ( root.find( 'MSG' ).get( 'Channels', '' ) )
            Ret = True
            return Ret, sSignalsFromProbes, sChannelsFromProbes

def WriteMessage(
    sMessage : str
    ):
    R = SVILinstruments.Viva.WriteMessage(
        sMessage
        )
    return R

def GetBoardBarcode(
    BoardsBarcodes : [str],
    nBoard : int
    ):
    BoardCode = str( SVILinstruments.Viva.GetSystemProperty( "BoardSubCode" ) )
    PanelCode = str( SVILinstruments.Viva.GetSystemProperty( "BoardCode" ) )
    if ( len( BoardsBarcodes ) > int( nBoard ) ):
        if ( BoardsBarcodes[ nBoard ] != "" ):
            return str( BoardsBarcodes[ nBoard ] )
        elif( BoardCode != "" ):
            return BoardCode
        elif( PanelCode != "" ):
            return PanelCode
        else:
            return ""
    elif( BoardCode != "" ):
        return BoardCode
    elif( PanelCode != "" ):
        return PanelCode
    else:
        return ""

def IsBoardFailed(
    BoardsFailed : [int],
    nBoard : int
    ):
    if ( BoardsFailed == "" ):
        return False
    for BoardFailed in BoardsFailed:
        if ( int( BoardFailed ) == int( nBoard ) ):
            return True
    return False

def SetBoardFailed(
    BoardsFailed : [int],
    nBoard : int,
    fFailed : bool
    ):
    if ( BoardsFailed == "" ):
        BoardsFailed = str( nBoard )
        return
    _BoardsFailed = str( BoardsFailed ).split( "," )
    fFound = False
    fChange = False
    for nBoard in range( len( _BoardsFailed ) ):
        if ( int( _BoardsFailed[ nBoard ] ) == int( nBoard ) ):
            if ( not fFailed ):
                _BoardsFailed[ nBoard ] = str( 0 )
                fChange = True
            fFound = True
            break
    if ( fFound and not fChange ):
        return
    BoardsFailed = _BoardsFailed
    if ( not fFound ):
        BoardsFailed.append( str( nBoard ) )

def WriteBoardsFailed(
    BoardsFailed : [int],
    fWrite : bool = False
    ):
    _BoardsFailed = BoardsFailed
    BoardsFailed = ""
    for BoardFailed in BoardsFailed:
        BoardsFailed += str( BoardFailed ) if ( BoardsFailed == "" ) else "," + str( BoardFailed )
    if ( fWrite ):
        if ( BoardsFailed != "" ):
            SetGlobalVariable( GVParallelMode._sBoardsFailed, BoardsFailed )

def GetSectionComponents(
    sSectionName : str
    ):
    R, sComponentsName = SVILinstruments.Viva.GetSectionComponents( sSectionName, None )
    return R, sComponentsName

def GetComponentMacros(
    sComponent : str
    ):
    R, sMacrosName, nMacrosID = SVILinstruments.Viva.GetComponentMacros( sComponent, None, None )
    return R, sMacrosName, nMacrosID

def GetMacroIDLabels(
    sComponent : str,
    nMacroID : int
    ):
    R, sLabelsName = SVILinstruments.Viva.GetMacroIDLabels( sComponent, "", -1, nMacroID, None )
    return R, sLabelsName

def SetEmulationTime(
    nTime : int # us
    ):
    R = SVILinstruments.Viva.SetEmulationTime( nTime )
    return R

def GetLedSensorInfo(
    nSensorPin : int
    ):
    Params = int( nSensorPin )
    R, Response = SVILinstruments.Viva.SystemExecuteRAW(
        "GetLedSensorInfo",
        Params,
        ""
        )
    return R, Response

def GetLoopCounter():
    R, Response = SVILinstruments.Viva.TestExecuteRAW(
        "GetLoopCounter",
        None,
        ""
        )
    return R, Response

# ----------------------------
# ---------  ACLAM  ----------
# ----------------------------

def ACLAM_GetVersions():
    R, FW_version, SW_Version = SVILinstruments.Aclam.GetVersions( "", "" )
    return R, FW_version, SW_Version

def ACLAM_Execute(
    XmlRequest : str
    ):
    R, Response = SVILinstruments.Aclam.Execute(
        XmlRequest,
        ""
        )
    return R, Response

def ACLAM_ForceMovement(
    MesTypeV : float,
    MesTypeI : float,
    RangeV : float,
    RangeI : float
    ):
    R = SVILinstruments.Aclam.ForceMovement(
        MesTypeV,
        MesTypeI,
        RangeV,
        RangeI
        )
    return R

def SetACLAMFlyFixture(
    bFixtureFlying : bool = False
    ):
    R = SVILinstruments.Aclam.SetACLAMFlyFixture( bFixtureFlying )
    return R

def ReadNewFemtoInstalled():
    R, Response = SVILinstruments.Viva.ReadNewFemtoInstalled( "" )
    if ( R ):
        root = ET.fromstring( Response )
        sInstalled = str( root.find( 'MSG' ).get( 'Value' ) )
    return R, sInstalled

def ReadScaFPType():
    R, Response = SVILinstruments.Viva.ReadScaFPType( "" )
    if ( R ):
        root = ET.fromstring( Response )
        sType = str( root.find( 'MSG' ).get( 'Value' ) )
    return R, sType

# ----------------------------
# --------  RAM_EXT  ---------
# ----------------------------

def RAM_EXT_Set(
    Data : [float],
    NOMEDISP : str = "ACLAM",
    STARTADDR : int = 0,
    NDATA : int = 0,
    SIZE : SIZE = SIZE.S32,
    TYPE : TYPE = TYPE.INT
    ):
    R = SVILinstruments.RamExt.Set(
        Data,
        NOMEDISP,
        STARTADDR,
        NDATA,
        SIZE,
        TYPE
        )
    return R

def RAM_EXT_Get(
    NOMEDISP : str = "ACLAM",
    STARTADDR : int = 0,
    NDATA : int = 0,
    SIZE : SIZE = SIZE.S32,
    TYPE : TYPE = TYPE.INT
    ):
    R, Data = SVILinstruments.RamExt.Get(
        None,
        NOMEDISP,
        STARTADDR,
        NDATA,
        SIZE,
        TYPE
        )
    return R, Data

# ----------------------------
# ----------  GND  -----------
# ----------------------------

def GND_Clear():
    R = SVILinstruments.Gnd.Clear()
    return R

def GND_Set(
    OUT : int = GNDLINE.NONE,
    SOURCE : SOURCE = SOURCE.GND,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Gnd.Set(
        OUT,
        SOURCE,
        TIME_RELE
        )
    return R

# ----------------------------
# ----------  DRA  -----------
# ----------------------------

def DRA_Set(
    V : float = 0,
    I : float = 0.01,
    OFFSET : float = 0,
    DRRANGE : DRRANGE = DRRANGE.AUTO,
    MODE : DRAMODE = DRAMODE.V,
    VNEG : float = 0,
    FREQ : float = 1000,
    TIME : float = 0.001,
    WAVE : WAVE = WAVE.DC,
    START : DRSTART = DRSTART.IMMEDIATE,
    N_SAMPLE : float = 1000,
    ADDR : float = 0,
    DELAY_TRIG : float = 0.00000002,
    EVOLUTION : float = 1,
    COUPLING : COUPLING = COUPLING.DC,
    OUT : DRAOUT = DRAOUT.NONE,
    DOMAIN : DOMAIN = DOMAIN.INSTRUMENT,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Dra.Set(
        V,
        I,
        OFFSET,
        DRRANGE,
        MODE,
        VNEG,
        FREQ,
        TIME,
        WAVE,
        START,
        N_SAMPLE,
        ADDR,
        DELAY_TRIG,
        EVOLUTION,
        COUPLING,
        OUT,
        DOMAIN,
        TIME_RELE
        )
    return R

def DRA_Clear():
    R = SVILinstruments.Dra.Clear()
    return R

# ----------------------------
# ----------  DRB  -----------
# ----------------------------

def DRB_Set(
    V : float = 0,
    I : float = 0.01,
    OFFSET : float = 0,
    DRRANGE : DRRANGE = DRRANGE.AUTO,
    MODE : DRBMODE = DRBMODE.V,
    SENSE : DRBSENSE = DRBSENSE.INT,
    FREQ : float = 1000,
    TIME : float = 0.001,
    WAVE : WAVE = WAVE.DC,
    START : DRSTART = DRSTART.IMMEDIATE,
    N_SAMPLE : float = 1000,
    ADDR : float = 0,
    DELAY_TRIG : float = 0.00000002,
    EVOLUTION : float = 1,
    IN : IN = IN.DAC,
    OUT : DRBOUT = DRBOUT.NONE,
    DOMAIN : DOMAIN = DOMAIN.INSTRUMENT,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Drb.Set(
        V,
        I,
        OFFSET,
        DRRANGE,
        MODE,
        SENSE,
        FREQ,
        TIME,
        WAVE,
        START,
        N_SAMPLE,
        ADDR,
        DELAY_TRIG,
        EVOLUTION,
        IN,
        OUT,
        DOMAIN,
        TIME_RELE
        )
    return R

def DRB_Clear():
    R = SVILinstruments.Drb.Clear()
    return R

# ----------------------------
# ----------  DRC  -----------
# ----------------------------

def DRC_Set(
    VOLTAGE : float = 0,
    CURRENT : float = 0.01,
    OUT : DRCOUT = DRCOUT.NONE,
    START : DRCSTART = DRCSTART.IMMEDIATE
    ):
    R = SVILinstruments.Drc.Set(
        VOLTAGE,
        CURRENT,
        OUT,
        START
        )
    return R

def DRC_Clear():
    R = SVILinstruments.Drc.Clear()
    return R

# ----------------------------
# ----------  IMM  -----------
# ----------------------------

def IMM_Set(
    MEAS_V : MEAS_V = MEAS_V.BUFF_AUTO,
    MEAS_I : MEAS_I = MEAS_I.BUFF_AUTO,
    RANGE_V : RANGE_V = RANGE_V._10V,
    RANGE_I : RANGE_I = RANGE_I.NONE,
    MODE : MODE = MODE.NORMAL,
    N_SAMPLE : float = 1000,
    FREQ : float = 10000000,
    ADDR : float = 0,
    START : IMMSTART = IMMSTART.IMMEDIATE,
    TRIG_OUT : TRIG_OUT = TRIG_OUT.NONE,
    DELAY_TRIG : float = 0.00000002,
    EVOLUTION : float = 1,
    INP_VPOS : INP_VPOS = INP_VPOS.OPEN,
    INP_VNEG : INP_VNEG = INP_VNEG.OPEN,
    INP_I_V2 : INP_I_V2 = INP_I_V2.NONE,
    SENSE_I : SENSE_I = SENSE_I.INTERNAL,
    REF_I : REF_I = REF_I.GND,
    FILTER : FILTER = FILTER.NONE,
    ORDER : float = 3,
    FT1 : float = 0,
    FT2 : float = 0,
    DOMAIN : DOMAIN = DOMAIN.INSTRUMENT
    ):
    R = SVILinstruments.IMM.Set(
        MEAS_V,
        MEAS_I,
        RANGE_V,
        RANGE_I,
        MODE,
        N_SAMPLE,
        FREQ,
        ADDR,
        START,
        TRIG_OUT,
        DELAY_TRIG,
        EVOLUTION,
        INP_VPOS,
        INP_VNEG,
        INP_I_V2,
        SENSE_I,
        REF_I,
        FILTER,
        ORDER,
        FT1,
        FT2,
        DOMAIN
        )
    return R

def IMM_SetNoMoveFP(
    MEAS_V : MEAS_V = MEAS_V.BUFF_AUTO,
    MEAS_I : MEAS_I = MEAS_I.BUFF_AUTO,
    RANGE_V : RANGE_V = RANGE_V._10V,
    RANGE_I : RANGE_I = RANGE_I.NONE,
    MODE : MODE = MODE.NORMAL,
    N_SAMPLE : float = 1000,
    FREQ : float = 10000000,
    ADDR : float = 0,
    START : IMMSTART = IMMSTART.IMMEDIATE,
    TRIG_OUT : TRIG_OUT = TRIG_OUT.NONE,
    DELAY_TRIG : float = 0.00000002,
    EVOLUTION : float = 1,
    INP_VPOS : INP_VPOS = INP_VPOS.OPEN,
    INP_VNEG : INP_VNEG = INP_VNEG.OPEN,
    INP_I_V2 : INP_I_V2 = INP_I_V2.NONE,
    SENSE_I : SENSE_I = SENSE_I.INTERNAL,
    REF_I : REF_I = REF_I.GND,
    FILTER : FILTER = FILTER.NONE,
    ORDER : float = 3,
    FT1 : float = 0,
    FT2 : float = 0,
    DOMAIN : DOMAIN = DOMAIN.INSTRUMENT,
    MOVE : MOVEFP = MOVEFP.OFF
    ):
    R = SVILinstruments.IMM.SetNoMoveFP(
        MEAS_V,
        MEAS_I,
        RANGE_V,
        RANGE_I,
        MODE,
        N_SAMPLE,
        FREQ,
        ADDR,
        START,
        TRIG_OUT,
        DELAY_TRIG,
        EVOLUTION,
        INP_VPOS,
        INP_VNEG,
        INP_I_V2,
        SENSE_I,
        REF_I,
        FILTER,
        ORDER,
        FT1,
        FT2,
        DOMAIN,
        MOVE
        )
    return R

def IMM_Meas(
    MEAS : MEAS = MEAS.BUFFER_V,
    N_SAMPLE : float = 1,
    ADDR : float = 0
    ):
    R, OutBuf = SVILinstruments.IMM.Meas(
        None,
        MEAS,
        N_SAMPLE,
        ADDR
        )
    return R, OutBuf

def IMM_Clear():
    R = SVILinstruments.IMM.Clear()
    return R

# ----------------------------
# ---------  ANABUS  ---------
# ----------------------------

def ANABUS_Set(
    CHN : float = 0,
    LINEE : int = ELINE.NONE,
    CHN_SET : CHN_SET = CHN_SET.LEAVE,
    L_MODE : L_MODE = L_MODE.IMM,
    BLINE : int = ELINE.NONE,
    BL_MODE : L_MODE = L_MODE.IMM,
    PLINE : int = ELINE.NONE,
    PL_MODE : L_MODE = L_MODE.IMM,
    CLINE : int = ELINE.NONE,
    CL_MODE : CL_MODE = CL_MODE.IMM,
    ALL : ALL = ALL.OFF,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Anabus.Set(
        CHN,
        LINEE,
        CHN_SET,
        L_MODE,
        BLINE,
        BL_MODE,
        PLINE,
        PL_MODE,
        CLINE,
        CL_MODE,
        ALL,
        TIME_RELE
        )
    return R

# ----------------------------
# ----------  CAP  -----------
# ----------------------------

def CAP_Meas(
    CH1 : float = 0,
    CH2 : float = 0,
    CH3 : float = 0,
    CH4 : float = 0,
    MODE : CAPMODE = CAPMODE.DC_ACTIVE,
    WIRE : WIRE = WIRE._2WIRE,
    TIME_FREQ : float = 0,
    VOLT : float = 0,
    QUALITY : float = 0,
    NOISE : float = 0,
    R_SER : float = 0,
    R_PAR : float = 0,
    RESGUA_CH1 : float = 0,
    RESGUA_CH2 : float = 0,
    CAPGUA_CH1 : float = 0,
    CAPGUA_CH2 : float = 0
    ):
    R, Val = SVILinstruments.Cap.Meas(
        0,
        CH1,
        CH2,
        CH3,
        CH4,
        MODE,
        WIRE,
        TIME_FREQ,
        VOLT,
        QUALITY,
        NOISE,
        R_SER,
        R_PAR,
        RESGUA_CH1,
        RESGUA_CH2,
        CAPGUA_CH1,
        CAPGUA_CH2
        )
    return R, Val

# ----------------------------
# --------  CHANNEL  ---------
# ----------------------------

def CHANNEL_Set(
    CHN : float = 0,
    LINEE : int = ELINE.NONE,
    MODE : CHMODE = CHMODE._4L_IMM,
    BLINEE : BLINEE = BLINEE.CLOSE,
    ALL : ALL = ALL.OFF,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Channel.Set(
        CHN,
        LINEE,
        MODE,
        BLINEE,
        ALL,
        TIME_RELE
        )
    return R

def CHANNEL_Clear():
    R = SVILinstruments.Channel.Clear()
    return R

# ----------------------------
# ---------  DISCAP  ---------
# ----------------------------

def DISCAP_Set(
    CH1 : int = 0,
    CH2 : int = 0,
    CURRENT : float = 0.02,
    MODE : DISCAPMODE = DISCAPMODE.DRC_OFF
    ):
    R = SVILinstruments.Discap.Set(
        CH1,
        CH2,
        CURRENT,
        MODE
        )
    return R

# ----------------------------
# --------  CONTACT  ---------
# ----------------------------

def CONTACT_Meas(
    FROM : float = 0,
    TO : float = 0,
    MODE : CTCMODE = CTCMODE.EXECUTE,
    OHM : float = 1000000,
    TIME : float = 0,
    VOLT : float = 1.2
    ):
    R = SVILinstruments.Contact.Meas(
        FROM,
        TO,
        MODE,
        OHM,
        TIME,
        VOLT
        )
    return R

def CONTACT_Get(
    TYPE : CTCTYPE = CTCTYPE.FAIL_CH
    ):
    R, Data = SVILinstruments.Contact.Get(
        [],
        TYPE
        )
    return R, Data

# ----------------------------
# ---------  FLASH  ----------
# ----------------------------

def FLASH_Set(
    SEGMENT : SEGMENT = SEGMENT.VECT1,
    OFFSET : int = 0,
    N_SAMPLE : int = 0,
    CONVERSION : CONVERSION = CONVERSION.NONE,
    Data : [float] = []
    ):
    R = SVILinstruments.Flash.Set(
        Data,
        SEGMENT,
        OFFSET,
        N_SAMPLE,
        CONVERSION
        )
    return R

# ----------------------------
# --------  IOV5LOAD  --------
# ----------------------------

def IOV5LOAD_Clear(
    BOARD : float = 0
    ):
    R = SVILinstruments.IOV5Load.Clear(
        BOARD
        )
    return R

def IOV5LOAD_Set(
    BOARD : float = 0,
    OEB : OEB = OEB.ON
    ):
    R = SVILinstruments.IOV5Load.Set(
        BOARD,
        OEB
        )
    return R

def IOV5LOAD_OUTASet(
    OUT : float = 0,
    STATUS : OUT_A_STATUS = OUT_A_STATUS.NONE
    ):
    R = SVILinstruments.IOV5Load.OUT_A_Set(
        OUT,
        STATUS
        )
    return R

def IOV5LOAD_OUTANASet(
    ANALOG : float = 0,
    V : float = 0
    ):
    R = SVILinstruments.IOV5Load.OUT_ANA_Set(
        ANALOG,
        V
        )
    return R

def IOV5LOAD_OUTBSet(
    OUT : float = 0,
    STATUS : OUT_B_STATUS = OUT_B_STATUS.NONE
    ):
    R = SVILinstruments.IOV5Load.OUT_B_Set(
        OUT,
        STATUS
        )
    return R

def IOV5LOAD_OUTLoadSet(
    LOAD : float = 0,
    OHM : float = 0,
    ON_OFF : OUTLOAD_ONOFF = OUTLOAD_ONOFF.OFF
    ):
    R = SVILinstruments.IOV5Load.OUT_LOAD_Set(
        LOAD,
        OHM,
        ON_OFF
        )
    return R

def IOV5LOAD_OUTOptoSet(
    OUT : float = 0,
    STATUS : OUTOPTO_STATUS = OUTOPTO_STATUS.OFF
    ):
    R = SVILinstruments.IOV5Load.OUT_OPTO_Set(
        OUT,
        STATUS
        )
    return R

# ----------------------------
# ----------  LINE  ----------
# ----------------------------

def LINE_Clear():
    R = SVILinstruments.Line.Clear()
    return R

def LINE_Set(
    OUT_LINES : OUT_LINES = OUT_LINES.CLOSE,
    MODE : LINEMODE = LINEMODE._4L,
    INT_LINES : INT_LINES = INT_LINES.ALL,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Line.Set(
        OUT_LINES,
        MODE,
        INT_LINES,
        TIME_RELE
        )
    return R

# ----------------------------
# --------  LINE_EXT  --------
# ----------------------------

def LINEEXT_Clear():
    R = SVILinstruments.LineExt.Clear()
    return R

def LINEEXT_Set(
    OUT : float = 0,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.LineExt.Set(
        OUT,
        TIME_RELE
        )
    return R

# ----------------------------
# --------  MONITOR  ---------
# ----------------------------

def MONITOR_Set(
    OUT : MON_OUT = MON_OUT.IDRA
    ):
    R = SVILinstruments.Monitor.Set(
        OUT
        )
    return R

# ----------------------------
# -------  POWERSCAN  --------
# ----------------------------

def POWERSCAN_Clear():
    R = SVILinstruments.Powerscan.Clear()
    return R

def POWERSCAN_Set(
    BOARD : int = 0,
    MODE : POS_MODE = POS_MODE.MODE_0,
    OEB : OEB = OEB.ON,
    SIGNAL : int = 0,
    S20BDLINE : int = 0,
    PWRBDLINE : int = 255,
    CROSSLINE : int = 255,
    MERGEPWRS20LINE : int = 0
    ):
    R = SVILinstruments.Powerscan.Set(
        BOARD,
        MODE,
        OEB,
        SIGNAL,
        S20BDLINE,
        PWRBDLINE,
        CROSSLINE,
        MERGEPWRS20LINE
        )
    return R

# ----------------------------
# ----------  PULL  ----------
# ----------------------------

def PULL_Clear():
    R = SVILinstruments.Pull.Clear()
    return R

def PULL_Set(
    VAL : VAL = VAL.R_NONE,
    SOURCE : PUL_SOURCE = PUL_SOURCE.NONE,
    TIME_RELE : TIME_RELE = TIME_RELE.ON
    ):
    R = SVILinstruments.Pull.Set(
        VAL,
        SOURCE,
        TIME_RELE
        )
    return R

# ----------------------------
# -----------  HW  -----------
# ----------------------------

def RD_HW_Meas(
    TYPE : RD_TYPE = RD_TYPE.RT
    ):
    R, Result = SVILinstruments.HW.RD_HW_Meas(
        0,
        TYPE
        )
    return R, Result

def WR_HW_Set(
    TYPE : WR_TYPE = WR_TYPE.OC,
    DATA : float = 0
    ):
    R = SVILinstruments.HW.WR_HW_Set(
        TYPE,
        DATA
        )
    return R

# ----------------------------
# ----------  RES  -----------
# ----------------------------

def RES_Meas(
    VAL : float = 1000,
    CH1 : float = 0,
    CH2 : float = 0,
    CH3 : float = 0,
    CH4 : float = 0,
    MODE : RES_MODE = RES_MODE.DC_ACTIVE,
    WIRE : WIRE = WIRE._2WIRE,
    TIME_FREQ : float = 0,
    VOLT : float = 0,
    QUALITY : float = 10,
    NOISE : float = 1,
    C_SER : float = 0,
    C_PAR : float = 0,
    L_SER : float = 0,
    L_PAR : float = 0,
    RESGUA_CH1 : float = 0,
    RESGUA_CH2 : float = 0,
    CAPGUA_CH1 : float = 0,
    CAPGUA_CH2 : float = 0
    ):
    R, Result = SVILinstruments.Res.Meas(
        0,
        VAL,
        CH1,
        CH2,
        CH3,
        CH4,
        MODE,
        WIRE,
        TIME_FREQ,
        VOLT,
        QUALITY,
        NOISE,
        C_SER,
        C_PAR,
        L_SER,
        L_PAR,
        RESGUA_CH1,
        RESGUA_CH2,
        CAPGUA_CH1,
        CAPGUA_CH2
        )
    return R, Result

# ----------------------------
# ----------  SCAY  ----------
# ----------------------------

def SCAY_Clear(
    BOARD : float = 0
    ):
    R = SVILinstruments.ScaY.Clear(
        BOARD
        )
    return R

def SCAY_Set(
    BOARD : float = 0,
    MODE : SCY_MODE = SCY_MODE.MODE_0,
    OEB : OEB = OEB.ON
    ):
    R = SVILinstruments.ScaY.Set(
        BOARD,
        MODE,
        OEB
        )
    return R

# ----------------------------
# --------  COUNTER  ---------
# ----------------------------

def COUNTER_Set(
    MODE : CNT_MODE = CNT_MODE.COUNT,
    VAL : float = 0,
    AVERAGE : float = 1,
    GATE : float = 0,
    DOMAIN : DOMAIN = DOMAIN.INSTRUMENT,
    INP_A : INP_A = INP_A.NONE,
    INP_B : INP_B = INP_B.NONE,
    LEVEL_A : float = 0,
    LEVEL_B : float = 0,
    SLOPE_A : SLOPE = SLOPE.POS,
    SLOPE_B : SLOPE = SLOPE.POS,
    RANGE_A : CNT_RANGE = CNT_RANGE._10V,
    RANGE_B : CNT_RANGE = CNT_RANGE._10V,
    START : CNT_START = CNT_START.IMMEDIATE,
    DELAY_TRIG : float = 0.00000002,
    TRIG_OUT : TRIG_OUT = TRIG_OUT.NONE,
    HISTERESIS : HISTERESIS = HISTERESIS.AUTO
    ):
    R = SVILinstruments.Counter.Set(
        MODE,
        VAL,
        AVERAGE,
        GATE,
        DOMAIN,
        INP_A,
        INP_B,
        LEVEL_A,
        LEVEL_B,
        SLOPE_A,
        SLOPE_B,
        RANGE_A,
        RANGE_B,
        START,
        DELAY_TRIG,
        TRIG_OUT,
        HISTERESIS
        )
    return R

def COUNTER_Meas():
    R, Result = SVILinstruments.Counter.Meas( 0 )
    return R, Result

def COUNTER_Clear():
    R = SVILinstruments.Counter.Clear()
    return R

# ----------------------------
# ---------  SHORT  ----------
# ----------------------------

def SHORT_Get(
    TYPE : SHT_TYPE = SHT_TYPE.FAIL_CH
    ):
    R, Data = SVILinstruments.Short.Get(
        [],
        TYPE
        )
    return R, Data

def SHORT_Meas(
    FROM : float = 0,
    TO : float = 0,
    MODE : SHT_MODE = SHT_MODE.EXECUTE,
    OHM : float = 6,
    TIME : float = 0,
    VOLT : float = 0.6
    ):
    R = SVILinstruments.Short.Meas(
        FROM,
        TO,
        MODE,
        OHM,
        TIME,
        VOLT
        )
    return R

# ----------------------------
# ---------  SCAEVO  ---------
# ----------------------------

def SCAEVO_Set(
    BOARD : int = 0,
    MODE : SCE_MODE = SCE_MODE.MODE_F,
    S20BDLINE : int = 255,
    ODDEVEN : int = 0,
    MATRIX_EXT : int = 0,
    SHUNT : float = 0xFFFFFFFFFFFFFFFF
    ):
    R = SVILinstruments.ScaEvo.Set(
        BOARD,
        MODE,
        S20BDLINE,
        ODDEVEN,
        MATRIX_EXT,
        SHUNT
        )
    return R

def SCAEVO_Clear(
    BOARD : int = 0
    ):
    R = SVILinstruments.ScaEvo.Clear(
        BOARD
        )
    return R

# ----------------------------
# -----------  PW  -----------
# ----------------------------

def PW_Set(
    PW : int = 1,
    V : float = 0,
    I : float = 0.5,
    State : STATE = STATE.OFF,
    Mode : PW_MODE = PW_MODE.INT,
    Sense : SENSE = SENSE.OFF,
    Delay : float = 100,
    Operation : OPERATION = OPERATION.SET
    ):
    R = SVILinstruments.PW.Set(
        PW,
        V,
        I,
        State,
        Mode,
        Sense,
        Delay,
        Operation
        )
    return R

def PW_Meas(
    PW : int = 1,
    Measure : MEASURE = MEASURE.V,
    Mode : PW_MODE = PW_MODE.INT
    ):
    R, Result = SVILinstruments.PW.Meas(
        0,
        PW,
        Measure,
        Mode
        )
    return R, Result

def PW_Clear():
    R = SVILinstruments.PW.Clear()
    return R

def PW_Execute(
    Service : str,
    Params : object
    ):
    R, Response = SVILinstruments.PW.Execute(
        Service,
        Params
        )
    return R, Response

def PW_ReadStatusPWS(
    PW : int = 1,
    Opz : READSTATUS = READSTATUS.PWS_O3_STATUS
    ):
    R, Response = SVILinstruments.PW.ReadStatusPWS(
        PW,
        Opz
        )
    return R, Response

# ----------------------------
# -----------  POWER  --------
# ----------------------------

def POWER_Set(
    ConnectionMode : POWER_CONN = POWER_CONN.FIXED,
    PWSelect : POWER_SELECT = POWER_SELECT.AUTO,
    VoltageV : float = 0,
    SupplyP : int = 0,
    SupplyN : int = 0,
    Current : float = 0,
    Delay : float = 0,
    ApplyMode : APPLY_MODE = APPLY_MODE.ON,
    ApplySense : APPLY_SENSE = APPLY_SENSE.OFF
    ):
    R = SVILinstruments.POWER.Set(
        ConnectionMode,
        PWSelect,
        VoltageV,
        SupplyP,
        SupplyN,
        Current,
        Delay,
        ApplyMode,
        ApplySense
        )
    return R

def POWER_Measure_V(
    PWSelect : POWER_SELECT = POWER_SELECT.AUTO,
    TolP : float = 0,
    TolN : float = 0,
    SupplyP : int = 0,
    SupplyN : int = 0,
    ValueV : float = 0
    ):
    R, Result = SVILinstruments.POWER.Measure_V(
        0,
        PWSelect,
        TolP,
        TolN,
        SupplyP,
        SupplyN,
        ValueV
        )
    return R, Result

def POWER_Measure_I(
    PWSelect : POWER_SELECT = POWER_SELECT.AUTO,
    SupplyP : float = 0,
    SupplyN : float = 0,
    CurrMin : float = 0,
    CurrMax : float = 0
    ):
    R, Result = SVILinstruments.POWER.Measure_I(
        0,
        PWSelect,
        SupplyP,
        SupplyN,
        CurrMin,
        CurrMax
        )
    return R, Result

def POWER_Clear():
    R = SVILinstruments.POWER.Clear()
    return R

def POWER_Execute(
    Service : str,
    Params : object
    ):
    R, Response = SVILinstruments.POWER.Execute(
        Service,
        Params
        )
    return R, Response

def POWER_Remove(
    PWSelect : POWER_SELECT = POWER_SELECT.AUTO,
    SupplyP : int = 0,
    SupplyN : int = 0
    ):
    R = SVILinstruments.POWER.Remove(
        PWSelect,
        SupplyP,
        SupplyN
        )
    return R

# ----------------------------
# --------  GUAPOINT  --------
# ----------------------------

def GUAPOINT_Set(
    GuardChannels : [float] = []
    ):
    R = SVILinstruments.Guapoint.Set(
        GuardChannels
        )
    return R

def GUAPOINT_Clear():
    R = SVILinstruments.Guapoint.Clear()
    return R

# ----------------------------
# ---------  LOGIC  ----------
# ----------------------------

def LOGIC_Set(
    CH_1 : CH = CH.IL,
    CH_2 : CH = CH.IL,
    CH_3 : CH = CH.IL,
    CH_4 : CH = CH.IL,
    MODE : BURST = BURST.OFF
    ):
    R = SVILinstruments.Logic.Set(
        CH_1,
        CH_2,
        CH_3,
        CH_4,
        MODE
        )
    return R

def LOGIC_Meas():
    R, OutBuff = SVILinstruments.Logic.Meas( [] )
    return R, OutBuff

def LOGIC_LevelSet(
    IH : float = 2.4,
    IL : float = 0,
    OH : float = 1.2,
    OL : float = 0.8
    ):
    R = SVILinstruments.Logic.LevelSet(
        IH,
        IL,
        OH,
        OL
        )
    return R

def LOGIC_ModeSet(
    OUT_CH1 : OUT_CH1 = OUT_CH1.NONE,
    OUT_CH2 : OUT_CH2 = OUT_CH2.NONE,
    OUT_CH3 : OUT_CH3 = OUT_CH3.NONE,
    OUT_CH4 : OUT_CH4 = OUT_CH4.NONE,
    INP_CH1 : INP_CH1_3 = INP_CH1_3.DSP,
    INP_CH2 : INP_CH2_4 = INP_CH2_4.DSP,
    INP_CH3 : INP_CH1_3 = INP_CH1_3.DSP,
    INP_CH4 : INP_CH2_4 = INP_CH2_4.DSP,
    PLL_FREQ : float = 500000,
    N_STEP : float = 0,
    PERIOD : float = 0.00005
    ):
    R = SVILinstruments.Logic.ModeSet(
        OUT_CH1,
        OUT_CH2,
        OUT_CH3,
        OUT_CH4,
        INP_CH1,
        INP_CH2,
        INP_CH3,
        INP_CH4,
        PLL_FREQ,
        N_STEP,
        PERIOD
        )
    return R

def LOGIC_Clear():
    R = SVILinstruments.Logic.Clear()
    return R

def LOGIC_LevelClear():
    R = SVILinstruments.Logic.LevelClear()
    return R

def LOGIC_ModeClear():
    R = SVILinstruments.Logic.ModeClear()
    return R

# ----------------------------
# --------  FEMTO  -----------
# ----------------------------

def FEMTO_Read(
    Value : [float] = 0,
    Channel : [float] = 0,
    Mode : [FMT_MODE] = FMT_MODE._ModeNone,
    ToDo : [TODO] = TODO._FemtoNone,
    ReadRecycles : int = 1
    ):
    R, Read = SVILinstruments.Femto.Read(
        None,
        Value,
        Channel,
        Mode,
        ToDo,
        ReadRecycles
        )
    return R, Read

# ----------------------------
# ----------  IPY  -----------
# ----------------------------

def IPY_ExecuteCode(
    jsonI : str = "",
    myCode : str = ""
    ):
    R, jsonO = SVILinstruments.Ipy.ExecuteCode(
        jsonI,
        myCode,
        ""
        )
    return R, jsonO
    
# ----------------------------
# --------  ICTCTRL  ---------
# ----------------------------

def ICTCTRL_Name():
    Name = SVILinstruments.IctCtrl.Name
    return Name

def ICTCTRL_EnableEmulation(
    Enable : bool
    ):
    R = SVILinstruments.IctCtrl.EnableEmulation( Enable )
    return R

def ICTCTRL_Init(
    IOHandle : int = -1
    ):
    R = SVILinstruments.IctCtrl.Init( IOHandle )
    return R

def ICTCTRL_Term():
    R = SVILinstruments.IctCtrl.Term()
    return R

def ICTCTRL_Clear():
    R = SVILinstruments.IctCtrl.Clear()
    return R

def ICTCTRL_Measure(
    Head : int,    # 0-7
    Module : int,  # 0-8, 8=all
    N_SAMPLES : int = 1
    ):
    R, OutBuff = SVILinstruments.IctCtrl.Measure(
        None,
        Head,
        Module,
        N_SAMPLES
        )
    return R, OutBuff

def ICTCTRL_Execute(
    Service : str,
    Params : object
    ):
    R, Response = SVILinstruments.IctCtrl.ExecuteRAW(
        Service,
        Params
        )
    return R, Response

# ------------------------------------------
# GUI - Viva Dynamic Terminal
# ------------------------------------------

def VDT_Write(
    Message : str = ""
    ):
    R = SVILinstruments.VDT.Write( Message )
    return R

def VDT_Pause(
    Message : str = ""
    ):
    R = SVILinstruments.VDT.Pause( Message )
    return R

def VDT_Execute(
    Service : str,
    Params : str = "",
    Response : str = ""
    ):
    R = SVILinstruments.VDT.Execute( Service, Params, Response )
    return R

# ----------------------------
# -------- LedSensor ---------
# ----------------------------

def LEDSENSOR_Name():
    Name = SVILinstruments.LedSensor.Name
    return Name

def LEDSENSOR_Execute(
    Service : str,
    Params : object
    ):
    R, Response = SVILinstruments.LedSensor.Execute(
        Service,
        Params
        )
    return R, Response

