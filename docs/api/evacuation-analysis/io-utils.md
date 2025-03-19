# IO Utilities

The `io_utils.py` module provides functions for reading and writing geospatial data files, including shapefiles, rasters, and output formats for analyses.

## Functions

### `read_shapefile`

```python
def read_shapefile(path, crs_epsg=32651)
```

Read a shapefile into a GeoDataFrame with proper coordinate reference system handling.

This function reads a shapefile from the specified path using fiona and GeoPandas, and ensures that a coordinate reference system (CRS) is assigned. If the shapefile does not have a defined CRS, it will assign the specified EPSG code.

**Parameters:**

- `path (str)`: The file path to the shapefile to be read.
- `crs_epsg (int, optional)`: The EPSG code to assign if the shapefile lacks a CRS. Default is 32651 (WGS 84 / UTM zone 51N), which is appropriate for Indonesia/Sumatra region.

**Returns:**

- `geopandas.GeoDataFrame`: A GeoDataFrame containing the features from the shapefile with the proper CRS.

**Raises:**

- `FileNotFoundError`: If the shapefile does not exist at the specified path.
- `fiona.errors.DriverError`: If the file exists but cannot be read as a shapefile.

---

### `read_raster`

```python
def read_raster(path)
```

Read a raster file and return its data and associated metadata.

This function opens a raster file using rasterio and extracts the raster data, metadata, spatial reference information, and other key properties needed for geospatial analysis.

**Parameters:**

- `path (str)`: The file path to the raster file to be read.

**Returns:**

- `tuple`: A tuple containing:
  - `data (numpy.ndarray)`: The raster data with shape (bands, rows, cols)
  - `meta (dict)`: A copy of the raster metadata
  - `transform (affine.Affine)`: The affine transform defining the relationship between pixel coordinates and geographic coordinates
  - `nodata (float or int)`: The value used to represent no data or null values
  - `bounds (rasterio.coords.BoundingBox)`: The geographic bounds of the raster (left, bottom, right, top)
  - `resolution (tuple)`: A tuple (x_res, y_res) containing the pixel size in the x and y directions

**Raises:**

- `FileNotFoundError`: If the raster file does not exist at the specified path.
- `rasterio.errors.RasterioIOError`: If the file exists but cannot be read as a raster.

---

### `save_raster`

```python
def save_raster(output_path, data, meta, dtype=rasterio.float32, nodata=-1)
```

Save a numpy array as a raster file with specified metadata.

This function writes a numpy array to disk as a geospatial raster file with appropriate metadata, including coordinate reference system, transformation, and no-data value.

**Parameters:**

- `output_path (str)`: The file path where the raster will be saved.
- `data (numpy.ndarray)`: The raster data to be saved. If 3D, the first dimension should be bands. If 2D, it will be treated as a single-band raster.
- `meta (dict)`: Metadata dictionary containing information such as width, height, transform, and CRS. This is typically obtained from another raster.
- `dtype (rasterio data type, optional)`: The data type to use for the output raster. Default is rasterio.float32.
- `nodata (int or float, optional)`: The value to use for no-data or missing values in the output raster. Default is -1.

**Returns:**

- `None`: The function does not return a value, but writes the raster to disk.

---

### `load_raster`

```python
def load_raster(file_path)
```

Load a single-band raster file and return its data and metadata.

This function opens a raster file using rasterio and extracts the first band of data along with its metadata. Unlike the read_raster function which reads all bands, this function is optimized for single-band rasters.

**Parameters:**

- `file_path (str)`: The file path to the raster file to be loaded.

**Returns:**

- `tuple`: A tuple containing:
  - `data (numpy.ndarray)`: The raster data from the first band with shape (rows, cols)
  - `meta (dict)`: A copy of the raster metadata

**Raises:**

- `FileNotFoundError`: If the raster file does not exist at the specified path.
- `rasterio.errors.RasterioIOError`: If the file exists but cannot be read as a raster.

---

### `save_analysis_report`

```python
def save_analysis_report(output_path, results, min_coords, source_names, walking_speeds, safe_zone_distances)
```

Save evacuation analysis results to a formatted text report file.

This function generates a human-readable text report summarizing the minimum travel times from various sources to safe zones for different walking speeds.

**Parameters:**

- `output_path (str)`: The file path where the report will be saved.
- `results (dict)`: A nested dictionary containing travel time results: `{speed_name: {safe_zone_distance: [times_per_source]}}` where times_per_source is a list of travel times (in hours) for each source.
- `min_coords (dict)`: A nested dictionary containing the coordinates of minimum travel times: `{speed_name: {safe_zone_distance: [coords_per_source]}}` where coords_per_source is a list of (row, col) tuples for each source.
- `source_names (list)`: A list of source location names corresponding to indices in the results arrays.
- `walking_speeds (dict)`: Dictionary mapping speed names (str) to speed values (float) in meters per second.
- `safe_zone_distances (list)`: List of safe zone distances used in the analysis.

**Returns:**

- `None`: The function does not return a value, but writes results to a text file.

---

### `save_metrics_csv`

```python
def save_metrics_csv(output_path, results, min_coords, source_names, walking_speeds, safe_zone_distances)
```

Save evacuation analysis metrics to a CSV file for further processing.

This function exports the analysis results in a tabular format suitable for import into spreadsheet software or data analysis tools. Each row represents a unique combination of walking speed, safe zone distance, and source location.

**Parameters:**

- `output_path (str)`: The file path where the CSV will be saved.
- `results (dict)`: A nested dictionary containing travel time results: `{speed_name: {safe_zone_distance: [times_per_source]}}` where times_per_source is a list of travel times (in hours) for each source.
- `min_coords (dict)`: A nested dictionary containing the coordinates of minimum travel times: `{speed_name: {safe_zone_distance: [coords_per_source]}}` where coords_per_source is a list of (row, col) tuples for each source.
- `source_names (list)`: A list of source location names corresponding to indices in the results arrays.
- `walking_speeds (dict)`: Dictionary mapping speed names (str) to speed values (float) in meters per second.
- `safe_zone_distances (list)`: List of safe zone distances used in the analysis.

**Returns:**

- `None`: The function does not return a value, but writes results to a CSV file.
