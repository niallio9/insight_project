#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 02:24:23 2020

@author: niall
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
df = df[df['collision_count'] > 100]

df = df.reset_index(drop=True)

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