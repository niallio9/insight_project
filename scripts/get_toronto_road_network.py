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
from scipy import stats
import matplotlib.pyplot as plt
matplotlib.use( 'tkagg' )

G = ox.graph_from_place('Piedmont, California, USA', network_type='drive')

#bbox = [44.58216, 43.34912, -78.73891, -79.71775]
bbox = [43.673214, 43.629795, -79.313880, -79.467897] # from looking at google maps
G = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type='drive') # N, S, E, W

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

nearest_edges = ox.get_nearest_edges(G, dataset.longitude, dataset.latitude, method='balltree')
nearest_edges_unique, unique_edge_counts = np.unique(nearest_edges, axis=0, return_counts=True)

plt.hist(unique_edge_counts, bins=100)
plt.show()

fig, ax = ox.plot_graph(G)