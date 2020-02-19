#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: niall

The local path must be edited to match your directory.
The Dark Sky API key must be valid (see Readme)
"""
import pandas as pd
from darksky import forecast
import pickle
from datetime import datetime as dt
import osmnx as ox
import networkx as nx

local_path = '/Users/niall/insight_project'

def get_current_weather_toronto():
    api_key = 'xxxxxxxxxxxxxxxx' # THIS SHOULD BE REPLACED WITH YOUR API KEY FROM DARK SKY API
    TORONTO = api_key, 43.6529, -79.3849
    toronto = forecast(*TORONTO) # the call to the Dark Sky API
    data_current = toronto.currently._data
    df_data = pd.DataFrame(data_current, index=[0]) # the time of the collision
    columns_to_keep = ['time', 'summary', 'icon', 'temperature',
                       'apparentTemperature', 'dewPoint', 'humidity', 'pressure',
                       'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex',
                       'visibility']
    df_data = df_data[columns_to_keep]
    # convert temperature from F to C
    df_data.loc[0, 'temperature'] = (df_data.loc[0, 'temperature'] - 32) / 1.8
    df_data.loc[0, 'apparentTemperature'] = (df_data.loc[0, 'apparentTemperature'] - 32) / 1.8
    x = list(df_data.columns)
    x[-1] = 'visibility.1' # there is already a (crappy) visibility feature in the collision data
    df_data.columns = x
    current_weather = df_data
    return current_weather

def add_current_weather_to_unique_roads(current_weather):
    filein = '%s/data/cleaned/collision_events_clean_with_roads.csv' % (local_path)
    df_roads = pd.read_csv(filein)
    df_roads = df_roads[df_roads['collision_count'] > 50]
    df_roads = df_roads.drop_duplicates(subset=['u', 'v'], keep='first') # get the unique roads
    for name in current_weather.columns:
        df_roads.loc[:, name] = current_weather[name].values
    ## add the current hour, day, and month to the unique roads
    today = dt.today()
    df_roads['year'] = today.year
    df_roads['month'] = today.month
    df_roads['hour_of_day'] = today.hour
    df_roads['day_of_week'] = today.weekday() + 1 # 0=monday, 6=sunday. we're using 1-7
    unique_roads_with_weather = df_roads.copy()
    return unique_roads_with_weather

def get_collision_probs(unique_roads_with_weather):
    # read in the model and the preprocessor
    filein = '%s/data/processed/model_RF_weather.sav' % (local_path)
    model = pickle.load(open(filein,"rb"))
    filein = '%s/data/processed/feature_encoder_RF_weather.sav' % (local_path)
    preprocessor = pickle.load(open(filein,"rb"))
    features = ['longitude', 'latitude',
       'road_class', 'visibility', 'light', 'road_surface_cond', 'month',
       'day_of_week', 'hour_of_day','collision_count','summary', 'icon', 'temperature',
       'apparentTemperature', 'dewPoint', 'humidity', 'windSpeed', 'windGust',
       'windBearing', 'cloudCover', 'uvIndex', 'visibility.1']
#    features_num = ['longitude', 'latitude', 'collision_count', 'temperature',
#       'apparentTemperature', 'dewPoint', 'humidity', 'windSpeed', 'windGust',
#       'windBearing', 'cloudCover', 'uvIndex', 'visibility.1']
#    features_cat = ['road_class', 'visibility', 'light',
#                'road_surface_cond', 'month', 'day_of_week', 'hour_of_day',
#                'summary', 'icon']
    X = unique_roads_with_weather[features].copy()
    X = preprocessor.transform(X)
    unique_roads_with_weather['collision_yn'] = model.predict(X)
    return unique_roads_with_weather

def plot_map_with_probs_routes(unique_roads_with_weather, origin=[43.663389, -79.461929],
                               destination=[43.650854, -79.377587],
                               filename=''): # each input is a list with [lat, lon]
    
    lats = [origin[1], destination[1]]
    lons = [origin[0], destination[0]]
    #load the city network for plotting
    filein = '%s/data/cleaned/Toronto_large.graphml' % (local_path)
    G = ox.load_graphml(filein)
    df_roads = unique_roads_with_weather
    df_roads = df_roads[['u', 'v', 'collision_yn']]
    df_roads['colour'] = 'red'
    df_roads['weights'] = df_roads['collision_yn'] * 10000
    
    nearest_nodes = ox.get_nearest_nodes(G, lats, lons, method=None)
    #add colour to the edges that have a crash risk
    nodes, edges = ox.graph_to_gdfs(G)
    edges = edges.merge(df_roads, on=['u', 'v'], how='left')
    edges.colour[edges.colour.isna()] = 'grey'
    edges.weights[edges.weights.isna()] = 1
    edges.weights[edges.weights == 0] = 1
    
    #add the weights to the edge attributes as impedance
    i = 0
    for u, v, k, data in G.edges(keys=True, data=True):
    #    print(data)
        data['impedance'] = edges['weights'][i]
    #    print(data['length'])
    #    print(data['impedance'])
    #    print(edges['weights'][i])
    #    print(edges['weights'][i])
        i = i+1
        
    #calculate the routes
    route_by_weight = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='impedance')
    route_by_length = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='length')
    routes = [route_by_weight, route_by_length]
    # create route colors
    rc1 = ['green'] * (len(route_by_weight))
    rc2 = ['blue'] * len(route_by_length)
    route_colours = rc1 + rc2
    # save the figure as a png
    filename_save = filename
    fig, ax = ox.plot_graph_routes(G, routes, node_size=0, route_color=route_colours,
                                   orig_dest_node_color='green', edge_color=edges.colour, 
                                   fig_height=8.8, fig_width=12, margin=0, axis_off=True,
                                   show=False, save=True, file_format='png',
                                   filename=filename_save)
    return

