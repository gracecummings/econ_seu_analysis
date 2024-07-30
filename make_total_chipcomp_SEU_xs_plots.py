import matplotlib.pyplot as plt
import pandas as pd
import mplhep as hep
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
from datetime import date
from hexaboardAndChip import HexaInfo
import numpy as np

def makeFigureFile(descrip,ftype,hexab,chipn):
    if not os.path.exists("figures/"+str(date.today())+"/"):
        os.makedirs("figures/"+str(date.today())+"/")
    outFile = "figures/"+str(date.today())+"/"+descrip+"_"+hexab+"_chip"+chipn+ftype
    return outFile

if __name__=='__main__':
    #d1path = '../data/seu_total_xs_per_tmrblock_per_ff_cleaned_hexa48.csv'
    #d2path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa44.csv'
    #d3path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa42.csv'
    #d4path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa43.csv'

    #d1path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa42_ECONT_jun24.csv'
    d1path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa43_ECOND_jun24.csv'
    #d2path = '../data/seu_total_xs_per_tmrblock_per_ff_hexa44_ECONT_jun24.csv'
    d2path = '../../ECOND_Aug2023_SEU_Analysis/data/seu_total_xs_per_tmrblock_per_ff_hexa43_ECOND_jan24.csv'
    d1 = HexaInfo(d1path)
    d2 = HexaInfo(d2path)
    #d3 = HexaInfo(d3path)
    #d4 = HexaInfo(d4path)
    #lab1 = "Chip {0}, front 2023-08 (higher fluence)".format(d1.chip)
    #lab2 = "Chip {0}, back 2023-08".format(d2.chip)
    #lab3 = "Chip {0}, front 2024-01 (higher fluence)".format(d3.chip)
    #lab4 = "Chip {0}, back 2024-01".format(d4.chip)

    lab1 = "Chip {0}, June 2024".format(d1.chip)
    #lab2 = "Chip {0}, front(higher fluence)".format(d2.chip)
    lab2 = "Chip {0}, January 2024".format("ECONDP1v2-603")

    d1tmr = d1.df.columns[1:]
    d2tmr = d2.df.columns[1:]
    #d3tmr = d3.df.columns[1:]
    #d4tmr = d4.df.columns[1:]

    print(d2.df)
    
    d1xsfull    = d1.df.iloc[0][1:]
    d1xsuncfull = d1.df.iloc[1][1:]
    #d2xsfull    = d2.df.iloc[0][1:]
    #d2xsuncfull = d2.df.iloc[1][1:]

    d2xsfull    = d2.df.iloc[2][1:]
    d2xsuncfull = d2.df.iloc[3][1:]
    
    #d3xsfull    = d3.df.iloc[2][1:]
    #d3xsuncfull = d3.df.iloc[3][1:]
    #d4xsfull    = d4.df.iloc[2][1:]
    #d4xsuncfull = d4.df.iloc[3][1:]

    errdivfullfront = d1xsfull/d2xsfull*((d1xsuncfull/d1xsfull)**2+(d2xsuncfull/d2xsfull)**2)**(1/2)
    divfullfront = d1xsfull/d2xsfull
    
    #errdivfullfront = d1xsfull/d3xsfull*((d1xsuncfull/d1xsfull)**2+(d3xsuncfull/d3xsfull)**2)**(1/2)
    #errdivfullback = d2xsfull/d4xsfull*((d2xsuncfull/d2xsfull)**2+(d4xsuncfull/d4xsfull)**2)**(1/2)
    #divfullfront = d1xsfull/d3xsfull
    #divfullback = d2xsfull/d4xsfull

    tmrnamesfull = list(set(d1tmr).intersection(set(d2tmr)))
    tmrlost  = list(set(d1tmr).symmetric_difference(set(d2tmr)))

    tmrnames = []
    d1xs = [] 
    d1xsunc = []
    d2xs = []
    d2xsunc = []
    d3xs = []
    d3xsunc = []
    d4xs = []
    d4xsunc = [] 
    errdivfront = []
    divfront = []
    errdivback = []
    divback = []

    tmrnamesfull = sorted(tmrnamesfull)
    
    for name in tmrnamesfull:
        if 'Ch' in name:
            continue
        else:
            tmrnames.append(name.split("cnt_")[-1])
            d1xs.append(d1xsfull[name])
            d1xsunc.append(d1xsuncfull[name])
            d2xs.append(d2xsfull[name])
            d2xsunc.append(d2xsuncfull[name])

            #d3xs.append(d3xsfull[name])
            #d3xsunc.append(d3xsuncfull[name])
            #d4xs.append(d4xsfull[name])
            #d4xsunc.append(d4xsuncfull[name])

            
            errdivfront.append(errdivfullfront[name])
            divfront.append(divfullfront[name])

            #errdivback.append(errdivfullback[name])
            #divback.append(divfullback[name])
    
    if len(tmrlost)>0:
        print("Unmathced TMR counters: ",tmrlost)

    print(d1xs)
        
    fig, ax  = plt.subplots(2,1,height_ratios=[2.25,1],figsize=(9,7),dpi=100)
    #fig, ax  = plt.subplots(3,1,height_ratios=[2.25,1,1],figsize=(7,10),dpi=100)
    hep.style.use("CMS")
    hep.cms.text("Internal",loc=1,fontsize=18,ax=ax[0])
    hep.cms.label("xs per FF", loc=2,fontsize=18,data=True,llabel="xs per FF",rlabel="",ax=ax[0])
    #ax[0].text(0.05,0.9,"ECONT-Prod, xs per FF",transform=ax[0].transAxes,fontsize=14,fontstyle='italic',fontweight='bold')
    
    ax[0].errorbar(tmrnames,d1xs,yerr=d1xsunc,label=lab1,fmt="o-")
    ax[0].errorbar(tmrnames,d2xs,yerr=d2xsunc,label=lab2,fmt="o-")
    #ax[0].errorbar(tmrnames,d3xs,yerr=d3xsunc,label=lab3,fmt="o-")
    #ax[0].errorbar(tmrnames,d4xs,yerr=d4xsunc,label=lab4,fmt="o-")
    ax[1].errorbar(tmrnames,divfront,yerr=errdivfront,color="black",marker="o",linestyle='None')
    ax[1].axhline(1)
    #ax[2].errorbar(tmrnames,divback,yerr=errdivback,color="black",marker="o",linestyle='None')
    #ax[2].axhline(1)
        
    #ax[0].set_yscale('log')
    #ax[0].set_ylim([0.000000000000001,0.0000000000001])#log scale
    ax[0].set_ylim([0.00000000000001,0.00000000000005])#linae scale
    
    ax[0].set_ylabel(r'Cross section cm$^{-2}$',fontsize=14,loc='top')
    ax[0].tick_params(labelsize=10)
    ax[0].yaxis.get_offset_text().set_fontsize(10)
    ax[0].tick_params(axis="x",labelbottom=False,direction="in",which="both")
    ax[0].tick_params(axis="y",bottom=True,direction="in",which="both")

    #ax[1].set_ylabel(str(d1.chip)+"/"+str(d2.chip),fontsize=14,loc='top')
    ax[1].set_ylabel(str(d1.chip)+"/ECONDp1v2",fontsize=14,loc='top')
    ax[1].tick_params(labelsize=10)
    ax[1].xaxis.set_minor_locator(MultipleLocator(1))
    ax[1].set_xlabel("Block",fontsize=14,loc='right')
    #ax[1].tick_params(axis="x",labelbottom=False,direction="in",which="both")
    ax[1].tick_params(axis="x",bottom=True,direction="in",which="both",labelrotation=60)
    ax[1].tick_params(axis="x",bottom=True,direction="in",which="both")

    #ax[2].tick_params(axis="x",bottom=True,direction="in",which="both",labelrotation=60)
    #ax[2].set_xticklabels(ax[2].get_xticklabels(),ha='right')
    #ax[2].set_ylabel("Chip"+str(d2.chip)+"/Chip"+str(d4.chip),fontsize=14,loc='top')
    #ax[2].set_xlabel("Block",fontsize=14,loc='right')
    #ax[2].tick_params(labelsize=10)
    #ax[2].locator_params(axis='x',nbins=5)
    #ax[2].xaxis.set_minor_locator(MultipleLocator(1))
    #ax[2].tick_params(axis="x",bottom=True,direction="in",which="both")
        
    ax[0].legend(loc=3,fontsize=11,bbox_to_anchor=(0.3,0.55),frameon=False)
    fig.tight_layout()
    #plt.show()

    figname = makeFigureFile("total_xs_chip_comp_allblocksbutChAl",".png","prelimcompecontprodjune_ECONDp1v2ECOND","both")
    fignamepdf = makeFigureFile("total_xs_chip_comp_allblocksbutChAl",".pdf","prelimcomecontpradjune_ECONDp1v2ECOND","both")
    plt.savefig(figname,bbox_inches="tight")
    plt.savefig(fignamepdf,bbox_inches="tight")
    
    
