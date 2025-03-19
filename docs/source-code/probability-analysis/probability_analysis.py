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
Evacuation path analysis, safe zone calculations, and related functionality.
"""

import os
import numpy as np
import rasterio

from data_utils import load_raster, save_raster, save_analysis_report, create_statistics_table
from raster_utils import process_raster, to_1d
from graph_utils import build_adjacency_matrix, compute_shortest_paths


def perform_evacuation_analysis(cost_paths, source_coords, source_names, walking_speeds, output_dir):
    """
    Perform evacuation analysis for multiple cost datasets and walking speeds.
    
    Args:
        cost_paths (dict): Dictionary of cost raster paths
        source_coords (list): List of source (row, col) coordinates
        source_names (list): List of source names
        walking_speeds (dict): Dictionary of walking speeds
        output_dir (str): Directory to save outputs
        
    Returns:
        tuple: (all_results, dataset_info)
    """
    # Dictionary to store results
    all_results = {}
    dataset_info = {}
    
    # Process each cost dataset
    for dataset_key, current_cost_path in cost_paths.items():
        print(f"\nProcessing cost dataset: {dataset_key}")
        
        # Read the cost raster
        cost_array, cost_meta, transform, cost_nodata, raster_bounds, resolution = read_raster(current_cost_path)
        print(f"Raster shape: {cost_array.shape}")
        
        # Get the dimensions of the raster
        bands, rows, cols = cost_array.shape
        
        # Convert 2D source coordinates to 1D node indices
        source_nodes = [to_1d(r, c, cols) for (r, c) in source_coords]
        print("Source Nodes (1D):", source_nodes)
        
        # Build the adjacency matrix
        graph_csr = build_adjacency_matrix(cost_array, rows, cols)
        
        # Compute shortest paths
        distances, predecessors = compute_shortest_paths(graph_csr, source_nodes)
        
        # Save the base cost distance rasters
        for i, source_name in enumerate(source_names):
            source_distance = distances[i, :].reshape(rows, cols)
            source_distance[np.isinf(source_distance)] = -1
            out_filename = f'cost_distance_{source_name}_{dataset_key}.tif'
            out_path = os.path.join(output_dir, out_filename)
            save_raster(out_path, source_distance, cost_meta, dtype=rasterio.float32, nodata=-1)
            print(f"Saved base cost distance raster for {source_name}: {out_filename}")
        
        # Convert to travel time for each walking speed
        for speed_name, speed_value in walking_speeds.items():
            print(f"\nProcessing travel time rasters for walking speed '{speed_name}' ({speed_value} m/s)...")
            
            for source_name in source_names:
                base_raster_filename = f'cost_distance_{source_name}_{dataset_key}.tif'
                base_raster_path = os.path.join(output_dir, base_raster_filename)
                
                cost_array_base, cost_meta_base = load_raster(base_raster_path)
                travel_time_array = process_raster(cost_array_base, speed_value)
                
                out_filename = f'cost_distance_{source_name}_{dataset_key}_{speed_name}_hours.tif'
                out_path = os.path.join(output_dir, out_filename)
                
                save_raster(out_path, travel_time_array, cost_meta_base, dtype=rasterio.float32, nodata=-1)
                print(f"Saved travel time raster for {source_name} at speed '{speed_name}': {out_filename}")
        
        # Store info for this dataset
        summit_idx = 0  # Assuming summit is always the first source
        dataset_info[dataset_key] = {
            "pred_summit": predecessors[summit_idx],
            "rows": rows,
            "cols": cols,
            "transform": transform,
            "summit_raster_coords": source_coords[summit_idx]
        }
        
        print(f"Processing for dataset '{dataset_key}' complete!")
    
    return all_results, dataset_info


def analyze_safe_zones(probability_path, travel_time_data, thresholds, source_names, walking_speeds, dataset_key, output_dir):
    """
    Analyze safe zones based on eruption probability thresholds.
    
    Args:
        probability_path (str): Path to the eruption probability raster
        travel_time_data (dict): Dictionary of travel time data
        thresholds (list): List of probability thresholds
        source_names (list): List of source names
        walking_speeds (dict): Dictionary of walking speeds
        dataset_key (str): Key for the dataset
        output_dir (str): Directory to save outputs
        
    Returns:
        tuple: (results, min_coords)
    """
    print("\nPerforming safe zone analysis based on eruption probability thresholds...")
    
    # Load the eruption probability raster
    with rasterio.open(probability_path) as src:
        probability_array = src.read(1)
    
    # Initialize result dictionaries
    results = {speed_name: {} for speed_name in walking_speeds.keys()}
    min_coords = {speed_name: {} for speed_name in walking_speeds.keys()}
    
    # Analyze each walking speed
    for speed_name in walking_speeds.keys():
        print(f"\n--- Walking speed: {speed_name} ---")
        results[speed_name] = {}
        
        # Analyze each probability threshold
        for thresh in thresholds:
            print(f"\nEruption Probability Threshold: {thresh}")
            
            # Flatten probability array for easier masking
            probability_flat = probability_array.ravel()
            
            # Create safe zone mask where probability <= threshold
            safe_zone_mask = (probability_flat <= thresh)
            
            min_times_in_zone = []
            coords_in_zone = []
            
            # Find minimum travel time for each source
            for source_name in source_names:
                cost_array_flat = travel_time_data[speed_name][source_name]['cost_array_flat']
                
                # Find valid times within the safe zone
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
                
                min_times_in_zone.append(min_time)
                coords_in_zone.append((min_r, min_c))
                print(f"{source_name}: min travel time = {min_time:.2f} hrs at cell ({min_r}, {min_c})")
            
            results[speed_name][thresh] = min_times_in_zone
            min_coords[speed_name][thresh] = coords_in_zone
    
    # Save analysis reports
    report_path, csv_path = save_analysis_report(
        results, min_coords, source_names, thresholds, 
        walking_speeds, dataset_key, output_dir
    )
    
    # Create and save statistics table
    table_path, stats_csv_path = create_statistics_table(
        results, source_names, walking_speeds, 
        thresholds, dataset_key, output_dir
    )
    
    print(f"Saved analysis report: {report_path}")
    print(f"Saved metrics CSV: {csv_path}")
    print(f"Saved statistics table: {table_path}")
    print(f"Saved statistics CSV: {stats_csv_path}")
    
    return results, min_coords


def load_travel_time_data(dataset_key, source_names, walking_speeds, output_dir):
    """
    Load travel time rasters for further analysis.
    
    Args:
        dataset_key (str): Key for the dataset
        source_names (list): List of source names
        walking_speeds (dict): Dictionary of walking speeds
        output_dir (str): Directory where rasters are stored
        
    Returns:
        dict: Dictionary of travel time data
    """
    travel_time_data = {speed_name: {} for speed_name in walking_speeds.keys()}
    
    for speed_name in walking_speeds.keys():
        for source_name in source_names:
            raster_filename = f'cost_distance_{source_name}_{dataset_key}_{speed_name}_hours.tif'
            raster_path = os.path.join(output_dir, raster_filename)
            
            cost_array_hours, meta_hours = load_raster(raster_path)
            rows_rt, cols_rt = cost_array_hours.shape
            cost_array_hours = np.where(cost_array_hours == meta_hours['nodata'], np.nan, cost_array_hours)
            
            travel_time_data[speed_name][source_name] = {
                'cost_array': cost_array_hours,
                'meta': meta_hours,
                'shape': (rows_rt, cols_rt),
                'cost_array_flat': cost_array_hours.ravel()
            }
        
        print(f"Loaded travel time data for speed '{speed_name}'")
    
    return travel_time_data


def read_raster(path):
    """
    Read a raster file and return its data, metadata, and properties.
    
    Args:
        path (str): Path to the raster file
        
    Returns:
        tuple: (data, meta, transform, nodata, bounds, resolution)
    """
    with rasterio.open(path) as src:
        data = src.read()
        meta = src.meta.copy()
        transform = src.transform
        nodata = src.nodata
        bounds = src.bounds
        resolution = src.res
    return data, meta, transform, nodata, bounds, resolution
