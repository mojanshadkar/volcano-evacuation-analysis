# Grid Utilities

The `grid_utils.py` module provides functions for working with raster grids, including coordinate transformations and distance calculations.

## Functions

### `coords_to_raster`

```python
def coords_to_raster(gdf, transform, bounds, res)
```

Convert geographic coordinates to raster row and column indices.

This function takes a GeoDataFrame containing point geometries and converts the geographic coordinates (x, y) of each point to raster indices (row, col), based on the provided raster transform, bounds, and resolution.

**Parameters:**

- `gdf (geopandas.GeoDataFrame)`: A GeoDataFrame containing point geometries to be converted to raster indices.
- `transform (affine.Affine)`: The affine transform of the raster, defining the relationship between pixel coordinates and geographic coordinates.
- `bounds (rasterio.coords.BoundingBox)`: The geographic bounds of the raster (left, bottom, right, top).
- `res (tuple)`: A tuple (x_res, y_res) containing the pixel resolution in the x and y directions (typically in map units per pixel).

**Returns:**

- `raster_coords (list)`: A list of tuples (row, col) representing the raster indices corresponding to each point in the input GeoDataFrame. Points that fall outside the raster bounds are excluded from the returned list.

---

### `to_1d`

```python
def to_1d(r, c, cols)
```

Convert 2D raster coordinates (row, column) to a 1D array index.

This function maps 2D coordinates in a raster or grid to the corresponding 1D array index, assuming row-major order (C-style).

**Parameters:**

- `r (int)`: The row index (zero-based).
- `c (int)`: The column index (zero-based).
- `cols (int)`: The total number of columns in the 2D array or grid.

**Returns:**

- `int`: The 1D array index corresponding to the given 2D coordinates.

**Examples:**

```python
>>> to_1d(2, 3, 5)
13
# In a 5-column grid, the position at row 2, column 3 maps to index 13
```

---

### `raster_coord_to_map_coords`

```python
def raster_coord_to_map_coords(row, col, transform)
```

Convert raster coordinates (row, column) to geographic map coordinates (x, y).

This function transforms pixel coordinates in a raster to their corresponding geographic coordinates using the raster's affine transform.

**Parameters:**

- `row (int)`: The row index in the raster (zero-based).
- `col (int)`: The column index in the raster (zero-based).
- `transform (affine.Affine)`: The affine transform of the raster, defining the relationship between pixel coordinates and geographic coordinates.

**Returns:**

- `tuple`: A tuple (x, y) containing the geographic coordinates corresponding to the center of the specified raster cell.

---

### `process_raster`

```python
def process_raster(cost_array, walking_speed)
```

Convert base cost raster to travel time in hours.

This function transforms a cost raster into a travel time raster by applying the following steps:
1. Multiply by cell size (100m) to convert to distance units
2. Divide by walking speed to convert to time in seconds
3. Convert seconds to hours
4. Replace infinite values with -1 (indicating inaccessible areas)

**Parameters:**

- `cost_array (numpy.ndarray)`: Input cost raster array. Values typically represent the inverse of the travel cost or difficulty of traversing each cell.
- `walking_speed (float)`: Walking speed in meters per second (m/s). Used to convert distance to time.

**Returns:**

- `numpy.ndarray`: Array of travel times in hours. The array has the same shape as the input cost_array, with infinite values replaced by -1.

---

### `calculate_distance_from_summit`

```python
def calculate_distance_from_summit(summit_coords, rows, cols, cell_size=100)
```

Compute Euclidean distance (in meters) from the summit for each cell in a raster.

This function creates a distance raster where each cell contains the straight-line distance from that cell to the summit location. The distance is calculated using the Euclidean formula and converted to meters using the specified cell size.

**Parameters:**

- `summit_coords (tuple)`: A tuple (row, col) containing the raster coordinates of the summit.
- `rows (int)`: The number of rows in the output raster.
- `cols (int)`: The number of columns in the output raster.
- `cell_size (float, optional)`: The cell size in meters. Default is 100 meters.

**Returns:**

- `numpy.ndarray`: A 2D array of shape (rows, cols) containing the Euclidean distance from each cell to the summit in meters.
