#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 17:41:53 2025

@author: chelseathomas
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filename = "SAA2_WC_2017_metocean_10min_avg.csv"
data = pd.read_csv(filename)

data['TIME_SERVER'] = pd.to_datetime(data['TIME_SERVER'])

start_date = "2017/06/28 17:10"
end_date = "2017/07/04 23:50"
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = data[(data['TIME_SERVER'] >= start_date) & (data['TIME_SERVER'] <= end_date)]
scatter = plt.scatter(filtered_data["WIND_SPEED_TRUE"],filtered_data["AIR_TEMPERATURE"], c=filtered_data['LATITUDE'], cmap='viridis', edgecolors='k')
plt.colorbar(scatter,label='Latitude')
plt.ylabel("Air Temperature / °C", fontsize=12)
plt.xlabel("Wind Speed / m/s", fontsize=12)
plt.title("Scatter Plot to Show Wind Speed / m/s , Air Temperature /°C and Latitude", fontsize=14)

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("scatter_plot.png", dpi=300,bbox_inches='tight')
plt.show()
