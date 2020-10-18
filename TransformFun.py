import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spc
import os
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA


def ReadSpectra(filename):

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

def ReadFromDir(Directory,ext='.spc',orient='Row'):

    #Read all files from directory and create a list, also ensures that the extension of file is correct
    Flist = [f for f in listdir(Directory) if isfile(join(Directory, f)) and f.endswith(ext)]

    SpectraDict={}
    #Read all of them an add them to a dictionary
    for file in Flist:
        Spec=ReadSpectra(Directory+"/"+file)
        SpectraDict[file]=Spec

    #Decide the orientation of dataframe, column-wise or row-wise.
    if orient=='Row':
        SpectraDataFrame=pd.DataFrame(SpectraDict).transpose()
    else:
        SpectraDataFrame = pd.DataFrame(SpectraDict)

    return SpectraDataFrame, SpectraDict

class GeneralTransformer():

    def __init__(self):
        pass

    def fit_transform(self,spc):
        self.fit(spc)
        return self.transform(spc)


class SNV(GeneralTransformer):
    def __init__(self):
        '''
        Performs standard normal variate transformation.

        '''
        self.MeanSpectra=None
        self.StdSpectra=None

    def fit(self,spc):
        self.MeanSpectra=spc.mean(axis=0)
        self.StdSpectra=spc.std(axis=0)
        return None

    def transform(self,spc):
        return (spc -self.MeanSpectra)/self.StdSpectra

class MSC(GeneralTransformer):
    def __init__(self):
        '''
        spc: Input dataframe of spectra
        Conduct multiple scattering correction
        '''
        self.MeanSpectra=None

    def fit(self,spc):
        self.MeanSpectra= np.array(spc.mean(axis=0))

    def transform(self,spc):
        import numpy as np
        def transformMSC(xi,MeanSpectra):
            m,b= np.polyfit(MeanSpectra,xi,1)
            return (xi-b)*m

        return spc.apply(transformMSC,args=(self.MeanSpectra,),axis=1)


class Transformer():
    import numpy as np
    import pandas as pd
    def __init__(self):
        self.spectra=None
        self.MeanSpectra=None
        self.StDevSpectra=None

    def initial_validation(self):
        if self.spectra != None:
            self.MeanSpectra= self.spectra.mean(axis=0)
            self.StDevSpectra=self.spectra.std(axis=0)

    def SNV(self,spc):
        '''
        spc: Input dataframe of spectra
        return: dataframe after SNV

        '''
        pass

    def MSC(self):
        pass

    def Detrend(self):
        pass

    def Transform(self,spc,methods):
        '''
        :param spc: Input dataframe with all spectra samples
        :param methods: List  with dictionary ordered methods
        :return: Transformed dataframe
        '''
        #Input data
        pass


