# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
"""
Graph construction, shortest path calculation, and path analysis utilities.
"""

import time
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.csgraph import dijkstra
from tqdm import tqdm
from numpy import sqrt

from raster_utils import to_1d


def build_adjacency_matrix(cost_array, rows, cols):
    """
    Build an adjacency matrix (graph) from a cost raster.
    
    Args:
        cost_array (numpy.ndarray): Cost array (bands, rows, cols)
        rows (int): Number of rows
        cols (int): Number of columns
        
    Returns:
        scipy.sparse.csr_matrix: CSR format adjacency matrix
    """
    print("Building adjacency matrix...")
    graph = lil_matrix((rows * cols, rows * cols), dtype=np.float32)
    
    # Define 8 movement directions and map them to band indices
    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, 1),    # Right
        (0, -1),   # Left
        (-1, 1),   # Up-Right
        (-1, -1),  # Up-Left
        (1, 1),    # Down-Right
        (1, -1)    # Down-Left
    ]
    direction_indices = {dir: idx for idx, dir in enumerate(directions)}
    
    for r in tqdm(range(rows), desc="Processing rows"):
        for c in range(cols):
            current_node = to_1d(r, c, cols)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_node = to_1d(nr, nc, cols)
                    idx = direction_indices[(dr, dc)]
                    cost_val = cost_array[idx, r, c]
                    
                    # Skip invalid costs
                    if np.isnan(cost_val) or np.isinf(cost_val) or cost_val <= 0:
                        continue
                    
                    # Apply sqrt(2) factor for diagonal movement
                    if abs(dr) == 1 and abs(dc) == 1:
                        cost_val *= sqrt(2)
                    
                    graph[current_node, neighbor_node] = cost_val
    
    # Convert to CSR format for faster computation
    graph_csr = graph.tocsr()
    print("Adjacency matrix created.")
    
    return graph_csr


def compute_shortest_paths(graph_csr, source_nodes):
    """
    Compute shortest paths from source nodes using Dijkstra's algorithm.
    
    Args:
        graph_csr (scipy.sparse.csr_matrix): CSR format adjacency matrix
        source_nodes (list): List of source node indices
        
    Returns:
        tuple: (distances, predecessors)
    """
    print("Running Dijkstra's algorithm for all sources...")
    start_time = time.time()
    distances, predecessors = dijkstra(
        csgraph=graph_csr, 
        directed=True, 
        indices=source_nodes, 
        return_predecessors=True
    )
    end_time = time.time()
    print(f"Dijkstra's algorithm completed in {end_time - start_time:.2f} seconds.")
    
    return distances, predecessors


def reconstruct_path(predecessors, source_node, target_node, cols):
    """
    Reconstruct the path from source_node to target_node using the predecessor array.
    
    Args:
        predecessors (numpy.ndarray): Predecessor array from Dijkstra's algorithm
        source_node (int): Source node index
        target_node (int): Target node index
        cols (int): Number of columns in the raster
        
    Returns:
        list: List of (row, col) coordinates for the path
    """
    if target_node == -9999 or np.isnan(target_node):
        return []
    
    path_nodes = []
    current = target_node
    
    while current != source_node and current != -9999:
        path_nodes.append(current)
        current = predecessors[current]
    
    path_nodes.append(source_node)
    path_nodes.reverse()
    
    # Convert each 1D index to (row, col)
    return [(node // cols, node % cols) for node in path_nodes]


def calculate_path_metrics(predecessors, source_node, target_node, graph_csr, rows, cols):
    """
    Calculate metrics for a path between source and target nodes.
    
    Args:
        predecessors (numpy.ndarray): Predecessor array from Dijkstra's algorithm
        source_node (int): Source node index
        target_node (int): Target node index
        graph_csr (scipy.sparse.csr_matrix): CSR format adjacency matrix
        rows (int): Number of rows in the raster
        cols (int): Number of columns in the raster
        
    Returns:
        tuple: (pixel_count, cell_costs, total_cost)
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
