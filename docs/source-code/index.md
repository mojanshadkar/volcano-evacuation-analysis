# Source Code

This section provides direct access to the Python source files that implement the Volcano Pedestrian Evacuation Analysis toolkit. You can view and download these files for use in your own projects.





## Available Modules

### Cost Calculation

- [data-loading.py](cost-calculation/data-loading.py): Functions for loading shapefiles and raster data
- [dem-processing.py](cost-calculation/dem-processing.py): Functions for calculating slopes and walking speeds
- [cost-calculations.py](cost-calculation/cost-calculations.py): Core functions for creating and manipulating cost surfaces
- [plotting-utils.py](cost-calculation/plotting-utils.py): Visualization functions for raster data and analysis results

### Evacuation Analysis

- [io-utils.py](evacuation-analysis/io-utils.py): Input/output utilities
- [config.py](evacuation-analysis/config.py): Configuration settings and parameters
- [analysis.py](evacuation-analysis/analysis.py): Core evacuation analysis functions
- [grid-utils.py](evacuation-analysis/grid-utils.py): Utilities for working with raster grids
- [path-utils.py](evacuation-analysis/path-utils.py): Utilities for path finding and graph operations
- [decomposition.py](evacuation-analysis/decomposition.py): Functions for analyzing factor contributions
- [visualization.py](evacuation-analysis/visualization.py): Functions for visualizing evacuation analysis results

### Probability Analysis

- [data-utils.py](probability-analysis/data-utils.py): Data handling utilities
- [raster-utils.py](probability-analysis/raster-utils.py): Raster processing and coordinate transformations
- [probability-analysis.py](probability-analysis/probability-analysis.py): Probability-based evacuation analysis
- [graph-utils.py](probability-analysis/graph-utils.py): Graph construction and shortest path algorithms
- [prob-visualization.py](probability-analysis/prob-visualization.py): Visualization functions for probability analysis

## Dependencies

These modules require several Python packages to function properly. Please see the [Installation Guide](../installation.md) for detailed dependency information.

## Documentation

For detailed documentation of each module and function, please visit the [API Reference](../api/) section.

