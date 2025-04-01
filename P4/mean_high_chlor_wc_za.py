import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset
ds_chl = xr.open_dataset('ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc')

# Sort time values to avoid slicing errors
ds_chl = ds_chl.sortby('time')

# Extract chlorophyll variable
chlor_data = ds_chl['chlor_a']

# Define region coordinates
lat_min, lat_max = -34.5, -32.75
lon_min, lon_max = 15.5, 19.0

# Subset chlorophyll data to region of interest
region_chl_data = chlor_data.sel(lat=slice(lat_max, lat_min), lon=slice(lon_min, lon_max))

# 🌟 **Filter all data from 1997-1998**
region_chl_97_98 = region_chl_data.where(region_chl_data['time'].dt.year.isin([1997, 1998]), drop=True)

# Check available months
print("Available months in 1997-1998:", region_chl_97_98['time'].values)

# Compute mean seasonal cycle for 1997-1998
seasonal_cycle_97_98 = region_chl_97_98.groupby('time.month').mean(dim=['lat', 'lon'])

# Select a high-chlorophyll location
high_chl_point_97_98 = region_chl_97_98.sel(lat=-33.2, lon=18.0, method='nearest')
point_timeseries_97_98 = high_chl_point_97_98.groupby('time.month').mean(dim='time')

# 🌟 **Ensure all 12 months are included**
all_months = np.arange(1, 13)
seasonal_cycle_97_98 = seasonal_cycle_97_98.reindex(month=all_months)
point_timeseries_97_98 = point_timeseries_97_98.reindex(month=all_months)

# 🌟 **Plot the data**
plt.figure(figsize=(10, 5))

plt.plot(all_months, seasonal_cycle_97_98, label="Regional Mean", color='blue', linewidth=2)
plt.plot(all_months, point_timeseries_97_98, label="High-Chl Point (-33.2°S, 18.0°E)", color='red', linestyle='dashed', linewidth=2)

# **Customize labels**
plt.xlabel('Month')
plt.ylabel('Chlorophyll-a (mg/m³)')
plt.title('Mean Seasonal Cycle of Chlorophyll-a (1997-1998) \nRegional Average vs. High Chlorophyll Location', fontsize=14, fontweight='bold')

plt.xticks(ticks=all_months, labels=pd.date_range("1997-01-01", periods=12, freq="M").strftime('%b'))  # Month names
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)

plt.show()