# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:55:52 2021

@author: Alison Lui

Read an excel file of data from the Landry DLS machine and plot 
Semilog graphs. Make one graph for each of the triplicated experiments and
one for the cumulative work.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel(r"C:\Users\sunsh\Downloads\drive-download-20210827T225234Z-001\20210826_liposome_dataexport_fixed.xlsx")
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

# average triplicate data
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

    #plt.figure(x+1)
    ax1.semilogx(xavgs[x,:], yavgs[x,:])
    ax1.set_xscale('log')
    #plt.semilogx(xavgs[x,:], yavgs[x,:])
    #ax1.ylabel("Percent%")
    #ax1.xlabel("Diameter (nm)")
    #ax1.title(Havgs[x])
    ax1.set_title(Havgs[x])
    ax1.set_ylabel('Percent by Size')
    ax1.set_xlabel('Diameter (nm)')
    fig.savefig(Havgs[x])
    
# Plot all lines together
fig, ax1 = plt.subplots(1, 1)

evenly_spaced_interval = np.linspace(0, 1, t-1)
colors = [plt.cm.viridis(x) for x in evenly_spaced_interval]
    
for x in range(0,t-1):
    ax1.semilogx(xavgs[x,:], yavgs[x,:], color = colors[x], label = Havgs[x])
    ax1.set_xscale('log')
    
ax1.set_ylabel('Percent by Size')
ax1.set_xlabel('Diameter (nm)')
#ax1.legend(Havgs)
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
fig.savefig("Cumulative")

        