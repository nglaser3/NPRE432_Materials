import numpy as np 
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import os,sys,glob

def read_datafile(filepath):
    with open(filepath,'r') as file:
        propfile = file.readline().split(']')[0][1:]
        i = -3
        val = '0'
        while val != '1':
            string = file.readline()
            val = string.split(',')[0]
            i += 1
            
    FullData = pd.read_csv(filepath,header=i)
    Data = {'Raw':{},'Data':{}}
    units = {}
    for k in FullData.keys():
        vals = FullData[k]
        key_args = k.split(' ')
        param, unit = key_args[0],key_args[-1]
        vals = np.array(vals)
        try:
            vals = np.float64(vals)
            nan_i = np.where(np.isnan(vals))[0][0]
            Data['Data'][param] = vals[:nan_i]
        except:
            if param == 'Point':
                
                ind = np.where(vals=='[Raw Data]')[0][0]
                calc_data,raw_data = vals[:ind],vals[ind+2:]
                Data['Data'][param] = np.float64(calc_data)
                Data['Raw'][param] = np.float64(raw_data)
            else:
                calc_data,raw_data = vals[:ind],vals[ind+2:]
                Data['Data'][param] = np.float64(calc_data)
                Data['Raw'][param] = np.float64(raw_data)
            
        units[param] = unit if key_args[0] != 'Point' else 'N/A'
    Data['Units'] = units

    files = glob.glob(f'*/{propfile}*',recursive=True)
    files.remove(filepath)
    return Data, files[0]

def read_propfile(filepath):
    with open(filepath,'r') as file:
        i = 0
        while file.readline() != '[Step [1] Data]\n':
            i+=1
            if i ==20:
                raise Exception(f'Failed to Read Property File: {filepath}')
                break
        
        lines = file.readlines()[1:-1] 
    
    Data = {}
    units = []
    for line in lines:
        line = line[:-1] #getting rid of the \n at the end
        comps = line.split(',')
        if comps[0] == 'Specimen ID':  #pulling the specimen id out
            specimen = ''.join(comps[1:-1])
        else:    
            Data[comps[0]] = comps[1]
            units.append( tuple((comps[0],comps[-1])))
    
    return specimen, Data, units

def make_fulldict(directory):
    Filenames = glob.glob(directory + '*Spec*')
    Dictionary = {}
    for Filename in Filenames:
        Dict,Par = read_datafile(Filename)
        Spec,_Dict,Uni = read_propfile(Par)
        Dict['Params'] = _Dict
        Dict['FilePrefix'] = Par
        for key,unit in Uni:
            Dict['Units'][key]= unit
        Dictionary[Spec] = Dict
    return Dictionary

class Data:
    def __init__(self,Path):
        self.Dict = make_fulldict(Path)
        keys = []
        for k in (self.Dict).keys():
            keys.append(k)
        self.mats = keys
        keys = []
        for k in (self.Dict[self.mats[0]]['Data']).keys():
            keys.append(k)
        self.datakeys = keys
        keys = []
        for k in (self.Dict[self.mats[0]]['Params']).keys():
            keys.append(k)
        self.paramkeys = keys
        
    def get_mat(self, pattern,temp=None):
        returner = []
        for key in self.mats:
            if pattern in key:
                returner.append(key)
        if temp == None:
            return returner
        
        real = []
        for ret in returner:
            if temp in ret:
                real.append(ret)
        if pattern == 'PMMA' and temp == 'BW':
            real.append('PMMA-100C')
        if pattern == 'PMMA' and temp == '0C':
            real.remove('PMMA-100C')
        return real
        
    def get_data(self,key,values):

        if type(values) != list:
            values = [values]
            
        returner = []

        for value in values:
            returner.append(self.Dict[key]['Data'][value])
        return returner

    def get_param(self,key,values):
        if type(values) != list:
            values = [values]
        returner = []

        for value in values:
            returner.append(self.Dict[key]['Params'][value])
        return returner