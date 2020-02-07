#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:52:52 2020

@author: niall
"""
#import pandas as pd
##from datetime import datetime as dt
#from darksky import forecast
#import pickle
#from datetime import datetime as dt
import osmnx as ox
import custom_funcs as CF

input1 = '253 merton street, toronto'
input2 = '20 adelaide street east, toronto'
origin = list(ox.geocode(input1))
destination = list(ox.geocode(input2))
filename_out = '/Users/niall/insight_project/projectname/projectname/custom_functions_test_output'

current_weather = CF.get_current_weather_toronto()
# add the weather data to the unique roads
roads_with_weather = CF.add_current_weather_to_unique_roads(current_weather)
# run the unique roads through the classifier and save locally
roads_with_weather = CF.get_collision_probs(roads_with_weather)
# save the graph as the name used by the return statement below
CF.plot_map_with_probs_routes(roads_with_weather, origin, destination, filename=filename_out)
