#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:37:08 2020

@author: niall
"""
import pandas as pd
import numpy as np


df = pd.read_csv('/Users/niall/insight_project/data/raw/weather_darksky.csv')
#df = df.head(1000)

#
irows, icolumns = np.where(df.iloc[:,6:] > 800)
icolumns = icolumns + 6
real_pressure_column = 11

df_new = df.iloc[:,real_pressure_column - 5: real_pressure_column + 6].copy()
df_new[:] = np.nan

for i in range(len(icolumns)):
    jcol = icolumns[i] # this is the location of pressure in the original df
    jrow = irows[i]
    df_new.iloc[jrow, :] = df.iloc[jrow, jcol-5:jcol+6].values
    
    if i % 5000 == 0:
        df_new.to_csv('/Users/niall/insight_project/data/raw/weather_darksky_subset_inprocess.csv')

df = df.iloc[:, 0:3]
df = pd.concat([df, df_new], axis=1)
df.to_csv('/Users/niall/insight_project/data/raw/weather_darksky_subset.csv', index=False)
#df = df.head()