# Visualization

The `visualization.py` module provides functions for creating visualizations of volcanic evacuation analysis results, including travel time comparisons, cost surfaces with evacuation paths, and VEI (Volcanic Explosivity Index) comparison plots.

## Functions

### `plot_travel_time_comparison`

```python
def plot_travel_time_comparison(all_results, source_names, thresholds, walking_speeds, output_dir, filename="comparison_travel_time_by_source.png")
```

Plot a comparison of travel times between datasets.

This function creates a multi-panel plot comparing evacuation travel times for different probability thresholds, walking speeds, and terrain scenarios (original vs. penalized landcover).

**Parameters:**

- `all_results (dict)`: Dictionary of results from all datasets, structured as:
  ```
  {
      dataset_key: {
          speed_name: {
              threshold: [times_per_source]
          }
      }
  }
  ```
- `source_names (list)`: List of source names (e.g., 'summit', 'camp1').
- `thresholds (list)`: List of probability thresholds for safe zones.
- `walking_speeds (dict)`: Dictionary mapping speed names to values in m/s.
- `output_dir (str)`: Directory to save the plot.
- `filename (str)`: Filename for the output plot (default: "comparison_travel_time_by_source.png").

**Returns:**

- `str`: Path to the saved plot.

---

### `plot_cost_surface_with_paths`

```python
def plot_cost_surface_with_paths(dataset_info, evacuation_paths, eruption_probability_path, hiking_path, selected_speed, thresholds, output_dir, vei_label="VEI4")
```

Plot cost surface with evacuation paths.

This function generates a visualization of evacuation paths overlaid on cost surfaces for different terrain scenarios, incorporating eruption probability contours and hiking trails.

**Parameters:**

- `dataset_info (dict)`: Dictionary containing information about each dataset.
- `evacuation_paths (dict)`: Dictionary of evacuation paths structured as: 
  ```
  {
      dataset_key: {
          threshold: [(row, col), ...]
      }
  }
  ```
- `eruption_probability_path (str)`: Path to the eruption probability raster.
- `hiking_path (str)`: Path to the hiking trail shapefile.
- `selected_speed (str)`: Selected walking speed for visualization (e.g., 'medium').
- `thresholds (list)`: List of probability thresholds for evacuation paths.
- `output_dir (str)`: Directory to save the plot.
- `vei_label (str)`: VEI label for the title (default: "VEI4").

**Returns:**

- `str`: Path to the saved plot.

---

### `create_vei_comparison_plot`

```python
def create_vei_comparison_plot(eruption_probability_paths, hiking_path, summit_path, output_dir)
```

Create a comparison plot of contour maps for different VEI levels side by side.

This function creates a multi-panel visualization showing probability contours for different Volcanic Explosivity Index (VEI) levels, helping to compare the spatial extent of hazards across eruption scenarios.

**Parameters:**

- `eruption_probability_paths (dict)`: Dictionary mapping VEI levels to file paths of eruption probability rasters.
- `hiking_path (str)`: Path to the hiking trail shapefile.
- `summit_path (str)`: Path to the summit point shapefile.
- `output_dir (str)`: Directory to save the plot.

**Returns:**

- `str`: Path to the saved plot.
