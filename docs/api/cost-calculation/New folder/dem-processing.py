# dem_processing.py

import numpy as np

def calculate_slope(dem_data, resolution_x, resolution_y, no_data):
    """
    Calculates the slope in eight directions from a DEM.

    Parameters:
    dem_data (numpy.ndarray): 2D array representing the DEM data.
    resolution_x (float): The resolution of the DEM in the x direction.
    resolution_y (float): The resolution of the DEM in the y direction.
    no_data (float): The value representing no data in the DEM.

    Returns:
    numpy.ndarray: A 3D array where the first dimension represents the eight directions 
    (North, South, East, West, North-East, North-West, South-East, South-West),
    and the other two dimensions represent the slope values for each cell in the DEM.
    """
    rows, cols = dem_data.shape
    slope_array = np.full((8, rows, cols), np.nan)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if dem_data[i, j] == no_data:
                continue

            dz_n  = dem_data[i - 1, j] - dem_data[i, j]  # North
            dz_s  = dem_data[i + 1, j] - dem_data[i, j]  # South
            dz_e  = dem_data[i, j + 1] - dem_data[i, j]  # East
            dz_w  = dem_data[i, j - 1] - dem_data[i, j]  # West
            dz_ne = dem_data[i - 1, j + 1] - dem_data[i, j]  # North-East
            dz_nw = dem_data[i - 1, j - 1] - dem_data[i, j]  # North-West
            dz_se = dem_data[i + 1, j + 1] - dem_data[i, j]  # South-East
            dz_sw = dem_data[i + 1, j - 1] - dem_data[i, j]  # South-West

            d_h = resolution_x
            d_d = np.sqrt(resolution_x**2 + resolution_y**2)

            slope_array[0, i, j] = (dz_n / d_h)   # North
            slope_array[1, i, j] = (dz_s / d_h)   # South
            slope_array[2, i, j] = (dz_e / d_h)   # East
            slope_array[3, i, j] = (dz_w / d_h)   # West
            slope_array[4, i, j] = (dz_ne / d_d)  # North-East
            slope_array[5, i, j] = (dz_nw / d_d)  # North-West
            slope_array[6, i, j] = (dz_se / d_d)  # South-East
            slope_array[7, i, j] = (dz_sw / d_d)  # South-West

    return slope_array


def calculate_walking_speed(slope_array):
    """
    Calculates walking speed using Tobler's Hiking Function.
    This function calculates the walking speed given an array of slope values.
    The walking speed is computed using the formula:
    speed = 6 * exp(-3.5 * abs(slope + 0.05))
    Parameters:
    slope_array (numpy.ndarray): An array of slope values.
    Returns:
    numpy.ndarray: An array of walking speeds corresponding to the input slope values.
    """
    return 6 * np.exp(-3.5 * np.abs(slope_array + 0.05))

def get_max_velocity():
    """
    Calculates the maximum velocity based on Tobler's Hiking Function.
    The maximum velocity occurs at a slope of zero.
    Returns:
    float: The maximum walking velocity.
    """
    slope_zero = 0
    return 6 * np.exp(-3.5 * np.abs(slope_zero + 0.05))

def normalize_walking_speed(walking_speed_array):
    """
    Normalize the walking speed array by dividing each element by the maximum velocity.
    The maximum velocity is dynamically calculated using Tobler's Hiking Function at a slope of zero.
    Parameters:
    walking_speed_array (numpy.ndarray): Array of walking speeds to be normalized.
    Returns:
    numpy.ndarray: The normalized walking speed array.
    """
    max_velocity = get_max_velocity()
    return walking_speed_array / max_velocity
