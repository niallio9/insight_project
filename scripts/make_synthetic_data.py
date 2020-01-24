#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 09:47:47 2020

@author: niall
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randrange
from io import StringIO
from csv import writer

df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
df = df[df['collision_count'] > 50]
df = df.reset_index(drop=True)
df_ = df.head()
#df1 = df.copy()

#i_hour_of_day = df.columns.get_loc("hour_of_day")
#i_day_of_week = df.columns.get_loc("day_of_week")
#i_month_of_year = df.columns.get_loc("month")

#road_ids = df[['u', 'v', 'key', 'osmid']]
#unique_roads = road_ids.drop_duplicates()

fixed_road_features = ['collision_id', 'collision_time', 'longitude', 'latitude', 'street_1',
       'street_type_1', 'road_class','u', 'v', 'key', 'osmid', 'name',
       'highway', 'maxspeed', 'oneway', 'length', 'geometry', 'lanes']
i_fixed_road_features = [df.columns.get_loc(col) for col in fixed_road_features]
original_length = len(df.iloc[:,1])

output = StringIO()
csv_writer = writer(output)
for i in range(original_length):
#for i in range(1000):
#    print(i)
    for j in range(1):
        i_random_row = randrange(original_length) # get random row index for later
        random_row = df.iloc[i_random_row,:]
        while i_random_row == i:
            i_random_row = randrange(original_length) # get random row index for later
            random_row = df.iloc[i_random_row,:]
        row = df.iloc[i,:] # the row to alter
        #modify some parameters of the row
        row[i_fixed_road_features] = random_row[i_fixed_road_features]
        #change the road segment and other parameters that are 
        if not (df == row).all(1).any():
            csv_writer.writerow(row)
#            df.append(row, ignore_index=True)
#            df.loc[len(df.iloc[:,1])] = row
output.seek(0) # we need to get back to the start of the BytesIO
df_synthetic = pd.read_csv(output, header=None)
#Change all of the collision label to 0 for no collision
df_synthetic.iloc[:,df.columns.get_loc('collision')] = 0
df_synthetic_top = df_synthetic.head()
df_synthetic.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads.csv', index=False)
df_new = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic.csv',names=df.columns)

#df = df.append(df_synthetic, ignore_index=True)
#df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_and_synthetic.csv', index=False)

#
#df2 = df.copy()
#df.iloc[1,:] = row1
#road_surface_condition_unique = list(dict.fromkeys(df['road_surface_cond']))