# Path Utilities

The `path_utils.py` module provides functions for working with path finding and graph operations in evacuation analysis.

## Functions

### `calculate_path_metrics`

```python
def calculate_path_metrics(predecessors, source_node, target_node, graph_csr, rows, cols)
```

Calculate metrics for the shortest path between source and target nodes.

This function reconstructs the shortest path using the predecessor array and computes various metrics including the number of pixels in the path, the cost of each step, and the total path cost.

**Parameters:**

- `predecessors (numpy.ndarray)`: A 1D array where predecessors[i] contains the predecessor node of node i on the shortest path from the source.
- `source_node (int)`: The source node index (starting point) of the path.
- `target_node (int or float)`: The target node index (destination) of the path. Can be -9999 or NaN to indicate an invalid target.
- `graph_csr (scipy.sparse.csr_matrix)`: The graph in CSR format where each entry (i,j) represents the cost/weight of the edge from node i to node j.
- `rows (int)`: The number of rows in the original raster grid.
- `cols (int)`: The number of columns in the original raster grid.

**Returns:**

- `tuple`: A tuple containing:
  - `pixel_count (int)`: The number of pixels in the path.
  - `cell_costs (list)`: A list of the costs for each step in the path.
  - `total_cost (float)`: The sum of all cell costs along the path.

---

### `reconstruct_path`

```python
def reconstruct_path(pred, source_node, target_node, cols)
```

Reconstruct the shortest path from source to target and convert to 2D coordinates.

This function traces back through a predecessor array to reconstruct the path from source to target, then converts the 1D node indices to 2D grid coordinates.

**Parameters:**

- `pred (numpy.ndarray)`: A 1D array where pred[i] contains the predecessor node of node i on the shortest path from the source.
- `source_node (int)`: The source node index (starting point) of the path.
- `target_node (int or float)`: The target node index (destination) of the path. Can be -9999 or NaN to indicate an invalid target.
- `cols (int)`: The number of columns in the grid, used to convert 1D indices to 2D coordinates.

**Returns:**

- `list`: A list of tuples (row, col) representing the 2D coordinates of each point along the path from source to target. Returns an empty list if no valid path exists.

---

### `build_adjacency_matrix`

```python
def build_adjacency_matrix(cost_array, rows, cols, directions)
```

Build a sparse adjacency matrix representing the graph for path finding.

This function creates a graph representation of the raster grid where nodes are grid cells and edges represent possible movements between adjacent cells. Edge weights are derived from the cost array, with diagonal movements adjusted by a factor of sqrt(2) to account for the increased distance.

**Parameters:**

- `cost_array (numpy.ndarray)`: A 3D array of shape (n_directions, rows, cols) containing the cost values for moving in each direction from each cell. The first dimension corresponds to the directions defined in the directions parameter.
- `rows (int)`: The number of rows in the grid.
- `cols (int)`: The number of columns in the grid.
- `directions (list of tuples)`: A list of (dr, dc) tuples defining the possible movement directions. Typically includes the 8 neighboring directions (cardinal and diagonal).

**Returns:**

- `scipy.sparse.csr_matrix`: A sparse CSR matrix representation of the graph, where each entry (i, j) represents the cost of moving from node i to node j. The matrix has dimensions (rows*cols, rows*cols).
