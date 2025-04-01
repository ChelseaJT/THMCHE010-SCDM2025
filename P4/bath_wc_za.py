import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.gridliner as cgrid
import numpy as np

bathymetry_file = 'GMRTv4_3_0_20250331topo.grd'
ds = xr.open_dataset(bathymetry_file)

print(ds)

bathymetry = ds['altitude']

lat = ds['lat'].values
lon = ds['lon'].values
bathy_values = bathymetry.values

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

ax.coastlines(resolution='10m')

ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

c = ax.pcolormesh(lon, lat, bathy_values, cmap='terrain', shading='auto')

fig.colorbar(c, ax=ax, label='Depth (m)', orientation='vertical')

gl = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5, color="gray")
gl.top_labels = False  
gl.right_labels = False
gl.xformatter = cgrid.LongitudeFormatter()  
gl.yformatter = cgrid.LatitudeFormatter()   

contour_levels = np.arange(np.nanmin(bathy_values), np.nanmax(bathy_values), 250)  
contours = ax.contour(lon, lat, bathy_values, levels=contour_levels, colors='black', linewidths=0.7)
ax.clabel(contours, inline=True, fontsize=8, fmt='%d m')

ax.set_title('Bathymetry of the \nWest Coast of South Africa', fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

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
    ax.plot(lon_point, lat_point, marker='o', color='white', markersize=6) 
    label_options = location_labels.get(location, {})
    ax.text(lon_point + label_options.get('position')[0], lat_point + label_options.get('position')[1], label_options.get('text'), 
            fontsize=label_options.get('fontsize', 10), color=label_options.get('color', 'black'),
            bbox=label_options.get('bbox', {'facecolor': 'white', 'edgecolor': 'black', 'boxstyle': 'round,pad=0.2'}))  

plt.show()