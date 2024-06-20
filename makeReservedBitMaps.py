import csv
import pandas as pd
import math
import argparse
import json

econd_tmr_names = ['Aligner_Global_tmr_err_cnt_aligner', 'ChAligner_00_tmr_err_cnt_chan_aligner', 'ChAligner_00_tmr_err_cnt_chan_err', 'ChAligner_00_tmr_err_cnt_chan_eprxgrp', 'ChAligner_01_tmr_err_cnt_chan_aligner', 'ChAligner_01_tmr_err_cnt_chan_err', 'ChAligner_01_tmr_err_cnt_chan_eprxgrp', 'ChAligner_02_tmr_err_cnt_chan_aligner', 'ChAligner_02_tmr_err_cnt_chan_err', 'ChAligner_02_tmr_err_cnt_chan_eprxgrp', 'ChAligner_03_tmr_err_cnt_chan_aligner', 'ChAligner_03_tmr_err_cnt_chan_err', 'ChAligner_03_tmr_err_cnt_chan_eprxgrp', 'ChAligner_04_tmr_err_cnt_chan_aligner', 'ChAligner_04_tmr_err_cnt_chan_err', 'ChAligner_04_tmr_err_cnt_chan_eprxgrp', 'ChAligner_05_tmr_err_cnt_chan_aligner', 'ChAligner_05_tmr_err_cnt_chan_err', 'ChAligner_05_tmr_err_cnt_chan_eprxgrp', 'ChAligner_06_tmr_err_cnt_chan_aligner', 'ChAligner_06_tmr_err_cnt_chan_err', 'ChAligner_06_tmr_err_cnt_chan_eprxgrp', 'ChAligner_07_tmr_err_cnt_chan_aligner', 'ChAligner_07_tmr_err_cnt_chan_err', 'ChAligner_07_tmr_err_cnt_chan_eprxgrp', 'ChAligner_08_tmr_err_cnt_chan_aligner', 'ChAligner_08_tmr_err_cnt_chan_err', 'ChAligner_08_tmr_err_cnt_chan_eprxgrp', 'ChAligner_09_tmr_err_cnt_chan_aligner', 'ChAligner_09_tmr_err_cnt_chan_err', 'ChAligner_09_tmr_err_cnt_chan_eprxgrp', 'ChAligner_10_tmr_err_cnt_chan_aligner', 'ChAligner_10_tmr_err_cnt_chan_err', 'ChAligner_10_tmr_err_cnt_chan_eprxgrp', 'ChAligner_11_tmr_err_cnt_chan_aligner', 'ChAligner_11_tmr_err_cnt_chan_err', 'ChAligner_11_tmr_err_cnt_chan_eprxgrp', 'ClocksAndResets_Global_tmr_err_cnt_clocks_and_resets', 'ELinkProcessors_Global_tmr_err_cnt_elink_processors', 'ERx_Global_tmr_err_cnt_erx', 'ETx_Global_tmr_err_cnt_etx', 'EprxGrpTop_Global_tmr_err_cnt_eprxgrp_top', 'ErrTop_Global_tmr_err_cnt_err_top', 'FCtrl_Global_tmr_err_cnt_fast_ctrl_decoder', 'FormatterBuffer_Global_tmr_err_cnt_formatter_buffer', 'Misc_TMRErrCnt_Global_tmr_err_cnt_misc', 'PingPongSRAM_Global_tmr_err_cnt_bist_ctrl', 'RocDaqCtrl_Global_tmr_err_cnt_roc_daq_ctrl', 'Watchdog_Global_tmr_err_cnt_reset_request', 'ZS_Global_tmr_err_cnt_zero_suppress', 'ZSmOne_Global_tmr_err_cnt_zero_suppress_m']

econt_tmr_names = ['Aligner_Global_tmr_err_cnt_aligner', 'ChAligner_00_tmr_err_cnt_chan_aligner', 'ChAligner_00_tmr_err_cnt_chan_err', 'ChAligner_00_tmr_err_cnt_chan_eprxgrp', 'ChAligner_01_tmr_err_cnt_chan_aligner', 'ChAligner_01_tmr_err_cnt_chan_err', 'ChAligner_01_tmr_err_cnt_chan_eprxgrp', 'ChAligner_02_tmr_err_cnt_chan_aligner', 'ChAligner_02_tmr_err_cnt_chan_err', 'ChAligner_02_tmr_err_cnt_chan_eprxgrp', 'ChAligner_03_tmr_err_cnt_chan_aligner', 'ChAligner_03_tmr_err_cnt_chan_err', 'ChAligner_03_tmr_err_cnt_chan_eprxgrp', 'ChAligner_04_tmr_err_cnt_chan_aligner', 'ChAligner_04_tmr_err_cnt_chan_err', 'ChAligner_04_tmr_err_cnt_chan_eprxgrp', 'ChAligner_05_tmr_err_cnt_chan_aligner', 'ChAligner_05_tmr_err_cnt_chan_err', 'ChAligner_05_tmr_err_cnt_chan_eprxgrp', 'ChAligner_06_tmr_err_cnt_chan_aligner', 'ChAligner_06_tmr_err_cnt_chan_err', 'ChAligner_06_tmr_err_cnt_chan_eprxgrp', 'ChAligner_07_tmr_err_cnt_chan_aligner', 'ChAligner_07_tmr_err_cnt_chan_err', 'ChAligner_07_tmr_err_cnt_chan_eprxgrp', 'ChAligner_08_tmr_err_cnt_chan_aligner', 'ChAligner_08_tmr_err_cnt_chan_err', 'ChAligner_08_tmr_err_cnt_chan_eprxgrp', 'ChAligner_09_tmr_err_cnt_chan_aligner', 'ChAligner_09_tmr_err_cnt_chan_err', 'ChAligner_09_tmr_err_cnt_chan_eprxgrp', 'ChAligner_10_tmr_err_cnt_chan_aligner', 'ChAligner_10_tmr_err_cnt_chan_err', 'ChAligner_10_tmr_err_cnt_chan_eprxgrp', 'ChAligner_11_tmr_err_cnt_chan_aligner', 'ChAligner_11_tmr_err_cnt_chan_err', 'ChAligner_11_tmr_err_cnt_chan_eprxgrp', 'ClocksAndResets_Global_tmr_err_cnt_clocks_and_resets', 'ERx_Global_tmr_err_cnt_erx', 'ETx_Global_tmr_err_cnt_etx', 'EprxGrpTop_Global_tmr_err_cnt_eprxgrp_top', 'ErrTop_Global_tmr_err_cnt_err_top', 'FCtrl_Global_tmr_err_cnt_fast_ctrl_decoder', 'Misc_TMR_ERR_CNT_Global_tmr_err_cnt_misc', 'Config_Global_tmr_err_cnt_mfc', 'Algo_Global_tmr_err_cnt_alg', 'FormatterBuffer_Global_tmr_err_cnt_fmtbuf', 'Encoder_Global_tmr_err_cnt_auto_encoder']

def makeTMRcntrToRegNameMap(nomdf):
    #nomdf -> df of 'econd_rtl/vrf/uvcs/ral/csv/regs.csv'
    tmrnomdf = nomdf[nomdf["Field Name"].str.contains("tmr")]#Get all tmr counters
    tmrstrs = list(tmrnomdf["Register Name"])#string for last reg it covers
    tmrnoms = list(tmrnomdf["Field Name"])#name of tmrcounters
    tmrstrs = [x.replace("xx","{0}")[3:] for x in tmrstrs]#replace the channel so it can be formatted later
    tmrids  = dict(zip(tmrnoms,tmrstrs))

    return tmrids

def getFFCoveredByTMR(tmrcnt,tmrids,mapdf,target):
    #Takes the tmr error counter name from econ_sw + pytest output
    #tmrids -> dictionary that tmr counter name to covered engineering name
    #mapdf -> dataframe of all RW and WO registers. df of below
    #'econd_rtl/vrf/uvcs/ral/csv/maps.csv'
    if target == "ECOND":
        tag = "tmr"+tmrcnt.split("_tmr")[-1]
        if "PingPong" in tmrcnt:
            tag = "tmr_err_cnt_pingpong_sram_bist_ctrl"
            idstr = tmrids[tag][:-2]
        elif "zero_suppress_m" in tmrcnt:
            tag = "tmr_err_cnt_zero_suppress_m1"
            idstr = tmrids[tag][:-6]
        elif "zero_suppress" in tmrcnt:
            idstr = tmrids[tag][:-6]  
        elif "Ch" in tmrcnt:
            num = tmrcnt.split("_tmr")[0].split("_")[-1]
            if "tmr_err_cnt_chan_aligner" in tmrcnt:
                idstr = tmrids[tag].format(num)[:-2]
            if "tmr_err_cnt_chan_err" in tmrcnt:
                idstr = "CHERR_{0}_ALL_w".format(num)
            if "tmr_err_cnt_chan_eprxgr" in tmrcnt:
                idstr = "CHEPRXGRP_{0}_ALL".format(num)
        elif "Watchdog_Global_tmr_err_cnt_reset_request" in tmrcnt:
            idstr = "WATCHDOG_ALL_w"
        elif "Misc_TMRErrCnt_Global_tmr_err_cnt_misc" in tmrcnt:
            idstr = "MISC_ALL_w"
        else:
            idstr = tmrids[tag][:-2]

    if target == "ECONT":
        tag = "tmr"+tmrcnt.split("_tmr")[-1]
        if "Ch" in tmrcnt:
            num = tmrcnt.split("_tmr")[0].split("_")[-1]
            if "tmr_err_cnt_chan_aligner" in tmrcnt:
                idstr = tmrids[tag].format(num)[:-2]
            if "tmr_err_cnt_chan_err" in tmrcnt:
                idstr = "CHERR_{0}_ALL_w".format(num)
            if "tmr_err_cnt_chan_eprxgr" in tmrcnt:
                idstr = "CHEPRXGRP_{0}_ALL".format(num)
        elif "Misc_TMR_ERR_CNT" in tmrcnt:
            idstr = "MISC_ALL_w"
        elif "Config" in tmrcnt:
            idstr = "MFC"
        elif "Algo" in tmrcnt:
            idstr = "ALG_"
        elif "Encoder" in tmrcnt:
            idstr = "AUTO_ENCODER_"
        else:
            idstr = tmrids[tag][:-2]

    #print("   using string ",idstr)
    regsdfRW = mapdf[mapdf["BlockMap Instance Name"].str.contains("RW_"+idstr)]
    regsdfWO = mapdf[mapdf["BlockMap Instance Name"].str.contains("WO_"+idstr)]
    numbits = (8*len(regsdfRW)+8*len(regsdfWO))*3

    if tmrcnt == "ZS_Global_tmr_err_cnt_zero_suppress":
        zermrw = len(mapdf[mapdf["BlockMap Instance Name"].str.contains("RW_"+tmrids["tmr_err_cnt_zero_suppress_m1"][:-6])])
        zermwo = len(mapdf[mapdf["BlockMap Instance Name"].str.contains("WO_"+tmrids["tmr_err_cnt_zero_suppress_m1"][:-6])])
        numbits = numbits-8*zermrw*3-8*zermwo*3

    return numbits


if __name__=='__main__':
    #get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--target","--target", type=str,help = "chip flavor: ECOND or ECONT")
    args = parser.parse_args()

    if args.target == 'ECOND':
        regmap  = '../ECOND_Aug2023_SEU_Analysis/econd_lightweight/vrf/uvcs/ral/csv/maps.csv'
        regnom  = '../ECOND_Aug2023_SEU_Analysis/econd_lightweight/vrf/uvcs/ral/csv/regs.csv'
        tmrnames = econd_tmr_names
        outname = 'econd_tmr_numbbits.json'
    elif args.target == 'ECONT':
        regmap  = '../ECOND_Aug2023_SEU_Analysis/econt_lightweight/vrf/uvcs/ral/csv/maps.csv'
        regnom  = '../ECOND_Aug2023_SEU_Analysis/econt_lightweight/vrf/uvcs/ral/csv/regs.csv'
        tmrnames = econt_tmr_names
        outname = 'econt_tmr_numbbits.json'
    else:
        print("No specific ECON targetted, script will fail.")
        regmap  = '../ECOND_Aug2023_SEU_Analysis/econt_lightweight/vrf/uvcs/ral/csv/maps.csv'
        regnom  = '../ECOND_Aug2023_SEU_Analysis/econt_lightweight/vrf/uvcs/ral/csv/regs.csv'
        tmrnamse = []
        outname = ''

    #make into dataframes
    mapdf = pd.read_csv(regmap)
    nomdf = pd.read_csv(regnom)
    tmrids = makeTMRcntrToRegNameMap(nomdf)

    bitdict = {}
    if len(tmrnames) > 0:
        for tmrcntr in tmrnames:
            bitdict[tmrcntr] = getFFCoveredByTMR(tmrcntr,tmrids,mapdf,args.target)
            print("{} : {}".format(tmrcntr,bitdict[tmrcntr]))

    with open(outname,'w') as f:
        json.dump(bitdict,f)
        

