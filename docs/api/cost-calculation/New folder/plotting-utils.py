# plotting_utils.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import numpy.ma as ma
import rasterio
from rasterio.plot import plotting_extent
from typing import Any
import geopandas as gpd
from matplotlib.colors import Normalize, ListedColormap, LinearSegmentedColormap
from matplotlib.colors import TwoSlopeNorm


def plot_continuous_raster_with_points(raster_data: np.ndarray, extent: Any, points_gdf: gpd.GeoDataFrame, title: str, colorbar_label: str, output_file_path: str) -> None:
    """
    Plots a continuous raster with overlaid points.

    Parameters:
    raster_data (np.ndarray): The raster data to be plotted.
    extent (Any): The extent of the raster data.
    points_gdf (gpd.GeoDataFrame): GeoDataFrame containing the points to be overlaid.
    title (str): The title of the plot.
    colorbar_label (str): The label for the colorbar.
    output_file_path (str): The file path where the plot will be saved.

    Returns:
    None
    """
    # A4 width is 210mm = 8.27 inches
    a4_width = 8.27
    
    # Create figure with two subplots in 1 row, 2 columns with A4 width
    # Add extra width to accommodate the colorbar
    fig, axes = plt.subplots(1, 2, figsize=(a4_width + 1.5, a4_width/2))
    
    # If we're plotting a single raster, simply use the first axis and hide the second
    if not isinstance(raster_data, list):
        # Display the raster on the first subplot
        cax = axes[0].imshow(raster_data, extent=extent, cmap='viridis', interpolation='none')
        axes[0].set_title(title, fontsize=10, fontweight='bold')
        axes[0].scatter(points_gdf.geometry.x, points_gdf.geometry.y, color="red", marker="^", s=50, label="Summit")
        axes[0].legend()
        
        # Hide the second subplot
        axes[1].axis('off')
        
        # Add colorbar
        cbar = fig.colorbar(cax, ax=axes[0], fraction=0.046, pad=0.04)
        cbar.set_label(colorbar_label)
    else:
        # For comparison plots with two rasters
        # Find common color scale if needed
        if len(raster_data) == 2:
            vmin = min(np.nanmin(raster_data[0]), np.nanmin(raster_data[1]))
            vmax = max(np.nanmax(raster_data[0]), np.nanmax(raster_data[1]))
            
            # If we have a list of titles, use them
            titles = title if isinstance(title, list) and len(title) == 2 else [f"{title} (1)", f"{title} (2)"]
            
            # Determine the global extent to use for both plots
            if isinstance(extent, list):
                # If different extents provided, find the union
                global_extent = [
                    min(extent[0][0], extent[1][0]),  # xmin
                    max(extent[0][1], extent[1][1]),  # xmax
                    min(extent[0][2], extent[1][2]),  # ymin
                    max(extent[0][3], extent[1][3])   # ymax
                ]
            else:
                # Use the same extent for both
                global_extent = extent
            
            # Plot first raster
            cax1 = axes[0].imshow(raster_data[0], extent=global_extent, 
                               cmap='viridis', interpolation='none', vmin=vmin, vmax=vmax)
            axes[0].set_title(titles[0], fontsize=12, fontweight='bold')
            pt_gdf = points_gdf if not isinstance(points_gdf, list) else points_gdf[0]
            axes[0].scatter(pt_gdf.geometry.x, pt_gdf.geometry.y, color="red", marker="^", s=50, label="Summit")
            axes[0].legend()
            
            # Plot second raster
            cax2 = axes[1].imshow(raster_data[1], extent=global_extent, 
                               cmap='viridis', interpolation='none', vmin=vmin, vmax=vmax)
            axes[1].set_title(titles[1], fontsize=12, fontweight='bold')
            pt_gdf = points_gdf if not isinstance(points_gdf, list) else points_gdf[1]
            axes[1].scatter(pt_gdf.geometry.x, pt_gdf.geometry.y, color="red", marker="^", s=50, label="Summit")
            axes[1].legend()
            
            # Add colorbar on the right side of the second subplot
            # Use specific positioning to ensure it's outside the plot
            cbar = fig.colorbar(cax2, ax=axes[1], pad=0.05)
            cbar.set_label(colorbar_label, fontsize=10)
            
            # Make sure both plots have the same aspect ratio
            for ax in axes:
                ax.set_aspect('equal')
                
                # Improve x-axis tick formatting
                ax.ticklabel_format(style='plain', axis='x')
                ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
                
                # Improve y-axis tick formatting
                ax.ticklabel_format(style='plain', axis='y')
                
                # Adjust tick label font size
                ax.tick_params(axis='both', labelsize=9)
                
                # Ensure there's enough space for tick labels
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Adjust spacing to make room for x-axis labels
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(output_file_path, format="jpg", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

def plot_normalized_walking_speed(raster_data: np.ndarray, extent: Any, points_gdf: gpd.GeoDataFrame, title: str, output_file_path: str) -> None:

       
    """
    Plots the normalized walking speed raster with summit points.
     Parameters:
        raster_data (np.ndarray): The raster data representing normalized walking speeds.
        extent (Any): The extent of the raster data in the format (xmin, xmax, ymin, ymax).
        points_gdf (gpd.GeoDataFrame): A GeoDataFrame containing the summit points to be plotted.
        title (str): The title of the plot.
        output_file_path (str): The file path where the plot will be saved.

        Returns:
        None
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import numpy.ma as ma

    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.viridis
    masked_raster_data = ma.masked_invalid(raster_data)
    cax = ax.imshow(masked_raster_data, extent=extent, cmap=cmap, interpolation='none')
    ax.set_facecolor("white")
    ax.set_title(title, fontsize=10, fontweight='bold')
    cbar = plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Speed Conservation Values of Slope")
    ax.scatter(points_gdf.geometry.x, points_gdf.geometry.y, color="red", marker="*", s=85, label="Summit", zorder=5)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(output_file_path, format="jpg", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

def plot_adjusted_cost_raster(adjusted_cost_raster, extent, points_gdf, title, output_file_path):

        
    """
    Plots the adjusted cost raster with summit points.
    Parameters:
        adjusted_cost_raster (numpy.ndarray): A 2D array representing the adjusted cost raster data.
        extent (list or tuple): The bounding box in the form [xmin, xmax, ymin, ymax] for the raster.
        points_gdf (geopandas.GeoDataFrame): A GeoDataFrame containing the summit points with geometry column.
        title (str): The title of the plot.
        output_file_path (str): The file path where the plot image will be saved.

        Returns:
        None
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    import numpy.ma as ma

    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.Blues
    masked_raster_data = ma.masked_invalid(adjusted_cost_raster)
    cax = ax.imshow(masked_raster_data, extent=extent, cmap=cmap, interpolation='none')
    ax.set_facecolor("white")
    ax.set_title(title, fontsize=10, fontweight='bold')
    cbar = plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Walking Speed (m/s)")
    ax.scatter(points_gdf.geometry.x, points_gdf.geometry.y, color="red", marker="*", s=85, label="Summit", zorder=5)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(output_file_path, format="jpg", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

def plot_inverted_cost_raster(inverted_cost_raster, extent, points_gdf, title, output_file_path):

     
    """
    Plots the inverted cost raster with summit points.
       Parameters:
        inverted_cost_raster (numpy.ndarray): 2D array representing the inverted cost raster.
        extent (list or tuple): The bounding box in data coordinates (left, right, bottom, top).
        points_gdf (geopandas.GeoDataFrame): GeoDataFrame containing the summit points with geometry column.
        title (str): Title of the plot.
        output_file_path (str): Path to save the output plot image.

        Returns:
        None
    """


    # Create masks
    mask_nan = np.isnan(inverted_cost_raster)
    mask_special = (inverted_cost_raster == 1e6)
    mask_continuous = (~mask_nan & ~mask_special)

    # Create masked arrays
    continuous_data = ma.masked_where(~mask_continuous, inverted_cost_raster)
    special_data = ma.masked_where(~mask_special, inverted_cost_raster)

    # Determine normalization range
    clean_data = continuous_data[~mask_nan & ~mask_special]
    vmin, vmax = np.percentile(clean_data, [2, 98])

    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.imshow(continuous_data, extent=extent, cmap='Blues', norm=Normalize(vmin=vmin, vmax=vmax))
    ax.imshow(special_data, extent=extent, cmap=ListedColormap(['blue', 'none']), alpha=0.7)
    ax.set_facecolor("white")
    ax.set_title(title, fontsize=16, fontweight='bold')
    cbar = plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Cost (excluding 1e6)', fontsize=12)
    ax.scatter(points_gdf.geometry.x, points_gdf.geometry.y, color="red", marker="*", s=85, label="Summit", zorder=5)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(output_file_path, format="jpg", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)





def plot_walking_speed_vs_slope(slope_array, walking_speed_array, directions, output_file_path):
    """
    Plots the walking speed versus slope for all eight directions in a subplot layout.

    Parameters:
    slope_array (numpy.ndarray): A 3D array representing slope values for eight directions.
                                  The first dimension represents directions: North, South, East, West,
                                  North-East, North-West, South-East, South-West.
    walking_speed_array (numpy.ndarray): A 3D array representing walking speed values for eight directions.
                                         The first dimension represents directions: North, South, East, West,
                                         North-East, North-West, South-East, South-West.
    directions (list): A list of direction labels.
    output_file_path (str): The file path where the combined plot will be saved.

    Returns:
    None
    """
    fig, axes = plt.subplots(4, 2, figsize=(15, 20))
    fig.suptitle("Walking Speed vs Slope for All 8 Directions", fontsize=16)

    for direction in range(8):
        # Flatten the slope and walking speed arrays for the current direction
        slope_values = slope_array[direction].flatten()
        walking_speed_values = walking_speed_array[direction].flatten()

        # Filter out NaN values from both slope and walking speed arrays
        valid_mask = ~np.isnan(slope_values) & ~np.isnan(walking_speed_values)
        slope_values = slope_values[valid_mask]
        walking_speed_values = walking_speed_values[valid_mask]

        # Get the corresponding axis for the current direction
        ax = axes[direction // 2, direction % 2]
        
        # Create a scatter plot of walking speed vs. slope
        ax.scatter(slope_values, walking_speed_values, alpha=0.5, s=1)
        ax.set_title(f"{directions[direction]} Direction")
        ax.set_xlabel("Slope")
        ax.set_ylabel("Walking Speed (m/s)")

    # Adjust layout to prevent overlapping
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_file_path, dpi=300)
    plt.show()
    plt.close(fig)

def plot_north_east_speed_conservation(normalized_walking_speed_array, extent, points_gdf, title, output_file_path):
    """
    Plots the normalized walking speed raster for North and East directions in a subplot.
    
    Parameters:
        normalized_walking_speed_array (np.ndarray): The 3D array of normalized walking speeds where
                                                    first dimension represents directions 
                                                    (North: 0, East: 2)
        extent (Any): The extent of the raster data in the format (xmin, xmax, ymin, ymax).
        points_gdf (gpd.GeoDataFrame): A GeoDataFrame containing the summit points to be plotted.
        title (str): The main title of the plot.
        output_file_path (str): The file path where the plot will be saved.
        
    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import numpy.ma as ma
    
    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    # Direction labels
    directions = ['North', 'East']
    indices = [0, 2]  # North is at index 0, East is at index 2 in the array
    
    # Create a common color scale for both plots
    vmin = np.nanmin([normalized_walking_speed_array[0], normalized_walking_speed_array[2]])
    vmax = np.nanmax([normalized_walking_speed_array[0], normalized_walking_speed_array[2]])
    cmap = plt.cm.viridis
    
    # Loop through the two directions
    for i, (ax, direction, idx) in enumerate(zip(axes, directions, indices)):
        # Get the data for this direction
        raster_data = normalized_walking_speed_array[idx]
        
        # Mask invalid data
        masked_raster_data = ma.masked_invalid(raster_data)
        
        # Plot the data
        cax = ax.imshow(masked_raster_data, extent=extent, cmap=cmap, 
                        interpolation='none', vmin=vmin, vmax=vmax)
        
        # Set background color for NaN values
        ax.set_facecolor("white")
        
        # Add title for this subplot
        ax.set_title(f"{direction} Direction", fontsize=12, fontweight='bold')
        
        # Add summit points
        ax.scatter(points_gdf.geometry.x, points_gdf.geometry.y, 
                  color="red", marker="*", s=85, label="Summit", zorder=5)
        
        # Add legend
        ax.legend(loc='upper right')
    
    # Add a colorbar that applies to both subplots
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
    cbar = plt.colorbar(cax, cax=cbar_ax)
    cbar.set_label("Speed Conservation Values of Slope")
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])  # Adjust layout to give space for colorbar
    
    # Save the figure
    plt.savefig(output_file_path, format="jpg", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)
