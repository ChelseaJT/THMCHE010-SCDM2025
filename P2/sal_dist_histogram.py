#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:30:06 2025

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

# Define bin edges from 30 to 35 with step size of 0.5
bins = np.arange(30, 35.5, 0.5)  # Includes 35

# Plot histogram
plt.figure(figsize=(8, 5))
plt.hist(filtered_data["TSG_SALINITY"], bins=bins, color="blue", edgecolor="black", alpha=0.7)

# Labels and Title
plt.xlabel("Salinity (psu)")
plt.ylabel("Frequency")
plt.title("Histogram of Salinity (30 - 35 psu)")

# Grid for better readability
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
plt.show()