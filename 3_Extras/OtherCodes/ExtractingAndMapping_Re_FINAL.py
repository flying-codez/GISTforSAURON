#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:09:11 2023

@author: lucasalonso-munoyerro
"""

import astropy.io.fits as fits
import pandas as pd
import numpy as np


'''
This code has the purpose of extracting the velocity dispersion (sigma) for specific BinID's inside a specified radius from the center.
The SAURON data cubes have the galaxy centered at 0,0 but to make sure of this, the code searches for the BINID with the highest flux 
signal and defines as such the center.

The first section uses code from the kinematic plotting portion of GIST to match the contents in the _table.fits file with the contents 
of _kin.fits. The second section focuses on extracting sigma values for data within a certain radius. Finally there is a visualization 
portion that uses the pixelsize determined in the _table.fits file to map the selected bins as pixels rather than points.

'''

'''
SECTION 1:
    
'''
PATH = 'Define the path to your GIST results folder here.'
RUN_ID = 'Insert RUN_ID here'

# open table with BIN_ID and associated data 

table_hdu = fits.open(PATH + '/' + RUN_ID + '_table.fits')

idx_inside  = np.where( table_hdu[1].data.BIN_ID >= 0        )[0]

flux        = np.array( table_hdu[1].data.FLUX[idx_inside]   ) # chooses where BIN_ID > 0
snr         = np.array( table_hdu[1].data.SNR[idx_inside] )
binNum_long = np.array( table_hdu[1].data.BIN_ID[idx_inside] ) # BIN_ID where BIN_ID > 0
xbin        = np.array( table_hdu[1].data.XBIN[idx_inside] )
ybin        = np.array( table_hdu[1].data.YBIN[idx_inside] )
ubins       = np.unique( np.abs( np.array( table_hdu[1].data.BIN_ID ) ) ) # all the absolute values of the BIN_ID's that are unique
pixelsize   = table_hdu[0].header['PIXSIZE'] 

# open FITS file with kinematic results
hdu = fits.open(PATH + '/' + RUN_ID + '_kin.fits')

# initialize result array
result = np.zeros((len(ubins), 4))
result[:, 0] = np.array(hdu[1].data.V)
result[:, 1] = np.array(hdu[1].data.SIGMA)
result[:, 2] = np.array(hdu[1].data.ERR_SIGMA) # Only available if MC simulations are set to at least 1
result[:, 3] = np.array(hdu[1].data.FORM_ERR_SIGMA)

# convert results to long version
result_long = np.zeros((len(binNum_long), result.shape[1]))
result_long[:, :] = np.nan

for i in range(len(ubins)):
    idx = np.where(ubins[i] == np.abs(binNum_long))[0]
    result_long[idx, :] = result[i, :]

result = result_long

# subtract median V value from V column so as to normalize data -- can be activated if desired. Since the current focus of the code is SIGMA it is not activated.
result[:, 0] = result[:, 0] - np.nanmedian(result[:, 0])

# create new table with BIN_ID, FLUX, SNR, XBIN, YBIN, V, and SIGMA columns -- It is important to note that a run with no MC simulations will not create an ERR_SIGMA column.

data = {'BIN_ID': binNum_long,'FLUX': flux, 'SNR': snr, 'XBIN' : xbin, 'YBIN' : ybin, 'V': result[:, 0], 'SIGMA': result[:, 1], 'ERR_SIGMA': result[:, 2], 'FORM_ERR_SIGMA': result[:, 3]}
arr_dat = pd.DataFrame(data)

'''
SECTION 2:

This next section goes through our combined data file and selects the values of sigma within a certain radius and
allocates the row data to a new df.


        If already created, then no need to use the following function:
'''
arr_dat.to_csv(PATH + '/' + RUN_ID + '_combined.csv')

'''  
        It is an extra step that helps correct the endianess.
'''


arr_dat = pd.read_csv(PATH + '/' + RUN_ID + '_combined.csv')

# Define the origin of the galaxy as the point of max flux

max_flux_index = arr_dat['FLUX'].idxmax()
max_xbin = arr_dat.loc[max_flux_index, 'XBIN']
max_ybin = arr_dat.loc[max_flux_index, 'YBIN']

# Define the radial distance
distance = ((arr_dat['XBIN'] - max_xbin) ** 2 + (arr_dat['YBIN'] - max_ybin) ** 2) ** 0.5

# Choose data with distance within our determined radius 

radius = 2.24 # radius range
selected_rows = arr_dat.loc[distance <= radius]

final_selec = selected_rows[['BIN_ID', 'FLUX', 'SNR', 'XBIN', 'YBIN', 'SIGMA','ERR_SIGMA','FORM_ERR_SIGMA']]
final_selec.to_csv(PATH + 'INSERT HERE the desired name of the table followed by .csv')

'''

SECTION 3:

This is the plotting portion of the code which will use the selected radius. 
It can also be implemented on section one to obtain full SIGMA plot.

'''

import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Define grid
xgrid = np.arange(final_selec['XBIN'].min(), final_selec['XBIN'].max() + pixelsize, pixelsize)
ygrid = np.arange(final_selec['YBIN'].min(), final_selec['YBIN'].max() + pixelsize, pixelsize)
X, Y = np.meshgrid(xgrid, ygrid)

# Interpolate sigma values onto grid
Z = griddata((final_selec['XBIN'], final_selec['YBIN']), final_selec['SIGMA'], (X, Y), method='nearest')
Z[Z==np.nan] = np.nan

# Plot color map
plt.imshow(Z, cmap='jet', origin='lower', extent=[xgrid.min(), xgrid.max(), ygrid.min(), ygrid.max()])
plt.colorbar(label=r'$\sigma$ (km/s)')
plt.xlabel('X (arcsec)')
plt.ylabel('Y (arcsec)')
plt.show()
