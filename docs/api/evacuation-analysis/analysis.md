# Analysis

The `analysis.py` module provides functions for conducting evacuation analysis using Dijkstra's algorithm and processing travel times.

## Functions

### `run_dijkstra_analysis`

```python
def run_dijkstra_analysis(graph_csr, source_nodes)
```

Run Dijkstra's algorithm for all source nodes.

This function computes the shortest paths from a set of source nodes to all other nodes in a given graph using Dijkstra's algorithm. The graph is represented in Compressed Sparse Row (CSR) format.

**Parameters:**

- `graph_csr (scipy.sparse.csr_matrix)`: The graph in CSR format where each entry represents the weight of the edge between nodes.
- `source_nodes (array-like)`: A list or array of source node indices from which to calculate the shortest paths.

**Returns:**

- `distances (numpy.ndarray)`: A 2D array where distances[i, j] represents the shortest distance from source_nodes[i] to node j.
- `predecessors (numpy.ndarray)`: A 2D array where predecessors[i, j] represents the predecessor node on the shortest path from source_nodes[i] to node j. A value of -9999 indicates no path exists.

---

### `process_travel_times`

```python
def process_travel_times(base_path, source_name, dataset_key, speed_name, speed_value, meta)
```

Process and save travel time rasters for a given speed value.

This function loads a base raster, processes it to calculate travel times based on the specified speed, and saves the resulting raster to disk.

**Parameters:**

- `base_path (str)`: The file path to the base raster.
- `source_name (str)`: The name of the source for which travel times are being processed.
- `dataset_key (str)`: A key identifying the dataset, used in the output filename.
- `speed_name (str)`: The name of the speed category (e.g., 'slow', 'moderate', 'fast').
- `speed_value (float)`: The speed value to be used in processing the raster.
- `meta (dict)`: Metadata for the output raster file.

**Returns:**

- `numpy.ndarray`: The processed travel time array.

**Raises:**

- `FileNotFoundError`: If the base raster file does not exist.
- `ValueError`: If there is an issue with the raster data or processing.

---

### `analyze_safe_zones`

```python
def analyze_safe_zones(distance_from_summit, travel_time_data, safe_zone_distances, source_names)
```

Analyze minimum travel times within specified safe zones from different source locations.

**Parameters:**

- `distance_from_summit (numpy.ndarray)`: A 2D array representing the distance from the summit.
- `travel_time_data (dict)`: A dictionary containing travel time data for different speeds and sources.
  The structure is expected to be:
  ```
  {
      'speed_name': {
          'source_name': {
              'cost_array_flat': numpy.ndarray,  # Flattened travel times
              'cost_array': numpy.ndarray        # 2D travel times
          }
      }
  }
  ```
- `safe_zone_distances (list)`: A list of distances defining the safe zones in meters.
- `source_names (list)`: A list of source names corresponding to the travel time data.

**Returns:**

- `tuple`: A tuple containing two dictionaries:
  - `results`: A dictionary with the minimum travel times (in hours) for each speed and safe zone.
    The structure is:
    ```
    {
        'speed_name': {
            safe_zone_distance: [min_time1, min_time2, ...]
        }
    }
    ```
    where the list indices correspond to the order of source_names.
  - `min_coords`: A dictionary with the coordinates of the minimum travel times for each speed and safe zone.
    The structure is:
    ```
    {
        'speed_name': {
            safe_zone_distance: [(min_r1, min_c1), (min_r2, min_c2), ...]
        }
    }
    ```
    where each tuple contains the row and column indices in the original 2D array.
