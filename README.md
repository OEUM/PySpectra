# Pyspectra
Welcome to pyspectra. <br>
This package is intended to  put functions together to analyze and transform spectral data from multiple spectroscopy instruments. <br>

Currently supported input files are:
* .spc
* .dx

PySpectra is intended to facilitate working with spectroscopy files in python by using a friendly  integration with pandas dataframe objects. <br>.
Also pyspectra provides a set of routines to execute spectral pre-processing like:<br>
* MSC
* SNV
* Detrend
* Savitzky - Golay
* Derivatives
* ..

Data spectra can be used for traditional chemometrics analysis but also can be used in general advanced analytics modelling in order to deliver additional  information to manufacturing models by supplying spectral information.


```python
#Import basic libraries
import spc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
```

# Read .spc file
## Read a single file


```python
from pyspectra.readers.read_spc import read_spc
spc=read_spc('pyspectra/sample_spectra/VIAVI/JDSU_Phar_Rotate_S06_1_20171009_1540.spc')
spc.plot()
plt.xlabel("nm")
plt.ylabel("Abs")
plt.grid(True)
print(spc.head())
```

    gx-y(1)
    908.100000    0.123968
    914.294355    0.118613
    920.488710    0.113342
    926.683065    0.108641
    932.877419    0.098678
    dtype: float64
    


![Single spc spectra](https://github.com/OEUM/PySpectra/blob/main/images/output_3_1_SingleSpectraSPC.png?raw=true)


## Read multiple .spc files from a directory


```python
from pyspectra.readers.read_spc import read_spc_dir

df_spc, dict_spc=read_spc_dir('pyspectra/sample_spectra/VIAVI')
display(df_spc.transpose())
f, ax =plt.subplots(1, figsize=(18,8))
ax.plot(df_spc.transpose())
plt.xlabel("nm")
plt.ylabel("Abs")
ax.legend(labels= list(df_spc.transpose().columns))
plt.show()
```

    gx-y(1)
    gx-y(1)
    gx-y(1)
    gx-y(1)
    gx-y(1)
    gx-y(1)
    gx-y(1)
    gx-y(1)
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>JDSU_Phar_Rotate_S06_1_20171009_1540.spc</th>
      <th>JDSU_Phar_Rotate_S11_2_20171009_1614.spc</th>
      <th>JDSU_Phar_Rotate_S17_1_20171009_1652.spc</th>
      <th>JDSU_Phar_Rotate_S23_1_20171009_1734.spc</th>
      <th>JDSU_Phar_Rotate_S30_2_20171009_1815.spc</th>
      <th>JDSU_Phar_Rotate_S37_2_20171009_1853.spc</th>
      <th>JDSU_Phar_Rotate_S43_2_20171009_1928.spc</th>
      <th>JDSU_Phar_Rotate_S49_1_20171009_2000.spc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>908.100000</th>
      <td>0.123968</td>
      <td>0.164750</td>
      <td>0.156647</td>
      <td>0.147828</td>
      <td>0.182833</td>
      <td>0.171957</td>
      <td>0.164471</td>
      <td>0.149373</td>
    </tr>
    <tr>
      <th>914.294355</th>
      <td>0.118613</td>
      <td>0.159980</td>
      <td>0.150746</td>
      <td>0.142974</td>
      <td>0.178452</td>
      <td>0.166827</td>
      <td>0.159545</td>
      <td>0.142818</td>
    </tr>
    <tr>
      <th>920.488710</th>
      <td>0.113342</td>
      <td>0.155193</td>
      <td>0.144959</td>
      <td>0.138178</td>
      <td>0.173734</td>
      <td>0.161695</td>
      <td>0.154330</td>
      <td>0.136648</td>
    </tr>
    <tr>
      <th>926.683065</th>
      <td>0.108641</td>
      <td>0.151398</td>
      <td>0.140178</td>
      <td>0.134014</td>
      <td>0.170061</td>
      <td>0.157110</td>
      <td>0.149876</td>
      <td>0.130452</td>
    </tr>
    <tr>
      <th>932.877419</th>
      <td>0.098678</td>
      <td>0.141859</td>
      <td>0.129715</td>
      <td>0.124426</td>
      <td>0.160590</td>
      <td>0.147076</td>
      <td>0.140119</td>
      <td>0.119561</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1651.422581</th>
      <td>0.220935</td>
      <td>0.262070</td>
      <td>0.259643</td>
      <td>0.242916</td>
      <td>0.279041</td>
      <td>0.271492</td>
      <td>0.260664</td>
      <td>0.252704</td>
    </tr>
    <tr>
      <th>1657.616935</th>
      <td>0.221848</td>
      <td>0.262732</td>
      <td>0.260664</td>
      <td>0.243092</td>
      <td>0.278962</td>
      <td>0.272893</td>
      <td>0.261647</td>
      <td>0.254481</td>
    </tr>
    <tr>
      <th>1663.811290</th>
      <td>0.219904</td>
      <td>0.260335</td>
      <td>0.258975</td>
      <td>0.240656</td>
      <td>0.276382</td>
      <td>0.271624</td>
      <td>0.260278</td>
      <td>0.253761</td>
    </tr>
    <tr>
      <th>1670.005645</th>
      <td>0.214080</td>
      <td>0.253475</td>
      <td>0.253110</td>
      <td>0.234047</td>
      <td>0.269528</td>
      <td>0.265615</td>
      <td>0.254568</td>
      <td>0.248288</td>
    </tr>
    <tr>
      <th>1676.200000</th>
      <td>0.204217</td>
      <td>0.242375</td>
      <td>0.243082</td>
      <td>0.223539</td>
      <td>0.258771</td>
      <td>0.255306</td>
      <td>0.244826</td>
      <td>0.238663</td>
    </tr>
  </tbody>
</table>
<p>125 rows × 8 columns</p>
</div>



![Multiple spectra spc](https://github.com/OEUM/PySpectra/blob/main/images/output_5_2_MultiSpectraSPC.png?raw=true)


# Read .dx spectral files
Pyspectra is also built with a set of regex that allows to read the most common .dx file formats from different vendors like:
 * FOSS
 * Si-Ware Systems
 * Spectral Engines
 * Texas Instruments
 * VIAVI

## Read a single .dx file
.dx reader can read:
* Single files containing single spectra : read
* Single files containing multiple spectra : read
* Multiple files from directory : read_from_dir
### Single file, single spectra


```python
# Single file with single spectra
from pyspectra.readers.read_dx import read_dx
#Instantiate an object
Foss_single= read_dx()
# Run  read method
df=Foss_single.read(file='pyspectra/sample_spectra/DX multiple files/Example1.dx')
df.transpose().plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1f44faa7940>




![Single DX spectra](https://github.com/OEUM/PySpectra/blob/main/images/output_8_1_SingleSpectraDX.png?raw=true)


### Single file, multiple spectra:
.dx reader stores all the information as attributes of the object on Samples. Each key represent a sample.


```python
Foss_single= read_dx()
# Run  read method
df=Foss_single.read(file='pyspectra/sample_spectra/FOSS/FOSS.dx')
df.transpose().plot(legend=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1f44f7f2e50>




![Multi DX spectra](https://github.com/OEUM/PySpectra/blob/main/images/output_10_1_MultiSpectraDX.png?raw=true)



```python
for c in Foss_single.Samples['29179'].keys():
    print(c)
```

    y
    Conc
    TITLE
    JCAMP_DX
    DATA TYPE
    CLASS
    DATE
    DATA PROCESSING
    XUNITS
    YUNITS
    XFACTOR
    YFACTOR
    FIRSTX
    LASTX
    MINY
    MAXY
    NPOINTS
    FIRSTY
    CONCENTRATIONS
    XYDATA
    X
    Y
    

# Spectra preprocessing
Pyspectra has a set of built in classes to perform spectra  pre-processing like: <br>
* MSC: Multiplicative scattering correction
* SNV: Standard normal variate
* Detrend
* n order derivative
* Savitzky golay smmothing


```python
from pyspectra.transformers.spectral_correction import msc, detrend ,sav_gol,snv
```


```python
MSC= msc()
MSC.fit(df)
df_msc=MSC.transform(df)


f, ax= plt.subplots(2,1,figsize=(14,8))
ax[0].plot(df.transpose())
ax[0].set_title("Raw spectra")

ax[1].plot(df_msc.transpose())
ax[1].set_title("MSC spectra")
plt.show()
```


![MSC transformation](https://github.com/OEUM/PySpectra/blob/main/images/output_14_0_MSC.png?raw=true)



```python
SNV= snv()
df_snv=SNV.fit_transform(df)

Detr= detrend()
df_detrend=Detr.fit_transform(spc=df_snv,wave=np.array(df_snv.columns))

f, ax= plt.subplots(3,1,figsize=(18,8))
ax[0].plot(df.transpose())
ax[0].set_title("Raw spectra")

ax[1].plot(df_snv.transpose())
ax[1].set_title("SNV spectra")

ax[2].plot(df_detrend.transpose())
ax[2].set_title("SNV+ Detrend spectra")

plt.tight_layout()
plt.show()
```


![SNV and Detrend transformations](https://github.com/OEUM/PySpectra/blob/main/images/output_15_0_SNV_Detrend.png?raw=true)


# Modelling of spectra

## Decompose using PCA


```python
pca=PCA()
pca.fit(df_msc)
plt.figure(figsize=(18,8))
plt.plot(range(1,len(pca.explained_variance_)+1),100*pca.explained_variance_.cumsum()/pca.explained_variance_.sum())
plt.grid(True)
plt.xlabel("Number of components")
plt.ylabel(" cumulative % of explained variance")
```




   




![PCAcumulative variance](https://github.com/OEUM/PySpectra/blob/main/images/output_18_1_PCA_Variance.png?raw=true)



```python
df_pca=pd.DataFrame(pca.transform(df_msc))
plt.figure(figsize=(18,8))
plt.plot(df_pca.loc[:,0:25].transpose())


plt.title("Transformed spectra PCA")
plt.ylabel("Response feature")
plt.xlabel("Principal component")
plt.grid(True)
plt.show()
```


![Transformed PCA values](https://github.com/OEUM/PySpectra/blob/main/images/output_19_0_PCA_values.png?raw=true)


## Using automl libraries to deploy faster models


```python
import tpot
from tpot import TPOTRegressor
from sklearn.model_selection import RepeatedKFold
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
model = TPOTRegressor(generations=10, population_size=50, scoring='neg_mean_absolute_error',
                      cv=cv, verbosity=2, random_state=1, n_jobs=-1)
```


```python
y=Foss_single.Conc[:,0]
x=df_pca.loc[:,0:25]
model.fit(x,y)
```


    HBox(children=(FloatProgress(value=0.0, description='Optimization Progress', max=550.0, style=ProgressStyle(de…


    
    Generation 1 - Current best internal CV score: -0.30965836730187607
    
    Generation 2 - Current best internal CV score: -0.30965836730187607
    
    Generation 3 - Current best internal CV score: -0.30965836730187607
    
    Generation 4 - Current best internal CV score: -0.308295313408046
    
    Generation 5 - Current best internal CV score: -0.308295313408046
    
    Generation 6 - Current best internal CV score: -0.308295313408046
    
    Generation 7 - Current best internal CV score: -0.308295313408046
    
    Generation 8 - Current best internal CV score: -0.3082953134080456
    
    Generation 9 - Current best internal CV score: -0.3082953134080456
    
    Generation 10 - Current best internal CV score: -0.3078569602146527
    
    Best pipeline: LassoLarsCV(PCA(LinearSVR(input_matrix, C=0.1, dual=True, epsilon=0.1, loss=epsilon_insensitive, tol=0.01), iterated_power=3, svd_solver=randomized), normalize=False)
    




    TPOTRegressor(cv=RepeatedKFold(n_repeats=3, n_splits=10, random_state=1),
                  generations=10, n_jobs=-1, population_size=50, random_state=1,
                  scoring='neg_mean_absolute_error', verbosity=2)




```python
from sklearn.metrics import r2_score
r2=round(r2_score(y,model.predict(x)),2)
plt.scatter(y,model.predict(x),alpha=0.5, color='r')
plt.plot([y.min(),y.max()],[y.min(),y.max()],LineStyle='--',color='black')
plt.xlabel("y actual")
plt.ylabel("y predicted")
plt.title("Spectra model prediction R^2:"+ str(r2))

plt.show()
```


![TPOT model fit](https://github.com/OEUM/PySpectra/blob/main/images/output_23_0_model_fit.png?raw=true)

