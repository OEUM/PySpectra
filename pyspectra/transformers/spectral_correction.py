
import numpy as np
from scipy.signal import savgol_filter
import pandas as pd
class GeneralTransformer():

    def __init__(self):
        pass


    def fit_transform(self,spc):
        self.fit(spc)
        return self.transform(spc)



class snv(GeneralTransformer):
    def __init__(self):
        '''
        Performs standard normal variate transformation.

        '''
        self.MeanSpectra=None
        self.StdSpectra=None

    def fit(self,spc):
        '''
        Calculates Standard normal variate transformation by:
            (xi - x_mean)/x_std
        :param spc: row wise dataframe of spectra. Each row is a different sample
        :return: Fitted object  with mean and std.
        '''
        self.MeanSpectra=spc.mean(axis=0)
        self.StdSpectra=spc.std(axis=0)
        return None

    def transform(self,spc):
        return (spc -self.MeanSpectra)/self.StdSpectra

class msc(GeneralTransformer):
    '''
    This function implements the multiplicative scatter correction method which attempts to remove physical light scatter
     by accounting for additive and multiplicative effects
     The Multiplicative Scatter Correction (MSC) is a normalization method that attempts to account for additive and
      multiplicative effects by aligning each spectrum (x_ix_i) with an ideal reference one (x_rx_r) as follows:

    x_i = m_i x_r + a_ix_i = m_i x_r + a_i MSC(x_i) = a_i - x_im_iMSC(x_i) = a_i - x_i/m_i
    where a_ia_i and m_im_i are the additive and multiplicative terms respectively.
    '''
    def __init__(self):
        '''
        spc: Input dataframe of spectra
        Conduct multiple scattering correction
        '''
        self.MeanSpectra=None

    def fit(self,spc):
        '''

        :param spc: Row wise input data frame
        :return:
        '''
        self.MeanSpectra= np.array(spc.mean(axis=0))

    def transform(self,spc):

        def transformMSC(xi,MeanSpectra):
            '''
            Fits coeffients of linear regression: (Mean spectra, spectra_i)
            :param xi: Each row or sample of spectra .
            :param MeanSpectra: Mean spectra of all samples.
            :return: Linear regression coefficients
            '''
            m,b= np.polyfit(MeanSpectra,xi,1)
            return (xi-b)*m

        return spc.apply(transformMSC,args=(self.MeanSpectra,),axis=1)


class detrend(GeneralTransformer):
    '''
    Normalizes each row of an input data.frame or matrix by  fitting a second order linear model and returning the fitted residuals.
    The detrend is a row-wise transformation that allows to correct for wavelength-dependent scattering effects (variations in curvilinearity).
    A second-degree polynomial is fit through each spectrum
    '''
    def __init__(self):

        self.MeanSpectra=None

    def fit(self,spc):
        pass

    def fit_transform(self,spc,wave,deg=2):
        '''

        :param spc:  Input  dataframe (row wise) with the Abs of each spectrum
        :param wave: Wavelength array vector
        :return:  Detrended  spectra array or matrix
        '''

        detrend_df= spc.apply(lambda x: x- np.polyval(np.polyfit(wave,x,deg), wave),axis=1)
        return  detrend_df


class derivative(GeneralTransformer):

    def __init__(self):

        pass

    def fit(self,spc):
        pass

    def fit_transform(self,spc, d=2,drop=True):
        '''

        :param spc:  Input  row wise dataframe to calculate derivative
        :param d:  Degree of derivative
        :param drop: Drop nan columns after derivation
        :return: Calculated derivated dataframe.
        '''

        df_deriv=spc.diff(d,axis=1)

        if drop:
            cols_to_drop= list(df_deriv.columns)[0:2]
            df_deriv.drop(columns=cols_to_drop,inplace=True)
        return df_deriv


class sav_gol(GeneralTransformer):

    def __init__(self):
        pass

    def fit(self):
        pass

    def transform(self,spc, window=7,poly=3,deriv=0):
        '''

        :param spc: Input row wise dataframe of spectra
        :param window: The length of the filter window (i.e., the number of coefficients). window_length must be a positive odd integer.
        :param poly:The order of the polynomial used to fit the samples. polyorder must be less than window_length.
        :param deriv: The order of the derivative to compute. This must be a nonnegative integer. The default is 0, which means to filter the data without differentiating.
        :return:
        '''

        self.orig_cols=np.array(spc.columns)
        self.min_wave= self.orig_cols.min()
        self.max_wave= self.orig_cols.max()

        df_sg=pd.DataFrame(savgol_filter(spc,window_length=window,polyorder=poly,axis=1,deriv=deriv))
        self.new_cols= np.linspace(self.min_wave,self.max_wave,len(df_sg.columns))

        #Rename index and columns from dataframe
        df_sg.index=spc.index
        df_sg.columns=self.new_cols

        return df_sg
