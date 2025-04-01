import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from scipy.interpolate import griddata

ds_chl = xr.open_dataset('ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc')

chlor_data = ds_chl['chlor_a']
lat_data = ds_chl['lat']
lon_data = ds_chl['lon']
time_data = ds_chl['time']

time = pd.to_datetime(time_data.values)

lat_min, lat_max = -34.5, -32.75
lon_min, lon_max = 15.5, 19.0

region_chl_data = chlor_data.sel(lat=slice(lat_max, lat_min), lon=slice(lon_min, lon_max))

start_time, end_time = np.datetime64('1997-01-01'), np.datetime64('1998-12-31')
valid_times = time_data.where((time_data >= start_time) & (time_data <= end_time), drop=True)
region_chl_data_1997_1998 = region_chl_data.sel(time=valid_times)

mean_region_data = region_chl_data_1997_1998.mean(dim='time')

masked_mean_region_data = mean_region_data.where(mean_region_data > 0.05)

lon_grid, lat_grid = np.meshgrid(masked_mean_region_data.lon.values, masked_mean_region_data.lat.values)
points = np.array([lon_grid.flatten(), lat_grid.flatten()]).T
values = masked_mean_region_data.values.flatten()
interpolated_data = griddata(points, values, (lon_grid, lat_grid), method='linear')

fig, ax = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, color='grey')
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)

gridlines = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
gridlines.right_labels = False
gridlines.top_labels = False
gridlines.xlocator = plt.FixedLocator(np.arange(lon_min, lon_max + 0.5, 0.5)) 
gridlines.ylocator = plt.FixedLocator(np.arange(lat_min, lat_max + 0.25, 0.25)) 

chl_plot = ax.contourf(
    lon_grid, lat_grid, np.log10(interpolated_data),
    cmap='summer', levels=np.linspace(-1, 1, 100),
    transform=ccrs.PlateCarree()
)

locations = {
    'False Bay': (-34.2, 18.5),
    'Cape Town': (-33.9, 18.4),
    'Robben Island': (-33.8, 18.4),
    'St Helena Bay': (-32.8, 17.9),
    'Saldanha Bay': (-33.0, 17.9)
}
location_labels = {
    'False Bay': {'text': 'False Bay', 'fontsize': 12, 'position': (-0.02, 0.1), 'color': 'black', 'bbox': {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}},
    'Cape Town': {'text': 'Cape Town', 'fontsize': 12, 'position': (-0.5, 0), 'color': 'black', 'bbox': {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}},
    'Robben Island': {'text': 'Robben Island', 'fontsize': 12, 'position': (-0.63, 0.04), 'color': 'black', 'bbox': {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}},
    'St Helena Bay': {'text': 'St Helena Bay', 'fontsize': 12, 'position': (0.1, 0), 'color': 'black', 'bbox': {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}},
    'Saldanha Bay': {'text': 'Saldanha Bay', 'fontsize': 12, 'position': (0.1, 0), 'color': 'black', 'bbox': {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}}
}

for location, coords in locations.items():
    lat_point, lon_point = coords
    ax.plot(lon_point, lat_point, marker='o', color='black', markersize=6) 
    label_options = location_labels.get(location, {})
    ax.text(lon_point + label_options.get('position')[0], lat_point + label_options.get('position')[1], label_options.get('text'), 
            fontsize=label_options.get('fontsize', 10), color=label_options.get('color', 'black'),
            bbox=label_options.get('bbox', {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}))  

cbar = plt.colorbar(chl_plot, ax=ax, orientation='vertical', shrink=0.7)
cbar.set_label(r'Log10(Chlorophyll Concentration) (mg/m$^3$)')

ax.set_title('Chlorophyll Concentration between 1997-1998 \n on the West Coast of South Africa', fontsize=14, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.tight_layout()
plt.show()
