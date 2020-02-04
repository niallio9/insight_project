#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:48:29 2020

@author: niall
"""
import pandas as pd
#from datetime import datetime as dt
from darksky import forecast
import pickle
from datetime import datetime as dt


def get_current_weather_toronto():
    api_key = 'be5915f53fd9d45fd540944f2182476b'
    TORONTO = api_key, 43.6529, -79.3849
#    t  = dt.now().isoformat()
    toronto = forecast(*TORONTO)
    data_current = toronto.currently._data
    df_data = pd.DataFrame(data_current, index=[0])
    columns_to_keep = ['time', 'summary', 'icon', 'precipAccumulation', 'temperature',
                       'apparentTemperature', 'dewPoint', 'humidity', 'pressure',
                       'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex',
                       'visibility']
    df_data = df_data[columns_to_keep]
    df_data.loc[0, 'temperature'] = (df_data.loc[0, 'temperature'] - 32) / 1.8
    df_data.loc[0, 'apparentTemperature'] = (df_data.loc[0, 'apparentTemperature'] - 32) / 1.8
    return df_data

def add_current_weather_to_unique_roads(current_weather):
    df_roads = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
    df_roads = df_roads[df_roads['collision_count'] > 50]
    df_roads = df_roads.drop_duplicates(subset=['u', 'v'], keep='first') # get the unique roads
    for name in current_weather.columns:
        df_roads[name] = current_weather[name].values
    ## add the current hour, day, and month to the unique roads
    today = dt.today()
    df_roads['year'] = today.year
    df_roads['month'] = today.month
    df_roads['hour_of_day'] = today.hour
    df_roads['day_of_week'] = today.weekday() + 1 # 0=monday, 6=sunday. we're using 1-7
    return df_roads

def get_collision_probs(unique_roads_with_weather):
    # read in the model
    model = pickle.load(open("/Users/niall/insight_project/data/processed/model_RF_weather.sav","rb"))
    preprocessor = pickle.load(open("/Users/niall/insight_project/data/processed/feature_encoder_RF_weather.sav","rb"))
    features = ['longitude', 'latitude',
       'road_class', 'visibility', 'light', 'road_surface_cond', 'month',
       'day_of_week', 'hour_of_day','collision_count','summary', 'icon', 'temperature',
       'apparentTemperature', 'dewPoint', 'humidity', 'windSpeed', 'windGust',
       'windBearing', 'cloudCover', 'uvIndex', 'visibility.1']
    features_num = ['longitude', 'latitude', 'collision_count', 'temperature',
       'apparentTemperature', 'dewPoint', 'humidity', 'windSpeed', 'windGust',
       'windBearing', 'cloudCover', 'uvIndex', 'visibility.1']
    features_cat = ['road_class', 'visibility', 'light',
                'road_surface_cond', 'month', 'day_of_week', 'hour_of_day',
                'summary', 'icon']
    X = unique_roads_with_weather[features].copy()
    X = preprocessor.transform(X)
    unique_roads_with_weather['collision_yn'] = model.predict(X)
    return unique_roads_with_weather
