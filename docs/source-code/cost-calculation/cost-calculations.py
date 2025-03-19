# cost_calculations.py

import numpy as np
import rasterio
from rasterio.features import rasterize

def map_landcover_to_cost(landcover_data, land_cover_cost_mapping):
    """
    Maps land cover classes to their corresponding cost values.
    Parameters:
    landcover_data (numpy.ndarray): A 2D array representing land cover classes.
    land_cover_cost_mapping (dict): A dictionary where keys are land cover class identifiers 
    and values are the corresponding cost values.
    Returns:
    numpy.ndarray: A 2D array of the same shape as landcover_data, where each element is the 
    cost value corresponding to the land cover class at that position.
    """
  
    cost_raster = np.zeros_like(landcover_data, dtype=np.float32)
    for land_cover_class, cost_value in land_cover_cost_mapping.items():
        cost_raster[landcover_data == land_cover_class] = cost_value
    return cost_raster

def rasterize_layer(geometry_list, out_shape, transform, burn_value, fill_value=np.nan):
    """
    Rasterizes a given geometry.

    Parameters:
    geometry_list (list): A list of geometries to rasterize.
    out_shape (tuple): The shape of the output array (height, width).
    transform (Affine): The affine transformation to apply.
    burn_value (float): The value to burn into the raster for the geometries.
    fill_value (float, optional): The value to fill the raster where there are no geometries. Default is np.nan.

    Returns:
    numpy.ndarray: A 2D array with the rasterized geometries.
    """
    return rasterize(
        [(geom, burn_value) for geom in geometry_list],
        out_shape=out_shape,
        transform=transform,
        fill=fill_value,
        all_touched=True,
        dtype='float32'
    )

def update_cost_raster(landcover_cost_data, stream_raster, hiking_path_raster):
    """
    Updates the cost raster based on landcover data, stream locations, and hiking paths.
    Parameters:
    landcover_cost_data (numpy.ndarray): A 2D array representing the cost associated with different landcover types.
    stream_raster (numpy.ndarray): A 2D array where non-NaN values indicate the presence of streams.
    hiking_path_raster (numpy.ndarray): A 2D array where non-NaN values indicate the presence of hiking paths.
    Returns:
    numpy.ndarray: A 2D array with updated cost values where streams are marked as impassable (cost = 0) 
    and hiking paths are marked as passable (cost = 1).
    """
   
    updated_cost_raster = landcover_cost_data.copy()
    landcover_mask = np.isnan(landcover_cost_data)
    updated_cost_raster[~landcover_mask & ~np.isnan(stream_raster)] = 0  # Streams impassable
    updated_cost_raster[~landcover_mask & ~np.isnan(hiking_path_raster)] = 1  # Hiking paths passable
    return updated_cost_raster

def adjust_cost_with_walking_speed(normalized_walking_speed_array, combined_data):
    """
    Adjusts the cost based on the normalized walking speed.

    This function takes an array of normalized walking speeds and an array of combined data,
    and returns an array where each element is the product of the corresponding elements
    from the input arrays.

    Parameters:
    normalized_walking_speed_array (numpy.ndarray): An array of normalized walking speeds.
    combined_data (numpy.ndarray): An array of combined data.

    Returns:
    numpy.ndarray: An array of adjusted costs.
    """

    adjusted_cost_array = normalized_walking_speed_array * combined_data
    return adjusted_cost_array

def invert_cost_array(adjusted_cost_array):
    """
    Inverts the values in the given cost array.
    This function takes an array of adjusted costs and inverts each value. 
    If a value is zero, it is replaced with NaN before inversion to avoid 
    division by zero. After inversion, NaN values are replaced with a large 
    number (1e6).
    Parameters:
    adjusted_cost_array (numpy.ndarray): A numpy array of adjusted costs.
    Returns:
    numpy.ndarray: A numpy array with the inverted cost values.
    """
  
    def invert_values(combined_value):
        combined_value[combined_value == 0] = np.nan
        inverted_values = np.where(np.isnan(combined_value), np.nan, 1.0 / combined_value)
        inverted_values[np.isnan(inverted_values)] = 1e6
        return inverted_values

    inverted_cost_array = np.apply_along_axis(invert_values, -1, adjusted_cost_array)
    return inverted_cost_array
def invert_walking_speed(normalized_walking_speed_array):
    """
    Inverts walking speed values and handles zeros/NaNs appropriately.
    """
    inverted = np.zeros_like(normalized_walking_speed_array)
    for i in range(8):
        temp = normalized_walking_speed_array[i].copy()
        temp[temp == 0] = np.nan
        inverted[i] = np.where(np.isnan(temp), 1e6, 1.0 / temp)
    return inverted

def invert_cost_raster(updated_cost_raster):
    """
    Inverts cost raster values and handles zeros/NaNs appropriately.
    """
    inverted = updated_cost_raster.copy()
    inverted[inverted == 0] = np.nan
    return np.where(np.isnan(inverted), 1e6, 1.0 / inverted)