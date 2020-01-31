#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:37:08 2020

@author: niall
"""
import pandas as pd

# Read in the collision data and add
df_roads = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_20plus_collisions.csv')
df_weather = pd.read_csv('/Users/niall/insight_project/data/raw/weather_darksky_subset.csv')

df = pd.concat([df_roads, df_weather], axis=1)

df['temperature'] = (df['temperature'] - 32) / 1.8
df['apparentTemperature'] = (df['apparentTemperature'] - 32) / 1.8

# there are a few instances with no wind speed. It's a small fraction so just remove them for now
df = df.dropna(axis='rows', how='any', thresh=None, subset=['windSpeed'], inplace=False)
df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_with_roads_and_weather_clean.csv', index=False)


#################################################
## For now, add weather data to the synthetic weather data you already made.
## In future, make better synthetic data from the real dataset made above, which
## also has weather added.
#################################################
#df_real = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_with_roads_and_weather_clean.csv')
#df_real= df_real[df_real['collision_count'] > 50]
#df_synthetic = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads.csv')
#df_synthetic.columns = df_roads.columns
#df_real_weather = df_real.iloc[:, 29:]
#df_synthetic = df_synthetic.iloc[0:36494,:]
#
#for name in df_real_weather.columns:
#    df_synthetic[name] = df_real_weather[name]
#
#df_synthetic.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads_and_weather.csv', index=False)
#
##test = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads_and_weather.csv')












#df_weather = df_weather.drop('Unnamed: 0', axis=1)
#df = df.head()

#column_names_weather = ['time', 'summary', 'icon', 'precipIntensity', 'precipProbability', 'precipType', 'precipAccumulation', 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'pressure', 'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex', 'visibility']