import argparse
import json
import glob
import numpy as np

def countsTotal(x):
    #if all registers are identically zero, this is likely an I2C NACK, not actually a rollover
    allZeros = (x[1:]==0).all(axis=1).reshape(-1,1)
    rollOvers = ((x[1:]-x[:-1])<0)
    rollOvers = (rollOvers & ~allZeros).sum(axis=0)
    return rollOvers*256 + x[-1]

if __name__=='__main__':
    #get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-hexa","--hexaboard", type=int,help = "hexaboard number")
    parser.add_argument("-j","--json", type=str,help = "file with tmr counts")
    parser.add_argument("--target","--target", type=str,help = "chip flavor: ECOND or ECONT")
    parser.add_argument("-p","--fluence", type=float,help = "fluence in scientific notation")
    parser.add_argument("-all","--allblocks", type=bool,default=False,help = "calc XS for all blocks, not just largest")
    parser.add_argument("-combo","--combineruns",type=bool,default=False,help = "calc XS combining runs on the fly")
    args = parser.parse_args()

    #Inputs needed to calculate the xs
    if args.target == 'ECOND':
        bitsf = json.load(open('econd_tmr_numbbits.json'))
    elif args.target == 'ECONT':
        bitsf = json.load(open('econt_tmr_numbbits.json'))
    else:
        print("No clue what chip you want to calculate the xs for, try again, with a good target.")
        bitsf = []

    maxblock = max(bitsf,key=bitsf.get)
    nbits = bitsf[maxblock]
    hexab  = args.hexaboard
    fluenc = args.fluence

    
    if not args.allblocks and not args.combineruns:
        f = json.load(open(args.json))
        tmrerridx = f['tests'][1]['metadata']['tmr_err_names'].index(maxblock)
        corrcounts = countsTotal(np.array(f['tests'][1]['metadata']['tmr_err_cnts']))
        #tmrcounts = f['tests'][1]['metadata']['tmr_err_cnts'][-1][tmrerridx]#last read of counts in max block
        tmrcounts = corrcounts[tmrerridx]#last read of counts in max block
        
        xs = tmrcounts/nbits/fluenc

        print("Checking XS for largest block: ",maxblock)
        print("             Fluence [1/cm^2]: ",fluenc)
        print("               Number of bits: ",nbits)
        print("               Number of errs: ",tmrcounts)
        print("        xs (errs/bits/fluence): ",xs)

    elif not args.allblocks and args.combineruns:
        fnames = glob.glob('Run*testReport_hexa'+str(hexab)+'*')
        tmrcounts = 0
        for f in fnames:
            f = json.load(open(f))
            tmrerridx = f['tests'][1]['metadata']['tmr_err_names'].index(maxblock)
            corrcounts = countsTotal(np.array(f['tests'][1]['metadata']['tmr_err_cnts']))
            tmrcounts += corrcounts[tmrerridx]#last read of counts in max block
        xs = tmrcounts/nbits/fluenc

        print("Checking XS for largest block: ",maxblock)
        print("      Number of combined runs: ",len(fnames))
        print("             Fluence [1/cm^2]: ",fluenc)
        print("               Number of bits: ",nbits)
        print("               Number of errs: ",tmrcounts)
        print("        xs (errs/bits/fluence): ",xs)

    elif args.allblocks and not args.combineruns:
        f = json.load(open(args.json))
        nbits =sum(bitsf.values())
        corrcounts = countsTotal(np.array(f['tests'][1]['metadata']['tmr_err_cnts']))
        tmrcounts = sum(corrcounts)
        xs = tmrcounts/nbits/fluenc
        
        print("Checking XS using all bits")
        print("          Fluence [1/cm^2]: ",fluenc)
        print("            Number of bits: ",nbits)
        print("            Number of errs: ",tmrcounts)
        print("    xs (errs/bits/fluence): ",xs)
        
    elif args.allblocks and args.combineruns:
        fnames = glob.glob('Run*testReport_hexa'+str(hexab)+'*')
        tmrcounts = 0
        for f in fnames:
            f = json.load(open(f))
            corrcounts = countsTotal(np.array(f['tests'][1]['metadata']['tmr_err_cnts']))
            tmrcounts += sum(corrcounts)
        xs = tmrcounts/nbits/fluenc

        print("Checking XS for all bits")
        print("      Number of combined runs: ",len(fnames))
        print("             Fluence [1/cm^2]: ",fluenc)
        print("               Number of bits: ",nbits)
        print("               Number of errs: ",tmrcounts)
        print("        xs (errs/bits/fluence): ",xs)

        
