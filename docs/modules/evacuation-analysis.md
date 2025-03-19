# Evacuation Analysis Module

## Overview

The Evacuation Analysis module provides tools for analyzing evacuation scenarios in volcanic risk assessments. Building on the cost surfaces created by the [Cost Calculation](modules/cost-calculations.md) module, it performs path finding, calculates evacuation times, and analyzes safe zones based on distance from hazard sources.

## Key Capabilities

- Building graph representations of geographic terrain for path finding
- Computing optimal evacuation routes using Dijkstra's algorithm
- Analyzing minimum travel times to reach safe zones
- Decomposing evacuation paths to understand contributing factors
- Visualizing evacuation paths and travel times

## Components

The Evacuation Analysis module consists of the following primary components:

### Path Utilities (`path_utils.py`)

This component provides functions for path finding and analysis:

- `build_adjacency_matrix`: Converts cost rasters to graph representations
- `reconstruct_path`: Converts shortest path results to coordinate sequences
- `calculate_path_metrics`: Computes metrics for evacuation paths

### Analysis (`analysis.py`)

This component contains the core evacuation analysis functionality:

- `run_dijkstra_analysis`: Executes Dijkstra's algorithm for shortest path finding
- `process_travel_times`: Converts cost distances to time-based metrics
- `analyze_safe_zones`: Identifies minimum travel times to safe zones

### Decomposition (`decomposition.py`)

This component analyzes the relative contributions of different factors to evacuation paths:

- `reconstruct_path`: Path reconstruction for detailed analysis
- `expand_single_band`: Expands single-band cost data to directional analysis
- `run_decomposition_analysis`: Quantifies slope vs. land cover contributions

### IO Utilities (`io_utils.py`)

This component provides input/output functions for evacuation analysis:

- `read_shapefile` & `read_raster`: Data loading functions
- `save_raster`: Saves analysis results as geospatial rasters
- `save_analysis_report` & `save_metrics_csv`: Export analysis results

### Configuration (`config.py`)

This component defines parameters and settings for the analysis:

- Walking speeds for different scenarios
- File paths for input data
- Source locations and safe zone distances
- Movement direction definitions

### Grid Utilities (`grid_utils.py`)

This component provides utilities for working with raster grids:

- `coords_to_raster`: Converts geographic coordinates to raster indices
- `to_1d`: Converts 2D grid coordinates to 1D indices
- `raster_coord_to_map_coords`: Converts raster indices to geographic coordinates
- `process_raster`: Converts cost values to travel times
- `calculate_distance_from_summit`: Computes Euclidean distances from points

## Workflow

A typical workflow using the Evacuation Analysis module involves:

1. Loading cost surfaces from the Cost Calculation module
2. Building a graph representation of the terrain
3. Computing shortest paths from evacuation sources
4. Analyzing travel times to safe zones
5. Decomposing evacuation paths to understand contributing factors
6. Generating visualizations and reports

## Usage Example

```python
# Import necessary modules
from io_utils import read_raster, save_analysis_report
from path_utils import build_adjacency_matrix
from analysis import run_dijkstra_analysis, analyze_safe_zones
from grid_utils import calculate_distance_from_summit, to_1d
from config import WALKING_SPEEDS, SOURCE_NAMES, SAFE_ZONE_DISTANCES

# Load inverted cost raster
cost_array, meta, transform, nodata, bounds, res = read_raster("inverted_cost.tif")
rows, cols = cost_array.shape[1:3]

# Define source coordinates (summit and camps)
source_coords = [(100, 150), (120, 140)]  # Example coordinates

# Convert 2D source coordinates to 1D node indices
source_nodes = [to_1d(r, c, cols) for r, c in source_coords]

# Build adjacency matrix for path finding
graph_csr = build_adjacency_matrix(cost_array, rows, cols)

# Run Dijkstra's algorithm
distances, predecessors = run_dijkstra_analysis(graph_csr, source_nodes)

# Calculate distance from summit for safe zone analysis
distance_from_summit = calculate_distance_from_summit(source_coords[0], rows, cols)

# Process travel times and analyze safe zones
travel_time_data = {}
for speed_name, speed_value in WALKING_SPEEDS.items():
    travel_time_data[speed_name] = {}
    for i, source_name in enumerate(SOURCE_NAMES):
        distance_array = distances[i].reshape(rows, cols)
        travel_time = distance_array * 100 / speed_value / 3600  # Convert to hours
        travel_time_data[speed_name][source_name] = {
            'cost_array': travel_time,
            'cost_array_flat': travel_time.ravel()
        }

# Analyze safe zones
results, min_coords = analyze_safe_zones(
    distance_from_summit, 
    travel_time_data, 
    SAFE_ZONE_DISTANCES, 
    SOURCE_NAMES
)

# Save analysis report
save_analysis_report(
    "evacuation_report.txt",
    results,
    min_coords,
    SOURCE_NAMES,
    WALKING_SPEEDS,
    SAFE_ZONE_DISTANCES
)
```

## Integration

The Evacuation Analysis module builds upon the cost surfaces created by the [Cost Calculation](modules/cost-calculations.md) module and is extended by the [Probability Analysis](modules/Probability-Analysis.md) module, which incorporates eruption probability thresholds into the evacuation analysis. Together, these modules provide a comprehensive framework for volcanic evacuation analysis and planning.
