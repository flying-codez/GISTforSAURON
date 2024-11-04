#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 12:16:34 2023

@author: lucasalonso-munoyerro
"""

import astropy.io.fits as pyfits 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib.pyplot as plt
import math as m

from plotbin.display_bins_generators import display_bins_generators 


#bestfit = "NGC3489TRY1_kin-bestfit.fits" 
#binspec = "NGC3489TRY1_BinSpectra.fits"

hdu_best = pyfits.open("NGC3489_100sim_kin-bestfit.fits") 
hdu_binspec = pyfits.open("NGC3489_100sim_BinSpectra.fits") 

#Opening bestfit and obtaining a spectrum

bestspec = hdu_best[1].data 
besty = bestspec[0][0]
bestlog = hdu_best[2].data 
bestlog= [x[0] for x in bestlog]
bestlog = np.exp(bestlog)

binspec = hdu_binspec[1].data 
biny = binspec[0][0]
binlog = hdu_binspec[2].data 
binlog= [x[0] for x in binlog]
binlog= np.exp(binlog)

plt.plot(bestlog,besty)
plt.plot(binlog,biny)
plt.axvline(x=4958.83, color = 'r', label = 'axvline - full height')
plt.axvline(x=5006.77, color = 'r', label = 'axvline - full height')

plt.show()