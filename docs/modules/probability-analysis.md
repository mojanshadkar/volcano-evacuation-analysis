# Probability Analysis Module

## Overview

The Probability Analysis module extends the evacuation analysis framework to incorporate volcanic eruption probability thresholds. This module enables the assessment of evacuation scenarios based on probabilistic hazard zones, allowing for more nuanced risk assessment across different Volcanic Explosivity Index (VEI) levels.

## Key Capabilities

- Integrating eruption probability data into evacuation analysis
- Defining safe zones based on probability thresholds rather than simple distances
- Comparing evacuation scenarios across different VEI levels
- Visualizing evacuation paths with probability contours
- Generating statistical reports and visualizations of analysis results

## Components

The Probability Analysis module consists of the following primary components:

### Graph Utilities (`graph_utils.py`)

This component provides functions for graph-based path finding with probability considerations:

- `build_adjacency_matrix`: Creates graph representations for path analysis
- `compute_shortest_paths`: Calculates optimal evacuation routes
- `reconstruct_path`: Converts path results to geographic coordinates
- `calculate_path_metrics`: Analyzes metrics for evacuation paths

### Raster Utilities (`raster_utils.py`)

This component contains utilities for raster processing and coordinate conversion:

- `resample_raster`: Aligns probability rasters with cost rasters
- `coords_to_raster`: Converts geographic coordinates to raster indices
- `raster_coord_to_map_coords`: Converts indices to geographic coordinates
- `process_raster`: Converts costs to travel times

### Visualization (`visualization.py`)

This component provides specialized visualization functions for probability-based analysis:

- `plot_travel_time_comparison`: Compares evacuation times for different thresholds
- `plot_cost_surface_with_paths`: Visualizes evacuation paths with probability contours
- `create_vei_comparison_plot`: Compares eruption scenarios across VEI levels

### Data Utilities (`data_utils.py`)

This component contains data handling functions specific to probability analysis:

- `read_shapefile` & `read_raster`: Data loading functions
- `save_raster`: Saves analysis results as geospatial rasters
- `save_analysis_report`: Creates reports of probability-based evacuation analysis
- `create_statistics_table`: Generates statistical summaries of evacuation times

### Analysis (`analysis.py`)

This component extends evacuation analysis to incorporate probability thresholds:

- `perform_evacuation_analysis`: Conducts evacuation analysis across datasets
- `analyze_safe_zones`: Identifies safe areas based on probability thresholds
- `load_travel_time_data`: Prepares travel time data for analysis
- `read_raster`: Reads eruption probability and cost rasters

## Workflow

A typical workflow using the Probability Analysis module involves:

1. Loading eruption probability rasters for one or more VEI levels
2. Aligning probability data with cost surfaces from previous analysis
3. Computing evacuation paths for different probability thresholds
4. Analyzing travel times to probability-based safe zones
5. Comparing evacuation scenarios across different VEI levels
6. Generating visualizations and statistical reports

## Usage Example

```python
# Import necessary modules
from data_utils import read_shapefile, read_raster, save_analysis_report
from graph_utils import build_adjacency_matrix, compute_shortest_paths
from raster_utils import resample_raster, coords_to_raster
from analysis import analyze_safe_zones, load_travel_time_data
from visualization import plot_cost_surface_with_paths, create_vei_comparison_plot

# Define paths and parameters
cost_paths = {
    'final': 'inverted_cost_original.tif',
    'modify_landcover': 'inverted_cost_modified.tif'
}
probability_paths = {
    'VEI3': 'eruption_probability_vei3.tif',
    'VEI4': 'eruption_probability_vei4.tif',
    'VEI5': 'eruption_probability_vei5.tif'
}
source_names = ['summit', 'camp1']
walking_speeds = {'slow': 0.91, 'medium': 1.22, 'fast': 1.52}
probability_thresholds = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]
output_dir = 'results'

# Load source locations
summit_data = read_shapefile('summit.shp')
hiking_data = read_shapefile('hiking_path.shp')

# Process each VEI level
for vei, prob_path in probability_paths.items():
    print(f"\nAnalyzing {vei} scenario...")
    
    # Process each cost dataset
    for dataset_key, cost_path in cost_paths.items():
        # Load travel time data
        travel_time_data = load_travel_time_data(
            dataset_key, source_names, walking_speeds, output_dir
        )
        
        # Analyze safe zones based on probability thresholds
        results, min_coords = analyze_safe_zones(
            prob_path, travel_time_data, probability_thresholds,
            source_names, walking_speeds, dataset_key, output_dir
        )
        
        # Create evacuation path visualizations
        plot_cost_surface_with_paths(
            dataset_info, evacuation_paths, prob_path,
            hiking_data, 'medium', probability_thresholds,
            output_dir, vei_label=vei
        )

# Create VEI comparison visualization
create_vei_comparison_plot(
    probability_paths, 'hiking_path.shp', 'summit.shp', output_dir
)
```

## Integration

The Probability Analysis module builds upon both the [Cost Calculation](modules/cost-calculations.md) and [Evacuation Analysis](modules/Evacuation-Analysis.md) modules to provide a comprehensive framework for volcanic risk assessment. By incorporating eruption probability data, it enables more realistic and nuanced evacuation planning that accounts for the variable spatial distribution of volcanic hazards across different eruption scenarios.
