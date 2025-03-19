# decomposition.py

import numpy as np
from config import COST_PATHS, DIRECTIONS
from io_utils import read_raster
from grid_utils import to_1d

def reconstruct_path(predecessors, target, source):
    """
    Reconstruct the shortest path from source to target using the predecessor array.
    
    This function traces back through a predecessor array produced by a shortest path
    algorithm (like Dijkstra's) to reconstruct the complete path from source to target.
    
    Parameters:
    -----------
    predecessors : numpy.ndarray
        A 1D array where predecessors[i] contains the predecessor node of node i
        on the shortest path from the source. This array should be for a single
        source node.
    
    target : int
        The target node index (destination) for which to reconstruct the path.
    
    source : int
        The source node index (starting point) from which the path begins.
    
    Returns:
    --------
    path : list
        A list of node indices representing the shortest path from source to target,
        inclusive of both endpoints. The path is ordered from source to target.
    
    Notes:
    ------
    - The function assumes that node indices are represented as integers.
    - A special value (-9999) in the predecessor array indicates "no predecessor".
    - If there is no valid path from source to target, the returned path will
      only contain the target node.
    - The path includes both the source and target nodes.
    """
    path = []
    node = target
    # Use a special value (-9999) to indicate "no predecessor"
    while node != source and node != -9999:
        path.append(node)
        node = predecessors[node]
    path.append(source)
    path.reverse()
    return path

def expand_single_band(cost_array):
    """
    Expand a single-band raster into an 8-band array representing different movement directions.
    
    This function takes a single-band cost raster and expands it into 8 bands corresponding to
    the 8 movement directions (4 cardinal and 4 diagonal). The diagonal directions (bands 4-7)
    are multiplied by sqrt(2) to account for the increased distance when moving diagonally.
    
    Parameters:
    -----------
    cost_array : numpy.ndarray
        Input cost raster with shape (1, rows, cols), where the first dimension
        represents a single band.
    
    Returns:
    --------
    expanded : numpy.ndarray
        An 8-band raster with shape (8, rows, cols), where each band represents
        the cost in one of the 8 movement directions. Bands 0-3 represent cardinal
        directions, while bands 4-7 represent diagonal directions with costs
        multiplied by sqrt(2).
    
    Notes:
    ------
    - The function assumes that the input cost_array has shape (1, rows, cols).
    - The cardinal directions are ordered as: Up, Down, Right, Left
    - The diagonal directions are ordered as: Up-Right, Up-Left, Down-Right, Down-Left
    - The returned array preserves the data type of the input array.
    """
    single_band = cost_array[0]
    rows, cols = single_band.shape
    expanded = np.zeros((8, rows, cols), dtype=single_band.dtype)
    for i in range(8):
        expanded[i] = single_band.copy()
        if i >= 4:  # Diagonal directions
            expanded[i] *= np.sqrt(2)
    return expanded

def run_decomposition_analysis(dataset_info, min_coords_all):
    """
    Perform a decomposition analysis to quantify the relative contributions of slope and land cover
    to the optimal evacuation paths from the summit.
    
    This function analyzes the shortest paths identified for different safe zone thresholds and
    calculates the percentage contribution of slope (walking speed) and land cover factors to
    the overall path cost. The analysis uses three cost rasters: the final combined cost,
    the walking speed (slope) cost, and the base (land cover) cost.
    
    Parameters:
    -----------
    dataset_info : dict
        Dictionary containing information about the datasets, including:
        - 'final': dict containing:
            - 'pred_summit': ndarray - Predecessor array for the summit source
            - 'cols': int - Number of columns in the raster
            - 'summit_raster_coords': tuple or list - Coordinates of the summit in the raster
    
    min_coords_all : dict
        Nested dictionary containing the minimum travel time coordinates for each dataset,
        speed, and safe zone distance:
        {
            dataset_key: {
                speed_name: {
                    safe_zone_distance: [(row, col), ...]
                }
            }
        }
    
    Returns:
    --------
    list of dict
        A list of dictionaries, each representing a row in the results table with keys:
        - "Safe Zone Threshold (m)": int - The safe zone distance threshold
        - "Slope Contribution (%)": float - Percentage contribution of slope to the path cost
        - "Landcover Contribution (%)": float - Percentage contribution of land cover to the path cost
    
    Notes:
    ------
    - The function assumes that the summit is at index 0 in the source list.
    - Contributions are calculated using the logarithmic sum of costs along the path.
    - The 'medium' speed category is used for analysis.
    - Safe zone distances from 500m to 4500m in 500m increments are analyzed.
    - Paths with missing or invalid cost values are skipped.
    """
    print("\n=== Running Decomposition Analysis ===")
    
    # 1. Read final cost raster
    final_array, meta_final, transform_final, nodata_final, bounds_final, res_final = read_raster(COST_PATHS['final'])
    if final_array.shape[0] == 1:
        print("Expanding single-band final raster to 8 directions...")
        final_array = expand_single_band(final_array)

    # 2. Read walking speed (slope) cost raster
    walking_speed_array, meta_ws, transform_ws, nodata_ws, bounds_ws, res_ws = read_raster(COST_PATHS['walking_speed'])
    if walking_speed_array.shape[0] == 1:
        print("Expanding single-band walking_speed raster to 8 directions...")
        walking_speed_array = expand_single_band(walking_speed_array)

    # 3. Read base cost (landcover) raster
    base_cost_array, meta_base, transform_base, nodata_base, bounds_base, res_base = read_raster(COST_PATHS['base_cost'])
    if base_cost_array.shape[0] == 1:
        print("Expanding single-band base_cost raster to 8 directions...")
        base_cost_array = expand_single_band(base_cost_array)

    # 4. Retrieve the predecessor array from the final dataset (summit source index 0)
    pred_final = dataset_info['final']['pred_summit']
    cols = dataset_info['final']['cols']

    # 5. Retrieve the summit raster coords
    if isinstance(dataset_info['final']['summit_raster_coords'], tuple):
        summit_idx = dataset_info['final']['summit_raster_coords']
    else:
        summit_idx = dataset_info['final']['summit_raster_coords'][0]
    summit_node = to_1d(summit_idx[0], summit_idx[1], cols)

    # We assume the same safe zone thresholds used previously
    safe_zone_distances = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]

    # For the final dataset, we pick a walking speed from min_coords_all, e.g. 'medium'
    selected_speed = 'medium'
    print(f"Decomposition analysis for 'final' dataset, source: summit, speed: {selected_speed}")

    # Prepare a list for table rows
    table_data = []

    # Create a lookup for directions => band index
    direction_indices = {d: i for i, d in enumerate(DIRECTIONS)}

    # 6. Loop over each safe zone threshold, reconstruct path, compute contributions
    for safe_zone in safe_zone_distances:
        # Summits are at source index 0 in your code
        safe_zone_coord = min_coords_all['final'][selected_speed][safe_zone][0]  # (row, col)
        # Skip if no valid coordinate
        if np.isnan(safe_zone_coord[0]) or np.isnan(safe_zone_coord[1]):
            print(f"Safe zone {safe_zone} m: No valid pixel found.")
            continue

        target_node = to_1d(int(safe_zone_coord[0]), int(safe_zone_coord[1]), cols)
        path_nodes = reconstruct_path(pred_final, target_node, summit_node)

        sum_log_slope = 0.0
        sum_log_land = 0.0
        valid_path = True

        for i in range(len(path_nodes) - 1):
            current = path_nodes[i]
            nxt = path_nodes[i+1]
            r, c = divmod(current, cols)
            nr, nc = divmod(nxt, cols)
            dr = nr - r
            dc = nc - c
            direction = (dr, dc)
            if direction not in direction_indices:
                print(f"Unexpected movement direction {direction} from {current} to {nxt}")
                valid_path = False
                break

            band = direction_indices[direction]
            slope_val = walking_speed_array[band, r, c]
            land_val = base_cost_array[band, r, c]
            # Check positivity for log
            if slope_val <= 0 or land_val <= 0:
                print(f"Invalid cost at {r},{c}, slope={slope_val}, land={land_val}")
                valid_path = False
                break

            sum_log_slope += np.log(slope_val)
            sum_log_land += np.log(land_val)

        if not valid_path:
            print(f"Safe zone {safe_zone} m: path issue, skipping.")
            continue

        total_log = sum_log_slope + sum_log_land
        perc_slope = (sum_log_slope / total_log) * 100
        perc_land = (sum_log_land / total_log) * 100

        # Store one row for the table
        row_dict = {
            "Safe Zone Threshold (m)": safe_zone,
            "Slope Contribution (%)": round(perc_slope, 2),
            "Landcover Contribution (%)": round(perc_land, 2)
        }
        table_data.append(row_dict)

    return table_data