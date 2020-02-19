#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:37:08 2020

@author: niall
"""
import pandas as pd
from csv import writer
from datetime import datetime as dt
from darksky import forecast

api_key = 'be5915f53fd9d45fd540944f2182476b'

df = pd.read_csv('/Users/niall/saferoute/data/cleaned/collision_events_clean_with_roads_20plus_collisions.csv')
myfile = open('/Users/niall/insight_project/data/raw/myfile.csv','w')
wrtr = writer(myfile, delimiter=',')
#csv_writer = writer(output)
TORONTO = api_key, 43.6529, -79.3849

print('loop length is '+str(len(df.index)))
for i in range(len(df.index)):
    try:
        if i % 1000 == 0:
            print('past loop '+ str(i))
        time_dt = dt.strptime(df['collision_time'][i], '%Y-%m-%d %H:%M:%S') # easy format to work with datetime
        t = dt(time_dt.year, time_dt.month, time_dt.day, time_dt.hour).isoformat()
        toronto = forecast(*TORONTO, time=t) # call the Dark SkyAPI
        x = toronto.currently._data # this is the weather at the time of the collision
        data = list(x.values())
        wrtr.writerow(data)
        myfile.flush()
    except: # on a rare occasion, the API will return a bad value. the weather from the previous collision is a good indication of the weather we are looking for
        print(i)
        print("error "+ str(i) )
        wrtr.writerow(data)
        continue

myfile.close()

#END