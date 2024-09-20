import numpy as np
import pandas as pd

def read_params(file_path,params,max_its):
    line = ''
    values = []
    for param in params:
        i=-3
        file = open(file_path,'r')
        while line != param:
            i+=1
            _line = file.readline()
            line = _line.split(',')[0]
            if i == max_its:
                print('Failed to find parameter "{}" in {} \nMake sure you spelled it right / it exists (it may     not)'.format(param,file_path))
                break
        if param == params[-1]:
            values.append(i)
            break
        if i != max_its:
            values.append(_line.split('"')[-2])
        else:
            values.append('N/A')
    ret_pams = []
    ret_pams = params[:-1]
    ret_pams.append('Header')
    return ret_pams,values

def read_vals(file_path,header):
    data = pd.read_csv(file_path,header=header)
    return data.columns,np.array(data)

def ReadFiles(file_paths,params,max_its=1000):
    '''
    Inputs:
    
        file_paths: list of file paths to read
    
        params:     list of non-csv data to find in file

        max_its:    max number of iterations to use to check for param, 
                    set to roughly the number of lines of file

    Returns:

        ret_Dict: Dict of Dicts
                    keys to access Dicts are material names
                    keys to access data in Dicts are params
    ''' 
    
    ret_Dict = {}
    for file in file_paths:
        _params = params
        pams, vals=read_params(file,_params,max_its)
        cols, data = read_vals(file,vals[-1])
        fDict = {p:v for p,v in zip(pams[1:-1],vals[1:-1])}
        fDict['data'] = data
        ret_Dict[vals[0]] = fDict
    print('\nDone :)')
    print('CSV labels are: ',cols)
    return ret_Dict
