#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 12:03:01 2025

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
temp_mean = np.mean(filtered_data["TSG_TEMP"])
temp_std = np.std(filtered_data["TSG_TEMP"])
sal_mean = np.mean(filtered_data["TSG_SALINITY"])
sal_std = np.std(filtered_data["TSG_SALINITY"])

temp_q1 = np.nanpercentile(filtered_data["TSG_TEMP"], 25)
temp_q3 = np.nanpercentile(filtered_data["TSG_TEMP"], 75)
temp_iqr = temp_q3 - temp_q1

sal_q1 = np.nanpercentile(filtered_data["TSG_SALINITY"], 25)
sal_q3 = np.nanpercentile(filtered_data["TSG_SALINITY"], 75)
sal_iqr = sal_q3 - sal_q1

table_data = [
    ["Sea Surface Temperature °C", f"{temp_mean:.2f}", f"{temp_std:.2f}", f"{temp_iqr:.2f}"],
    ["Salinity psu", f"{sal_mean:.2f}", f"{sal_std:.2f}", f"{sal_iqr:.2f}"]
]

columns = ["Variable", "Mean", "Standard Deviation", "Interquartile Range (IQR)"]

fig, ax = plt.subplots(figsize=(7, 2))
ax.set_axis_off()

table = ax.table(cellText=table_data, colLabels=columns, cellLoc="center", loc="center")

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([0, 1, 2, 3])

plt.show()
