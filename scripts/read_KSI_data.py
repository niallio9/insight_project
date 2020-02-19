#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:30:45 2020

@author: niall
"""

# Importing the libraries
#import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
#from collections import OrderedDict

# Importing the dataset
df = pd.read_csv('/Users/niall/insight_project/data/raw/collisions_events.csv', sep=';')
df_top = df.head()
wanted_columns = ['collision_id', 'collision_date', 'collision_time','longitude',
                  'latitude', 'street_1', 'street_type_1','road_class',
                  'visibility', 'collision_type','impact_type',
                  'light', 'road_surface_cond']
df = df[wanted_columns]

# remove dodgy data
# ther number of dodgy data is ~1% of the total data, so a simple remove is acceptable in this case
df = df.dropna(axis='rows', how='any', thresh=None, subset=None, inplace=False)
df = df[df.longitude != 0]
df = df[df.latitude != 0]
df = df[df.visibility != 'OTHER']
df = df[df.light != 'OTHER']
df = df[df.impact_type != 'OTHER']
df = df[df.road_surface_cond != 'OTHER']
df = df[df.road_surface_cond != '222']
df = df[df.road_surface_cond != 'PENDING']
df = df[df.road_surface_class != '222']
df.reset_index()

# Set up timestamps
df_top = df.head()
df['collision_time'] = df['collision_time'].apply(lambda x: '{0:0>4}'.format(x)).astype(str)
df['collision_time'] = df['collision_date'] + " " + df['collision_time'].str[0:2] + ":" + df['collision_time'].str[2:4]
df['collision_time'] = pd.to_datetime(df['collision_time'])
del df['collision_date']
df['year'] = pd.DatetimeIndex(df['collision_time']).year
df['month'] = pd.DatetimeIndex(df['collision_time']).month
df['day_of_week'] = df.collision_time.dt.dayofweek
df['hour_of_day'] = df.collision_time.dt.hour
df['collision'] = 1 # This is the label for the data

# Save the cleaned data to a csv
df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean.csv', index=False)

## END