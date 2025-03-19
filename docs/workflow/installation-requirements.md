# Installation Requirements

This page details all the required libraries and dependencies needed to run the Volcano Pedestrian Evacuation Analysis toolkit. Install these packages before proceeding with the analysis workflow.

## Environment Setup

We recommend using a virtual environment to manage dependencies. You can create one using either conda or venv:

=== "Using conda"
    ```bash
    conda create -n volcano-evacuation python=3.8
    conda activate volcano-evacuation
    ```

=== "Using venv"
    ```bash
    python -m venv volcano-env
    # On Windows
    volcano-env\Scripts\activate
    # On macOS/Linux
    source volcano-env/bin/activate
    ```

## Core Dependencies

These core packages are essential for the basic functionality of the toolkit:

```bash
pip install numpy scipy pandas matplotlib tqdm
```

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | >=1.20.0 | Array processing and numerical operations |
| scipy | >=1.7.0 | Sparse matrices and graph algorithms for path finding |
| pandas | >=1.3.0 | Data analysis and statistical summaries |
| matplotlib | >=3.4.0 | Visualization of results and map creation |
| tqdm | >=4.60.0 | Progress tracking for long-running operations |

## Geospatial Processing Libraries

These libraries handle the geospatial data processing and analysis:

```bash
pip install rasterio geopandas pyproj fiona affine
```

| Package | Version | Purpose |
|---------|---------|---------|
| rasterio | >=1.2.0 | Reading and writing raster data (DEM, land cover) |
| geopandas | >=0.9.0 | Working with vector data (points, paths, polygons) |
| pyproj | >=3.1.0 | Coordinate system transformations and UTM projections |
| fiona | >=1.8.0 | Low-level vector data I/O operations |
| affine | >=2.3.0 | Working with affine transformations in raster data |

## Google Earth Engine Integration

For remote sensing data acquisition from Google Earth Engine:

```bash
pip install earthengine-api
```

You'll need to authenticate with Google Earth Engine. The data acquisition notebook will guide you through this process, or you can run:

```bash
earthengine authenticate
```

## Visualization Enhancements (Optional)

For enhanced visualization capabilities:

```bash
pip install contextily folium seaborn
```

| Package | Purpose |
|---------|---------|
| contextily | Adding basemaps to matplotlib/geopandas maps |
| folium | Creating interactive maps with evacuation routes |
| seaborn | Enhanced statistical visualizations |

## Complete Installation

For a complete installation of all required dependencies, you can use the requirements file:

```bash
pip install -r requirements.txt
```

Create a `requirements.txt` file in your project root with the following content:

```
# Core Scientific Computing
numpy>=1.20.0
scipy>=1.7.0
pandas>=1.3.0
matplotlib>=3.4.0
tqdm>=4.60.0

# Geospatial Libraries
rasterio>=1.2.0
geopandas>=0.9.0
pyproj>=3.1.0
fiona>=1.8.0
affine>=2.3.0

# Remote Sensing
earthengine-api>=0.1.290

# Optional Visualization
contextily>=1.2.0
folium>=0.12.0
seaborn>=0.11.0
```

## Testing Your Installation

You can test your installation by running the following Python script:

```python
# test_installation.py
import sys
import importlib

required_packages = [
    'numpy', 'scipy', 'pandas', 'matplotlib', 'tqdm',
    'rasterio', 'geopandas', 'pyproj', 'fiona', 'affine', 
    'ee'
]

for package in required_packages:
    try:
        importlib.import_module(package)
        print(f"✓ {package} successfully imported")
    except ImportError:
        print(f"✗ {package} MISSING")
        
print("\nIf any packages are missing, install them using pip:")
print("pip install <package_name>")
```

Save this as `test_installation.py` and run it with:

```bash
python test_installation.py
```

## Troubleshooting Common Issues

### GDAL-Related Errors

If you encounter issues with GDAL (which underlies rasterio and fiona), try installing it separately:

=== "Using conda"
    ```bash
    conda install -c conda-forge gdal
    ```

=== "Using pip"
    ```bash
    # On Windows
    pip install pipwin
    pipwin install gdal
    
    # On Ubuntu/Debian
    sudo apt-get install libgdal-dev
    pip install gdal==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
    ```

### Google Earth Engine Authentication Issues

If you encounter issues authenticating with Google Earth Engine:

1. Ensure you have a Google account with access to Earth Engine
2. Try re-authenticating: `earthengine authenticate --quiet`
3. Check if your authentication credentials are stored properly:
   ```bash
   # On Linux/macOS
   cat ~/.config/earthengine/credentials
   # On Windows
   type %USERPROFILE%\.config\earthengine\credentials
   ```

## Next Steps

Once you have successfully installed all the required dependencies, proceed to the [Data Acquisition](data-acquisition.md) step to begin downloading the necessary data for your analysis.
