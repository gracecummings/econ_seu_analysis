import argparse
import json
import glob

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
        tmrcounts = f['tests'][1]['metadata']['tmr_err_cnts'][-1][tmrerridx]#last read of counts in max block
        xs = tmrcounts/nbits/fluenc

        print("Checking XS for largest block: ",maxblock)
        print("             Fluence [1/cm^2]: ",fluenc)
        print("               Number of bits: ",nbits)
        print("               Number of errs: ",tmrcounts)
        print("        xs (errs/bits/fluence): ",xs)

    elif not args.allblocks and args.combineruns:
        fnames = glob.glob('testReport_hexa'+str(hexab)+'*')
        tmrcounts = 0
        for f in fnames:
            f = json.load(open(args.json))
            tmrerridx = f['tests'][1]['metadata']['tmr_err_names'].index(maxblock)
            tmrcounts += f['tests'][1]['metadata']['tmr_err_cnts'][-1][tmrerridx]#last read of counts in max block
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
        tmrcounts = sum(f['tests'][1]['metadata']['tmr_err_cnts'][-1])
        xs = tmrcounts/nbits/fluenc
        
        print("Checking XS using all bits")
        print("          Fluence [1/cm^2]: ",fluenc)
        print("            Number of bits: ",nbits)
        print("            Number of errs: ",tmrcounts)
        print("    xs (errs/bits/fluence): ",xs)
        

        
