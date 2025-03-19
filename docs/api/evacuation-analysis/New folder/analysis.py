import os
import time
import numpy as np
import rasterio
from scipy.sparse.csgraph import dijkstra
from grid_utils import process_raster, to_1d
from io_utils import save_raster, load_raster

def run_dijkstra_analysis(graph_csr, source_nodes):
    """
    Run Dijkstra's algorithm for all source nodes.
    
    This function computes the shortest paths from a set of source nodes to all other nodes
    in a given graph using Dijkstra's algorithm. The graph is represented in Compressed Sparse
    Row (CSR) format.
    
    Parameters:
    -----------
    graph_csr (scipy.sparse.csr_matrix): The graph in CSR format where each entry represents
                                        the weight of the edge between nodes.
    
    source_nodes (array-like): A list or array of source node indices from which to calculate
                              the shortest paths.
    
    Returns:
    --------
    distances (numpy.ndarray): A 2D array where distances[i, j] represents the shortest distance
                              from source_nodes[i] to node j.
    
    predecessors (numpy.ndarray): A 2D array where predecessors[i, j] represents the predecessor
                                 node on the shortest path from source_nodes[i] to node j.
                                 A value of -9999 indicates no path exists.
    
    Notes:
    ------
    - Progress and timing information is printed to standard output.
    - The function uses scipy's implementation of Dijkstra's algorithm.
    - The graph is treated as directed.
    """
    print("\nRunning Dijkstra's algorithm...")
    start_time = time.time()
    distances, predecessors = dijkstra(csgraph=graph_csr, directed=True,
                                      indices=source_nodes, return_predecessors=True)
    end_time = time.time()
    print(f"Dijkstra's algorithm completed in {end_time - start_time:.2f} seconds")
    return distances, predecessors

def process_travel_times(base_path, source_name, dataset_key, speed_name, speed_value, meta):
    """
    Process and save travel time rasters for a given speed value.
    
    This function loads a base raster, processes it to calculate travel times 
    based on the specified speed, and saves the resulting raster to disk.
    
    Parameters:
    -----------
    base_path (str): The file path to the base raster.
    
    source_name (str): The name of the source for which travel times are being processed.
    
    dataset_key (str): A key identifying the dataset, used in the output filename.
    
    speed_name (str): The name of the speed category (e.g., 'slow', 'moderate', 'fast').
    
    speed_value (float): The speed value to be used in processing the raster.
    
    meta (dict): Metadata for the output raster file.
    
    Returns:
    --------
    numpy.ndarray: The processed travel time array.
    
    Raises:
    -------
    FileNotFoundError: If the base raster file does not exist.
    
    ValueError: If there is an issue with the raster data or processing.
    
    Notes:
    ------
    - Progress and timing information is printed to standard output.
    - Output file is saved as 'cost_distance_{source_name}_{dataset_key}_{speed_name}_hours.tif'
      in the same directory as the input file.
    - Output raster uses float32 data type with -1 as the nodata value.
    """
    print(f"Processing travel times for {source_name} at {speed_name} speed...")
    
    cost_array_base, cost_meta_base = load_raster(base_path)
    travel_time_array = process_raster(cost_array_base, speed_value)
    
    out_filename = f'cost_distance_{source_name}_{dataset_key}_{speed_name}_hours.tif'
    out_path = os.path.join(os.path.dirname(base_path), out_filename)
    save_raster(out_path, travel_time_array, meta, dtype=rasterio.float32, nodata=-1)
    
    return travel_time_array

def analyze_safe_zones(distance_from_summit, travel_time_data, safe_zone_distances, source_names):
    """
    Analyze minimum travel times within specified safe zones from different source locations.
    
    Parameters:
    -----------
    distance_from_summit (numpy.ndarray): A 2D array representing the distance from the summit.
    
    travel_time_data (dict): A dictionary containing travel time data for different speeds and sources.
                             The structure is expected to be:
                             {
                                 'speed_name': {
                                     'source_name': {
                                         'cost_array_flat': numpy.ndarray,  # Flattened travel times
                                         'cost_array': numpy.ndarray        # 2D travel times
                                     }
                                 }
                             }
    
    safe_zone_distances (list): A list of distances defining the safe zones in meters.
    
    source_names (list): A list of source names corresponding to the travel time data.
    
    Returns:
    --------
    tuple: A tuple containing two dictionaries:
           - results: A dictionary with the minimum travel times (in hours) for each speed and safe zone.
                      The structure is:
                      {
                          'speed_name': {
                              safe_zone_distance: [min_time1, min_time2, ...]
                          }
                      }
                      where the list indices correspond to the order of source_names.
           
           - min_coords: A dictionary with the coordinates of the minimum travel times for each speed and safe zone.
                         The structure is:
                         {
                             'speed_name': {
                                 safe_zone_distance: [(min_r1, min_c1), (min_r2, min_c2), ...]
                             }
                         }
                         where each tuple contains the row and column indices in the original 2D array.
    
    Notes:
    ------
    - Progress and timing information is printed to standard output during execution.
    - Safe zones are defined as areas where distance_from_summit >= safe_zone_distance.
    - If no valid times are found within a safe zone, np.nan is used for both time and coordinates.
    - All travel times are in hours.
    """
    print("\nAnalyzing safe zones...")
    
    results = {}
    min_coords = {}
    
    for speed_name in travel_time_data.keys():
        print(f"\nProcessing {speed_name} speed...")
        results[speed_name] = {}
        min_coords[speed_name] = {}
        distance_from_summit_1d = distance_from_summit.ravel()
        
        for safe_zone in safe_zone_distances:
            safe_zone_mask = (distance_from_summit_1d >= safe_zone)
            min_times_in_safe_zone = []
            coords_in_safe_zone = []
            
            for source_name in source_names:
                cost_array_flat = travel_time_data[speed_name][source_name]['cost_array_flat']
                valid_times = cost_array_flat[safe_zone_mask]
                valid_times = valid_times[~np.isnan(valid_times)]
                
                if len(valid_times) > 0:
                    min_time = np.min(valid_times)
                    cost_array_2d = travel_time_data[speed_name][source_name]['cost_array']
                    safe_zone_mask_2d = safe_zone_mask.reshape(cost_array_2d.shape)
                    valid_times_2d = np.where(safe_zone_mask_2d, cost_array_2d, np.nan)
                    min_idx = np.nanargmin(valid_times_2d)
                    min_r, min_c = np.unravel_index(min_idx, cost_array_2d.shape)
                else:
                    min_time = np.nan
                    min_r, min_c = (np.nan, np.nan)
                    
                min_times_in_safe_zone.append(min_time)
                coords_in_safe_zone.append((min_r, min_c))
                print(f"{source_name} at {safe_zone}m: min time = {min_time:.2f} hrs")
                
            results[speed_name][safe_zone] = min_times_in_safe_zone
            min_coords[speed_name][safe_zone] = coords_in_safe_zone
            
    return results, min_coords

