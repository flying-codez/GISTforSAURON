#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:06:33 2023

@author: lucasalonso-munoyerro
"""

from astropy.io import fits 
import numpy as np
import pandas as pd
import os 

'''

Context for the code : the following are the replaced sections of the template configuration file with their provided value

'AAAA' = 'RUN_ID'
'BBBB' ='INPUT'
'CCCC' = 'REDSHIFT'
'DDDD' = 'SIGMA'
'EEEE' = 'MC'

'''

# shell comands

cd = 'Enter Directory with .csv table. Leave Template MasterConfig inside the designated configFiles folder' #choose directory

# read csv table with above necessary data 

galdat = pd.read_csv('BatchConfigInfo.csv')
galdat = galdat.reset_index() #indexes pair with rows
print(galdat)

# Create a ConfigFile 

SampleConfig = 'configFiles/MasterConfigTemp' #M asterConfigTemp is name of template MasterConfig
sc= open(SampleConfig, 'r')
template = sc.read() #template file to ovewrite

for index, row in galdat.iterrows():
    # replace the necessary variables        
    new = template.replace('AAAA',str(row['RUN_ID'])).replace('BBBB',str(row['INPUT']))\
        .replace('CCCC', str(row['REDSHIFT'])).replace('DDDD', str(row['SIGMA'])).replace('EEEE', str(row['MC']))
    # Export new file
    f = open('configFiles/MasterConfig_'+str(row['RUN_ID']), 'w+')
    f.write(new)
    print('MasterConfig_'+str(row['RUN_ID']), 'was successfuly created')
    mainname = 'MasterConfig_'+str(row['RUN_ID'])
    
    os.system(cd)
    os.system('gistPipeline --config configFiles/MasterConfig_' + str(row['RUN_ID']) + ' --default-dir configFiles/defaultDir')

    # extract average sigma value from previous run and run again with such value - iterate 3 times
    for i in range(2):
        k = 'results/' + str(row['RUN_ID']) + '/' +str(row['RUN_ID']) +'_kin.fits'
        if i < 2:
            hdu_k = fits.open(k)
            data = hdu_k[1].data 
            sigma_data = data['SIGMA']
            medsig = np.median(sigma_data)
            print('Median Sig for iteration ' + str(i+1) + ':', medsig)
            new2 = template.replace('AAAA',str(row['RUN_ID']) +'_iter_' + str(i+1))\
                                    .replace('BBBB',str(row['INPUT']))\
                                    .replace('CCCC', str(row['REDSHIFT']))\
                                    .replace('DDDD', str(medsig))\
                                    .replace('EEEE', '0')
            
            filename = 'MasterConfig_' + str(row['RUN_ID']) + '_iter_' + str(i+1)
            kinname = str(row['RUN_ID'])+ '_iter_' + str(i+1) +'_kin.fits'
            
            f2 = open('configFiles/' + filename,'w+')
            f2.write(new2)
            
            os.system(cd)
            os.system('gistPipeline --config configFiles/' + filename + ' --default-dir configFiles/defaultDir')
            k = 'results/' + str(row['RUN_ID']) + '/' + kinname
        else:
            k = 'results/' + str(row['RUN_ID']) + '_iter_' + str(i) + '/' + str(row['RUN_ID']) + '_iter_' + str(i) + '_kin.fits'
            hdu_k = fits.open(k)
            data = hdu_k[1].data 
            sigma_data = data['SIGMA']
            medsig = np.median(sigma_data)
            new3 = template.replace('AAAA',str(row['RUN_ID'])+'_final_iter')\
                .replace('BBBB',str(row['INPUT']))\
                .replace('CCCC', str(row['REDSHIFT']))\
                .replace('DDDD', str(medsig))\
                .replace('EEEE', '100')
            
            filename = 'MasterConfig_'+str(row['RUN_ID'])+'_final_iter'
            f3 = open('configFiles/'+ filename, 'w+')
            f3.write(new3)
            
            os.system(cd)
            os.system('gistPipeline --config configFiles/' + filename + ' --default-dir configFiles/defaultDir')
            print("median SIGMA value used for final run:",  medsig)