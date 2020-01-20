#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:30:45 2020

@author: niall
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict

# Importing the dataset
dataset = pd.read_csv('collisions_events.csv', sep=';')
data_top = dataset.head()
data_times = dataset.iloc[:1000, 2]
data_street_type = dataset.iloc[:, 5]
data_road_class = dataset.iloc[:, 17]
data_visibilty = dataset.iloc[:, 18]
data_lat = dataset.iloc[:, -1]
data_lon = dataset.iloc[:, -2]

# subset data by lat/lon
bbox = [43.673214, 43.629795, -79.313880, -79.467897] # from looking at google maps. N S E W
dataset = dataset[(dataset.longitude >= bbox[3]) & (dataset.longitude <= bbox[2])]
dataset = dataset[(dataset.latitude >= bbox[1]) & (dataset.latitude <= bbox[0])]



isanan = data_visibilty.isna()



vis = list(OrderedDict.fromkeys(data_visibilty))
vis1 = list(dict.fromkeys(data_visibilty))



X = dataset.iloc[:, [2, 3]].values
y = dataset.iloc[:, 4].values



plt.scatter(data_lon, data_lat)
plt.show()