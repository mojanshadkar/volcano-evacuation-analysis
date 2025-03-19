# Decomposition

The `decomposition.py` module provides functions for analyzing the relative contributions of different factors (slope and land cover) to evacuation paths.

## Functions

### `reconstruct_path`

```python
def reconstruct_path(predecessors, target, source)
```

Reconstruct the shortest path from source to target using the predecessor array.

This function traces back through a predecessor array produced by a shortest path algorithm (like Dijkstra's) to reconstruct the complete path from source to target.

**Parameters:**

- `predecessors (numpy.ndarray)`: A 1D array where predecessors[i] contains the predecessor node of node i on the shortest path from the source. This array should be for a single source node.
- `target (int)`: The target node index (destination) for which to reconstruct the path.
- `source (int)`: The source node index (starting point) from which the path begins.

**Returns:**

- `path (list)`: A list of node indices representing the shortest path from source to target, inclusive of both endpoints. The path is ordered from source to target.

---

### `expand_single_band`

```python
def expand_single_band(cost_array)
```

Expand a single-band raster into an 8-band array representing different movement directions.

This function takes a single-band cost raster and expands it into 8 bands corresponding to
the 8 movement directions (4 cardinal and 4 diagonal). The diagonal directions (bands 4-7)
are multiplied by sqrt(2) to account for the increased distance when moving diagonally.

**Parameters:**

- `cost_array (numpy.ndarray)`: Input cost raster with shape (1, rows, cols), where the first dimension represents a single band.

**Returns:**

- `expanded (numpy.ndarray)`: An 8-band raster with shape (8, rows, cols), where each band represents the cost in one of the 8 movement directions. Bands 0-3 represent cardinal directions, while bands 4-7 represent diagonal directions with costs multiplied by sqrt(2).

---

### `run_decomposition_analysis`

```python
def run_decomposition_analysis(dataset_info, min_coords_all)
```

Perform a decomposition analysis to quantify the relative contributions of slope and land cover to the optimal evacuation paths from the summit.

This function analyzes the shortest paths identified for different safe zone thresholds and calculates the percentage contribution of slope (walking speed) and land cover factors to the overall path cost. The analysis uses three cost rasters: the final combined cost, the walking speed (slope) cost, and the base (land cover) cost.

**Parameters:**

- `dataset_info (dict)`: Dictionary containing information about the datasets, including:
  - 'final': dict containing:
    - 'pred_summit': ndarray - Predecessor array for the summit source
    - 'cols': int - Number of columns in the raster
    - 'summit_raster_coords': tuple or list - Coordinates of the summit in the raster

- `min_coords_all (dict)`: Nested dictionary containing the minimum travel time coordinates for each dataset, speed, and safe zone distance:
  ```
  {
      dataset_key: {
          speed_name: {
              safe_zone_distance: [(row, col), ...]
          }
      }
  }
  ```

**Returns:**

- `list of dict`: A list of dictionaries, each representing a row in the results table with keys:
  - "Safe Zone Threshold (m)": int - The safe zone distance threshold
  - "Slope Contribution (%)": float - Percentage contribution of slope to the path cost
  - "Landcover Contribution (%)": float - Percentage contribution of land cover to the path cost
