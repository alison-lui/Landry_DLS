# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:55:52 2021

@author: Alison Lui

Read an excel file of data from the Landry DLS machine and plot 
Semilog graphs. Make one graph for each of the triplicated experiments and
one for the cumulative work.
"""


""" Start by changing the following parameters """

workingdir = r"D:\Documents\Research"
fname = r"D:\Documents\Research\20210826_liposome_dataexport_fixed.xlsx"
sheetname = r"Chris-Sizes"
SizeDataorNumberData = "Size" # Sets y-label. Write "Size" or "Number"
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

xmin = 1
xmax = int((L-1)/2)

ymin = 0
ymax = H-1

Headers = data[:,0]
Ydata = data[:,xmin:xmax]
Xdata = data[:,xmin+xmax:xmax+xmax]

if SizeDataorNumberData == "Size":
    yl = "Percent by Size"
    ender = "_Size"
else:
    yl = "Percent by Number"
    ender = "_Number"

""" Is the data in triplicates and should we average it? """

if AverageDatainTriplicates == True:
    t = int(H/3) # number of datasets to average

    # data goes here
    xavgs = []
    yavgs = []
    Havgs = []

    for x in range(0,t-1):
        r = int(x*3)
        xavgs = np.append(xavgs, np.mean(Xdata[r:r+3,:],0)).reshape((x+1,xmax-1))
        yavgs = np.append(yavgs, np.mean(Ydata[r:r+3,:],0)).reshape((x+1,xmax-1))
        temptitle = Headers[x*3]
        Havgs = np.append(Havgs, temptitle[:-2])
        
        fig, ax1 = plt.subplots(1, 1)
    
        ax1.semilogx(xavgs[x,:], yavgs[x,:])
        ax1.set_xscale('log')
        ax1.set_title(Havgs[x])
        ax1.set_ylabel(yl)
        ax1.set_xlabel('Diameter (nm)')
        fig.savefig(Havgs[x] + ender + ".png")
        
else:
    CleanHeaders = []
    for x in range(0,H):
        temptitle = Headers[x]
        CleanHeaders = np.append(CleanHeaders, temptitle[:-2])
        
        fig, ax1 = plt.subplots(1, 1)
    
        ax1.semilogx(Xdata[x,:], Ydata[x,:])
        ax1.set_xscale('log')
        ax1.set_title(CleanHeaders[x])
        ax1.set_ylabel(yl)
        ax1.set_xlabel('Diameter (nm)')
        fig.savefig(CleanHeaders[x] + ender + ".png")
    
""" Plot all lines together """
 
fig, ax1 = plt.subplots(1, 1)

if AverageDatainTriplicates == True:
    evenly_spaced_interval = np.linspace(0, 1, t-1)
    colors = [plt.cm.viridis(x) for x in evenly_spaced_interval]

    for x in range(0,t-1):
        ax1.semilogx(xavgs[x,:], yavgs[x,:], color = colors[x], label = Havgs[x])
        ax1.set_xscale('log')
    
    ax1.set_ylabel(yl)
    ax1.set_xlabel('Diameter (nm)')
    ax1.set_title("Cumulative DLS Data")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    fig.savefig("Cumulative" + ender + ".png")

else:
    evenly_spaced_interval = np.linspace(0, 1, H-1)
    colors = [plt.cm.viridis(x) for x in evenly_spaced_interval]

    for x in range(0,H-1):
        ax1.semilogx(Xdata[x,:], Ydata[x,:], color = colors[x], label = CleanHeaders[x])
        ax1.set_xscale('log')
    
    ax1.set_ylabel(yl)
    ax1.set_xlabel('Diameter (nm)')
    ax1.set_title("Cumulative DLS Data")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    fig.savefig("Cumulative" + ender + ".png")
    

        