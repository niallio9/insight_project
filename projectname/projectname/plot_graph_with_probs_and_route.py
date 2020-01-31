#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:26:13 2020

@author: niall
"""

import osmnx as ox
import pandas as pd
import networkx as nx

origin = [43.681641, -79.423906]
destination = [43.650854, -79.377587]
#origin = [43.6949, -79.453]
#destination = [43.6966, -79.4453]
lats = [origin[1], destination[1]]
lons = [origin[0], destination[0]]

G = ox.load_graphml('/Users/niall/insight_project/data/cleaned/Toronto.graphml')
df = pd.read_csv('/Users/niall/insight_project/data/processed/roads_and_probs.csv')
df = df[['u', 'v', 'collision_prob', 'collision_yn']]
df['colour'] = 'red'
df['weights'] = df['collision_yn'] * 100000

nearest_nodes = ox.get_nearest_nodes(G, lats, lons, method=None)

#add colour to the edges that
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
    

route_color=['green', 'blue']

route_by_weight = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='impedance')
route_by_length = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='length')
routes = [route_by_weight, route_by_length]
# create route colors
rc1 = ['green'] * (len(route_by_weight) - 1)
rc2 = ['red'] * len(route_by_length)
route_colours = rc1 + rc2

fig, ax = ox.plot_graph_routes(G, routes, node_size=0, route_color=route_colours, orig_dest_node_color='green', edge_color=edges.colour)

#END

#fig, ax = ox.plot_graph_route(G, route_by_weight, node_size=0, route_color='green', orig_dest_node_color='green', edge_color=edges.colour)
#
#
#route_by_length = nx.shortest_path(G, source=nearest_nodes[0], target=nearest_nodes[1], weight='length')
#ox.plot_graph_route(G, route_by_length, node_size=0, route_color='blue', orig_dest_node_color='green', edge_color=edges.colour)
#
#
#ox.plot.plot_graph(G, edge_color=edges.colour, node_size=0, fig_height=12, fig_width=12)


#ox.plot.get_edge_colors_by_attr(G, attr, num_bins=5, cmap='viridis', start=0, stop=1, na_color='none')