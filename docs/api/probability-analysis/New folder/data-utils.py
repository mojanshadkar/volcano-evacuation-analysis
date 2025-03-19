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
Data loading and file operation utilities for the volcanic evacuation analysis.
"""

import os
import numpy as np
import rasterio
import geopandas as gpd
import fiona
import pandas as pd
import csv


def read_shapefile(path):
    """
    Read a shapefile into a GeoDataFrame.
    
    Args:
        path (str): Path to the shapefile
        
    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the shapefile data
    """
    with fiona.open(path) as src:
        return gpd.GeoDataFrame.from_features(src)


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


def load_raster(file_path):
    """
    Load a raster file and return its data and metadata.
    
    Args:
        file_path (str): Path to the raster file
        
    Returns:
        tuple: (data, meta)
    """
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Read the first band
        meta = src.meta.copy()
    return data, meta


def save_raster(output_path, data, meta, dtype=rasterio.float32, nodata=-1):
    """
    Save a numpy array as a raster file.
    
    Args:
        output_path (str): Path to save the raster
        data (numpy.ndarray): The raster data
        meta (dict): The raster metadata
        dtype: The data type of the output raster
        nodata: The NoData value
    """
    meta.update(dtype=dtype, count=1, compress='lzw', nodata=nodata)
    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(data, 1)


def save_analysis_report(results, min_coords, source_names, thresholds, walking_speeds, dataset_key, output_dir):
    """
    Save analysis results to a text report and CSV file.
    
    Args:
        results (dict): Dictionary of results
        min_coords (dict): Dictionary of coordinates
        source_names (list): List of source names
        thresholds (list): List of probability thresholds
        walking_speeds (dict): Dictionary of walking speeds
        dataset_key (str): Key for the dataset
        output_dir (str): Directory to save outputs
    """
    # Save text report
    output_report_path = os.path.join(output_dir, f"eruption_probability_travel_time_report_{dataset_key}.txt")
    with open(output_report_path, 'w') as f:
        f.write("Eruption Probability Travel Time Analysis Report\n")
        f.write("=================================================\n\n")
        for speed_name in walking_speeds.keys():
            f.write(f"\nWalking Speed: {speed_name} ({walking_speeds[speed_name]} m/s)\n")
            f.write("-" * 40 + "\n")
            for thresh in thresholds:
                f.write(f"\nEruption Probability Threshold: {thresh}\n")
                for idx, source_name in enumerate(source_names):
                    tt = results[speed_name][thresh][idx]
                    coords = min_coords[speed_name][thresh][idx]
                    f.write(f"{source_name}: Travel time = {tt:.2f} hrs at cell {coords}\n")
    
    # Save CSV file
    output_csv_path = os.path.join(output_dir, f"eruption_probability_travel_time_metrics_{dataset_key}.csv")
    with open(output_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Walking_Speed', 'Probability_Threshold', 'Source', 'Min_Travel_Time (hrs)', 'Min_Coords (row,col)'])
        for speed_name in walking_speeds.keys():
            for thresh in thresholds:
                for idx, source_name in enumerate(source_names):
                    writer.writerow([
                        speed_name,
                        thresh,
                        source_name,
                        results[speed_name][thresh][idx],
                        min_coords[speed_name][thresh][idx]
                    ])
    
    return output_report_path, output_csv_path


def create_statistics_table(results, source_names, walking_speeds, thresholds, dataset_key, output_dir):
    """
    Create a statistics table and save it as PNG and CSV.
    
    Args:
        results (dict): Dictionary of results
        source_names (list): List of source names
        walking_speeds (dict): Dictionary of walking speeds
        thresholds (list): List of probability thresholds
        dataset_key (str): Key for the dataset
        output_dir (str): Directory to save outputs
        
    Returns:
        tuple: Paths to the saved PNG and CSV files
    """
    import matplotlib.pyplot as plt
    
    stats_data = []
    for source_name in source_names:
        i = source_names.index(source_name)
        for metric in ['Min', 'Max', 'Mean']:
            row_data = {
                'Source': source_name,
                'Metric': f'{metric} (hours)'
            }
            for speed_name, speed_val in walking_speeds.items():
                times = [results[speed_name][thresh][i] for thresh in thresholds]
                times = [t for t in times if not np.isnan(t)]
                if len(times) == 0:
                    value = np.nan
                else:
                    if metric == 'Min':
                        value = min(times)
                    elif metric == 'Max':
                        value = max(times)
                    else:
                        value = np.mean(times)
                row_data[f'{speed_name.capitalize()} ({speed_val} m/s)'] = f"{value:.2f}" if not np.isnan(value) else "NaN"
            stats_data.append(row_data)
    
    df_stats = pd.DataFrame(stats_data)
    plt.figure(figsize=(12, 8))
    plt.axis('tight')
    plt.axis('off')
    table = plt.table(
        cellText=df_stats.values,
        colLabels=df_stats.columns,
        cellLoc='center',
        loc='center',
        colColours=['#e6e6e6']*len(df_stats.columns)
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    plt.title(f'Travel Time Statistics by Source and Walking Speed\n[Dataset: {dataset_key}]', pad=3, y=0.85)
    
    # Save as PNG
    table_output_path = os.path.join(output_dir, f"travel_time_statistics_by_source_{dataset_key}.png")
    plt.savefig(table_output_path, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    
    # Save as CSV
    csv_output_path = os.path.join(output_dir, f"travel_time_statistics_by_source_{dataset_key}.csv")
    df_stats.to_csv(csv_output_path, index=False)
    
    return table_output_path, csv_output_path
