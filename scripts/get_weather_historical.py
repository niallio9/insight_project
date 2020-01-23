#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:37:08 2020

@author: niall
"""

api_key = 'be5915f53fd9d45fd540944f2182476b'

from darksky import forecast
boston = forecast(api_key, 42.3601, -71.0589)