#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:26:13 2020

@author: niall
"""

import osmnx as ox
import pandas as pd

G = ox.load_graphml('/Users/niall/insight_project/data/cleaned/Toronto.graphml')
df = pd.read_csv('/Users/niall/insight_project/data/processed/roads_and_probs.csv')
df = df[['u', 'v', 'collision_prob', 'collision_yn']]
df['colour'] = 'red'

#add coloour to the edges that
nodes, edges = ox.graph_to_gdfs(G)
edges = edges.merge(df, on=['u', 'v'], how='left')
edges.colour[edges.colour.isna()] = 'grey'

ox.plot.plot_graph(G, edge_color=edges.colour, node_size=0, fig_height=12, fig_width=12)


#ox.plot.get_edge_colors_by_attr(G, attr, num_bins=5, cmap='viridis', start=0, stop=1, na_color='none')