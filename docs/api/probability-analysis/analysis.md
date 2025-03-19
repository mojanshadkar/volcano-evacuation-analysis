# Analysis Module

The `analysis.py` module provides functions for conducting volcanic evacuation analysis based on eruption probability thresholds and calculating travel times to safe zones.

## Functions

### `perform_evacuation_analysis`

```python
def perform_evacuation_analysis(cost_paths, source_coords, source_names, walking_speeds, output_dir)
```

Perform evacuation analysis for multiple cost datasets and walking speeds.

This function processes cost rasters, builds adjacency matrices, computes shortest paths, and generates travel time rasters for various evacuation scenarios.

**Parameters:**

- `cost_paths (dict)`: Dictionary mapping dataset keys to file paths of cost rasters.
- `source_coords (list)`: List of source (row, col) coordinates in the raster grid.
- `source_names (list)`: List of source names corresponding to the coordinates.
- `walking_speeds (dict)`: Dictionary mapping speed names to values in m/s.
- `output_dir (str)`: Directory to save the output files.

**Returns:**

- `tuple`: A tuple containing:
  - `all_results (dict)`: Dictionary of evacuation analysis results.
  - `dataset_info (dict)`: Dictionary of dataset information including path predecessors and raster properties.

---

### `analyze_safe_zones`

```python
def analyze_safe_zones(probability_path, travel_time_data, thresholds, source_names, walking_speeds, dataset_key, output_dir)
```

Analyze safe zones based on eruption probability thresholds.

This function identifies areas with eruption probability below specified thresholds and calculates minimum travel times to reach these safe zones from different source locations.

**Parameters:**

- `probability_path (str)`: Path to the eruption probability raster.
- `travel_time_data (dict)`: Dictionary of travel time data structured as:
  ```
  {
      speed_name: {
          source_name: {
              'cost_array': 2D array,
              'cost_array_flat': 1D array,
              'meta': metadata,
              'shape': tuple
          }
      }
  }
  ```
- `thresholds (list)`: List of probability thresholds defining safe zones.
- `source_names (list)`: List of source names.
- `walking_speeds (dict)`: Dictionary mapping speed names to values in m/s.
- `dataset_key (str)`: Key identifying the current dataset.
- `output_dir (str)`: Directory to save output files.

**Returns:**

- `tuple`: A tuple containing:
  - `results (dict)`: Dictionary of minimum travel times for each speed, threshold, and source.
  - `min_coords (dict)`: Dictionary of coordinates for minimum travel times.

---

### `load_travel_time_data`

```python
def load_travel_time_data(dataset_key, source_names, walking_speeds, output_dir)
```

Load travel time rasters for further analysis.

This function loads previously generated travel time rasters for a specific dataset and organizes them for safe zone analysis.

**Parameters:**

- `dataset_key (str)`: Key identifying the dataset.
- `source_names (list)`: List of source names.
- `walking_speeds (dict)`: Dictionary mapping speed names to values in m/s.
- `output_dir (str)`: Directory where rasters are stored.

**Returns:**

- `dict`: Dictionary of travel time data organized by speed and source.

---

### `read_raster`

```python
def read_raster(path)
```

Read a raster file and return its data, metadata, and properties.

This function opens a raster file and extracts its data and spatial properties.

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
