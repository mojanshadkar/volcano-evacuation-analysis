# DEM Processing

The `dem_processing.py` module provides functions for processing Digital Elevation Models (DEMs) to calculate slope and walking speeds based on Tobler's Hiking Function.

## Functions

### `calculate_slope`

```python
def calculate_slope(dem_data, resolution_x, resolution_y, no_data)
```

Calculates the slope in eight directions from a DEM.

**Parameters:**

- `dem_data (numpy.ndarray)`: 2D array representing the DEM data.
- `resolution_x (float)`: The resolution of the DEM in the x direction.
- `resolution_y (float)`: The resolution of the DEM in the y direction.
- `no_data (float)`: The value representing no data in the DEM.

**Returns:**

- `numpy.ndarray`: A 3D array where the first dimension represents the eight directions (North, South, East, West, North-East, North-West, South-East, South-West), and the other two dimensions represent the slope values for each cell in the DEM.

---

### `calculate_walking_speed`

```python
def calculate_walking_speed(slope_array)
```

Calculates walking speed using Tobler's Hiking Function.

This function calculates the walking speed given an array of slope values. The walking speed is computed using the formula:
```
speed = 6 * exp(-3.5 * abs(slope + 0.05))
```

**Parameters:**

- `slope_array (numpy.ndarray)`: An array of slope values.

**Returns:**

- `numpy.ndarray`: An array of walking speeds corresponding to the input slope values.

---

### `get_max_velocity`

```python
def get_max_velocity()
```

Calculates the maximum velocity based on Tobler's Hiking Function.

The maximum velocity occurs at a slope of zero.

**Returns:**

- `float`: The maximum walking velocity.

---

### `normalize_walking_speed`

```python
def normalize_walking_speed(walking_speed_array)
```

Normalize the walking speed array by dividing each element by the maximum velocity.

The maximum velocity is dynamically calculated using Tobler's Hiking Function at a slope of zero.

**Parameters:**

- `walking_speed_array (numpy.ndarray)`: Array of walking speeds to be normalized.

**Returns:**

- `numpy.ndarray`: The normalized walking speed array.
