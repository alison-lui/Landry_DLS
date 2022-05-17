# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:55:52 2021

@author: Alison Lui

Read an excel file of data from the Landry DLS machine and plot Semilog graphs. Make one graph for each of the triplicated experiments and one for the cumulative work.
Plots both by Intensity and by Number.
"""


""" Start by changing the following parameters """

workingdir = r"/Volumes/GoogleDrive/.shortcut-targets-by-id/1Fz5yERmDsm7k57_XOO1gSS5CsQd4gTUq/Blood and Plants/Data"
fname = r"/Volumes/GoogleDrive/.shortcut-targets-by-id/1Fz5yERmDsm7k57_XOO1gSS5CsQd4gTUq/Blood and Plants/Data/2022-04-22-26 POPC+DOTAP_LUV_zeta.xlsx"
sheetname = r"raw data"
AverageDatainTriplicates = True

#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import re

#%% Load data

os.chdir(workingdir)

df = pd.read_excel(fname, sheet_name=sheetname)
df = df.T

df.columns = df.iloc[0]
df = df.drop(index="Sample Name")
df = df.reset_index(drop=True)

#%%

L = [ int( (df[x].dropna().shape[0] ) / 2 ) for x in df.columns]

Xdata = pd.DataFrame(columns=df.columns)
Ydata = pd.DataFrame(columns=df.columns)

for i in np.arange(0,len(Xdata.columns)):
    
    colname = Xdata.columns[i]
    
    l = L[i]
    
    Ydata[colname] = df[colname].dropna().head(l).reset_index(drop=True)
    Xdata[colname] = df[colname].dropna().tail(l).reset_index(drop=True)

# make index into float values
Ydata = Ydata.set_index(Ydata.index.values.astype(float))
Xdata = Xdata.set_index(Xdata.index.values.astype(float))

#%%

# plot

fig, ax = plt.subplots()

for colname in Xdata.columns:
    ax.plot(Xdata[colname], Ydata[colname], label=colname)



#%%

# Smooth all data onto a new shared axis. Interpolate all missing values

# pull all x data into numpy array
newX = Xdata.values.ravel().astype(float)
# remove nan
newX = newX[~np.isnan(newX)]
# sort ascending
newX = np.sort(np.unique(newX))

# make new interpolated dataframe
df_int = pd.DataFrame(columns=Xdata.columns, index=newX)

for colname in Xdata.columns:
    test_df = pd.DataFrame()
    test_df['X'] = Xdata[colname]
    test_df['Y'] = Ydata[colname]
    
    test_df = test_df.set_index('X')
    test_df = test_df.dropna()

    df_int[colname] = test_df['Y']

df_int = df_int.apply(pd.to_numeric).interpolate(method='values').fillna(0)


#%%


""" Is the data in triplicates and should we average it? """

if AverageDatainTriplicates == True:
    # remove digit at end of sample name
    df_int.columns = df_int.columns.str[:-2]
    
    
#%% plot all
'''
fig, ax = plt.subplots()
sns.lineplot(data=df_int)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
'''
#%% plot sequential POPC:DOTAP component groups

clist = ['1:0 POPC:DOTAP 10x dilution in 20mM HEPES',
                '1:0.1 POPC:DOTAP 10x dilution in 20mM HEPES',
                '1:1 POPC:DOTAP in 20mM HEPES diluted',
                '0.1:1 POPC:DOTAP LUV in 20mM HEPES',
                '0:1 POPC:DOTAP in 20mM HEPES']

# make rename dictionary
coldict = {}
for colname in clist:
    coldict[colname] = re.search(r"(\d|\d\.\d):(\d|\d\.\d) POPC:DOTAP", colname).group(0)


fig, ax = plt.subplots()
sns.lineplot(data=df_int.loc[:,clist].rename(columns=coldict))

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.xlabel('Zeta Potential')
plt.ylabel('Count')
plt.tight_layout()

#%% plot a few specifically

print('individual')

fig, AX = plt.subplots(5, figsize=(10,5))
i=0
for colname in ['1:0 POPC:DOTAP 10x dilution in 20mM HEPES',
                '1:0.1 POPC:DOTAP 10x dilution in 20mM HEPES',
                '1:1 POPC:DOTAP in 20mM HEPES diluted',
                '0.1:1 POPC:DOTAP LUV in 20mM HEPES',
                '0:1 POPC:DOTAP in 20mM HEPES']:
    
    sns.lineplot(data=df_int.loc[:,colname], ax=AX[i], label=re.search(r"(\d|\d\.\d):(\d|\d\.\d) POPC:DOTAP", colname).group(0), legend=False)
    
    AX[i].legend(loc='center left', bbox_to_anchor=(1, 0.5))

    i += 1
plt.xlabel('Zeta Potential')
plt.ylabel('Count')
plt.tight_layout()






















