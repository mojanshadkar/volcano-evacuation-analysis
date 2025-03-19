# Data Loading

The `data_loading.py` module provides functions for loading geospatial data from shapefiles and raster files.

## Functions

### `read_shapefile`

```python
def read_shapefile(path)
```

Load a shapefile and return it as a GeoDataFrame.

**Parameters:**

- `path (str)`: The file path to the shapefile.

**Returns:**

- `gpd.GeoDataFrame`: A GeoDataFrame containing the data from the shapefile.

---

### `read_raster`

```python
def read_raster(path)
```

Reads a raster file and returns its data, profile, transform, CRS, and nodata value.

**Parameters:**

- `path (str)`: The file path to the raster file.

**Returns:**

- `tuple`: A tuple containing:
  - `data (numpy.ndarray)`: The raster data.
  - `profile (dict)`: The profile metadata of the raster.
  - `transform (affine.Affine)`: The affine transform of the raster.
  - `crs (rasterio.crs.CRS)`: The coordinate reference system of the raster.
  - `nodata (float or int)`: The nodata value of the raster.
