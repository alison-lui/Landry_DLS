# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:55:52 2021

@author: Alison Lui and Francis

Read an excel file of data from the Landry DLS machine and plot Semilog graphs. Make one graph for each of the triplicated experiments and one for the cumulative work.
You must specify if you're plotting either DLS data taken by Size or by Number.
"""


""" Start by changing the following parameters """

workingdir = r"C:\Users\sunsh\Documents\AL Data\B2P41_qPCR_Liposomes_adding_Triton_X-100\Liposomes 2nd purification\DLS - 345 combination"
fname = r"C:\Users\sunsh\Documents\AL Data\B2P41_qPCR_Liposomes_adding_Triton_X-100\Liposomes 2nd purification\DLS - 345 combination\20210901_Liposomesfrom345_Combined.xlsx"
sheetname = r"Sheet1"
AverageDatainTriplicates = True

#####################################################
#####################################################
#####################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(workingdir)

df = pd.read_excel(fname, sheet_name=sheetname)
data = df.to_numpy()

temp = np.shape(data)
H = temp[0]
L = temp[1]

new_L = 70

imin = 1
imax = new_L

smin = imin + new_L
smax = imax + new_L

nmin = smin + new_L
nmax = smax + new_L

diff = nmax + 1

ymin = 0
ymax = H-1

Headers = data[:,0]
Intensities = data[:,imin:imax]
Sizes = data[:,smin:smax]
Numbers = data[:,nmin:nmax]


""" Is the data in triplicates and should we average it? """

if AverageDatainTriplicates == True:
    t = int(H/3) # number of datasets to average (1/3 of total rows in dataset)

    # data goes here
    iavgs = []
    savgs = []
    navgs = []
    Havgs = []

    
    for x in range(0,t):
    
        # average data
        
        r = int(x*3)
        iavgs = np.append(iavgs, np.mean(Intensities[r:r+3,:],0)).reshape((x+1,new_L-1))
        savgs = np.append(savgs, np.mean(Sizes[r:r+3,:],0)).reshape((x+1,new_L-1))
        navgs = np.append(navgs, np.mean(Numbers[r:r+3,:],0)).reshape((x+1,new_L-1))
        temptitle = Headers[x*3]
        Havgs = np.append(Havgs, temptitle[:-2])
        
        # create a dual plot of each averaged dataset, both numbers and sizes
        
        fig, (ax1, ax2) = plt.subplots(2,1)
    
        # Plot Size data
        ax1.semilogx(savgs[x,:], iavgs[x,:])
        ax1.set_xscale('log')
        ax1.set_ylabel('Size by Intensity')
        ax1.set_xlabel('Diameter (nm)')

        # Plot Number data
        ax2.semilogx(savgs[x,:], navgs[x,:])
        ax2.set_xscale('log')
        ax2.set_ylabel('Size by Number')
        ax2.set_xlabel('Diameter (nm)')

        fig.suptitle(Havgs[x])
        fig.savefig(Havgs[x] + "_I_and_N.png")
        
else:
    CleanHeaders = []
    t = H
    
    for x in range(0,H):
        
        # create a dual plot of each averaged dataset, both numbers and sizes
        
        fig, (ax1, ax2) = plt.subplots(2,1)
    
        # Plot Size data
        ax1.semilogx(Sizes[x,:], Intensities[x,:])
        ax1.set_xscale('log')
        ax1.set_ylabel('Size by Intensity')
        ax1.set_xlabel('Diameter (nm)')

        # Plot Number data
        ax2.semilogx(Sizes[x,:], Numbers[x,:])
        ax2.set_xscale('log')
        ax2.set_ylabel('Size by Number')
        ax2.set_xlabel('Diameter (nm)')

        fig.suptitle(Headers[x])
        fig.savefig(Headers[x] + "_I_and_N.png")
    
""" Plot all lines together """
 
figN, axN = plt.subplots(1, 1)
figI, axI = plt.subplots(1, 1)

figN.set_size_inches(8, 4)
figI.set_size_inches(8, 4)

if AverageDatainTriplicates == True:
    evenly_spaced_interval = np.linspace(0, 1, t)
    colors = [plt.cm.viridis(x) for x in evenly_spaced_interval]

    for x in range(0,t):
        axN.semilogx(savgs[x,:], navgs[x,:], color = colors[x], label = Havgs[x])
        axN.set_xscale('log')
        axI.semilogx(savgs[x,:], iavgs[x,:], color = colors[x], label = Havgs[x])
        axI.set_xscale('log')
        
        print()
    
    axN.set_ylabel('Size Measured by Number')
    axN.set_xlabel('Diameter (nm)')
    axN.set_title("Cumulative DLS Size by Number")
    axN.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    figN.tight_layout()
    figN.savefig("Cumulative_Averaged_N" + ".png")
    
    axI.set_ylabel('Size Measured by Intensity')
    axI.set_xlabel('Diameter (nm)')
    axI.set_title("Cumulative DLS Size by Intensity")
    axI.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    figI.tight_layout()
    figI.savefig("Cumulative_Averaged_I" + ".png")

else:
    evenly_spaced_interval = np.linspace(0, 1, H)
    colors = [plt.cm.viridis(x) for x in evenly_spaced_interval]

    for x in range(0,t):
        axN.semilogx(Sizes[x,:], Numbers[x,:], color = colors[x], label = Headers[x])
        axN.set_xscale('log')
        axI.semilogx(Sizes[x,:], Intensities[x,:], color = colors[x], label = Headers[x])
        axI.set_xscale('log')
        
        #print("x = " + str(x))
        #print("Header = " + Headers[x])
    
    axN.set_ylabel('Size by Number')
    axN.set_xlabel('Diameter (nm)')
    axN.set_title("Cumulative DLS Size by Number")
    axN.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    figN.tight_layout()
    figN.savefig("Cumulative_N" + ".png")
    
    axI.set_ylabel('Size by Intensity')
    axI.set_xlabel('Diameter (nm)')
    axI.set_title("Cumulative DLS Size by Intensity")
    axI.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    figI.tight_layout()
    figI.savefig("Cumulative_I" + ".png")

        
