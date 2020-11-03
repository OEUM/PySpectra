import re
import numpy as np
import pandas as pd

class read_from_dx():

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


class read_from_dx_multi():

    def __init__(self):

        pass

    def read(self,file,start_code="##TITLE",end_code="##END"):

        start_code_len=len(start_code)
        end_code_len=len(end_code)

        self.FileName=file
        f= open(file,"r") #Open the file

        self.Params={} # Empty dict to store params
        self.x=[]  # Initialize empty list to store data
        self.y=[] #Initialize empty list to store data
        self.Samples={} # Dictionary to nest in multiple samples
        self.Y_matrix= np.array([])
        self.Conc=np.array([])
        start_key=None # Init none before first appear of title
        end_key=False

        # Loop over the lines
        param_name=""
        for line in f:
            line = line.replace("\n", "") # Delete line break

            if line[0:start_code_len]==start_code:

                _,start_key = re.findall('##(.+)\s*=\s*(.+)',line)[0] # get the title of the sample
                self.Samples[start_key]={} # Open a new dictionary for given sample defined by start key
                self.Samples[start_key]['y']=[] #Empty list to store Y data
                self.Samples[start_key]['Conc']=[] # Empty list t o store concentrations in case of needed

            if line[0:2]=='##': # It is a parameter, starts with....
                try:
                    # Extract data  as  ##Param = value, remove spaces from group with \s*
                    param_name, value =re.findall('##(.+)\s*=\s*(.+)',line)[0]
                    # Save it as dictionary
                    self.Samples[start_key][param_name]= value
                except Exception as ex:
                    param_name = re.findall('##(.+)\s*=', line)[0]
                    #print(line,"\n",ex)
                    pass
            else:
                pass

            #if doesn´t start with ## then it spectral data
            # extend data into the list
            # each line is read and splitted using +- separator
            # Only read from position 1 to end, since position 0 is X reference
            # Uses also the latest param to enter to  loop
            if param_name=='CONCENTRATIONS':
                try:
                    measure, value =re.findall('<(.+)>\s*,\s*(.+),',line)[0]
                    self.Samples[start_key]['Conc'].append(float(value))
                except Exception as ex:
                    #print(ex,line)
                    pass

            #print(start_key,param_name,self.Samples[start_key]['XYDATA'])
            if start_key  != None and param_name=='XYDATA':
                if self.Samples[start_key]['XYDATA']=='(X++(Y..Y))' and param_name=='XYDATA':

                    #Regex description:
                    #Starts with 0 or 1 '+', then 0 or 1 '-', then digits with 1 or more repetitions
                    #Then a decimal point (0 or 1) and then digits optional
                    splitted = re.findall('\+?\-?\d{1,16}\.?\d{1,16}', line)

                    self.Samples[start_key]['y'].extend(splitted[1:])

                elif self.Samples[start_key]['XYDATA']=='(XY..XY)' and param_name=='XYDATA': #SpectralEngines
                    #Data is in format  X, Y; X, Y;.
                    #Catches numbers that end with ;  and then remove it using a comprehension list
                    splitted = re.findall('\+?\-?\d{1,16}\.?\d{1,16}\;', line)
                    self.Samples[start_key]['y'].extend([val.replace(';','') for val in splitted])
                else:
                    pass


            if start_key != None and param_name == 'END':

                if line[0:end_code_len]==end_code:
                    end_key=True

                    if end_key:

                    #Define the end of file and transform to numeric
                        self.Samples[start_key]['X']=np.linspace(float(
                            self.Samples[start_key]['FIRSTX']),float(self.Samples[start_key]['LASTX'])
                            ,int(self.Samples[start_key]['NPOINTS']))*float(self.Samples[start_key]['XFACTOR'])
                        self.Samples[start_key]['Y']=np.array(list(map(float,self.Samples[start_key]['y'])))*float(self.Samples[start_key]['YFACTOR'])
                        # Y array matrix concatenation
                        if self.Y_matrix.shape[0]==0:
                            self.Y_matrix=self.Samples[start_key]['Y'] # 1st time
                            self.X_cols=self.Samples[start_key]['X']
                        else:
                            self.Y_matrix=np.vstack([self.Y_matrix,self.Samples[start_key]['Y']]) # Append and collect matrix
                        # Concentration matrix array
                        if self.Conc.shape[0]==0:
                            self.Conc=np.array(self.Samples[start_key]['Conc']) # 1st time

                        else:
                            self.Conc=np.vstack([self.Conc,self.Samples[start_key]['Conc']]) # Append and collect matrix

                        end_key=False # toggle off end key

        df=pd.DataFrame(data=self.Y_matrix,index=list(self.Samples.keys()))
        df.columns=self.Samples[start_key]['X']
        return df


