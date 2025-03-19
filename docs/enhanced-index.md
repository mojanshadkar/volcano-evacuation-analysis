# Volcano Pedestrian Evacuation Analysis

## Project Overview

This project provides a comprehensive toolkit for analyzing and visualizing pedestrian evacuation scenarios from active volcanoes. The analysis pipeline combines terrain characteristics, land cover data, and evacuation modeling to support emergency planning and risk reduction.

![Evacuation Analysis](assets/images/evacuation_example.jpg)

## Complete Analysis Workflow

Our toolkit implements a full evacuation analysis workflow:

1. **Data Acquisition** - Download high-resolution DEM (Digital Elevation Model) and land cover data using Google Earth Engine
2. **Cost Surface Generation** - Create anisotropic cost surfaces based on Tobler's hiking function and land cover characteristics
3. **Evacuation Analysis** - Calculate optimal evacuation routes and travel times from critical locations
4. **Probability Analysis** - Incorporate eruption probability thresholds for different VEI (Volcanic Explosivity Index) scenarios

## Key Features

- **Advanced Terrain Analysis**
  - Slope calculation in 8 cardinal and intercardinal directions
  - Implementation of Tobler's hiking function for realistic walking speeds
  - Integration of land cover data to account for terrain traversability

- **Sophisticated Path Finding**
  - Dijkstra's algorithm for optimal route determination
  - Multi-directional path analysis considering anisotropic movement
  - Evacuation time calculations for different population mobility scenarios (slow, medium, fast walking speeds)

- **Comprehensive Visualization**
  - Interactive maps of evacuation routes and travel times
  - Statistical analysis of evacuation feasibility
  - Visual comparison of different evacuation scenarios

- **Eruption Probability Integration**
  - Safe zone definition based on probabilistic hazard thresholds
  - Scenario analysis for different volcanic eruption intensities
  - Comparison of evacuation strategies across multiple VEI levels

## Case Studies: Mount Marapi and Mount Awu

The toolkit has been applied to Mount Marapi (Sumatra) and Mount Awu (Sangihe Islands) in Indonesia, demonstrating its effectiveness in diverse volcanic settings. These case studies provide:

- Realistic evacuation time estimates from summit and camping areas
- Identification of optimal evacuation routes based on terrain characteristics
- Assessment of safe zone accessibility for different population groups
- Scenario comparisons for various eruption intensities

## Modular Architecture

The toolkit is organized into three main module groups:

- **[Cost Calculation](modules/cost-calculations.md)**: Functions for generating cost surfaces from geographical data
- **[Evacuation Analysis](modules/evacuation-analysis.md)**: Tools for path finding and evacuation time analysis
- **[Probability Analysis](modules/probability-analysis.md)**: Methods for incorporating eruption probability thresholds

Each module is thoroughly documented with detailed API references and usage examples.

## Getting Started

To begin using the toolkit for your own volcano evacuation analysis:

1. Check the [Installation Requirements](workflow/installation-requirements.md) to set up your environment
2. Follow the [Workflow Guide](workflow/overview.md) for step-by-step instructions
3. Explore the [Demo Notebooks](demo/data-download.ipynb) for practical examples

For technical details, see the [API Reference](api/index.md) with full documentation of all functions and modules.
