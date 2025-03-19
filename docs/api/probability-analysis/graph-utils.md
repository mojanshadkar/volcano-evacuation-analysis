# Graph Utilities

The `graph_utils.py` module provides functions for constructing graphs from raster data, calculating shortest paths, and analyzing path metrics for evacuation analysis.

## Functions

### `build_adjacency_matrix`

```python
def build_adjacency_matrix(cost_array, rows, cols)
```

Build an adjacency matrix (graph) from a cost raster.

This function creates a sparse graph representation where nodes are raster cells and edges represent possible movements between adjacent cells. The cost of movement is determined by the cost array values and adjusted for diagonal movement.

**Parameters:**

- `cost_array (numpy.ndarray)`: Cost array with shape (bands, rows, cols) where bands represent 8 directions of movement.
- `rows (int)`: Number of rows in the raster.
- `cols (int)`: Number of columns in the raster.

**Returns:**

- `scipy.sparse.csr_matrix`: CSR format adjacency matrix representing the graph for path analysis.

---

### `compute_shortest_paths`

```python
def compute_shortest_paths(graph_csr, source_nodes)
```

Compute shortest paths from source nodes using Dijkstra's algorithm.

This function calculates the shortest paths from specified source nodes to all other nodes in the graph using Dijkstra's algorithm.

**Parameters:**

- `graph_csr (scipy.sparse.csr_matrix)`: CSR format adjacency matrix representing the graph.
- `source_nodes (list)`: List of source node indices from which to compute shortest paths.

**Returns:**

- `tuple`: A tuple containing:
  - `distances (numpy.ndarray)`: 2D array of distances from each source to all nodes.
  - `predecessors (numpy.ndarray)`: 2D array of predecessor nodes in the shortest paths.

---

### `reconstruct_path`

```python
def reconstruct_path(predecessors, source_node, target_node, cols)
```

Reconstruct the path from source_node to target_node using the predecessor array.

This function traces the shortest path from a source node to a target node using the predecessor information from Dijkstra's algorithm and converts the path to 2D raster coordinates.

**Parameters:**

- `predecessors (numpy.ndarray)`: Predecessor array from Dijkstra's algorithm.
- `source_node (int)`: Source node index (starting point).
- `target_node (int)`: Target node index (destination).
- `cols (int)`: Number of columns in the raster.

**Returns:**

- `list`: List of (row, col) coordinates for the path. Empty list if no valid path exists.

---

### `calculate_path_metrics`

```python
def calculate_path_metrics(predecessors, source_node, target_node, graph_csr, rows, cols)
```

Calculate metrics for a path between source and target nodes.

This function reconstructs the shortest path between a source and target node and calculates various metrics about the path, including its length and cost.

**Parameters:**

- `predecessors (numpy.ndarray)`: Predecessor array from Dijkstra's algorithm.
- `source_node (int)`: Source node index (starting point).
- `target_node (int)`: Target node index (destination).
- `graph_csr (scipy.sparse.csr_matrix)`: CSR format adjacency matrix.
- `rows (int)`: Number of rows in the raster.
- `cols (int)`: Number of columns in the raster.

**Returns:**

- `tuple`: A tuple containing:
  - `pixel_count (int)`: Number of pixels in the path.
  - `cell_costs (list)`: List of costs for each step in the path.
  - `total_cost (float)`: Sum of all costs along the path.
