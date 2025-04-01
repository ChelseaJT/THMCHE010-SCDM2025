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

monthly_means = region_chl_data.groupby('time.month').mean(dim='time')

fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()}, constrained_layout=True)
fig.suptitle('Monthly Chlorophyll Concentration (mg/m³) \n on the West Coast of South Africa', fontsize=16, fontweight='bold')

vmin, vmax = np.nanpercentile(monthly_means, [5, 95])

for i, ax in enumerate(axes.flat):
    month_name = pd.to_datetime(f'2024-{i+1}-01').strftime('%B')
    chl_data = monthly_means.sel(month=i+1)

    lon_grid, lat_grid = np.meshgrid(chl_data.lon.values, chl_data.lat.values)
    interpolated_data = griddata(
        (lon_grid.flatten(), lat_grid.flatten()),
        chl_data.values.flatten(),
        (lon_grid, lat_grid),
        method='linear'
    )

    im = ax.contourf(lon_grid, lat_grid, np.log10(interpolated_data), cmap='viridis', levels=20, vmin=np.log10(vmin), vmax=np.log10(vmax))

    ax.add_feature(cfeature.LAND, color='grey')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.set_title(month_name, fontsize=12)

cbar_ax = fig.add_axes([1.04, 0.2, 0.02, 0.6])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label(r'Log10(Chlorophyll) (mg/m³)', fontsize=12)

fig.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1, wspace=0.2, hspace=0.3)

plt.show()

