#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:48:48 2022

@author: lucasalonso-munoyerro
"""

import astropy.io.fits as pyfits 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib.pyplot as plt

from plotbin.display_bins_generators import display_bins_generators 

filename = "NGC3489TRY1_kin-bestfit.fits" 
hdu = pyfits.open(filename) 
spectrum = hdu[0].data 
table = hdu[2].data 
df = pd.DataFrame(table)

x = table["A"] # Coordinates of the original spaxels in arcsec (nort is up) 
y = table["D"] 
flux = np.mean(spectrum, 1) # surface brightness 

# Find a coordinate and extract the position (data already centered at 0,0)

x_0 = np.array(np.where(x==8))
y_0 = np.array(np.where(y==8))

loc= np.intersect1d(x_0,y_0)
print(loc)

# create x and y data and produce plots

specdat=spectrum[(int(loc)-1),:]
wavedat= np.arange(4824.6,5281.1,1.1)

plt.plot(wavedat,specdat)
plt.show()

#df=pd.DataFrame(flux)
#df.to_csv('fluxview.csv') 
