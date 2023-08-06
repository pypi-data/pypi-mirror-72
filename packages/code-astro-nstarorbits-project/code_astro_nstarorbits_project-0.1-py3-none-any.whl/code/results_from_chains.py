import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import pylab as py
import corner
import Chains
from astropy.io import ascii


"""
Parameters:
-----------
DO_EVERYTHING (bool):
     set to True to automatically run all functionality of this file (plot and save 1-D histograms, write summary statistics to a .csv file, and plot corner plot for all parameters)
     set to False to refrain from automatically running all functions. Functions can be called independently.

     
rootdir (str):
    the directory of input file

filename (str):
    the name of the input file

filetype (str):
    the type of the input file, default is 'chains'

input_type (str):
    type of input, e.g. 'hdf' for hdf5 file, 'txt' for txt file, 'arr' for arrays.
    Only 'hdf' is supported in V 0.1

nbins (int):
    bins of the histogram

header (str):
    the common characters in the header of the columns
    e.g., eval[0].HR2562.P
          eval[0].HR2562.e
          eval[0].HR2562.I
          eval[0].HR2562.Omega
          eval[0].HR2562.omega
          eval[0].HR2562.T0
     all have a common header of 'eval[0].HR2562.', which is not needed in plotting the axes
     If no header, set header = None


"""


DO_EVERYTHING = True

rootdir = '/u/kkosmo/Workshops/CodeAstro_workshop/codeastro/codeastro_workshop/example_data/'
filename = 'ChainsHR2562b.h5'
filetype = 'chains'
input_type = 'hdf'
nbins = 70
header = 'eval[0].HR2562.'


if input_type == 'hdf':
    c = Chains.Chains.from_hdf5(rootdir+filename)
    
def get_outfile():
        '''
        returns: csv file with median value, and 1,2,3-sigma envelopes for each parameter
        '''

        med = c.median #series
                
        sig1 = c.calculate_sigmas(1) #OrderedDict
        sig2 = c.calculate_sigmas(2)
        sig3 = c.calculate_sigmas(3)

        #convert OrderedDicts to DataFrames so they can be merged
        df1 = pd.DataFrame.from_dict(sig1)  #if you want the keys to be the rows not the columns, add additional argument: orient='index'
        df2 = pd.DataFrame.from_dict(sig2)
        df3 = pd.DataFrame.from_dict(sig3)


        #merge series with DataFrame
        frames = [df1,df2,df3]
        merged = pd.concat(frames)
        merged = merged.append(med, ignore_index=True)
        merged = merged.reindex([6,0,1,2,3,4,5])  #move median values to top row

        #remove column if column name is 'lnlike'
        if 'lnlike' in merged.columns:
            merged.pop('lnlike')

        #Clean up column names if there is a header
        if header:
                names = []
                col_names_dict = {}
                for i in range(len(merged.columns)):
                        names.append(merged.columns[i].replace(header,''))
                        col_names_dict.update( {merged.columns[i]: names[i]} )
                merged = merged.rename(columns = col_names_dict)
        
        #label rows
        merged = merged.rename(index = { 6: 'median', 1: '1_sig_min', 2:'1_sig_plus', 3: '2_sig_min', 4:'2_sig_plus', 5: '3_sig_min', 0:'3_sig_plus'})
        
        #write to csv (comma separated value) file
        merged.to_csv(rootdir+'param_stats.csv')
        

def plot_posteriors_1d(rootdir, filename, filetype, nbins, header):
    '''
    returns: .png files plotting 1-D histograms for each parameter
    
    Note: In plt.hist(), in python2 normed=True works, but for python3 you need to change the argument to density=1
    '''
    
    ## load results file
    root = '{0}/{1}'.format(rootdir, filename)
    table = pd.read_hdf(root, filetype)
        
    columns = table.columns
    weights = table['weights']
    
    ## extract the column names for each parameter
    params = []
    params_name = []            ## extract parameter name only wither header, used for plotting axis
    for i in range(len(columns)):
        if columns[i] != 'weights' and columns[i] != 'lnlike':
            columnone = columns[i]
            params.append(columnone)
            nameone = columnone.replace(header, '')
            params_name.append(nameone)
            
    pcnt = len(params)
    #print('lenth_params=', pcnt)
    
    py.figure(1,figsize=(10,10))
    for i in range(pcnt):
        py.clf()
        n, bins, patch = plt.hist(table[params[i]], histtype = 'step', density=1, align = 'left', weights = weights, bins = nbins, color = 'black', linewidth=2)
        
        bin_centers = (bins[:-1] + bins[1:])/2
        py.axis([min(bin_centers) - 0.1, max(bin_centers) + 0.1, 0, max(n) + (max(n) / 10.)])
        
        py.xlabel(params_name[i], fontsize = 20)
        py.ylabel('Probability Density', fontsize = 20)
        py.tick_params(axis = 'both', labelsize = 16)

        outfile = '{0}/posterior_{1}.png'.format(rootdir, params_name[i])
        py.savefig(outfile)
    return


if DO_EVERYTHING == True:
    get_outfile()
    
    c.plot_triangle()  #have to edit so it doesn't plot lnlike column
    plt.savefig(rootdir+'corner.pdf')
    
    plot_posteriors_1d(rootdir, filename, filetype, nbins, header)
    #look into pd.DataFrame.hist?




