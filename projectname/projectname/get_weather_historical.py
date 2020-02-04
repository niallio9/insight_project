#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:37:08 2020

@author: niall
"""
import pandas as pd
#from io import StringIO
from csv import writer
from datetime import datetime as dt
from darksky import forecast

api_key = 'be5915f53fd9d45fd540944f2182476b'

df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_20plus_collisions.csv')
#df = df.head()
#data = 
#output = StringIO()
myfile = open('/Users/niall/insight_project/data/raw/myfile.csv','w')
wrtr = writer(myfile, delimiter=',')
#csv_writer = writer(output)
TORONTO = api_key, 43.6529, -79.3849

print('loop length is '+str(len(df.index)))
for i in range(len(df.index)):
    try:
        if i % 1000 == 0:
            print('past loop '+ str(i))
        time_dt = dt.strptime(df['collision_time'][i], '%Y-%m-%d %H:%M:%S')
        t = dt(time_dt.year, time_dt.month, time_dt.day, time_dt.hour).isoformat()
        toronto = forecast(*TORONTO, time=t)
        x = toronto.currently._data
        data = list(x.values())
        wrtr.writerow(data)
        myfile.flush()
#        if i % 1000 == 0:
#            myfile.flush() # whenever you want, and/or
##        csv_writer.writerow(data)
    except:
        print(i)
        print("error "+ str(i) )
        wrtr.writerow(data)
#        csv_writer.writerow(data)
        continue

myfile.close()


##output.seek(0) # we need to get back to the start of the BytesIO
#df_weather = pd.read_csv(output, header=None)
#column_names = list(x.keys())
#df_weather.columns = column_names
#df_weather.to_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_20plus_collisions_weather.csv', index=False)
#test = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads_20plus_collisions_weather.csv')

# to get the datetime back from the unix time:
#x = dt.fromtimestamp(df_weather['time'][0]);