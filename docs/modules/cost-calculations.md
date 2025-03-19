# Cost Calculation Module

## Overview

The Cost Calculation module provides the foundation for creating and analyzing cost surfaces for geographic terrain analysis. It consists of a collection of utilities that enable processing of Digital Elevation Models (DEMs), handling of land cover data, and creation of cost surfaces that represent the difficulty of traversing different types of terrain.

## Key Capabilities

- Converting land cover classes to cost values
- Calculating slopes in multiple directions from DEMs
- Implementing Tobler's Hiking Function to estimate realistic walking speeds
- Adjusting cost surfaces based on terrain features such as streams and hiking paths
- Visualizing analysis results with customizable maps and plots

## Components

The Cost Calculation module consists of the following primary components:

### Cost Calculations (`cost_calculations.py`)

This component handles the conversion of land cover and terrain data into cost surfaces:

- `map_landcover_to_cost`: Maps land cover classes to associated traversal costs
- `rasterize_layer`: Converts vector geometries to raster format
- `update_cost_raster`: Updates cost values based on features like streams and hiking paths
- `adjust_cost_with_walking_speed`: Integrates slope-based walking speeds with land cover costs
- `invert_cost_array`: Prepares cost values for path finding by inverting them

### DEM Processing (`dem_processing.py`)

This component focuses on extracting and analyzing slope information from DEMs:

- `calculate_slope`: Computes slopes in eight cardinal and ordinal directions
- `calculate_walking_speed`: Applies Tobler's Hiking Function to estimate walking speeds
- `normalize_walking_speed`: Converts speeds to normalized values for analysis
- `get_max_velocity`: Calculates the maximum theoretical walking speed

### Data Loading (`data_loading.py`)

This component provides functions for loading geospatial data:

- `read_shapefile`: Loads vector data from shapefiles
- `read_raster`: Loads raster data with associated metadata

### Plotting Utilities (`plotting_utils.py`)

This component contains visualization functions for presenting analysis results:

- `plot_continuous_raster_with_points`: Creates maps with raster backgrounds and point overlays
- `plot_normalized_walking_speed`: Visualizes walking speed data across terrain
- `plot_walking_speed_vs_slope`: Creates slope-vs-speed relationship plots
- Various other specialized plotting functions for different analysis outputs

## Workflow

A typical workflow using the Cost Calculation module involves:

1. Loading terrain and land cover data using the data loading utilities
2. Processing the DEM to calculate slopes and walking speeds
3. Converting land cover data to cost values
4. Combining the walking speed and land cover costs to create a comprehensive cost surface
5. Inverting the cost surface for path finding
6. Visualizing the results using the plotting utilities

## Usage Example

```python
# Import necessary modules
from data_loading import read_raster, read_shapefile
from dem_processing import calculate_slope, calculate_walking_speed, normalize_walking_speed
from cost_calculations import map_landcover_to_cost, update_cost_raster, invert_cost_array
from plotting_utils import plot_continuous_raster_with_points

# Load data
dem_data, dem_meta, dem_transform, dem_nodata, dem_bounds, dem_res = read_raster("dem.tif")
landcover_data, lc_meta, lc_transform, lc_nodata, lc_bounds, lc_res = read_raster("landcover.tif")
summit_points = read_shapefile("summit.shp")

# Process DEM
slope_array = calculate_slope(dem_data[0], dem_res[0], dem_res[1], dem_nodata)
walking_speed_array = calculate_walking_speed(slope_array)
normalized_ws = normalize_walking_speed(walking_speed_array)

# Process land cover
land_cover_cost_mapping = {1: 1.0, 2: 1.5, 3: 3.0, 4: 10.0}  # Example mapping
landcover_cost = map_landcover_to_cost(landcover_data[0], land_cover_cost_mapping)

# Combine costs
adjusted_cost = adjust_cost_with_walking_speed(normalized_ws, landcover_cost)
inverted_cost = invert_cost_array(adjusted_cost)

# Visualize results
plot_continuous_raster_with_points(
    inverted_cost[0],  # Use first direction for visualization
    dem_transform.to_gdal(),
    summit_points,
    "Cost Surface with Summit Point",
    "Cost Value",
    "cost_surface_map.jpg"
)
```

## Integration

The Cost Calculation module serves as the foundation for the [Evacuation Analysis](modules/Evacuation-Analysis.md) module, which builds upon the cost surfaces to calculate evacuation paths and times. The outputs from this module can be directly fed into evacuation analysis workflows to model realistic terrain-based evacuation scenarios.
