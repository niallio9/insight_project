#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:22:10 2020

@author: niall
"""

import numpy as np
import pandas as pd
import pickle


# read in the model
model = pickle.load(open("/Users/niall/insight_project/projectname/projectname/model_RF.sav","rb"))

#read in the roads
df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
df = df[df['collision_count'] > 50]
unique_roads = df.drop_duplicates(subset=['u', 'v'], keep='first') # get the unique roads

# read in the feature transformer
preprocessor1 = pickle.load(open("/Users/niall/insight_project/projectname/projectname/feature_encoder_RF.sav","rb"))

##read in the unique road data
#unique_roads = pickle.load(open('/Users/niall/insight_project/data/cleaned/unique_roads.p',"rb"))
#unique_roads = unique_roads[0]

features = ['longitude', 'latitude',
       'road_class', 'visibility', 'light', 'road_surface_cond', 'month',
       'day_of_week', 'hour_of_day','collision_count']

features_cat = ['road_class', 'visibility', 'light',
                'road_surface_cond', 'month', 'day_of_week', 'hour_of_day']

X1 = unique_roads.copy()

# Pleaceholder data for now
X1['month'] = 1
X1['day_of_week'] = 5
X1['hour_of_day'] = 18
X1['road_surface_cond'] = 'DRY'
X1['visibility'] = 'CLEAR'
X1['light'] = 'DAYLIGHT'
X1 = X1[features]



#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#from sklearn.compose import make_column_transformer
#preprocessor = make_column_transformer( (OneHotEncoder(), features_cat), remainder="passthrough")
X1 = preprocessor1.transform(X1)

y_predict = model.predict(X1)

unique_roads['collision_yn'] = y_predict

unique_roads.to_csv('/Users/niall/insight_project/data/processed/unique_roads_collision_yn_RF.csv', index=False)

