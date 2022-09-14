# Version Info. Do not modify
# Version=3.0
# Version Info. Do not modify
import sys

from FNtools import *

def LeakTest( PinPositive, PinNegative, Max, Min, ValueCurrent, ValueVolt, Recycle, MeasTime, PreTime, Quality ):
    ClearReport()
    OSC_Disable()
    
    if( Recycle < 1 ):
        Recycle = 1
    elif( Recycle > 1000 ):
        Recycle = 1000
    Quality_Meas = QualityCalc( Quality )
    for index in range( 0, int( Recycle ) ):      # recycle on error
        MeasI = MEASURE_LEAK( ValueVolt, ValueCurrent, PinPositive, PinNegative, PreTime, MeasTime, Max, Min, Quality_Meas )
        if( MeasI < Max ):
            break
    MeasReport = ( ( MeasI * 1000000 * 10000 ) + 0.5 ) / 10000
    MeasReport1 = ValueVolt / MeasReport
    if( MeasI > Max ):
        WriteReport( str( MeasReport ) + 'uA' )
        WriteReport( str( MeasReport1 ) + 'MOhm' )
    
    return ScriptResult.TestContinue

def QualityCalc( Quality ):
    Quality_Meas = Quality / 10
    
    if( Quality_Meas < 1 ):
        Quality_Meas = 1
    elif( Quality_Meas < 2 ):
        Quality_Meas = 2
    elif( Quality_Meas < 3 ):
        Quality_Meas = 3
    elif( Quality_Meas < 4):
        Quality_Meas = 4
    elif( Quality_Meas < 5 ):
        Quality_Meas = 5
    elif( Quality_Meas < 6 ):
        Quality_Meas = 6
    elif( Quality_Meas < 7 ):
        Quality_Meas = 7
    elif( Quality_Meas < 8 ):
        Quality_Meas = 8
    elif( Quality_Meas < 9 ):
        Quality_Meas = 9
    elif( Quality_Meas < 10 ):
        Quality_Meas = 10
    
    return Quality_Meas

def CurrRange( CurrentRangeSel ):
    # CurrentRangeSel = CurrentRangeSel * 1.5;    # maggioro il valore da misurare del 50% per stare comodi nella scala di misura
    if( CurrentRangeSel > 0 ):
        if( CurrentRangeSel < 0.000001 ):
            nCurrentRange = RANGE_I._1UADC      # 69
        elif( CurrentRangeSel <= 0.0000025 ):
            nCurrentRange = RANGE_I._2P5UADC    # 68
        elif( CurrentRangeSel <= 0.000005 ):
            nCurrentRange = RANGE_I._5UADC      # 67
        elif( CurrentRangeSel <= 0.00001 ):
            nCurrentRange = RANGE_I._10UADC     # 66
        elif( CurrentRangeSel <= 0.000025 ):
            nCurrentRange = RANGE_I._25UADC     # 65
        elif( CurrentRangeSel <= 0.00005 ):
            nCurrentRange = RANGE_I._50UADC     # 64
        elif( CurrentRangeSel <= 0.0001 ):
            nCurrentRange = RANGE_I._100UADC    # 50
        elif( CurrentRangeSel <= 0.00025 ):
            nCurrentRange = RANGE_I._250UADC    # 49
        elif( CurrentRangeSel <= 0.0005 ):
            nCurrentRange = RANGE_I._500UADC    # 48
        elif( CurrentRangeSel <= 0.001 ):
            nCurrentRange = RANGE_I._1MADC      # 34
        elif( CurrentRangeSel <= 0.0025 ):
            nCurrentRange = RANGE_I._2P5MADC    # 33
        elif( CurrentRangeSel <= 0.005 ):
            nCurrentRange = RANGE_I._5MADC      # 32
        elif( CurrentRangeSel <= 0.01 ):
            nCurrentRange = RANGE_I._10MADC     # 18
        elif( CurrentRangeSel <= 0.025 ):
            nCurrentRange = RANGE_I._25MADC     # 17
        elif( CurrentRangeSel <= 0.05 ):
            nCurrentRange = RANGE_I._50MADC     # 16
        elif( CurrentRangeSel <= 0.01 ):
            nCurrentRange = RANGE_I._100MADC    # 2
        elif( CurrentRangeSel <= 0.25 ):
            nCurrentRange = RANGE_I._250MADC    # 1
        else:
            nCurrentRange = RANGE_I._500MAAC    # 0
    else:
        nCurrentRange = RANGE_I._500MAAC        # 0
    return nCurrentRange

def MEASURE_LEAK( ValueVolt, ValueCurrent, PinPositive, PinNegative, PreTime, MeasTime, Max, Min, Quality_Meas ):
    MeasIOff = 0.0
    if( MeasTime > 0.1 ):
        MeasTime = 0.1
    FreqACQ = 400000
    NSampleACQ = int( MeasTime * FreqACQ )
    TimeACQ = NSampleACQ / FreqACQ
    TimeSempleACQ = 1 / FreqACQ
    
    # --- misura di preparazione ---
    delayTime = 0.01
    delayTimeLOW = delayTime * 0.2
    delayTimeHIG = delayTime * 0.8
    DISCAP_Set( CH1 = PinPositive, CH2 = PinNegative, CURRENT = ValueCurrent )
    LINE_Set( MODE = LINEMODE._4L )
    GND_Set( OUT = GNDLINE.L3 )
    PULL_Set( VAL = VAL.R_1K, SOURCE = PUL_SOURCE.L2, TIME_RELE = TIME_RELE.ON )
    nCurrentRange = CurrRange( Max )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.L1, MODE = CHMODE._4L_IMM )
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = 10,
        FREQ = 10000000,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = 2e-8,
        EVOLUTION = 1,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    DRA_Set( MODE = DRAMODE.V, V = ValueVolt, I = ValueCurrent,OUT = DRAOUT.L2 )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )  # corto pull
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L2, MODE = CHMODE._4L_INC_C )  # corto pull
    time.sleep( delayTimeLOW )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )
    time.sleep( delayTimeHIG )
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = NSampleACQ,
        FREQ = FreqACQ,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = delayTime,
        EVOLUTION = Quality_Meas,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )
    IMM_Clear()
    DRA_Clear()
    PULL_Clear()
    GND_Clear()
    DISCAP_Set( CH1 = PinPositive, CH2 = PinNegative, CURRENT = ValueCurrent )
    # --- fine misura di preparazione ---

    delayTime = PreTime
    delayTimeLOW = delayTime * 0.2
    delayTimeHIG = delayTime * 0.8
    LINE_Set( MODE = LINEMODE._4L )
    GND_Set( OUT = GNDLINE.L3 )
    PULL_Set( VAL = VAL.R_1K, SOURCE = PUL_SOURCE.L2, TIME_RELE = TIME_RELE.ON )
    nCurrentRange = CurrRange( Max )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L3, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.L3, MODE = CHMODE._4L_IMM )
    # movimento
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = 10,
        FREQ = 10000000,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = 2e-8,
        EVOLUTION = 1,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )
    DRA_Set( MODE = DRAMODE.V, V = 0.0, I = ValueCurrent, OUT = DRAOUT.L2 )
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = NSampleACQ,
        FREQ = FreqACQ,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = delayTime,
        EVOLUTION = Quality_Meas,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    resV, OutBuff = IMM_Meas( MEAS.AVERAGE_V, 1, 0 )
    MeasV = OutBuff[0] if resV else 0.0
    # VDT_Write( " MeasV = " + str( MeasV ) )
    # VDT_Pause()
    resI, OutBuff = IMM_Meas( MEAS.AVERAGE_I, 1, 0 )
    MeasIOff = OutBuff[0] if resI else 0.0
    # VDT_Write( " MeasI Null = " + str( MeasIOff ) )
    # VDT_Pause()
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.L1, MODE = CHMODE._4L_IMM )
    # movimento
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = 10,
        FREQ = 10000000,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = 2e-8,
        EVOLUTION = 1,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    DRA_Set( MODE = DRAMODE.V, V = ValueVolt, I = ValueCurrent, OUT = DRAOUT.L2 )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )  # corto pull
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L2, MODE = CHMODE._4L_INC_C )  # corto pull
    time.sleep( delayTimeLOW )
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )
    time.sleep( delayTimeHIG )
    IMM_Set(
        MEAS_V = MEAS_V.DC,
        MEAS_I = MEAS_I.DC,
        RANGE_V = RANGE_V._10VG,
        RANGE_I = nCurrentRange,
        MODE = 3,
        N_SAMPLE = NSampleACQ,
        FREQ = FreqACQ,
        START = IMMSTART.SW1,
        TRIG_OUT = TRIG_OUT.SW1,
        DELAY_TRIG = delayTime,
        EVOLUTION = Quality_Meas,
        INP_VPOS = INP_VPOS.L4,
        INP_VNEG = INP_VNEG.GND,
        INP_I_V2 = INP_I_V2.L1_I,
        REF_I = REF_I.GND
        )
    res, OutBuff = IMM_Meas( MEAS.AVERAGE_V, 1, 0 )
    MeasV = OutBuff[0] if res else 0.0
    # VDT_Write( " MeasV = " + str( MeasV ) )
    # VDT_Pause()
    res, OutBuff = IMM_Meas( MEAS.AVERAGE_I, 1, 0 )
    MeasI = OutBuff[0] if res else 0.0
    # VDT_Write( " MeasIOff = " + str( MeasIOff ) )
    # VDT_Write( " MeasI = " + str( MeasI ) )
    # VDT_Pause()
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.L4, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.L1, MODE = CHMODE._4L_IMM )
    MeasI = MeasI - MeasIOff
    CHANNEL_Set( CHN = PinPositive, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )
    CHANNEL_Set( CHN = PinNegative, LINEE = ELINE.NONE, MODE = CHMODE._4L_IMM )

    if( Max == 0 ):
        TolPosLimit = 0.000001
    else:
        TolPosLimit = ( ( Max + Max * 0.2 ) + 0.000001 ) # ! +20%

    if( Min == 0 ):
        TolNegLimit = -0.000001
    else:
        TolNegLimit = ( ( Min + Min * 0.2 ) - 0.000001 ) # ! +20%

    TolPosLimit = TolPosLimit * 1000000
    TolNegLimit = TolNegLimit * 1000000

    # --- scope ---
    scopevisible, StrResponse = SystemExecute( "VivaOscilloscopeIsVisible", '' )
    if( scopevisible ):
        OSC_Clear()
        OSC_Set(
            SCOPE = 1,
            NAME_X = "Time",
            MIN_X = 0,
            MAX_X = 0.005,
            NAME_Y = "Current",
            MIN_Y = TolNegLimit,
            MAX_Y = TolPosLimit,
            TIME_DIV = 0.000001
            )
        OSC_SetTrack(
            SCOPE = 1,
            TRACK = OscChannel.TR_1,
            NAME = "Leakage",
            SCALE_Y = 1.0,
            OFFSET_Y = 0.0,
            MODE = OscTrackMode.Clear,
            COLOR = OscColor.Red
            )
        res, VetWrite = IMM_Meas( MEAS.BUFFER_I, NSampleACQ, 0 )
        if res:
            MVetWrite = list( VetWrite )
            for idy in range( 0, NSampleACQ ):
                MVetWrite[ idy ] = MVetWrite[ idy ] * 1000000
            OSC_Write(
                DATA = MVetWrite,
                SCOPE = 1,
                TRACK = OscChannel.TR_1,
                ACQUISITION = NSampleACQ
                )
        OSC_SetTrack(
            SCOPE = 1,
            TRACK = OscChannel.TR_2,
            NAME = "Volt",
            SCALE_Y = 1.0,
            OFFSET_Y = 0.0,
            MODE = OscTrackMode.Clear,
            COLOR = OscColor.Green
            )
        res, VetWrite = IMM_Meas( MEAS.BUFFER_V, NSampleACQ, 0 )
        if( res ):
            OSC_Write(
                DATA = VetWrite,
                SCOPE = 1,
                TRACK = OscChannel.TR_2,
                ACQUISITION = NSampleACQ
                )
    OSC_Draw( SCOPE = 1 )
    # --- fine scope ---

    IMM_Clear()
    DRA_Clear()
    PULL_Clear()
    GND_Clear()

    if resI and resV :
        SetTestInfo("A", MeasI, Min, MeasI, Max, TestResult.TestResult )
    else:
        SetTestInfo("A", 0, Min, 0, Max, TestResult.TestResult )

    return MeasI
