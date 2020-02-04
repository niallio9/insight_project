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
import osmnx as ox
import networkx as nx


def get_current_weather_toronto():
    api_key = 'be5915f53fd9d45fd540944f2182476b'
    TORONTO = api_key, 43.6529, -79.3849
#    t  = dt.now().isoformat()
    toronto = forecast(*TORONTO)
    data_current = toronto.currently._data
    df_data = pd.DataFrame(data_current, index=[0])
    columns_to_keep = ['time', 'summary', 'icon', 'temperature',
                       'apparentTemperature', 'dewPoint', 'humidity', 'pressure',
                       'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex',
                       'visibility']
    df_data = df_data[columns_to_keep]
    df_data.loc[0, 'temperature'] = (df_data.loc[0, 'temperature'] - 32) / 1.8
    df_data.loc[0, 'apparentTemperature'] = (df_data.loc[0, 'apparentTemperature'] - 32) / 1.8
    x = list(df_data.columns)
    x[-1] = 'visibility.1'
    df_data.columns = x
    current_weather = df_data.copy()
    return current_weather

def add_current_weather_to_unique_roads(current_weather):
    df_roads = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
    df_roads = df_roads[df_roads['collision_count'] > 50]
    df_roads = df_roads.drop_duplicates(subset=['u', 'v'], keep='first') # get the unique roads
    for name in current_weather.columns:
        print(name)
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
    unique_roads_with_weather.to_csv('/Users/niall/insight_project/data/processed/unique_roads_collision_yn_RF_weather.csv', index=False)
    return unique_roads_with_weather

def plot_map_with_probs_routes(origin, destination): # each input is a list with [lat, lon]
    #origin = [43.6949, -79.453]
    #destination = [43.6966, -79.4453]
    lats = [origin[1], destination[1]]
    lons = [origin[0], destination[0]]
    #load the 
    G = ox.load_graphml('/Users/niall/insight_project/data/cleaned/Toronto.graphml')
    df_roads = pd.read_csv('/Users/niall/insight_project/data/processed/unique_roads_collision_yn_RF_weather.csv')
    df_roads = df_roads[['u', 'v', 'collision_yn']]
    df_roads['colour'] = 'red'
    df_roads['weights'] = df_roads['collision_yn'] * 100000
    
    nearest_nodes = ox.get_nearest_nodes(G, lats, lons, method=None)
    #add colour to the edges that have a crash risk
    nodes, edges = ox.graph_to_gdfs(G)
    edges = edges.merge(df_roads, on=['u', 'v'], how='left')
    edges.colour[edges.colour.isna()] = 'grey'
    edges.weights[edges.weights.isna()] = 1
    edges.weights[edges.weights == 0] = 1
    
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
    filename_save = '/Users/niall/insight_project/projectname/static/map_with_routes_for_web'
    fig, ax = ox.plot_graph_routes(G, routes, node_size=0, route_color=route_colours,
                                   orig_dest_node_color='green', edge_color=edges.colour, 
                                   fig_height=12, fig_width=12, margin=0, axis_off=False,
                                   show=True, save=True, file_format='png',
                                   filename=filename_save)

