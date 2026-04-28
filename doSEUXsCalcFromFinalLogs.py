import csv
import pandas as pd
import math
import argparse

if __name__=='__main__':
    #get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-hexa","--hexaboard", type=int,help = "hexaboard number")
    parser.add_argument("-f","--tmrfile", type=str,help = "file with tmr counts")
    parser.add_argument("-l","--runlog", type=str,help = "file with run log")
    parser.add_argument("-r","--runnum", type=int,help = "specific run to calculate xs for")
    parser.add_argument("-t","--total",type=bool,help="only do xs for all runs")
    parser.add_argument("-c","--clean",type=bool,help="only do xs for all runs but cleaned for chip 4")
    parser.add_argument("-v","--verbose",type=bool,help="Prints results for total xs calc")
    parser.add_argument("-n","--name",type=str,default="",help="additional string to append as name")
    args = parser.parse_args()
    
    #load files
    tmrerrs = args.tmrfile
    runinfo = args.runlog

    #make into dataframes
    errdf = pd.read_csv(tmrerrs)
    rundf = pd.read_csv(runinfo)

    #Repair runs 5a and 5b
    if args.hexaboard == 48:
        errdf.at[22,'Run'] = 5
        errdf.at[23,'Run'] = 5
        errdf['Run'] = errdf['Run'].map(int)
        errdf.loc[22]+=errdf.loc[23]
        errdf.drop(23,inplace=True)
        errdf.at[22,'Run'] = 5
        errdf.at[22,'Hexacontroller'] = 48
        #

    #TMR name bookkeeping
    tmrnames = list(errdf.columns[2:])#removes run num and hexa controller
    tmralldict = {}
    rundepdict = {}

    #Details of the running
    errmaskl = []
    fluruns = []
    byrun = False
    nruns = -1
    if "jan" in tmrerrs:
        nruns = 22
    if "aug" in tmrerrs:
        nruns = 18

    if args.total and not args.clean:
        errmaskl.append(errdf['Hexacontroller'] == args.hexaboard)
        fluruns.append(nruns+1)
        outname = "../data/seu_total_xs_per_tmrblock_per_ff_hexa"+str(args.hexaboard)+args.name+".csv"
        print("Saving summary in ",outname)
    elif args.total and args.clean:
        errmaskl.append(errdf['Hexacontroller'] == args.hexaboard)
        fluruns.append(nruns+1)
        outname = "../data/seu_total_xs_per_tmrblock_per_ff_cleaned_hexa"+str(args.hexaboard)+args.name+".csv"
        print("Saving summary in ",outname)
    elif args.runnum:
        errmaskl.append(errdf['Hexacontroller'] == args.hexaboard)
        fluruns.append(args.runnum)
        print("Not saving anything, just printing to screen")
    else:
        outname = "../data/seu_xs_per_run_per_tmrblock_per_ff_hexa"+str(args.hexaboard)+args.name+".csv"
        errmaskl = [errdf['Hexacontroller'] == args.hexaboard for x in rundf['Run']]
        #print(errmaskl)
        #flumaskl = [rundf['Run'] == x for x in rundf['Run']]
        #flumaskl = [errdf['Run'] == x for x in rundf['Run']]
        fluruns = [x for x in rundf['Run']]
        #fluruns = ["0"+x for x in
        byrun = True
        print("Saving summary in ",outname)
        print("not printing individual calculations, too many to do.")


    scenes = list(zip(errmaskl,fluruns))
    for tmrcnt in tmrnames:
        rundepdict[tmrcnt+"_xs"] = []
        rundepdict[tmrcnt+"_xsunc"] = []
        rundepdict["Fluence [1/cm2]"] = []
        rundepdict["Run #"] = []
        for scene in scenes:
            tmrinf = {}
            numbits = getFFCoveredByTMR(tmrcnt,tmrids,mapdf)
            tmrinf["nbits"] = numbits
            #print(errdf.dtypes)
            #print("hexaerrs: ")
            hexaerrs = errdf[scene[0]]
            #print(hexaerrs)
            #print("scene[1]: ")
            #print(scene[1])

            if args.total and not args.clean:
                runerrs = hexaerrs
                fludf = rundf
            elif args.total and args.clean:
                runerrs = hexaerrs[hexaerrs['Run'] < 16]
                runerrs = runerrs[runerrs['Run'] != 5]
                fludf = rundf[rundf['Run'] < 16]
                fludf = fludf[fludf['Run'] != 5]
            else:
                #print("err mask: ")
                #print(hexaerrs['Run'] == scene[1])
                #runerrs = hexaerrs[hexaerrs['Run'] == str(scene[1])]
                runerrs = hexaerrs[hexaerrs['Run'] == scene[1]]
                fludf = rundf[rundf['Run'] ==  scene[1]]

            tmrinf["nerrs"] = runerrs[tmrcnt].sum()
            fluence = fludf['Fluence [1/cm2]'].sum()
            if numbits != 0:
                tmrinf["xs"]    = tmrinf["nerrs"]/numbits/fluence
                tmrinf["xsunc"] = math.sqrt(tmrinf["nerrs"])/numbits/fluence
                tmralldict[tmrcnt] = tmrinf
            else:
                tmrinf["xs"] = -1
                tmrinf["xsunc"] = -1
                tmralldict[tmrcnt] = tmrinf

            rundepdict[tmrcnt+"_xs"].append(tmrinf["xs"])
            rundepdict[tmrcnt+"_xsunc"].append(tmrinf["xsunc"])

            if len(rundepdict["Fluence [1/cm2]"]) < nruns:
                rundepdict["Fluence [1/cm2]"].append(fluence)
            if byrun or args.runnum:
                if len(rundepdict["Run #"]) < nruns:
                    runnum = fludf["Run"].values[0]
                    rundepdict["Run #"].append(runnum)
            if not byrun and args.verbose:
                print("Counting bits and measureing xs of ",tmrcnt)
                print("    Number of bits ",tmrinf["nbits"])
                print("    Number of errors ",tmrinf["nerrs"])
                print("    xs (errors/bits/fluence): ",tmrinf["xs"])
                print("    stats unc: ",tmrinf["xsunc"])
            elif args.runnum:
                print("Counting bits and measureing xs of ",tmrcnt)
                print("    Number of bits ",tmrinf["nbits"])
                print("    Number of errors ",tmrinf["nerrs"])
                print("    xs (errors/bits/fluence): ",tmrinf["xs"])
                print("    stats unc: ",tmrinf["xsunc"])
            else:
                continue
                #print("Counting bits and measureing xs of ",tmrcnt)
                #print("    Number of bits ",tmrinf["nbits"])
                #print("    Number of errors ",tmrinf["nerrs"])
                #print("    xs (errors/bits/fluence): ",tmrinf["xs"])
                #print("    stats unc: ",tmrinf["xsunc"])
    #Save some stuff for ease
    if args.total:
        bytmrtotdf = pd.DataFrame.from_dict(tmralldict)
        bytmrtotdf.to_csv(outname)
    elif args.runnum:
        print("not saving, look at terminal, must be a special run.")
    else:
        byrundf = pd.DataFrame.from_dict(rundepdict)
        byrundf.to_csv(outname)
