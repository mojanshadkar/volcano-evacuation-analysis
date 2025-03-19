# Raster Utilities

The `raster_utils.py` module provides functions for working with raster data, including coordinate transformations, resampling, and data processing for evacuation analysis.

## Functions

### `resample_raster`

```python
def resample_raster(source_path, target_path, output_path, resampling_method=rasterio.warp.Resampling.bilinear)
```

Resample a source raster to match the grid of a target raster.

This function resamples a source raster to match the spatial reference system, resolution, and extent of a target raster, which is useful for ensuring multiple raster datasets align correctly for analysis.

**Parameters:**

- `source_path (str)`: Path to the source raster to be resampled.
- `target_path (str)`: Path to the target raster that provides the reference grid.
- `output_path (str)`: Path where the resampled raster will be saved.
- `resampling_method`: The resampling algorithm to use (default: bilinear interpolation).

**Returns:**

- `tuple`: A tuple containing:
  - `resampled_array (numpy.ndarray)`: The resampled data array.
  - `resampled_meta (dict)`: Metadata for the resampled raster.

---

### `coords_to_raster`

```python
def coords_to_raster(gdf, transform, bounds, res)
```

Convert geographic coordinates to raster row/column coordinates.

This function takes a GeoDataFrame containing point geometries and converts their geographic coordinates to corresponding row and column indices in a raster.

**Parameters:**

- `gdf (GeoDataFrame)`: GeoDataFrame containing point geometries.
- `transform`: The raster's affine transform defining the relationship between raster indices and geographic coordinates.
- `bounds`: The raster's geographic bounds (left, bottom, right, top).
- `res`: The raster's resolution as (x_resolution, y_resolution).

**Returns:**

- `list`: List of (row, col) coordinates corresponding to the input points. Points outside the raster bounds are excluded.

---

### `raster_coord_to_map_coords`

```python
def raster_coord_to_map_coords(row, col, transform)
```

Convert raster (row, col) coordinates to map (x, y) coordinates.

This function transforms raster grid indices to their corresponding geographic coordinates using the raster's affine transform.

**Parameters:**

- `row (int)`: Raster row index.
- `col (int)`: Raster column index.
- `transform`: Raster affine transform.

**Returns:**

- `tuple`: (x, y) map coordinates corresponding to the center of the specified raster cell.

---

### `to_1d`

```python
def to_1d(r, c, cols)
```

Convert 2D (row, col) coordinates to 1D index.

This function maps 2D raster coordinates to a 1D index, which is useful for working with graph algorithms that operate on linear arrays.

**Parameters:**

- `r (int)`: Row index.
- `c (int)`: Column index.
- `cols (int)`: Number of columns in the raster.

**Returns:**

- `int`: 1D index corresponding to the input row and column.

---

### `process_raster`

```python
def process_raster(cost_array, walking_speed, cell_size=100)
```

Convert cost raster to travel time (in hours).

This function transforms a cost raster into travel time by considering walking speed and cell size, which is essential for evacuation time analysis.

**Parameters:**

- `cost_array (numpy.ndarray)`: Cost array representing the difficulty or distance of traversing each cell.
- `walking_speed (float)`: Walking speed in meters per second.
- `cell_size (float)`: Cell size in meters (default: 100m).

**Returns:**

- `numpy.ndarray`: Travel time array in hours. Infinite values are replaced with -1.
