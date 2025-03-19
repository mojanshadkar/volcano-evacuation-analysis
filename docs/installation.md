# Installation Guide

This guide explains how to set up your environment for using the Volcano Pedestrian Evacuation Analysis toolkit.

## Prerequisites

Before installing the toolkit, ensure you have:

- **Python 3.8+** installed on your system
- **pip** (Python package installer) or **conda** for managing packages
- Basic familiarity with command-line operations

## Environment Setup

We recommend creating a dedicated virtual environment to manage dependencies cleanly:

=== "Using conda"
    ```bash
    # Create a new conda environment
    conda create -n volcano-evacuation python=3.8
    
    # Activate the environment
    conda activate volcano-evacuation
    ```

=== "Using venv"
    ```bash
    # Create a new virtual environment
    python -m venv volcano-env
    
    # Activate the environment (Windows)
    volcano-env\Scripts\activate
    
    # Activate the environment (macOS/Linux)
    source volcano-env/bin/activate
    ```

## Installing Required Packages




### Step-by-Step Installation


#### 1. Core Scientific Computing

These packages provide essential numerical and data processing capabilities:

```bash
pip install numpy scipy pandas matplotlib tqdm
```

#### 2. Geospatial Processing 

These libraries enable handling of geographic data formats and analysis:

```bash
pip install rasterio geopandas pyproj fiona affine
```

#### 3. Google Earth Engine Integration

For accessing remote sensing data (required for the Data Acquisition module):

```bash
pip install earthengine-api

# Authenticate with Earth Engine
earthengine authenticate
```

## Package Overview

| Category | Package | Purpose |
|----------|---------|---------|
| **Core Computing** | numpy | Efficient array operations and numerical computations |
| | scipy | Scientific algorithms including sparse matrix operations |
| | pandas | Data analysis and manipulation |
| | matplotlib | Data visualization and plotting |
| | tqdm | Progress bars for long-running operations |
| **Geospatial** | rasterio | Reading, writing and processing raster data |
| | geopandas | Working with vector geospatial data |
| | pyproj | Coordinate system transformations |
| | fiona | Low-level interface to vector data formats |
| | affine | Working with affine transformations |
| **Remote Sensing** | earthengine-api | Access to Google Earth Engine datasets |

## Verifying Your Installation

Run the following script to verify that all required packages are installed correctly:

```python
# check_installation.py
import sys

required_packages = [
    "numpy", "scipy", "pandas", "matplotlib", "tqdm",
    "rasterio", "geopandas", "pyproj", "fiona", "affine",
    "ee"  # Google Earth Engine API
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package}")
    except ImportError:
        missing.append(package)
        print(f"✗ {package} (MISSING)")

if missing:
    print("\nMissing packages. Install them with:")
    print(f"pip install {' '.join(missing)}")
else:
    print("\nAll required packages are installed!")
```

## Troubleshooting

### GDAL/Rasterio Installation Issues

If you encounter problems installing rasterio or other GDAL-based packages:

=== "Windows"
    ```bash
    # Use pipwin to install pre-compiled binaries
    pip install pipwin
    pipwin install gdal
    pipwin install rasterio
    pipwin install fiona
    ```

=== "Linux (Ubuntu/Debian)"
    ```bash
    # Install system dependencies first
    sudo apt-get update
    sudo apt-get install libgdal-dev gdal-bin
    
    # Then install Python packages
    pip install gdal==$(gdal-config --version) --no-binary=gdal
    pip install rasterio fiona
    ```

=== "macOS"
    ```bash
    # Using Homebrew
    brew install gdal
    
    # Then install Python packages
    pip install gdal rasterio fiona
    ```

### Google Earth Engine Authentication

If you encounter issues authenticating with Google Earth Engine:

1. Ensure you have [signed up](https://earthengine.google.com/signup/) for Earth Engine access
2. Try re-running the authentication: `earthengine authenticate --quiet`
3. If browser authentication doesn't work, try the manual authentication option

## Next Steps

Once you've completed the installation:

1. Proceed to the [Data Acquisition](../workflow/data-acquisition.md) section to download required datasets
2. Or explore the [Demo Notebooks](../demo/data-download.ipynb) for examples of the toolkit in action
