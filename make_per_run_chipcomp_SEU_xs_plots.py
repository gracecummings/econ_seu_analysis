import matplotlib.pyplot as plt
import pandas as pd
import mplhep as hep
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
from datetime import date
from hexaboardAndChip import HexaInfo
import numpy as np
import argparse

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
    parser.add_argument("-p1","--path1",type=str,help="path to per run .csv. for example ../data/seu_xs_per_run_per_tmrblock_per_ff_hexa48.csv")
    parser.add_argument("-p2","--path2",type=str,help="path to per run .csv. for example ../data/seu_xs_per_run_per_tmrblock_per_ff_hexa48.csv")

    args = parser.parse_args()
    
    d1path = args.path1
    d2path = args.path2
    d1 = HexaInfo(d1path)
    d2 = HexaInfo(d2path)
    lab1 = "Hexaboard {0}, Chip {1}".format(d1.hexaboard,d1.chip)
    lab2 = "Hexaboard {0}, Chip {1}".format(d2.hexaboard,d2.chip)
    divdf = d1.df.div(d2.df)
    errdf = np.sqrt(d1.df.mul(d1.df).div(d1.df)+d2.df.mul(d2.df).div(d2.df))*divdf

    tmrnames = list(set(d1.tmrnames).intersection(set(d2.tmrnames)))
    tmrlost  = list(set(d1.tmrnames).symmetric_difference(set(d2.tmrnames)))
    if len(tmrlost)>0:
        print("Unmathced TMR counters: ",tmrlost)
    for cntr in tmrnames:

        #error bar on divison
        errdiv = divdf[cntr+'_xs']*((d1.df[cntr+"_xsunc"]/d1.df[cntr+"_xs"])**2+(d2.df[cntr+"_xsunc"]/d2.df[cntr+"_xs"])**2)**(1/2)
        
        fig, ax  = plt.subplots(2,1,height_ratios=[3,1])
        hep.style.use("CMS")
        hep.cms.text("Internal",loc=1,fontsize=18,ax=ax[0])
        hep.cms.label(cntr+" xs per FF", loc=2,fontsize=18,data=True,llabel=cntr+" xs per FF",rlabel="",ax=ax[0])

        ax[0].errorbar(d1.df["Run #"],d1.df[cntr+"_xs"],yerr=d1.df[cntr+"_xsunc"],label=lab1,fmt="o-")
        ax[0].errorbar(d2.df["Run #"],d2.df[cntr+"_xs"],yerr=d2.df[cntr+"_xsunc"],label=lab2,fmt="o-")
        ax[1].axline((0,1),(18,1))
        ax[1].errorbar(d2.df["Run #"],divdf[cntr+"_xs"],yerr=errdiv,color="black",label=lab1,marker="o",linestyle='None')
        ax[1].fill_between(d2.df["Run #"],divdf[cntr+"_xs"]-errdf[cntr+"_xsunc"],divdf[cntr+"_xs"]+errdf[cntr+"_xsunc"],alpha=0.2)
        
        #ax[1].plot(d1.df["Run #"],divdf[cntr+"_xs"],color="black",label=lab1,marker="o")
        #ax[1].fill_between(d1.df["Run #"],divdf[cntr+"_xs"]-errdf[cntr+"_xsunc"],divdf[cntr+"_xs"]+errdf[cntr+"_xsunc"],alpha=0.2)


        ax[0].set_yscale('log')
        ax[0].set_ylim([0.000000000000001,0.00000001])#log scale
        divclean = divdf[divdf[cntr+"_xs"] != None]
        divclean = divclean[divclean[cntr+"_xs"] < 1000000000000000000]
        divstd = np.std(divclean[cntr+"_xs"][:-1])
        ax[1].set_ylim([1-3*divstd,1+3*divstd])
        ax[1].set_xlim([0,18])

        #ax[0].set_xlabel("Run #",fontsize=14)
        ax[0].set_ylabel(r'Cross section cm$^{-2}$',fontsize=14)
        ax[0].tick_params(labelsize=12)
        ax[0].locator_params(axis='x',nbins=5)
        #plt.locator_params(axis='y',nbins=4)
        ax[0].yaxis.get_offset_text().set_fontsize(12)
        ax[0].xaxis.set_minor_locator(MultipleLocator(1))
        #ax.yaxis.set_minor_locator(MultipleLocator(0.000000000000005))
        ax[0].tick_params(axis="x",bottom=True,direction="in",which="both")
        ax[0].tick_params(axis="y",bottom=True,direction="in",which="both")
        ax[1].set_ylabel("Chip"+str(d1.chip)+"/Chip"+str(d2.chip),fontsize=14)
        ax[1].set_xlabel("Run #",fontsize=14)
        ax[1].tick_params(labelsize=12)
        ax[1].locator_params(axis='x',nbins=5)
        ax[1].xaxis.set_minor_locator(MultipleLocator(1))
        ax[1].tick_params(axis="x",bottom=True,direction="in",which="both")


        ax[0].legend(loc=3,fontsize=14,bbox_to_anchor=(0.4,0.4))
        figname = makeFigureFile("seu_xs_per_chip_"+cntr,".png",args.name,"both")
        plt.savefig(figname,bbox_inches="tight")
        plt.close()
        #plt.show()

        print("Saving resulting figure in ",figname)

