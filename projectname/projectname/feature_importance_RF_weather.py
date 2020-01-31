#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:43:16 2019

@author: niall
"""


import numpy as np
import pandas as pd
import pickle


# read in the model
model = pickle.load(open("/Users/niall/insight_project/projectname/projectname/model_RF_with_weather.sav","rb"))

# read in the feature transformer
preprocessor1 = pickle.load(open("/Users/niall/insight_project/projectname/projectname/feature_encoder_RF_with_weather.sav","rb"))
