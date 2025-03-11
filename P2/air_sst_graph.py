#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:14:29 2025

@author: chelseathomas
"""

import matplotlib.pyplot as plt 
import pandas as pd 

filename = "SAA2_WC_2017_metocean_10min_avg.csv"
data = pd.read_csv(filename)

data['TIME_SERVER'] = pd.to_datetime(data['TIME_SERVER'])

start_date = "2017/06/28 17:10"
end_date = "2017/07/04 23:50"

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = data[(data['TIME_SERVER'] >= start_date) & (data['TIME_SERVER'] <= end_date)]
plt.style.use('grayscale')

# Adding labels for the legend
plt.plot(filtered_data['TIME_SERVER'], filtered_data['TSG_TEMP'], label="Sea Surface Temperature") 
plt.plot(filtered_data['TIME_SERVER'], filtered_data['AIR_TEMPERATURE'], label="Air Temperature")   

plt.xlabel('Date')
plt.ylabel('Temperature (Celsius)')
plt.title('Air and Sea Surface Temperature °C from SA Agulhas II Departure on 2017-06-28 to its Southernmost Location on 2017-07-04')

plt.xticks(rotation=90)
plt.legend(loc="upper right")  # Display legend with labels
plt.show()