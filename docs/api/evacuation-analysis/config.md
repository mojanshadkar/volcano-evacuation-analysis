# Configuration

The `config.py` module establishes environment variables, defines walking speeds, and specifies file paths for various geospatial datasets used in the volcanic evacuation analysis.

## Constants

### Walking Speeds

```python
WALKING_SPEEDS = {
   'slow': 0.91,
   'medium': 1.22,
   'fast': 1.52
}
```

Dictionary mapping speed categories to values in meters per second.

### File Paths

```python
DATA_FOLDER = r'C:\Users\Mojan\Desktop\RA Volcano\python_results'
```

Base directory for python results.

```python
COST_PATHS = {
    'final': os.path.join(DATA_FOLDER, 'Awu_inverted_cost_8_directions_original.tif'),
    'modify_landcover': os.path.join(DATA_FOLDER, 'Awu_inverted_cost_8_directions_modified.tif'),
    'walking_speed': os.path.join(DATA_FOLDER, 'inverted_Slopecost_8_directions_Awu_OriginalLandcover.tif'),
    'base_cost': os.path.join(DATA_FOLDER, 'invert_landcovercost_original_Awu.tif')
}
```

Dictionary mapping cost raster names to their file paths:
- 'final': Main cost raster with original hiking path
- 'modify_landcover': Cost raster with modified land cover
- 'walking_speed': Walking speed cost raster
- 'base_cost': Base cost raster

```python
SUMMIT_PATH = r"C:\Users\Mojan\Desktop\RA Volcano\projection\summit_awu_correct_proj_final.shp"
```

File path to the Mt. Marapi summit location (GPKG format).

```python
CAMP_SPOT_PATH = r"C:\Users\Mojan\Desktop\RA Volcano\projection\campspot_awu_correct_proj_final.shp"
```

File path to camping locations (GPKG format).

```python
HIKING_PATH = r'C:\Users\Mojan\Desktop\RA Volcano\projection\hikingpath_awu_buffer_correctproj_final.shp'
```

File path to the original hiking path (GPKG format).

```python
landcover_100m = r'C:\Users\Mojan\Desktop\RA Volcano\Dataset\Awu_LandCover_2019_100m_Buffer_UTM.tif'
```

File path to land cover data with 100m buffer (TIF format).

```python
DEM_100m = r"C:\Users\Mojan\Desktop\RA Volcano\Dataset\Awu_DEM_100m_Buffer_UTM.tif"
```

File path to digital elevation model with 100m buffer (TIF format).

### Source Names and Safe Zone Distances

```python
SOURCE_NAMES = ['summit', 'camp1']
```

List of source location names for evacuation analysis.

```python
SAFE_ZONE_DISTANCES = list(range(500, 5000, 500))
```

List of safe zone distances from 500m to 4500m in 500m increments.

### Movement Directions

```python
DIRECTIONS = [
   (-1, 0),   # Up
   (1, 0),    # Down
   (0, 1),    # Right
   (0, -1),   # Left
   (-1, 1),   # Up-Right
   (-1, -1),  # Up-Left
   (1, 1),    # Down-Right
   (1, -1)    # Down-Left
]
```

List of tuples representing the eight possible movement directions for path analysis (cardinal and intercardinal directions).

## Environment Variables

```python
os.environ['USE_PATH_FOR_GDAL_PYTHON'] = "True"
```

Set to "True" to use the system path for GDAL Python bindings.

```python
os.environ['PROJ_LIB'] = pyproj.datadir.get_data_dir()
```

Set to pyproj's data directory for projection information.
