#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:20:31 2023

@author: lucasalonso-munoyerro
"""
import numpy as np
import pandas as pd
import os 

# shell comands

cd = 'cd /home/astrogroup/lucasal/Batch' #choose directory

# read csv table with above necessary data 

galdat = pd.read_csv('BatchConfigInfo.csv')
galdat = galdat.reset_index() #indexes pair with rows
print(galdat)

# Create a ConfigFile 

SampleConfig = 'configFiles/MasterConfigTemp'
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

