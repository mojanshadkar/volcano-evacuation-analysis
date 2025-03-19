# Data Utilities

The `data_utils.py` module provides functions for loading, saving, and processing geospatial data files for volcanic evacuation analysis, including shapefiles, rasters, and analysis reports.

## Functions

### `read_shapefile`

```python
def read_shapefile(path)
```

Read a shapefile into a GeoDataFrame.

This function opens a shapefile using Fiona and converts it to a GeoPandas GeoDataFrame for further spatial analysis.

**Parameters:**

- `path (str)`: Path to the shapefile.

**Returns:**

- `gpd.GeoDataFrame`: GeoDataFrame containing the shapefile data.

---

### `read_raster`

```python
def read_raster(path)
```

Read a raster file and return its data, metadata, and properties.

This function opens a raster file using Rasterio and extracts the raster data along with its metadata and spatial properties.

**Parameters:**

- `path (str)`: Path to the raster file.

**Returns:**

- `tuple`: A tuple containing:
  - `data (numpy.ndarray)`: The raster data with shape (bands, rows, cols).
  - `meta (dict)`: A copy of the raster metadata.
  - `transform`: The affine transform of the raster.
  - `nodata`: The NoData value of the raster.
  - `bounds`: The spatial bounds of the raster.
  - `resolution`: The resolution of the raster.

---

### `load_raster`

```python
def load_raster(file_path)
```

Load a raster file and return its data and metadata.

A simplified version of `read_raster` that reads only the first band of a raster file and its metadata.

**Parameters:**

- `file_path (str)`: Path to the raster file.

**Returns:**

- `tuple`: A tuple containing:
  - `data (numpy.ndarray)`: The raster data from the first band.
  - `meta (dict)`: A copy of the raster metadata.

---

### `save_raster`

```python
def save_raster(output_path, data, meta, dtype=rasterio.float32, nodata=-1)
```

Save a numpy array as a raster file.

This function saves a numpy array to disk as a geospatial raster file with the specified metadata.

**Parameters:**

- `output_path (str)`: Path to save the raster.
- `data (numpy.ndarray)`: The raster data to save.
- `meta (dict)`: The raster metadata.
- `dtype`: The data type of the output raster (default: rasterio.float32).
- `nodata`: The NoData value for the output raster (default: -1).

**Returns:**

- None

---

### `save_analysis_report`

```python
def save_analysis_report(results, min_coords, source_names, thresholds, walking_speeds, dataset_key, output_dir)
```

Save analysis results to a text report and CSV file.

This function generates a human-readable text report and a CSV file summarizing the evacuation analysis results.

**Parameters:**

- `results (dict)`: Dictionary of results structured as:
  ```
  {
      speed_name: {
          threshold: [times_per_source]
      }
  }
  ```
- `min_coords (dict)`: Dictionary of coordinates structured as:
  ```
  {
      speed_name: {
          threshold: [coords_per_source]
      }
  }
  ```
- `source_names (list)`: List of source location names.
- `thresholds (list)`: List of probability thresholds.
- `walking_speeds (dict)`: Dictionary mapping speed names to values in m/s.
- `dataset_key (str)`: Key identifying the dataset.
- `output_dir (str)`: Directory to save outputs.

**Returns:**

- `tuple`: Paths to the saved text report and CSV file.

---

### `create_statistics_table`

```python
def create_statistics_table(results, source_names, walking_speeds, thresholds, dataset_key, output_dir)
```

Create a statistics table and save it as PNG and CSV.

This function generates a summary table of travel time statistics (min, max, mean) for different sources and walking speeds, and saves it as both a PNG visualization and a CSV file.

**Parameters:**

- `results (dict)`: Dictionary of results.
- `source_names (list)`: List of source names.
- `walking_speeds (dict)`: Dictionary of walking speeds.
- `thresholds (list)`: List of probability thresholds.
- `dataset_key (str)`: Key for the dataset.
- `output_dir (str)`: Directory to save outputs.

**Returns:**

- `tuple`: Paths to the saved PNG and CSV files.
