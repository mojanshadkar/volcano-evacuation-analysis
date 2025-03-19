# data_loading.py

import fiona
import geopandas as gpd
import rasterio
import numpy as np
from affine import Affine

def read_shapefile(path):
    """
    Load a shapefile and return it as a GeoDataFrame.
    Parameters:
    path (str): The file path to the shapefile.
    Returns:
    gpd.GeoDataFrame: A GeoDataFrame containing the data from the shapefile.
    """
    
    with fiona.open(path) as src:
        return gpd.GeoDataFrame.from_features(src, crs=src.crs)


def read_raster(path):
    """
    Reads a raster file and returns its data, profile, transform, CRS, and nodata value.
    Parameters:
    path (str): The file path to the raster file.
    Returns:
    tuple: A tuple containing:
        - data (numpy.ndarray): The raster data.
        - profile (dict): The profile metadata of the raster.
        - transform (affine.Affine): The affine transform of the raster.
        - crs (rasterio.crs.CRS): The coordinate reference system of the raster.
        - nodata (float or int): The nodata value of the raster.
    """
    
    with rasterio.open(path) as dataset:
        data = dataset.read(1)
        profile = dataset.profile
        transform = dataset.transform
        crs = dataset.crs
        nodata = dataset.nodata
    return data, profile, transform, crs, nodata
