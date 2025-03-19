# Visualization

The `visualization.py` module provides functions for visualizing evacuation analysis results, including travel time comparisons, cost surfaces, and decomposition analysis.

## Functions

### `load_raster`

```python
def load_raster(path)
```

Load a single-band raster file and return its data and metadata.

This helper function opens a raster file using rasterio and extracts the first band of data along with essential metadata for visualization.

**Parameters:**

- `path (str)`: The file path to the raster file to be loaded.

**Returns:**

- `tuple`: A tuple containing:
  - `array (numpy.ndarray)`: The raster data from the first band with shape (rows, cols)
  - `metadata (dict)`: A dictionary containing:
    - 'transform' (affine.Affine): The affine transform
    - 'crs' (CRS): The coordinate reference system
    - 'nodata' (float or int): The no-data value

---

### `raster_coord_to_map_coords`

```python
def raster_coord_to_map_coords(row, col, transform)
```

Convert raster coordinates (row, column) to map coordinates (x, y).

This function transforms pixel coordinates in a raster to their corresponding geographic coordinates using the raster's affine transform.

**Parameters:**

- `row (int)`: The row index in the raster (zero-based).
- `col (int)`: The column index in the raster (zero-based).
- `transform (affine.Affine or list/tuple)`: The affine transform of the raster, defining the relationship between pixel coordinates and geographic coordinates.

**Returns:**

- `tuple`: A tuple (x, y) containing the geographic coordinates corresponding to the specified raster cell.

---

### `plot_