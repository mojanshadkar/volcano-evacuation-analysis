import numpy as np
import time
from numpy import sqrt
from scipy.sparse import lil_matrix
from grid_utils import to_1d
from tqdm import tqdm

def calculate_path_metrics(predecessors, source_node, target_node, graph_csr, rows, cols):
    """
    Calculate metrics for the shortest path between source and target nodes.
    
    This function reconstructs the shortest path using the predecessor array and
    computes various metrics including the number of pixels in the path, the cost
    of each step, and the total path cost.
    
    Parameters:
    -----------
    predecessors : numpy.ndarray
        A 1D array where predecessors[i] contains the predecessor node of node i
        on the shortest path from the source.
    
    source_node : int
        The source node index (starting point) of the path.
    
    target_node : int or float
        The target node index (destination) of the path. Can be -9999 or NaN to
        indicate an invalid target.
    
    graph_csr : scipy.sparse.csr_matrix
        The graph in CSR format where each entry (i,j) represents the cost/weight
        of the edge from node i to node j.
    
    rows : int
        The number of rows in the original raster grid.
    
    cols : int
        The number of columns in the original raster grid.
    
    Returns:
    --------
    tuple
        A tuple containing:
        - pixel_count (int): The number of pixels in the path.
        - cell_costs (list): A list of the costs for each step in the path.
        - total_cost (float): The sum of all cell costs along the path.
    
    Notes:
    ------
    - If target_node is -9999 or NaN, the function returns (0, [], 0) indicating
      no valid path.
    - The path is reconstructed from the target to the source and then reversed.
    - A value of -9999 in the predecessors array indicates "no predecessor".
    - Progress and timing information is printed to standard output.
    """
    if target_node == -9999 or np.isnan(target_node):
        return 0, [], 0
    
    path = []
    current = target_node
    while current != source_node and current != -9999:
        path.append(current)
        current = predecessors[current]
    if current != -9999:
        path.append(source_node)
    path.reverse()
    
    pixel_count = len(path)
    cell_costs = []
    total_cost = 0
    for i in range(len(path)-1):
        cell_cost = graph_csr[path[i], path[i+1]]
        cell_costs.append(cell_cost)
        total_cost += cell_cost
    
    return pixel_count, cell_costs, total_cost

def reconstruct_path(pred, source_node, target_node, cols):
    """
    Reconstruct the shortest path from source to target and convert to 2D coordinates.
    
    This function traces back through a predecessor array to reconstruct the path
    from source to target, then converts the 1D node indices to 2D grid coordinates.
    
    Parameters:
    -----------
    pred : numpy.ndarray
        A 1D array where pred[i] contains the predecessor node of node i
        on the shortest path from the source.
    
    source_node : int
        The source node index (starting point) of the path.
    
    target_node : int or float
        The target node index (destination) of the path. Can be -9999 or NaN to
        indicate an invalid target.
    
    cols : int
        The number of columns in the grid, used to convert 1D indices to 2D coordinates.
    
    Returns:
    --------
    list
        A list of tuples (row, col) representing the 2D coordinates of each point
        along the path from source to target. Returns an empty list if no valid path exists.
    
    Notes:
    ------
    - If target_node is -9999 or NaN, the function returns an empty list.
    - The path is reconstructed from target to source and then reversed.
    - A value of -9999 in the predecessor array indicates "no predecessor".
    - 1D indices are converted to 2D coordinates using integer division and modulo operations.
    - Progress and timing information is printed to standard output.
    """
    if target_node == -9999 or np.isnan(target_node):
        return []
        
    path_nodes = []
    current = target_node
    while current != source_node and current != -9999:
        path_nodes.append(current)
        current = pred[current]
    path_nodes.append(source_node)
    path_nodes.reverse()
    
    # Convert each 1D index to (row, col)
    path_coords = [(node // cols, node % cols) for node in path_nodes]
    
    return path_coords

def build_adjacency_matrix(cost_array, rows, cols, directions):
    """
    Build a sparse adjacency matrix representing the graph for path finding.
    
    This function creates a graph representation of the raster grid where nodes
    are grid cells and edges represent possible movements between adjacent cells.
    Edge weights are derived from the cost array, with diagonal movements adjusted
    by a factor of sqrt(2) to account for the increased distance.
    
    Parameters:
    -----------
    cost_array : numpy.ndarray
        A 3D array of shape (n_directions, rows, cols) containing the cost values
        for moving in each direction from each cell. The first dimension corresponds
        to the directions defined in the directions parameter.
    
    rows : int
        The number of rows in the grid.
    
    cols : int
        The number of columns in the grid.
    
    directions : list of tuples
        A list of (dr, dc) tuples defining the possible movement directions.
        Typically includes the 8 neighboring directions (cardinal and diagonal).
    
    Returns:
    --------
    scipy.sparse.csr_matrix
        A sparse CSR matrix representation of the graph, where each entry (i, j)
        represents the cost of moving from node i to node j. The matrix has
        dimensions (rows*cols, rows*cols).
    
    Notes:
    ------
    - Progress information is displayed using tqdm and timing information is printed.
    - Invalid costs (NaN, infinite, negative, or zero) are skipped.
    - Diagonal movements have their costs multiplied by sqrt(2) to account for the
      increased distance.
    - The function first builds the matrix in LIL format for efficient construction,
      then converts to CSR format for efficient operations.
    - Nodes are indexed in row-major order using the to_1d function.
    """
    print("\nBuilding adjacency matrix...")
    start_time = time.time()
    
    graph = lil_matrix((rows * cols, rows * cols), dtype=np.float32)
    direction_indices = {dir: idx for idx, dir in enumerate(directions)}
    
    # Use tqdm for progress bar
    for r in tqdm(range(rows), desc="Processing rows"):
        for c in range(cols):
            current_node = to_1d(r, c, cols)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_node = to_1d(nr, nc, cols)
                    idx = direction_indices[(dr, dc)]
                    cost_val = cost_array[idx, r, c]
                    if np.isnan(cost_val) or np.isinf(cost_val) or cost_val <= 0:
                        continue
                    if abs(dr) == 1 and abs(dc) == 1:
                        cost_val *= sqrt(2)
                    graph[current_node, neighbor_node] = cost_val
    
    graph_csr = graph.tocsr()  # Convert to CSR format for efficient operations
    end_time = time.time()
    print(f"Adjacency matrix built in {end_time - start_time:.2f} seconds")
    print(f"Matrix shape: {graph_csr.shape}")
    print(f"Number of non-zero elements: {graph_csr.nnz}")
    return graph_csr