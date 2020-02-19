#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 02:24:23 2020

@author: niall

A basic script for making deom plots.

To Do: make individual functions for easier plotting from outside of an IDE
"""

#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import osmnx as ox

df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_with_roads_and_weather_clean.csv')
df = df[df['collision_count'] > 50]
df = df.reset_index(drop=True)
dftop = df.head()

G = ox.load_graphml('/Users/niall/insight_project/data/cleaned/Toronto_large.graphml')
nodes, edges = ox.graph_to_gdfs(G)

plt.figure()
plt.hist(edges['length'], bins = 50)
plt.title('Length of Toronto street segments')
plt.xlabel('road count')
plt.ylabel('length [m]')
plt.show()



plt.figure()
plt.scatter(df['longitude'], df['latitude'], s=2, c='r')
plt.title('Toronto collisions by location')
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.show()

plt.figure()
plt.hist(df['windSpeed'], bins=50)
plt.title('collisions by wind speed')
plt.xlabel('wind speed [mph]')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['windGust'], bins=50)
plt.title('collisions by wind gust')
plt.xlabel('wind gust [mph]')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['windBearing'], bins=50)
plt.title('collisions by wind bearing')
plt.xlabel('bearing [degrees clockwise from north]')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['temperature'], bins=100)
plt.title('collisions by temperature')
plt.xlabel('temperature [C]')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['hour_of_day'], bins=24)
plt.title('collisions by hour of day')
plt.xlabel('Hour')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['day_of_week'], bins=7)
plt.title('collisions by day of the week')
plt.xlabel('day')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['month'], bins=12)
plt.title('collisions by month')
plt.xlabel('month')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.hist(df['year'], bins=10)
plt.title('collisions by year')
plt.xlabel('year')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.scatter(df['year'], df['collision_count'])
plt.title('collisions by year')
plt.xlabel('year')
plt.ylabel('collision count')
plt.show()

plt.figure()
plt.scatter(df['longitude'], df['latitude'], color='yellow')
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.show()

df['road_surface_cond'].value_counts().plot(kind='bar')
plt.title('collisions by road condition')
plt.ylabel('collision count')
plt.show()

df['road_class'].value_counts().plot(kind='bar')
plt.title('collisions by road class')
plt.ylabel('collision count')
plt.show()

df['visibility'].value_counts().plot(kind='bar')
plt.title('collisions by visibility')
plt.ylabel('collision count')
plt.show()

df['light'].value_counts().plot(kind='bar')
plt.title('collisions by light')
plt.ylabel('collision count')
plt.show()

list(dict.fromkeys(df['road_surface_cond']))
list(dict.fromkeys(df['road_class']))