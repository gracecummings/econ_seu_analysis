import json
import pandas as pd
import numpy as np
import glob
import re
import argparse

hexacontrollers = [42,43,44]

target = 'ECONT'
firmdict = {'ECOND':'econ-d','ECONT':'econ-t'}
lengthdict = {'ECOND':51,'ECONT':48}

def countsTotal(x):
    #if all registers are identically zero, this is likely an I2C NACK, not actually a rollover
    allZeros = (x[1:]==0).all(axis=1).reshape(-1,1)
    rollOvers = ((x[1:]-x[:-1])<0)
    rollOvers = (rollOvers & ~allZeros).sum(axis=0)
    return rollOvers*256 + x[-1]

if __name__=='__main__':
    #get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--target","--target", type=str,help = "chip flavor: ECOND or ECONT")
    args = parser.parse_args()
    
    target = args.target
    errorCountLists=[]
    hexaData={}
    regNames = None
    for hexaNumber in hexacontrollers:
        hexa = f'hexa{hexaNumber}'
        hexaDataFiles = glob.glob(f'../logs/{hexa}/Run*json')
        fileNames=np.array(hexaDataFiles)
        fileNames.sort()
        print("Hexa: ",hexa)
        
        for fname in fileNames:
            runNum=re.findall('Run_(\w*)_test',fname)[0].split('_')[0]
            if "Run_01_PRBS_testReport_hexa44_2024-06-22_11-07-34.json" in fname:
                print("Skipping hexa44 run 1, remember to investigate")
                continue

            data=json.load(open(fname))
            firmware = data['firmware_name']
            if firmdict[target] not in firmware:
                continue

            print("adding info to csv")
            testNumber = -1
            for i in range(len(data['tests'])):
                id = data['tests'][i]['nodeid']
                if "beam_running" in id:
                    testNumber = i
            try:
                if regNames is None:
                    regNames=data['tests'][testNumber]['metadata']['tmr_err_names']
                errCounts=data['tests'][testNumber]['metadata']['tmr_err_cnts']
                errCounts=np.array(errCounts)
                errCounts=countsTotal(errCounts).tolist()
            except:
                errCounts=[0]*lengthdict[target]
            errorCountLists.append([runNum,hexaNumber]+errCounts)

    df=pd.DataFrame(errorCountLists)
    df.columns=['Run','Hexacontroller']+regNames

    filename = '../data/tmr_error_counts_by_run_'+target+'.csv'
    
    df.to_csv(filename,index=False)
