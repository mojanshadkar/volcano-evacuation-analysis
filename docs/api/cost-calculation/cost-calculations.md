# Cost Calculations

The `cost_calculations.py` module provides functions for calculating and manipulating cost surfaces for least-cost path analysis.

## Functions

### `map_landcover_to_cost`

```python
def map_landcover_to_cost(landcover_data, land_cover_cost_mapping)
```

Maps land cover classes to their corresponding cost values.

**Parameters:**

- `landcover_data (numpy.ndarray)`: A 2D array representing land cover classes.
- `land_cover_cost_mapping (dict)`: A dictionary where keys are land cover class identifiers and values are the corresponding cost values.

**Returns:**

- `numpy.ndarray`: A 2D array of the same shape as landcover_data, where each element is the cost value corresponding to the land cover class at that position.

---

### `rasterize_layer`

```python
def rasterize_layer(geometry_list, out_shape, transform, burn_value, fill_value=np.nan)
```

Rasterizes a given geometry.

**Parameters:**

- `geometry_list (list)`: A list of geometries to rasterize.
- `out_shape (tuple)`: The shape of the output array (height, width).
- `transform (Affine)`: The affine transformation to apply.
- `burn_value (float)`: The value to burn into the raster for the geometries.
- `fill_value (float, optional)`: The value to fill the raster where there are no geometries. Default is np.nan.

**Returns:**

- `numpy.ndarray`: A 2D array with the rasterized geometries.

---

### `update_cost_raster`

```python
def update_cost_raster(landcover_cost_data, stream_raster, hiking_path_raster)
```

Updates the cost raster based on landcover data, stream locations, and hiking paths.

**Parameters:**

- `landcover_cost_data (numpy.ndarray)`: A 2D array representing the cost associated with different landcover types.
- `stream_raster (numpy.ndarray)`: A 2D array where non-NaN values indicate the presence of streams.
- `hiking_path_raster (numpy.ndarray)`: A 2D array where non-NaN values indicate the presence of hiking paths.

**Returns:**

- `numpy.ndarray`: A 2D array with updated cost values where streams are marked as impassable (cost = 0) and hiking paths are marked as passable (cost = 1).

---

### `adjust_cost_with_walking_speed`

```python
def adjust_cost_with_walking_speed(normalized_walking_speed_array, combined_data)
```

Adjusts the cost based on the normalized walking speed.

**Parameters:**

- `normalized_walking_speed_array (numpy.ndarray)`: An array of normalized walking speeds.
- `combined_data (numpy.ndarray)`: An array of combined data.

**Returns:**

- `numpy.ndarray`: An array of adjusted costs.

---

### `invert_cost_array`

```python
def invert_cost_array(adjusted_cost_array)
```

Inverts the values in the given cost array.

This function takes an array of adjusted costs and inverts each value. If a value is zero, it is replaced with NaN before inversion to avoid division by zero. After inversion, NaN values are replaced with a large number (1e6).

**Parameters:**

- `adjusted_cost_array (numpy.ndarray)`: A numpy array of adjusted costs.

**Returns:**

- `numpy.ndarray`: A numpy array with the inverted cost values.

---

### `invert_walking_speed`

```python
def invert_walking_speed(normalized_walking_speed_array)
```

Inverts walking speed values and handles zeros/NaNs appropriately.

**Parameters:**

- `normalized_walking_speed_array (numpy.ndarray)`: Array of normalized walking speeds.

**Returns:**

- `numpy.ndarray`: Array with inverted walking speed values.

---

### `invert_cost_raster`

```python
def invert_cost_raster(updated_cost_raster)
```

Inverts cost raster values and handles zeros/NaNs appropriately.

**Parameters:**

- `updated_cost_raster (numpy.ndarray)`: Cost raster to be inverted.

**Returns:**

- `numpy.ndarray`: Inverted cost raster where zero values are handled by converting to NaN and then to 1e6.
