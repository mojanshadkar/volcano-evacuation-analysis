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
Raster operations and coordinate conversion utilities.
"""

import numpy as np
import rasterio
import rasterio.warp
from rasterio.transform import xy


def resample_raster(source_path, target_path, output_path, resampling_method=rasterio.warp.Resampling.bilinear):
    """
    Resample a source raster to match the grid of a target raster.
    
    Args:
        source_path (str): Path to the source raster
        target_path (str): Path to the target raster (for grid reference)
        output_path (str): Path to save the resampled raster
        resampling_method: Resampling method to use
        
    Returns:
        tuple: (resampled_array, resampled_meta)
    """
    # Load source raster
    with rasterio.open(source_path) as src:
        source_array = src.read(1)  # Read the first band
        source_meta = src.meta.copy()
        source_nodata = src.nodata
        source_transform = src.transform
        source_crs = src.crs
    
    # Replace NoData values with np.nan
    source_array = np.where(source_array == source_nodata, np.nan, source_array)
    
    # Get target grid properties
    with rasterio.open(target_path) as src:
        target_meta = src.meta.copy()
        target_transform = src.transform
        target_crs = src.crs
        target_shape = src.shape
    
    # Set up the output metadata
    resampled_meta = target_meta.copy()
    resampled_meta.update({
        'dtype': 'float32',
        'count': 1,
        'nodata': np.nan,
        'driver': 'GTiff'
    })
    
    # Create an empty array for the resampled data
    resampled_array = np.empty(target_shape, dtype=np.float32)
    
    # Perform the resampling
    rasterio.warp.reproject(
        source=source_array,
        destination=resampled_array,
        src_transform=source_transform,
        src_crs=source_crs,
        dst_transform=target_transform,
        dst_crs=target_crs,
        resampling=resampling_method
    )
    
    # Replace any remaining NoData values with np.nan
    resampled_array = np.where(np.isnan(resampled_array), np.nan, resampled_array)
    
    # Save the resampled raster
    with rasterio.open(output_path, 'w', **resampled_meta) as dst:
        dst.write(resampled_array, 1)
    
    return resampled_array, resampled_meta


def coords_to_raster(gdf, transform, bounds, res):
    """
    Convert geographic coordinates to raster row/column coordinates.
    
    Args:
        gdf (GeoDataFrame): GeoDataFrame containing point geometries
        transform: The raster's affine transform
        bounds: The raster's bounds
        res: The raster's resolution
        
    Returns:
        list: List of (row, col) coordinates
    """
    raster_coords = []
    for point in gdf.geometry:
        x, y = point.x, point.y
        if not (bounds.left <= x <= bounds.right and bounds.bottom <= y <= bounds.top):
            print(f"Point {x}, {y} is out of raster bounds.")
            continue
        col = int((x - bounds.left) / res[0])
        row = int((bounds.top - y) / res[1])
        raster_coords.append((row, col))
    return raster_coords


def raster_coord_to_map_coords(row, col, transform):
    """
    Convert raster (row, col) coordinates to map (x, y) coordinates.
    
    Args:
        row (int): Raster row index
        col (int): Raster column index
        transform: Raster affine transform
        
    Returns:
        tuple: (x, y) map coordinates
    """
    x, y = xy(transform, row, col, offset='center')
    return x, y


def to_1d(r, c, cols):
    """
    Convert 2D (row, col) coordinates to 1D index.
    
    Args:
        r (int): Row index
        c (int): Column index
        cols (int): Number of columns in the raster
        
    Returns:
        int: 1D index
    """
    return r * cols + c


def process_raster(cost_array, walking_speed, cell_size=100):
    """
    Convert cost raster to travel time (in hours).
    
    Args:
        cost_array (numpy.ndarray): Cost array
        walking_speed (float): Walking speed in m/s
        cell_size (float): Cell size in meters
        
    Returns:
        numpy.ndarray: Travel time array in hours
    """
    # Multiply by cell size to get distance
    cost_array = cost_array * cell_size  
    # Convert to seconds (m / (m/s) = s)
    cost_array = cost_array / walking_speed  
    # Convert seconds to hours
    cost_array = cost_array / 3600  
    # Replace infinite values with -1
    cost_array[np.isinf(cost_array)] = -1
    
    return cost_array
