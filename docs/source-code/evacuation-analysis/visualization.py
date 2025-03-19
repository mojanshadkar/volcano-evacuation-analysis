import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patheffects import withStroke
import os
import rasterio
import pandas as pd


def load_raster(path):
    """
    Load a single-band raster file and return its data and metadata.
    
    This helper function opens a raster file using rasterio and extracts
    the first band of data along with essential metadata for visualization.
    
    Parameters:
    -----------
    path : str
        The file path to the raster file to be loaded.
    
    Returns:
    --------
    tuple
        A tuple containing:
        - array (numpy.ndarray): The raster data from the first band with shape (rows, cols)
        - metadata (dict): A dictionary containing:
            - 'transform' (affine.Affine): The affine transform
            - 'crs' (CRS): The coordinate reference system
            - 'nodata' (float or int): The no-data value
    
    Notes:
    ------
    - This function is streamlined for visualization purposes, reading only the
      first band and a subset of metadata.
    - The raster file is properly closed after reading using a context manager.
    """
    with rasterio.open(path) as src:
        array = src.read(1)  # Read the first band
        metadata = {
            'transform': src.transform,
            'crs': src.crs,
            'nodata': src.nodata
        }
    return array, metadata


def raster_coord_to_map_coords(row, col, transform):
    """
    Convert raster coordinates (row, column) to map coordinates (x, y).
    
    This function transforms pixel coordinates in a raster to their corresponding
    geographic coordinates using the raster's affine transform.
    
    Parameters:
    -----------
    row : int
        The row index in the raster (zero-based).
    
    col : int
        The column index in the raster (zero-based).
    
    transform : affine.Affine or list/tuple
        The affine transform of the raster, defining the relationship between
        pixel coordinates and geographic coordinates. Can be provided as an
        Affine object or as a 6-element tuple/list in the form 
        [a, b, c, d, e, f] where:
        - a: width of a pixel
        - b: row rotation (typically 0)
        - c: x-coordinate of the upper-left corner
        - d: column rotation (typically 0)
        - e: height of a pixel (typically negative)
        - f: y-coordinate of the upper-left corner
    
    Returns:
    --------
    tuple
        A tuple (x, y) containing the geographic coordinates corresponding to
        the specified raster cell.
    
    Notes:
    ------
    - The function calculates coordinates based on the transform components
      rather than using the rasterio.transform.xy function, enabling use with
      transform arrays as well as Affine objects.
    """
    x = transform[2] + col * transform[0]
    y = transform[5] + row * transform[4]
    return x, y


def plot_travel_time_comparison(all_results, safe_zone_distances, source_names, speed_colors):
    """
    Create a comparison plot of minimum travel times for different evacuation scenarios.
    
    This function generates a figure with three subplots showing travel time curves
    for summit, camp1, and camp2 sources. Each subplot compares travel times for
    different walking speeds (slow, medium, fast) and terrain scenarios (original 
    and penalized landcover).
    
    Parameters:
    -----------
    all_results : dict
        A nested dictionary containing travel time results for different datasets:
        {dataset_key: {speed_name: {safe_zone_distance: [times_per_source]}}}
        where times_per_source is a list of travel times (in hours) for each source.
        Must include 'final' and 'modify_landcover' datasets.
    
    safe_zone_distances : list
        List of safe zone distances used in the analysis.
    
    source_names : list
        A list of source location names corresponding to indices in the results arrays.
        Must include 'summit', 'camp1', and 'camp2'.
    
    speed_colors : dict
        Dictionary mapping speed names (str) to color values for plotting.
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object containing the comparison plots, designed for A4 landscape format.
    
    Notes:
    ------
    - Progress and timing information is printed to standard output.
    - Plots use solid lines for original landcover and dashed lines for penalized landcover.
    - The figure includes a shared legend in the rightmost subplot.
    - Each subplot is labeled with a letter (A, B, C) in the top-left corner.
    """
    print("\nCreating travel time comparison plot...")
    start_time = time.time()
    
    # Define specific sources to plot
    selected_sources = ['summit', 'camp1']
    n_sources = len(selected_sources)
    
    # Create figure in A4 landscape format (11.69 x 8.27 inches)
    fig, axes = plt.subplots(1, 2, figsize=(11.69, 4), sharey=True)
    
    # Store lines and labels for the legend
    lines = []
    labels = []
    first_plot = True
    
    # For each source
    for src_idx, source_name in enumerate(selected_sources):
        ax = axes[src_idx]
        
        # Plot all walking speeds for both original and penalized
        for speed_name, speed_color in speed_colors.items():
            # Get data for original and penalized
            original = [
                all_results['final'][speed_name][sz][source_names.index(source_name)]
                for sz in safe_zone_distances
            ]
            penalized = [
                all_results['modify_landcover'][speed_name][sz][source_names.index(source_name)]
                for sz in safe_zone_distances
            ]
            
            # Plot with consistent line styles
            line1 = ax.plot(safe_zone_distances, original, '-', color=speed_color)
            line2 = ax.plot(safe_zone_distances, penalized, '--', color=speed_color)
            
            # Only store legend entries once
            if first_plot:
                lines.extend([line1[0], line2[0]])
                labels.extend([
                    f'{speed_name.capitalize()} - Original', 
                    f'{speed_name.capitalize()} - Penalized'
                ])
        
        # Add letter label in top left corner
        ax.text(0.05, 0.95, chr(65 + src_idx), transform=ax.transAxes, 
                fontsize=12, fontweight='bold', va='top')
        
        ax.set_xlabel("Safe Zone Radius (m)", fontsize=10)
        if src_idx == 0:  # Add ylabel only for leftmost plot
            ax.set_ylabel("Minimum Travel Time (hrs)", fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add legend to the right side of the third subplot
        if src_idx == 2:  # For the last subplot
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(lines, labels, fontsize=9, 
                      loc='center left', 
                      bbox_to_anchor=(1.05, 0.5))
        
        first_plot = False
    
    plt.tight_layout()
    
    # Comment out plt.show() to avoid opening a new window:
    plt.show()
    
    end_time = time.time()
    print(f"Travel time comparison plot created in {end_time - start_time:.2f} seconds")
    return fig


def create_cost_surface_subplots(dataset_info, cost_arrays, transforms, evacuation_paths, 
                               summit_coords, safe_zone_distances, hiking_gdf, output_path):
    """
    Create visualizations of cost surfaces with evacuation paths for two terrain scenarios.
    
    This function generates a figure with two cost surface maps showing optimal evacuation
    paths from the summit to different safe zone distances. The maps include distance contours,
    hiking paths, and the summit location. Cost surfaces use a logarithmic color scale to
    better visualize travel time differences.
    
    Parameters:
    -----------
    dataset_info : dict
        Dictionary containing information about each dataset, including:
        - keys: Dataset names (e.g., 'final', 'modify_landcover')
        - values: Dictionaries with dataset metadata
    
    cost_arrays : list
        List of numpy arrays containing the cost surfaces for each dataset.
    
    transforms : list
        List of affine transforms corresponding to each cost array.
    
    evacuation_paths : dict
        Dictionary of evacuation paths for each dataset and safe zone:
        {dataset_key: {safe_zone_distance: [path_coordinates]}}
        where path_coordinates is a list of (row, col) tuples.
    
    summit_coords : dict
        Dictionary mapping dataset keys to summit coordinates as (row, col) tuples.
    
    safe_zone_distances : list
        List of safe zone distances to plot paths for.
    
    hiking_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing hiking trail geometries to overlay on the maps.
    
    output_path : str
        File path where the figure will be saved.
    
    Returns:
    --------
    None
        The function saves the figure to the specified output path but does not return a value.
    
    Notes:
    ------
    - Progress and timing information is printed to standard output.
    - A logarithmic transformation is applied to the cost surfaces to enhance visualization.
    - The figure includes a color bar indicating the travel time.
    - Evacuation paths are color-coded by safe zone distance.
    - Contour lines show distance from the summit.
    - Each subplot is labeled with a letter (A, B) in the top-left corner.
    """
    print("\nCreating cost surface subplots...")
    start_time = time.time()
    
    # Create figure with larger size 
    fig = plt.figure(figsize=(11.69, 8.27))  # Landscape A4
    
    # Create subplot grid with space for legend and colorbar
    gs = plt.GridSpec(2, 2, height_ratios=[0.9, 0.1], hspace=0.1)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Create a common colormap and normalization
    cmap = plt.cm.RdYlBu_r.copy()
    cmap.set_bad('white', alpha=0)
    
    epsilon = 0.1
    max_log_cost = np.log1p(10 + epsilon)
    
    # Find global vmin and vmax for consistent color scaling
    vmin = float('inf')
    vmax = float('-inf')
    for cost_array in cost_arrays:
        cost_array_log = np.log1p(cost_array + epsilon)
        cost_array_log[cost_array_log > max_log_cost] = max_log_cost
        cost_array_masked = np.ma.masked_where(cost_array <= 0, cost_array_log)
        vmin = min(vmin, np.min(cost_array_log[~cost_array_masked.mask]))
        vmax = max(vmax, np.max(cost_array_log[~cost_array_masked.mask]))
    vcenter = vmin + (vmax - vmin) / 2
    
    norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    
    # Colors for paths
    colors_paths = ['lime', 'cyan', 'yellow', 'silver', 'pink', 'orange', 'red', 'blue', 'purple']
    
    # Plot both subplots
    for idx, (ax, ds_key) in enumerate(zip([ax1, ax2], dataset_info.keys())):
        cost_array = cost_arrays[idx]
        transform = transforms[idx]
        
        # Process cost array
        cost_array_log = np.log1p(cost_array + epsilon)
        cost_array_log[cost_array_log > max_log_cost] = max_log_cost
        cost_array_masked = np.ma.masked_where(cost_array <= 0, cost_array_log)
        
        # Plot cost surface
        im = ax.imshow(
            cost_array_masked, cmap=cmap, norm=norm,
            extent=[
                transform[2], 
                transform[2] + transform[0] * cost_array.shape[1],
                transform[5] + transform[4] * cost_array.shape[0],
                transform[5]
            ]
        )
        
        # Plot evacuation paths
        for i, distance in enumerate(safe_zone_distances):
            if distance in evacuation_paths[ds_key]:
                path = evacuation_paths[ds_key][distance]
                if path:
                    path_coords = [raster_coord_to_map_coords(row, col, transform) for row, col in path]
                    xs, ys = zip(*path_coords)
                    ax.plot(xs, ys, '-', color=colors_paths[i], 
                            linewidth=3, label=f'{distance}m safe zone',
                            alpha=1.0, zorder=5)
        
        # Plot hiking trail with outline effect
        hiking_trail = hiking_gdf.plot(ax=ax, color='red', linewidth=2.5, zorder=4)
        ax.plot([], [], color='red', linewidth=2.5, label='Hiking Path')
        plt.setp(hiking_trail, path_effects=[withStroke(linewidth=4, foreground='gray')])
        
        # Plot summit
        summit_x, summit_y = raster_coord_to_map_coords(
            summit_coords[ds_key][0], summit_coords[ds_key][1], transform
        )
        ax.plot(summit_x, summit_y, '*', color='yellow', markersize=15, label='Summit', zorder=6)
        
        # Add distance contours
        x = np.linspace(transform[2], transform[2] + transform[0] * cost_array.shape[1], cost_array.shape[1])
        y = np.linspace(transform[5] + transform[4] * cost_array.shape[0], transform[5], cost_array.shape[0])
        X, Y = np.meshgrid(x, y)
        distances = np.sqrt((X - summit_x)**2 + (Y - summit_y)**2)
        
        contours = ax.contour(X, Y, distances, levels=safe_zone_distances,
                              colors='black', linestyles='--', alpha=0.4,
                              linewidths=1.5, zorder=3)
        ax.clabel(contours, inline=True, fmt='%1.0fm', fontsize=8)
        
        # Set plot limits
        ax.set_xlim(summit_x - 5000, summit_x + 5000)
        ax.set_ylim(summit_y - 5000, summit_y + 5000)
        
        # Add simple A/B labels
        ax.text(0.02, 0.98, f'{chr(65+idx)}',
                transform=ax.transAxes, fontsize=10, fontweight='bold',
                verticalalignment='top')
        
        # Add axis labels
        ax.set_xlabel('Easting (m)')
        ax.set_ylabel('Northing (m)')
    
    # Add legend
    handles, labels = ax1.get_legend_handles_labels()
    unique_labels = []
    unique_handles = []
    seen_labels = set()
    for handle, label in zip(handles, labels):
        if label not in seen_labels:
            seen_labels.add(label)
            unique_labels.append(label)
            unique_handles.append(handle)
    
    ax2.legend(unique_handles, unique_labels, 
               loc='center left',
               bbox_to_anchor=(1.0, 0.5))
    
    # Add horizontal colorbar
    cbar_ax = fig.add_subplot(gs[1, :])
    cbar = plt.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Accumulated Cost', labelpad=10)
    
    cbar.set_ticks(np.linspace(vmin, vmax, 6))
    cbar.set_ticklabels([f'{np.expm1(v):.1f}' for v in np.linspace(vmin, vmax, 6)])
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2)
    
    # Comment out the plt.show() call:
    plt.show()
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    end_time = time.time()
    print(f"Cost surface subplots created in {end_time - start_time:.2f} seconds")


def create_decomposition_table(decomp_data, output_path):
    """
    Create a visualization table showing the relative contributions of slope and landcover factors.
    
    This function takes decomposition analysis results and creates a formatted table
    showing the percentage contribution of slope and landcover factors to the
    evacuation path costs for different safe zone thresholds.
    
    Parameters:
    -----------
    decomp_data : list of dict
        A list of dictionaries, each containing decomposition results for a safe zone:
        {
            "Safe Zone Threshold (m)": int,
            "Slope Contribution (%)": float,
            "Landcover Contribution (%)": float
        }
    
    output_path : str
        File path where the table visualization will be saved as an image.
    
    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the decomposition data, useful for further analysis.
    
    Notes:
    ------
    - The function creates a visualization of the table using matplotlib.
    - The table has a formatted header row and is styled for readability.
    - The table is saved as an image at the specified output path.
    """
    df = pd.DataFrame(decomp_data)
    
    # Create a figure for the table
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')
    
    # Create the table from the DataFrame
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.4)
    
    # Optionally style header row
    for key, cell in table.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e6e6e6')
    
    plt.tight_layout()
    plt.show()
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return df


def create_final_evacuation_table(all_results, source_names, output_path):
    """
    Create a comprehensive evacuation time table for different sources and walking speeds.
    
    This function generates a formatted table visualization showing evacuation times
    for different combinations of safe zone distances, source locations, and walking speeds.
    The table uses a multi-level column organization for clear presentation.
    
    Parameters:
    -----------
    all_results : dict
        A nested dictionary containing travel time results:
        {dataset_key: {speed_name: {safe_zone_distance: [times_per_source]}}}
        The function uses only the 'final' dataset from this dictionary.
    
    source_names : list
        A list of source location names corresponding to indices in the results arrays.
        Must include 'summit', 'camp1', and 'camp2'.
    
    output_path : str
        File path where the table visualization will be saved as an image.
    
    Returns:
    --------
    pandas.DataFrame
        A DataFrame with multi-level columns containing the evacuation time data.
    
    Notes:
    ------
    - The function selects only specific safe zone distances: 500, 1500, 2500, 3500, 4500m.
    - The table uses a three-level header structure:
      1. "Safe Zone (m)" / "Evacuation Time (hours)"
      2. Source names (Summit, Camp1, Camp2)
      3. Walking speeds (Slow, Moderate, Fast)
    - NaN values are handled appropriately in the output.
    - The table is styled with a bold header row and saved as an image.
    """
    
    # We only want to display these safe zones and these sources/speeds
    safe_zones = [500, 1500, 2500, 3500, 4500]
    sources_to_show = ['summit', 'camp1']
    speeds = ['slow', 'medium', 'fast']
    
    # Prepare the table rows
    table_data = []
    for sz in safe_zones:
        # First column is the safe zone distance
        row = [sz]
        for src in sources_to_show:
            for spd in speeds:
                # Find the index of this source in source_names
                src_idx = source_names.index(src)
                # Get the travel time from all_results['final']
                val = all_results['final'][spd][sz][src_idx]
                if np.isnan(val):
                    row.append("Nan")
                else:
                    row.append(f"{val:.2f}")
        table_data.append(row)
    
    # We will have 1 column for safe zone + 3 sources × 3 speeds = 1 + 9 = 10 columns total.
    # Build multi-level columns:
    #  Top row: "Safe Zone (m)" repeated once, then "Evacuation Time (hours)" repeated 9 times
    #  Middle row: "", "Summit" × 3, "Camp1" × 3, "Camp2" × 3
    #  Bottom row: "", "Slow walking speed", "Moderate walking speed", "Fast walking speed" repeated 3 times
    
    arrays = [
        ["Safe Zone (m)"] + ["Evacuation Time (hours)"] * 9,
        [""]
        + ["Summit"]*3
        + ["Camp1"]*3,
        [""]
        + ["Slow walking speed", "Moderate walking speed", "Fast walking speed"]*3
    ]
    # Convert these into a MultiIndex
    tuples = list(zip(*arrays))  # Transpose
    columns = pd.MultiIndex.from_tuples(tuples)
    
    # Create a DataFrame
    df = pd.DataFrame(table_data, columns=columns)
    
    # Now plot the DataFrame as a matplotlib table
    fig, ax = plt.subplots(figsize=(12, 3))  # Wider figure for more columns
    ax.axis('off')
    
    # Convert df to a 2D list (cellText) plus colLabels
    # However, we have a MultiIndex. We'll create a table with two header rows:
    # an approach is to flatten the columns for colLabels, but let's do a quick approach:
    
    # We can manually set up the table by using the DataFrame's .values for cellText
    # and the multi-level columns as a header.
    # For a nicely formatted multi-level header in matplotlib, it's a bit tricky,
    # so a simpler approach is to just let DataFrame do the "pretty printing" into a single row.
    
    # Easiest is to do:
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns.to_flat_index(),  # Flatten the multiindex for a single row of headers
        cellLoc='center',
        loc='center'
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.4)
    
    # Optionally style the top row
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e6e6e6')
    
    # Show the table inline
    plt.tight_layout()
    plt.show()
    
    # Save the figure
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return df