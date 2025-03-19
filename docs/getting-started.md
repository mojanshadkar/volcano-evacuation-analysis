# Getting Started

Welcome to the Volcano Pedestrian Evacuation Analysis toolkit! This guide will help you get started with setting up and running volcanic evacuation analyses.

## Introduction

This toolkit provides a comprehensive set of tools for analyzing pedestrian evacuation scenarios from active volcanoes. It allows you to:

- Download topographic and land cover data for volcanic regions
- Generate cost surfaces that model the difficulty of traversing different terrain types
- Calculate optimal evacuation routes and evacuation times
- Analyze evacuation scenarios based on probability thresholds for different eruption intensities
- Visualize results with informative maps and charts

## System Requirements

- **Python 3.8+**
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 8GB minimum, 16GB recommended for larger study areas
- **Storage**: At least 10GB free space for data and results
- **Internet Connection**: Required for initial data download from Google Earth Engine

## Quick Start

Follow these steps to get started with the toolkit:

1. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Google Earth Engine Account**:
   - Visit [Google Earth Engine](https://earthengine.google.com/) and sign up for an account
   - Follow the authentication instructions in the Data Acquisition workflow

3. **Download Sample Data**:
   - Run the data download notebook to acquire DEM and land cover data for your volcano of interest
   - Alternatively, use the pre-processed sample data provided in the repository

4. **Generate Cost Surface**:
   - Run the cost surface generation workflow to create traversal cost layers
   - Examine the output to ensure it accurately represents the terrain conditions

5. **Perform Evacuation Analysis**:
   - Execute the evacuation analysis to identify optimal routes and calculate evacuation times
   - Review the visualization outputs to understand evacuation scenarios

## Workflow Overview

The toolkit follows a modular workflow:

1. **[Data Acquisition](workflow/data-acquisition.md)**: Download DEM and land cover data
2. **[Cost Surface Generation](workflow/cost-surface.md)**: Create terrain-based traversal cost surfaces
3. **[Evacuation Analysis](workflow/evacuation-analysis.md)**: Calculate evacuation routes and times

Each module can be run independently with the outputs from the previous step, allowing for flexible workflow management and iterative analysis.

## Limitations

- The analysis is focused on pedestrian evacuation (not vehicular)
- Travel speeds are based on Tobler's hiking function and land cover-based assumptions
- The model does not account for potential infrastructure damage during eruptions
- Evacuation behavior (such as panic or group dynamics) is not modeled

## Getting Help

If you encounter any issues or have questions:

1. Check the detailed documentation for each module
2. Review example notebooks in the demo directory
3. Submit an issue on our GitHub repository

## Next Steps

To begin your evacuation analysis project, proceed to the [Workflow Overview](workflow/workflow-overview.md) section for a detailed description of each step in the process.
