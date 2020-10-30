# DX file is a plain text
# Use RegEx for read and split data
import re
import numpy as np
import matplotlib.pyplot as plt
file =r'C:\Users\uv7301\OneDrive - DuPont\Git\Spectra\SampleFiles\Raman\Raman_pectin_juice_spectra_Brab_2020\Raman_pectin_juice_spectra_Brab_2020\DUPONT_T11543-001A_0_0_20170906-144037_en.0.dx'

class DXReader():

    def __init__(self):

        pass

    def read(self,file):

        self.FileName=file

        #Open the file
        f= open(file,"r")
        #Loop over the lines
        self.Params={} # Empty dict to store params
        self.x=[]  # Initialize empty list to store data
        self.y=[] #Initialize empty list to store data
        for line in f:
            line = line.replace("\n", "") # Delete line break
            if line[0:2]=='##': # It is a parameter, starts with....
                try:
                    # Extract data  as  ##Param = value
                    param_name, value =re.findall('##(.+)=(.+)',line)[0]
                    print(param_name,"=",value)
                    # Save it as dictionary
                    self.Params[param_name]=value
                except Exception as ex:
                    print(ex)
            else:

                #if doesn´t start with ## then it spectral data
                # extend data into the list
                # each line is read and splitted using +- separator
                # Only read from position 1 to end, since position 0 is X reference
                # Uses also the latest param to enter to  loop
                if param_name=='CONCENTRATIONS':
                    pass

                if self.Params['XYDATA']=='(X++(Y..Y))' and param_name=='XYDATA':

                    #Regex description:
                    #Starts with 0 or 1 '+', then 0 or 1 '-', then digits with 1 or more repetitions
                    #Then a decimal point (0 or 1) and then digits optional
                    splitted = re.findall('\+?\-?\d{1,}\.?\d{1,}?', line)
                    self.y.extend(splitted[1:])

                elif self.Params['XYDATA']=='(XY..XY)' and param_name=='XYDATA': #SpectralEngines
                    #Data is in format  X, Y; X, Y;.
                    #Catches numbers that end with ;  and then remove it using a comprehension list
                    splitted = re.findall('\+?\-?\d{1,}\.?\d{1,}?\;', line)
                    self.y.extend([val.replace(';','') for val in splitted])
                else:
                    pass

        #Now convert data to numeric
        #Each spectra has an X and Y factor to multiply by
        self.x=np.linspace(float(self.Params['FIRSTX']),float(self.Params['LASTX']),int(self.Params['NPOINTS']))\
               *float(self.Params['XFACTOR'])
        self.y=np.array(list(map(float,self.y)))*float(self.Params['YFACTOR'])
        print("Done")



Spec=DXReader()
Spec.read(file)
plt.plot(Spec.x,Spec.y)
plt.grid(True)
plt.title(Spec.FileName)
5.7760576e-06