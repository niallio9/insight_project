#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 09:47:47 2020

@author: niall

A script for generating synthetic data. The basis is an undersampling of all
available no-collision data points over the time range of the collision data.
"""

import numpy as np
import pandas as pd
from random import randrange
from io import StringIO
from csv import writer

# Read in the coliision_and_road data and subset by
df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
min_collision_count = 20
df = df[df['collision_count'] > min_collision_count]
df = df.reset_index(drop=True)
df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_20plus_collisions.csv', index=False)

# for randomly changing the road, thesea are the values
fixed_road_features = ['collision_id', 'collision_time', 'longitude', 'latitude', 'street_1',
       'street_type_1', 'road_class','u', 'v', 'key', 'osmid', 'name',
       'highway', 'maxspeed', 'oneway', 'length', 'geometry', 'lanes']
i_fixed_road_features = [df.columns.get_loc(col) for col in fixed_road_features]
original_length = len(df.iloc[:,1])
output = StringIO()
csv_writer = writer(output)

# It semms like looping with pandas sucks. It's a bit faster writing synthetic data
# to a csv and reading it back in after.
for i in range(original_length):
    for j in range(1):
        i_random_row = randrange(original_length) # get random row index for later
        random_row = df.iloc[i_random_row,:]
        while i_random_row == i: # make sure the synthetic row does not already exist in the true data
            i_random_row = randrange(original_length) # get random row index for later
            random_row = df.iloc[i_random_row,:]
        row = df.iloc[i,:] # the row to alter
        #modify some parameters of the row
        row[i_fixed_road_features] = random_row[i_fixed_road_features]
        #change the road segment and it's parameters
        if not (df == row).all(1).any():
            csv_writer.writerow(row)
output.seek(0) # we need to get back to the start of the BytesIO
df_synthetic = pd.read_csv(output, header=None)

#Change all of the collision labels to 0 for synthetic data and save to csv
df_synthetic.iloc[:,df.columns.get_loc('collision')] = 0
df_synthetic_top = df_synthetic.head()
df_synthetic.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads.csv', index=False)

# END

#df_new = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic.csv',names=df.columns)

#df = df.append(df_synthetic, ignore_index=True)
#df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_and_synthetic.csv', index=False)

#
#df2 = df.copy()
#df.iloc[1,:] = row1
#road_surface_condition_unique = list(dict.fromkeys(df['road_surface_cond']))