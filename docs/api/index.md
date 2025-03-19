# API Reference

This section provides documentation for the Python modules that make up the Volcano Pedestrian Evacuation Analysis toolkit. Here you can explore the functionality and implementation details of each module.

## Documentation and Source Code

The API Reference is organized in two ways:

1. **Documentation Pages**: This section contains detailed documentation for each module, including function descriptions, parameters, and examples.

2. **Source Code**: All Python modules are also available for direct download in the [Source Code](../source-code/) section, where you can get the complete implementation files.

## How to Use These Modules

You can use these Python modules in several ways:

1. **Read the Documentation**: Browse through this section to understand the functionality and API details.

2. **Download the Source Code**: Visit the [Source Code](../source-code/) section to download the `.py` files directly.

3. **Integration in Your Project**: Place the downloaded `.py` files in your project directory or in a subdirectory (e.g., `/lib` or `/src`).

4. **Import in Your Code**: Import the modules as needed in your Python scripts:
   ```python
   # Example imports
   from cost_calculations import map_landcover_to_cost
   from dem_processing import calculate_slope
   from data_loading import read_shapefile
   ```

## Module Organization

The API is organized into three main components:

### Cost Calculation

These modules handle the creation of cost surfaces from DEM and land cover data:

- **[Data Loading](cost-calculation/data-loading.md)** ([download .py](../source-code/cost-calculation/data-loading.py)): Functions for loading shapefiles and raster data
- **[DEM Processing](cost-calculation/dem-processing.md)** ([download .py](../source-code/cost-calculation/dem-processing.py)): Functions for calculating slopes and walking speeds
- **[Cost Calculations](cost-calculation/cost-calculations.md)** ([download .py](../source-code/cost-calculation/cost-calculations.py)): Core functions for creating and manipulating cost surfaces
- **[Plotting Utils](cost-calculation/plotting-utils.md)** ([download .py](../source-code/cost-calculation/plotting-utils.py)): Visualization functions for raster data and analysis results

### Evacuation Analysis

These modules provide tools for calculating evacuation routes and times:

- **[IO Utilities](evacuation-analysis/io-utils.md)** ([download .py](../source-code/evacuation-analysis/io-utils.py)): Input/output utilities
- **[Configuration](evacuation-analysis/config.md)** ([download .py](../source-code/evacuation-analysis/config.py)): Configuration settings and parameters
- **[Analysis](evacuation-analysis/analysis.md)** ([download .py](../source-code/evacuation-analysis/analysis.py)): Core evacuation analysis functions
- **[Grid Utilities](evacuation-analysis/grid-utils.md)** ([download .py](../source-code/evacuation-analysis/grid-utils.py)): Utilities for working with raster grids
- **[Path Utilities](evacuation-analysis/path-utils.md)** ([download .py](../source-code/evacuation-analysis/path-utils.py)): Utilities for path finding and graph operations
- **[Decomposition](evacuation-analysis/decomposition.md)** ([download .py](../source-code/evacuation-analysis/decomposition.py)): Functions for analyzing factor contributions
- **[Visualization](evacuation-analysis/visualization.md)** ([download .py](../source-code/evacuation-analysis/visualization.py)): Functions for visualizing evacuation analysis results

### Probability Analysis

These modules extend the evacuation analysis to include probability thresholds:

- **[Data Utils](probability-analysis/data-utils.md)** ([download .py](../source-code/probability-analysis/data-utils.py)): Data handling utilities
- **[Raster Utilities](probability-analysis/raster-utils.md)** ([download .py](../source-code/probability-analysis/raster-utils.py)): Raster processing and coordinate transformations
- **[Analysis](probability-analysis/analysis.md)** ([download .py](../source-code/probability-analysis/probability_analysis.py)): Probability-based evacuation analysis
- **[Graph Utilities](probability-analysis/graph-utils.md)** ([download .py](../source-code/probability-analysis/graph-utils.py)): Graph construction and shortest path algorithms
- **[Visualization](probability-analysis/visualization.md)** ([download .py](../source-code/probability-analysis/prob_visualization.py)): Visualization functions for probability analysis

## Dependencies

Before using these modules, ensure you've installed all the required dependencies as specified in the [Installation Guide](../installation.md) page.



## API Version and Compatibility

These modules are compatible with Python 3.8+ and have been tested with the library versions specified in the installation requirements. When upgrading dependencies, always test your workflows to ensure compatibility.
