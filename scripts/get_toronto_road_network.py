#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:10:57 2020

@author: niall
"""
import osmnx as ox
import networkx as nx
import pandana as pdna
from pandana.loaders import osm
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use( 'tkagg' )


bbox = [43.703214, 43.629795, -79.303880, -79.477897] # NSEW from looking at google maps

# For getting map from collision coordinates
df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean.csv')
df = df[(df.longitude >= bbox[3]) & (df.longitude <= bbox[2])]
df = df[(df.latitude >= bbox[1]) & (df.latitude <= bbox[0])]
df = df.reset_index(drop=True)
df_top = df.head()
#bbox = [df[['latitude']].max().to_numpy(), df[['latitude']].min().to_numpy(), 
#        df[['longitude']].max().to_numpy(), df[['longitude']].min().to_numpy()]

G = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type='drive', simplify=True) # N, S, E, W
ox.clean_intersections(G, tolerance=15, dead_ends=False)

nearest_edges = ox.get_nearest_edges(G, df.longitude, df.latitude, method='balltree')
nearest_edges_unique, unique_edges_reverse_index, unique_edge_counts = np.unique(nearest_edges, axis=0, return_inverse =True, return_counts=True)

df['u'] = nearest_edges[:, 0]
df['v'] = nearest_edges[:, 1]
df['collision_count'] = unique_edge_counts[unique_edges_reverse_index]
df_top = df.head()

nodes, edges = ox.graph_to_gdfs(G)
merged_df = df.merge(edges, how='inner', on=['u', 'v'])
merged_df = merged_df[list(merged_df)[:29]] #these columns are empty
merged_df_top = merged_df.head()

merged_df.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv', index=False)

# NOW


df_top = df.head()
df_merged_top = merged_df.head()



plt.hist(unique_edge_counts, bins=100)
plt.show()

#ox.save_graphml(G, filename='Toronto.graphml')
#G2 = ox.load_graphml('Toronto.graphml')

fig, ax = ox.plot_graph(G)
fig, ax = ox.plot.plot_graph_route(G, [ nearest_edges_unique[18,:]])