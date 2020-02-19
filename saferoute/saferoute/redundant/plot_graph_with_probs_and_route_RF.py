#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:26:13 2020

@author: niall
"""

import osmnx as ox
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#origin = [43.681641, -79.423906]
origin = [43.663389, -79.461929]
destination = [43.650854, -79.377587]
#origin = [43.6949, -79.453]
#destination = [43.6966, -79.4453]
lats = [origin[1], destination[1]]
lons = [origin[0], destination[0]]

G = ox.load_graphml('/Users/niall/saferoute/data/cleaned/Toronto.graphml')
df = pd.read_csv('/Users/niall/insight_project/data/processed/unique_roads_collision_yn_RF.csv')
df = df[['u', 'v', 'collision_yn']]
df['colour'] = 'red'
df['weights'] = df['collision_yn'] * 100000

nearest_nodes = ox.get_nearest_nodes(G, lats, lons, method=None)

#add colour to the edges that have a crash risk
nodes, edges = ox.graph_to_gdfs(G)
edges = edges.merge(df, on=['u', 'v'], how='left')
edges.colour[edges.colour.isna()] = 'grey'
edges.weights[edges.weights.isna()] = 1
edges.weights[edges.weights == 0] = 1
#edges.weights = edges.weights.values * edges.length.values


i = 0
for u, v, k, data in G.edges(keys=True, data=True):
#    print(data)
    data['impedance'] = edges['weights'][i]
#    print(data['length'])
#    print(data['impedance'])
#    print(edges['weights'][i])
#    print(edges['weights'][i])
    i = i+1
    

route_by_weight = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='impedance')
route_by_length = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='length')
routes = [route_by_weight, route_by_length]
# create route colors
rc1 = ['green'] * (len(route_by_weight))
rc2 = ['blue'] * len(route_by_length)
route_colours = rc1 + rc2

filename_save = '/Users/niall/insight_project/projectname/static/map_with_routes'
fig, ax = ox.plot_graph_routes(G, routes, node_size=0, route_color=route_colours,
                               orig_dest_node_color='green', edge_color=edges.colour, 
                               fig_height=12, fig_width=12, margin=0, axis_off=False,
                               show=True, save=True, file_format='png',
                               filename=filename_save)

routes = route_by_length
route_colours = rc2
#fig, ax = ox.plot_graph_route(G, routes, node_size=0, route_color=route_colours,
#                               orig_dest_node_color='green', edge_color=edges.colour, 
#                               fig_height=12, fig_width=12, margin=0, axis_off=False,
#                               show=True, save=True, file_format='png',
#                               filename=filename_save)

y = ox.geocode('22, epsom avenue, toronto')
ox.plot_route_folium(G, routes, route_map=None, popup_attribute=None, tiles='cartodbpositron', zoom=1, fit_bounds=True, route_color='#cc0000', route_width=5, route_opacity=1)
#fig.savefig('/Users/niall/insight_project/data/map_output/map_with_routes.png')
plt.show()
#END
