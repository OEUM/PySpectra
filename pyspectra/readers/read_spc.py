import spc_spectra as spc
import pandas as pd
from os import listdir
from os.path import isfile, join

def read_spc(filename):

    f=spc.File(filename) #Read file
    #Extract X & y
    if f.dat_fmt.endswith('-xy'):
        for s in f.sub:
            x=s.x
            y=s.y
    else:
        for s in f.sub:
            x = f.x
            y = s.y

    Spec=pd.Series(y,index=x)

    return Spec

def read_spc_dir(Directory, ext='.spc', orient='Row'):

    #Read all files from directory and create a list, also ensures that the extension of file is correct
    Flist = [f for f in listdir(Directory) if isfile(join(Directory, f)) and f.endswith(ext.upper()) or f.endswith(ext.lower())]

    SpectraDict={}
    #Read all of them an add them to a dictionary
    for file in Flist:
        Spec=read_spc(Directory + "/" + file)
        SpectraDict[file]=Spec

    #Decide the orientation of dataframe, column-wise or row-wise.
    if orient=='Row':
        SpectraDataFrame=pd.DataFrame(SpectraDict).transpose()
    else:
        SpectraDataFrame = pd.DataFrame(SpectraDict)

    return SpectraDataFrame, SpectraDict
