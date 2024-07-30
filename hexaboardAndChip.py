import pandas as pd

chipdict = {#"hexa44":1,
            #"hexa48":4,
            #"hexa43":603,
            #"hexa42":604}
            "hexa42":"ECONT-001",
            "hexa43":"ECOND-001",
            "hexa44":"ECONT-002"}#need to adapt for other runs

class HexaInfo:
    def __init__(self,path):
        self.path = path
        self.df = pd.read_csv(self.path)
        hexnum = self.path.split("_")[-3].split(".csv")[0]
        self.chip = str(chipdict[hexnum])
        self.hexaboard = hexnum.split("hexa")[-1]
        tmrinfall = [x for x in list(self.df.columns) if 'tmr' in x]
        self.tmrnames = [x[:-3] for x in tmrinfall if 'unc' not in x]

        
