#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 17:13:40 2025

@author: chelseathomas
"""

import matplotlib.pyplot as plt
import pandas as pd  

filename = "ctd_data_29112008.dat"
ctd_data = pd.read_csv(filename, delim_whitespace=True)

ctd_data = ctd_data.sort_values(by="Depth(m)")

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 5))  # 1 row, 2 columns

fig.suptitle("CTD Temperature and Salinity Profiles with Depth")

ax1.plot(ctd_data["Temperature°C"], ctd_data["Depth(m)"], color='r', label="Temperature°C")
ax1.set_xlabel("Temperature°C", color='r')
ax1.set_ylabel("Depth (m)")
ax1.invert_yaxis()  # Make depth increase downward
ax1.tick_params(axis='x', labelcolor='r')
ax1.legend(loc="upper right")
ax1.grid(True)

ax2.plot(ctd_data["Salinity(psu)"], ctd_data["Depth(m)"], color='b', label="Salinity (psu)")
ax2.set_xlabel("Salinity (psu)", color='b')
ax2.tick_params(axis='x', labelcolor='b')
ax2.legend(loc="upper right")
ax2.grid(True)
plt.style.use('default')
plt.show()