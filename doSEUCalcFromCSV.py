import json
import pandas as pd
import math
import argparse
import numpy as np

gruns_jun24 = [5,6,7,8,9,10,11,12,14,15,16,19,20,21,22]

rundict = {"jun24":gruns_jun24}

if __name__=='__main__':
    #get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-hexa","--hexaboard", type=int,help = "hexaboard number")
    parser.add_argument("-f","--tmrfile", type=str,help = "file with tmr counts")
    parser.add_argument("-p","--runperiod", type=str,help = "Running period: jun24, jan24, aug23")
    parser.add_argument("-l","--runlog", type=str,help = "file with run log")
    parser.add_argument("-r","--runnum", type=int,help = "specific run to calculate xs for")
    parser.add_argument("--target","--target", type=str,help = "chip flavor: ECOND or ECONT")
    #parser.add_argument("-t","--total",type=bool,help="only do xs for all runs")
    #parser.add_argument("-c","--clean",type=bool,help="only do xs for all runs but cleaned for chip 4")
    #parser.add_argument("-v","--verbose",type=bool,help="Prints results for total xs calc")
    #parser.add_argument("-n","--name",type=str,default="",help="additional string to append as name")
    args = parser.parse_args()
    
    #load info
    tmrerrs = args.tmrfile
    runinfo = args.runlog
    goodruns = rundict[args.runperiod]
    if args.target == 'ECOND':
        bitsf = json.load(open('econd_tmr_numbbits.json'))
    elif args.target == 'ECONT':
        bitsf = json.load(open('econt_tmr_numbbits.json'))
    else:
        print("No clue what chip you want to calculate the xs for, try again, with a good target.")
        bitsf = []


    #make into dataframes
    errdf = pd.read_csv(tmrerrs)
    rundf = pd.read_csv(runinfo)
    hexadf = errdf[errdf['Hexacontroller'] == args.hexaboard]
    analdf = hexadf[hexadf['Run'].isin(goodruns)]
    grundf = rundf[rundf["Run"].isin(goodruns)]

    print(grundf.columns)

    #TMR name bookkeeping
    tmrnames = list(errdf.columns[2:])#removes run num and hexa controller
    tmralldict = {}
    rundepdict = {}
    fluenc = np.array(grundf['Computed Fluence [p/cm2]'])
    rundepdict["Fluence [1/cm2]"] = fluenc
    rundepdict["Run #"] = analdf["Run"]
    
    for tmrcnt in tmrnames:
        tmrinf = {}
        nbits = bitsf[tmrcnt]
        counts = np.array(analdf[tmrcnt])

        xsprun = counts/nbits/fluenc
        ucprun = np.sqrt(counts)/nbits/fluenc

        toterrs = analdf[tmrcnt].sum()
        totflu = grundf['Computed Fluence [p/cm2]'].sum()
        totxs =  toterrs/nbits/totflu

        print(tmrcnt)
        print("total errs: ",toterrs)
        print("total fluence: ",totflu)
        print("total xs: ",totxs)

        rundepdict[tmrcnt+"_xs"] = xsprun
        rundepdict[tmrcnt+"_xsunc"] = ucprun

        tmrinf["xs"] = totxs
        tmrinf["xsunc"] = math.sqrt(toterrs)/nbits/totflu
        tmrinf["nerrs"] = toterrs
        tmrinf["Total Fluence [1/cm2]"] = totflu
        tmralldict[tmrcnt] = tmrinf

    outnametot = "../data/seu_total_xs_per_tmrblock_per_ff_hexa"+str(args.hexaboard)+"_"+args.target+"_"+args.runperiod+".csv"
    outnameperrun = "../data/seu_per_run_xs_per_tmrblock_per_ff_hexa"+str(args.hexaboard)+"_"+args.target+"_"+args.runperiod+".csv"

    print('Saving .csv summaries in ',outnametot,outnameperrun)
    
    bytmrtotdf = pd.DataFrame.from_dict(tmralldict)
    bytmrtotdf.to_csv(outnametot)
    byrundf = pd.DataFrame.from_dict(rundepdict)
    byrundf.to_csv(outnameperrun)

