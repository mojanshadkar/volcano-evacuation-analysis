# Plotting Utils

The `plotting_utils.py` module provides functions for visualizing geospatial data including rasters, points, and analysis results.

## Functions

### `plot_continuous_raster_with_points`

```python
def plot_continuous_raster_with_points(raster_data, extent, points_gdf, title, colorbar_label, output_file_path)
```

Plots a continuous raster with overlaid points.

**Parameters:**

- `raster_data (np.ndarray)`: The raster data to be plotted.
- `extent (Any)`: The extent of the raster data.
- `points_gdf (gpd.GeoDataFrame)`: GeoDataFrame containing the points to be overlaid.
- `title (str)`: The title of the plot.
- `colorbar_label (str)`: The label for the colorbar.
- `output_file_path (str)`: The file path where the plot will be saved.

**Returns:**

- `None`

---

### `plot_normalized_walking_speed`

```python
def plot_normalized_walking_speed(raster_data, extent, points_gdf, title, output_file_path)
```

Plots the normalized walking speed raster with summit points.

**Parameters:**

- `raster_data (np.ndarray)`: The raster data representing normalized walking speeds.
- `extent (Any)`: The extent of the raster data in the format (xmin, xmax, ymin, ymax).
- `points_gdf (gpd.GeoDataFrame)`: A GeoDataFrame containing the summit points to be plotted.
- `title (str)`: The title of the plot.
- `output_file_path (str)`: The file path where the plot will be saved.

**Returns:**

- `None`

---

### `plot_adjusted_cost_raster`

```python
def plot_adjusted_cost_raster(adjusted_cost_raster, extent, points_gdf, title, output_file_path)
```

Plots the adjusted cost raster with summit points.

**Parameters:**

- `adjusted_cost_raster (numpy.ndarray)`: A 2D array representing the adjusted cost raster data.
- `extent (list or tuple)`: The bounding box in the form [xmin, xmax, ymin, ymax] for the raster.
- `points_gdf (geopandas.GeoDataFrame)`: A GeoDataFrame containing the summit points with geometry column.
- `title (str)`: The title of the plot.
- `output_file_path (str)`: The file path where the plot image will be saved.

**Returns:**

- `None`

---

### `plot_inverted_cost_raster`

```python
def plot_inverted_cost_raster(inverted_cost_raster, extent, points_gdf, title, output_file_path)
```

Plots the inverted cost raster with summit points.

**Parameters:**

- `inverted_cost_raster (numpy.ndarray)`: 2D array representing the inverted cost raster.
- `extent (list or tuple)`: The bounding box in data coordinates (left, right, bottom, top).
- `points_gdf (geopandas.GeoDataFrame)`: GeoDataFrame containing the summit points with geometry column.
- `title (str)`: Title of the plot.
- `output_file_path (str)`: Path to save the output plot image.

**Returns:**

- `None`

---

### `plot_walking_speed_vs_slope`

```python
def plot_walking_speed_vs_slope(slope_array, walking_speed_array, directions, output_file_path)
```

Plots the walking speed versus slope for all eight directions in a subplot layout.

**Parameters:**

- `slope_array (numpy.ndarray)`: A 3D array representing slope values for eight directions. The first dimension represents directions: North, South, East, West, North-East, North-West, South-East, South-West.
- `walking_speed_array (numpy.ndarray)`: A 3D array representing walking speed values for eight directions. The first dimension represents directions: North, South, East, West, North-East, North-West, South-East, South-West.
- `directions (list)`: A list of direction labels.
- `output_file_path (str)`: The file path where the combined plot will be saved.

**Returns:**

- `None`

---

### `plot_north_east_speed_conservation`

```python
def plot_north_east_speed_conservation(normalized_walking_speed_array, extent, points_gdf, title, output_file_path)
```

Plots the normalized walking speed raster for North and East directions in a subplot.

**Parameters:**

- `normalized_walking_speed_array (np.ndarray)`: The 3D array of normalized walking speeds where first dimension represents directions (North: 0, East: 2)
- `extent (Any)`: The extent of the raster data in the format (xmin, xmax, ymin, ymax).
- `points_gdf (gpd.GeoDataFrame)`: A GeoDataFrame containing the summit points to be plotted.
- `title (str)`: The main title of the plot.
- `output_file_path (str)`: The file path where the plot will be saved.

**Returns:**

- `None`
