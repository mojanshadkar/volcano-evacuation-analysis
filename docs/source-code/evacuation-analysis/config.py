"""
Configuration settings for volcanic evacuation analysis.

This module establishes environment variables, defines walking speeds,
and specifies file paths for various geospatial datasets used in the 
volcanic evacuation analysis for Mt. Marapi.

Constants:
----------
WALKING_SPEEDS : dict
   Dictionary mapping speed categories to values in meters per second:
   - 'slow': 0.91 m/s
   - 'medium': 1.22 m/s
   - 'fast': 1.52 m/s

DATA_FOLDER : str
   Base directory for python results.

COST_PATHS : dict
   Dictionary mapping cost raster names to their file paths:
   - 'final': Main cost raster with original hiking path
   - 'modify_landcover': Cost raster with modified land cover
   - 'walking_speed': Walking speed cost raster
   - 'base_cost': Base cost raster

SUMMIT_PATH : str
   File path to the Mt. Marapi summit location (GPKG format).

CAMP_SPOT_PATH : str
   File path to camping locations (GPKG format).

HIKING_PATH : str
   File path to the original hiking path (GPKG format).

LANDCOVER_100M : str
   File path to land cover data with 100m buffer (TIF format).

DEM_100M : str
   File path to digital elevation model with 100m buffer (TIF format).

SOURCE_NAMES : list
   List of source location names for evacuation analysis:
   ['summit', 'camp1', 'camp2', 'camp3', 'camp4']

SAFE_ZONE_DISTANCES : list
   List of safe zone distances from 500m to 4500m in 500m increments.

DIRECTIONS : list
   List of tuples representing the eight possible movement directions
   for path analysis (cardinal and intercardinal directions).

Environment Variables:
---------------------
USE_PATH_FOR_GDAL_PYTHON : str
   Set to "True" to use the system path for GDAL Python bindings.

PROJ_LIB : str
   Set to pyproj's data directory for projection information.
"""

import os
import pyproj
# Set environment variables
os.environ['USE_PATH_FOR_GDAL_PYTHON'] = "True"
os.environ['PROJ_LIB'] = pyproj.datadir.get_data_dir()
# Walking speeds (m/s)
WALKING_SPEEDS = {
   'slow': 0.91,
   'medium': 1.22,
   'fast': 1.52
}
# Define your paths directly
DATA_FOLDER = r'C:\Users\Mojan\Desktop\RA Volcano\python_results'
# Cost raster datasets
# Modified to include 4 datasets instead of 2.
# Cost raster datasets
COST_PATHS = {
    'final': os.path.join(DATA_FOLDER, 'Awu_inverted_cost_8_directions_original.tif'),
    'modify_landcover': os.path.join(DATA_FOLDER, 'Awu_inverted_cost_8_directions_modified.tif'),
    'walking_speed': os.path.join(DATA_FOLDER, 'inverted_Slopecost_8_directions_Awu_OriginalLandcover.tif'),
    'base_cost': os.path.join(DATA_FOLDER, 'invert_landcovercost_original_Awu.tif')
}
# Input paths
SUMMIT_PATH = r"C:\Users\Mojan\Desktop\RA Volcano\projection\summit_awu_correct_proj_final.shp"
CAMP_SPOT_PATH = r"C:\Users\Mojan\Desktop\RA Volcano\projection\campspot_awu_correct_proj_final.shp"
HIKING_PATH = r'C:\Users\Mojan\Desktop\RA Volcano\projection\hikingpath_awu_buffer_correctproj_final.shp'
landcover_100m = r'C:\Users\Mojan\Desktop\RA Volcano\Dataset\Awu_LandCover_2019_100m_Buffer_UTM.tif'
DEM_100m = r"C:\Users\Mojan\Desktop\RA Volcano\Dataset\Awu_DEM_100m_Buffer_UTM.tif"
# Source names
SOURCE_NAMES = ['summit', 'camp1']
# Safe zone distances
SAFE_ZONE_DISTANCES = list(range(500, 5000, 500))
# Movement directions
DIRECTIONS = [
   (-1, 0),   # Up
   (1, 0),    # Down
   (0, 1),    # Right
   (0, -1),   # Left
   (-1, 1),   # Up-Right
   (-1, -1),  # Up-Left
   (1, 1),    # Down-Right
   (1, -1)    # Down-Left
]