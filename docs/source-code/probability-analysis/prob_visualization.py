"""
Modified plotting and visualization functions for the volcanic evacuation analysis.
Handles multiple VEI levels and creates separate contour maps.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.patheffects import withStroke
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import CRS, Transformer
import contextily as ctx
from shapely.geometry import box
import geopandas as gpd

from raster_utils import raster_coord_to_map_coords
from data_utils import load_raster, read_shapefile


def plot_travel_time_comparison(all_results, source_names, thresholds, walking_speeds, output_dir, filename="comparison_travel_time_by_source.png"):
    """
    Plot a comparison of travel times between datasets.
    
    Args:
        all_results (dict): Dictionary of results from all datasets
        source_names (list): List of source names
        thresholds (list): List of probability thresholds
        walking_speeds (dict): Dictionary of walking speeds
        output_dir (str): Directory to save the plot
        filename (str): Filename for the plot
        
    Returns:
        str: Path to the saved plot
    """
    dataset_styles = {
        'final': {'label': 'Original', 'linestyle': '-', 'alpha': 0.9},
        'modify_landcover': {'label': 'Penalized', 'linestyle': '--', 'alpha': 0.9}
    }
    
    speed_markers = {'slow': 'o', 'medium': 's', 'fast': '^'}
    speed_colors = {'slow': 'red', 'medium': 'blue', 'fast': 'green'}
    
    # Create figure with one row, two columns
    n_sources = min(len(source_names), 2)  # Limit to first two sources
    fig, axes = plt.subplots(1, n_sources, figsize=(16, 6), sharey=True)
    
    # Handle case of single subplot
    if n_sources == 1:
        axes = [axes]
    
    # Store lines and labels for legend
    lines = []
    labels = []
    first_plot = True
    
    # Plot for each source
    for src_idx, source_name in enumerate(source_names[:n_sources]):
        ax = axes[src_idx]
        
        # Plot all walking speeds for both original and modified landcover
        for speed_name, speed_color in speed_colors.items():
            # Get data for both datasets
            original_times = [all_results['final'][speed_name][thresh][src_idx] for thresh in thresholds]
            modified_times = [all_results['modify_landcover'][speed_name][thresh][src_idx] for thresh in thresholds]
            
            # Plot with consistent line styles
            line1 = ax.plot(thresholds, original_times, '-', color=speed_color)
            line2 = ax.plot(thresholds, modified_times, '--', color=speed_color)
            
            # Store legend entries only once
            if first_plot:
                lines.extend([line1[0], line2[0]])
                labels.extend([f'{speed_name.capitalize()} - Original', 
                             f'{speed_name.capitalize()} - Penalized'])
        
        # Add label in the top left corner
        ax.text(0.05, 0.95, chr(65 + src_idx), transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top')
        
        # Invert the x-axis to show high probabilities first
        ax.invert_xaxis()
        
        ax.set_xlabel("Eruption Probability Threshold", fontsize=10)
        if src_idx == 0:  # Add ylabel only for leftmost plot
            ax.set_ylabel("Minimum Travel Time (hrs)", fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Set y-axis to go from 0 to 2.5
        ax.set_ylim(bottom=0, top=2.5)
        
        first_plot = False
    
    # Add legend to the right of the second subplot
    fig.legend(lines, labels, fontsize=9, loc='center left', 
              bbox_to_anchor=(1.02, 0.5))
    
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show() 
    plt.close()
    return output_path


def plot_cost_surface_with_paths(dataset_info, evacuation_paths, eruption_probability_path, 
                                  hiking_path, selected_speed, thresholds, output_dir, vei_label="VEI4"):
    """
    Plot cost surface with evacuation paths.
    
    Args:
        dataset_info (dict): Dictionary of dataset information
        evacuation_paths (dict): Dictionary of evacuation paths
        eruption_probability_path (str): Path to the eruption probability raster
        hiking_path (str): Path to the hiking path shapefile
        selected_speed (str): Selected walking speed
        thresholds (list): List of probability thresholds
        output_dir (str): Directory to save the plot
        vei_label (str): VEI label for the title
        
    Returns:
        str: Path to the saved plot
    """
    print(f"\nCreating cost surface subplots with evacuation paths for {vei_label}...")
    
    # Set up colors for each probability threshold
    threshold_colors = ['lime', 'cyan', 'yellow', 'silver', 'pink', 'orange']
    
    # Load hiking trail shapefile
    hiking_gdf = read_shapefile(hiking_path)
    
    # Load cost rasters for visualization
    cost_arrays = []
    transforms = []
    for ds_key in dataset_info.keys():
        cost_raster_path = os.path.join(output_dir, f'cost_distance_summit_{ds_key}_{selected_speed}_hours.tif')
        cost_array, cost_meta = load_raster(cost_raster_path)
        cost_arrays.append(cost_array)
        transforms.append(cost_meta['transform'])
    
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
    
    # Add title for the overall figure
    fig.suptitle(f'Contour Map Showing Summit Location and Hiking Trail for {vei_label}', fontsize=12)
    
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
        for i, thresh in enumerate(thresholds):
            if thresh in evacuation_paths[ds_key]:
                path = evacuation_paths[ds_key][thresh]
                if path:
                    path_coords = [raster_coord_to_map_coords(row, col, transform) for row, col in path]
                    xs, ys = zip(*path_coords)
                    ax.plot(xs, ys, '-', color=threshold_colors[i % len(threshold_colors)], 
                            linewidth=3, label=f'Prob ≤ {thresh}',
                            alpha=1.0, zorder=5)
        
        # Plot hiking trail with outline effect
        hiking_trail = hiking_gdf.plot(ax=ax, color='red', linewidth=2.5, zorder=4)
        ax.plot([], [], color='red', linewidth=2.5, label='Hiking Path')
        plt.setp(hiking_trail, path_effects=[withStroke(linewidth=4, foreground='gray')])
        
        # Plot summit
        summit_rc = dataset_info[ds_key]["summit_raster_coords"]
        summit_x, summit_y = raster_coord_to_map_coords(
            summit_rc[0], summit_rc[1], transform
        )
        ax.plot(summit_x, summit_y, '*', color='blue', markersize=15, label='Summit', zorder=6)
        
        # Add probability contours
        x = np.linspace(transform[2], transform[2] + transform[0] * cost_array.shape[1], cost_array.shape[1])
        y = np.linspace(transform[5] + transform[4] * cost_array.shape[0], transform[5], cost_array.shape[0])
        X, Y = np.meshgrid(x, y)
        
        # Load eruption probability raster
        with rasterio.open(eruption_probability_path) as src:
            prob_array = src.read(1)
            prob_transform = src.transform
        
        # Ensure probability array matches cost array dimensions
        if prob_array.shape != cost_array.shape:
            print(f"Reshaping probability array for {vei_label} to match cost array dimensions...")
            new_prob_array = np.empty(cost_array.shape, dtype=np.float32)
            reproject(
                source=prob_array,
                destination=new_prob_array,
                src_transform=prob_transform,
                dst_transform=transform,
                src_crs=CRS.from_epsg(32751),
                dst_crs=CRS.from_epsg(32751),
                resampling=Resampling.bilinear
            )
            prob_array = new_prob_array
        
        # Define contour levels in ASCENDING order (critical)
        contour_levels = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]  # Sorted in ascending order
        
        # Create contours for probability thresholds
        contours = ax.contour(X, Y, prob_array, levels=contour_levels,
                            colors='black', linestyles='--', alpha=0.7,
                            linewidths=1.5, zorder=3)
        ax.clabel(contours, inline=True, fmt='%1.2f', fontsize=8)
        
        # Set plot limits based on summit location (adjust as needed for different VEI levels)
        # For VEI3, use a smaller radius, for VEI5 use a larger radius
        if vei_label == 'VEI3':
            radius = 3500
        elif vei_label == 'VEI5':
            radius = 7000
        else:  # VEI4 default
            radius = 5000
            
        ax.set_xlim(summit_x - radius, summit_x + radius)
        ax.set_ylim(summit_y - radius, summit_y + radius)
        
        # Add legend with blue Summit star and red Hiking Path
        ax.legend(loc='upper right', fontsize=8)
        
        # Add axis labels
        ax.set_xlabel('Easting (m)')
        ax.set_ylabel('Northing (m)')
    
    # Add horizontal colorbar
    cbar_ax = fig.add_subplot(gs[1, :])
    cbar = plt.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Accumulated Cost', labelpad=10)
    
    cbar.set_ticks(np.linspace(vmin, vmax, 6))
    cbar.set_ticklabels([f'{np.expm1(v):.1f}' for v in np.linspace(vmin, vmax, 6)])
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2, top=0.92)  # Make room for suptitle
    
    # Save the plot
    output_path = os.path.join(output_dir, f'contour_map_showing_summit_location_and_hiking_trail_for_{vei_label}.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show() 
    plt.close()
    print(f"Cost surface visualization with evacuation paths for {vei_label} saved to: {output_path}")
    return output_path


def create_vei_comparison_plot(eruption_probability_paths, hiking_path, summit_path, output_dir):
    """
    Create a comparison plot of contour maps for different VEI levels side by side.
    
    Args:
        eruption_probability_paths (dict): Dictionary of VEI levels and their file paths
        hiking_path (str): Path to the hiking path shapefile
        summit_path (str): Path to the summit point shapefile
        output_dir (str): Directory to save the plot
        
    Returns:
        str: Path to the saved plot
    """
    print("\nCreating VEI comparison plot...")
    
    # Load hiking trail shapefile
    hiking_gdf = read_shapefile(hiking_path)
    
    # Load summit points
    summit_gdf = read_shapefile(summit_path)
    
    # Create figure with subplots for each VEI level
    fig, axes = plt.subplots(1, len(eruption_probability_paths), figsize=(18, 6), sharey=True)
    
    # If only one VEI level, convert axes to list
    if len(eruption_probability_paths) == 1:
        axes = [axes]
    
    # Define eruption probability thresholds - CRITICAL: Must be in ASCENDING order for matplotlib contour
    thresholds = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]
    
    # Process each VEI level
    for i, (vei, path) in enumerate(eruption_probability_paths.items()):
        ax = axes[i]
        
        # Load eruption probability raster
        with rasterio.open(path) as src:
            prob_array = src.read(1)
            transform = src.transform
            bounds = src.bounds
            
            # Get CRS information for the raster
            raster_crs = src.crs
            
            # Create coordinate grid
            x = np.linspace(bounds.left, bounds.right, prob_array.shape[1])
            y = np.linspace(bounds.bottom, bounds.top, prob_array.shape[0])
            X, Y = np.meshgrid(x, y)
            
            # Get summit coordinates
            summit_x = summit_gdf.geometry.x.values[0]
            summit_y = summit_gdf.geometry.y.values[0]
            
            # Set radius based on VEI level
            if vei == 'VEI3':
                radius = 3500
            elif vei == 'VEI5':
                radius = 7000
            else:  # VEI4 default
                radius = 5000
            
            # Create a bounding box for the area around the summit
            bbox = box(summit_x - radius, summit_y - radius, 
                      summit_x + radius, summit_y + radius)
            
            # Create a GeoDataFrame from the bounding box
            bbox_gdf = gpd.GeoDataFrame({'geometry': [bbox]}, crs=raster_crs)
            
            # Create a light blue background for the map
            ax.imshow(np.ones(prob_array.shape), 
                     extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
                     cmap='Blues', alpha=0.1, vmin=0, vmax=1)
            
            # Plot the OpenStreetMap tiles (wrapped in try/except in case of connection issues)
            try:
                ctx.add_basemap(ax, crs=raster_crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
                print(f"Successfully added OpenStreetMap background for {vei}")
            except Exception as e:
                print(f"Warning: Could not add OpenStreetMap basemap for {vei}. Error: {e}")
                # Continue without the basemap
            
            # Create contours for probability thresholds (already in ascending order)
            contours = ax.contour(X, Y, prob_array, levels=thresholds,
                                colors='black', linestyles='--', alpha=0.7,
                                linewidths=1.0)
            ax.clabel(contours, inline=True, fmt='%1.2f', fontsize=8)
            
            # Plot hiking trail
            hiking_trail = hiking_gdf.plot(ax=ax, color='red', linewidth=2.0)
            
            # Plot summit
            ax.plot(summit_x, summit_y, '*', color='blue', markersize=12)
            
            # Set title
            ax.set_title(f'Contour Map Showing Summit Location and Hiking Trail for {vei}', fontsize=10)
            
            # Set plot limits
            ax.set_xlim(summit_x - radius, summit_x + radius)
            ax.set_ylim(summit_y - radius, summit_y + radius)
            
            # Add axis labels
            ax.set_xlabel('Easting (m)')
            if i == 0:  # Only add y-label for the first subplot
                ax.set_ylabel('Northing (m)')
            
            # Add legend
            ax.plot([], [], '*', color='blue', markersize=12, label='Summit')
            ax.plot([], [], '-', color='red', linewidth=2.0, label='Hiking Path')
            ax.legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'vei_comparison_contour_maps.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"VEI comparison plot saved to: {output_path}")
    return output_path