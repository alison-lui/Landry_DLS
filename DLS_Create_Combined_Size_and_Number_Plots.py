# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 23:26:44 2021

@author: Alison Lui

Read an excel file of data from the Landry DLS machine including both Number and Size data in two different sheets. For each triplicated experiment, average the data and plot
Number and Size percentages on semilogx plots side-by-side. Save plots as png files.
"""


""" Start by changing the following parameters """

workingdir = r"D:\Documents\Research"
fname = r"D:\Documents\Research\20210826_liposome_dataexport_fixed.xlsx"
S_sheetname = r"Chris-Sizes"
N_sheetname = r"Alison-Numbers"
AverageDatainTriplicates = True

#####################################################
#####################################################
#####################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(workingdir)

df_S = pd.read_excel(fname, sheet_name=S_sheetname)
df_N = pd.read_excel(fname, sheet_name=N_sheetname)
data_S = df_S.to_numpy()
data_N = df_N.to_numpy()

temp = np.shape(data_S)
H = temp[0]
L = temp[1]

xmin = 1
xmax = int((L-1)/2)

ymin = 0
ymax = H-1

Headers = data_S[:,0]

Ydata_S = data_S[:,xmin:xmax]
Xdata_S = data_S[:,xmin+xmax:xmax+xmax]
Ydata_N = data_N[:,xmin:xmax]
Xdata_N = data_N[:,xmin+xmax:xmax+xmax]

""" Is the data in triplicates and should we average it? """

if AverageDatainTriplicates == True:
    t = int(H/3) # number of datasets to average

    # data goes here
    xavgs_S = []
    yavgs_S = []
    xavgs_N = []
    yavgs_N = []
    Havgs = []

    for x in range(0,t-1):
        r = int(x*3)
        xavgs_S = np.append(xavgs_S, np.mean(Xdata_S[r:r+3,:],0)).reshape((x+1,xmax-1))
        yavgs_S = np.append(yavgs_S, np.mean(Ydata_S[r:r+3,:],0)).reshape((x+1,xmax-1))
        xavgs_N = np.append(xavgs_N, np.mean(Xdata_N[r:r+3,:],0)).reshape((x+1,xmax-1))
        yavgs_N = np.append(yavgs_N, np.mean(Ydata_N[r:r+3,:],0)).reshape((x+1,xmax-1))
        
        temptitle = Headers[x*3]
        Havgs = np.append(Havgs, temptitle[:-2])
        
        fig, (ax1, ax2) = plt.subplots(2,1)
    
        # Plot Size data
        ax1.semilogx(xavgs_S[x,:], yavgs_S[x,:])
        ax1.set_xscale('log')
        ax1.set_ylabel('Percent by Size')
        ax1.set_xlabel('Diameter (nm)')

        # Plot Number data
        ax2.semilogx(xavgs_N[x,:], yavgs_N[x,:])
        ax2.set_xscale('log')
        ax2.set_ylabel('Percent by Number')
        ax2.set_xlabel('Diameter (nm)')

        fig.suptitle(Havgs[x])
        fig.savefig(Havgs[x] + "_N_and_S.png")
        
else:
    CleanHeaders = []
    for x in range(0,H):
        temptitle = Headers[x]
        CleanHeaders = np.append(CleanHeaders, temptitle[:-2])
        
        fig, (ax1, ax2) = plt.subplots(2,1)
    
        # Plot Size data
        ax1.semilogx(Xdata_S[x,:], Ydata_S[x,:])
        ax1.set_xscale('log')
        ax1.set_ylabel('Percent by Size')
        ax1.set_xlabel('Diameter (nm)')
        
        # Plot Number data
        ax2.semilogx(Xdata_N[x,:], Ydata_N[x,:])
        ax2.set_xscale('log')
        ax2.set_ylabel('Percent by Number')
        ax2.set_xlabel('Diameter (nm)')
        
        fig.suptitle(CleanHeaders[x])
        fig.savefig(CleanHeaders[x] + "_N_and_S.png")
