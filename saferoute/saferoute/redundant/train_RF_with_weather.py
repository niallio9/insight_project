#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:43:16 2019

@author: niall
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
#from sklearn import metrics

# Import the dataset
df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_with_roads_and_weather_clean.csv')
df = df[df['collision_count'] > 50]
df_synthetic = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads_and_weather.csv')
#df_synthetic.columns = df.columns
df = df.append(df_synthetic, ignore_index=True)
del df_synthetic
df_top = df.head()

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
#features_cat = ['highway']
X = df[features]
y = df['collision']

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
preprocessor = make_column_transformer( (OneHotEncoder(), features_cat), remainder="passthrough")
X = preprocessor.fit_transform(X)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)


# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy',class_weight='balanced', oob_score=True, random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

score = classifier.score( X_test, y_test)

# save the model to disk
filename = '/Users/niall/insight_project/data/processed/model_RF_weather.sav'
pickle.dump(classifier, open(filename, 'wb'))
filename_transformer = '/Users/niall/insight_project/data/processed/feature_encoder_RF_weather.sav'
pickle.dump(preprocessor, open(filename_transformer, 'wb'))

# feature importance
#preprocessor.fit(X[features_cat])
x = list(preprocessor.transformers_[0][1].get_feature_names(features_cat))
for name in features_num:
    x.append(name)

importances = classifier.feature_importances_
std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
x = [x[i] for i in indices]

# Print the feature ranking
print("Feature ranking:")
for f in range(len(x)):
    print("%d. feature %s (%f)" % (f + 1, x[f], importances[indices[f]]))

# plot fetures
# Plot the feature importances of the forest
i_features = 30
plt.figure()
plt.title("Feature importances")
plt.barh(range(i_features), importances[indices[:i_features]], color="b", xerr=std[indices[:i_features]], tick_label=x[:i_features])
plt.show()

#END