import matplotlib.pyplot as plt
import pandas as pd
import mplhep as hep
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
from datetime import date
import argparse
import json

parser = argparse.ArgumentParser()


chipdict = {"hexa42":"ECONT001",
            "hexa43":'ECOND001',
            "hexa44":"ECONT002",
            }

def makeFigureFile(descrip,ftype,hexab,chipn):
    if not os.path.exists("figures/"+str(date.today())+"/"):
        os.makedirs("figures/"+str(date.today())+"/")
    outFile = "figures/"+str(date.today())+"/"+descrip+"_"+hexab+"_chip"+chipn+ftype
    return outFile

if __name__=='__main__':
    parser.add_argument("-n","--name",type=str,default="noth",help="additional string to add to outfiles")
    parser.add_argument("-p","--path",type=str,help="path to per run .csv. for example ../data/seu_xs_per_run_per_tmrblock_per_ff_hexa48.csv")
    parser.add_argument("--target","--target", type=str,help = "chip flavor: ECOND or ECONT")
    args = parser.parse_args()
    data = args.path#'../data/seu_xs_per_run_per_tmrblock_per_ff_hexa48.csv'
    df = pd.read_csv(data)
    dfformean  = df.copy()
    tmrinfall = [x for x in list(df.columns) if 'tmr' in x]
    tmrnames = [x[:-3] for x in tmrinfall if 'unc' not in x]

    if args.target == 'ECOND':
        bitsf = json.load(open('econd_tmr_numbbits.json'))
    elif args.target == 'ECONT':
        bitsf = json.load(open('econt_tmr_numbbits.json'))
    else:
        print("No clue what chip you want to calculate the xs for, try again, with a good target.")
        bitsf = []


    hexnum = data.split("_")[-3].split(".csv")[0]
    chip = chipdict[hexnum]
    hexaboard = hexnum.split("hexa")[-1]
    pltlab = "Hexa {0}, Chip {1}".format(hexaboard,chip)

    fig, ax  = plt.subplots()
    hep.style.use("CMS")
    hep.cms.text("Internal",loc=1,fontsize=11)
    hep.cms.label(pltlab, loc=2,fontsize=11,data=True,llabel=pltlab,rlabel="")
    plt.ylim([0.000000000000001,0.00000000001])#log scale
    #plt.ylim([0.0000000000000000005,0.00000000000006])#linear scale, the two ZS ones
    ax.set_yscale('log')

    notplots = []
    #tmr_to_plt = [x for x in tmrnames if "ChAligner" not in x]
    tmr_to_plt = sorted(bitsf,key=bitsf.get,reverse=True)[:8]
    coltokeep = set([x+"_xs" for x in tmr_to_plt])
    coltodrop = set(list(dfformean.columns)) - coltokeep
    dfformean = dfformean.drop(columns=list(coltodrop))
    dfmean = dfformean.mean(axis=1)
    dfstd  = dfformean.std(axis=1)
    ax.plot(df["Run #"],dfmean,'-',color="black",label="mean")
    ax.fill_between(df["Run #"],dfmean-dfstd,dfmean+dfstd,alpha=0.2,label="STD")

    #tmr_to_plt = tmrnames
    for cntr in tmr_to_plt:
        if len(df[df[cntr+"_xsunc"] < 0]) > 0:
            notplots.append(cntr)
            continue
        plt.errorbar(df["Run #"],df[cntr+"_xs"],yerr=df[cntr+"_xsunc"],label=cntr.replace("_tmr_err_cnt",""),fmt="o")

    #print(df["Run #"])
    #print(df["ZSmOne_Global_tmr_err_cnt_zero_suppress_m_xs"])
    
    #plt.errorbar(df["Run #"],df["ZSmOne_Global_tmr_err_cnt_zero_suppress_m_xs"],yerr=df["ZSmOne_Global_tmr_err_cnt_zero_suppress_m_xsunc"],label='ZS M1 Block')
    #plt.errorbar(df["Run #"],df["ZS_Global_tmr_err_cnt_zero_suppress_xs"],yerr=df["ZS_Global_tmr_err_cnt_zero_suppress_xsunc"],label='ZS Block')
    #

    plt.xlabel("Run #",fontsize=14)
    plt.ylabel(r'Cross section cm$^{-2}$',fontsize=14)
    plt.tick_params(labelsize=12)
    plt.locator_params(axis='x',nbins=5)
    #plt.locator_params(axis='y',nbins=4)
    ax.yaxis.get_offset_text().set_fontsize(12)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    #ax.yaxis.set_minor_locator(MultipleLocator(0.000000000000005))
    plt.tick_params(axis="x",bottom=True,direction="in",which="both")
    plt.tick_params(axis="y",bottom=True,direction="in",which="both")


    #plt.legend(loc=3,fontsize=14,bbox_to_anchor=(0.5,0.5))#the two ZS ones
    #plt.legend(loc=3,fontsize=6.5,bbox_to_anchor=(0.50,0.35))#the non-cha align ones
    plt.legend(loc=3,fontsize=8,bbox_to_anchor=(0.45,0.5))#the cha align ones
    figname = makeFigureFile("seu_xs_per_run",".png",hexnum,chip+args.name)
    plt.savefig(figname,bbox_inches="tight")
    plt.show()

    print("Saving resulting figure in ",figname)
