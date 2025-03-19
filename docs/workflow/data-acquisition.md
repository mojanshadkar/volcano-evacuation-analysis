# Data Acquisition

This page explains how to acquire the necessary geospatial data for volcanic evacuation analysis. The primary datasets needed are Digital Elevation Models (DEMs) and land cover classification data for the volcanic region of interest.

## Overview

The data acquisition workflow leverages Google Earth Engine to download high-quality, consistent datasets for any volcano worldwide. The process:

1. Defines a study area around the volcano
2. Downloads elevation data from the ALOS World 3D-30m dataset
3. Downloads land cover classification from Copernicus Global Land Cover
4. Exports the data in appropriate projection for accurate analysis

## Required Datasets

| Dataset | Description | Source | Resolution |
|---------|-------------|--------|------------|
| Digital Elevation Model (DEM) | Elevation data for calculating slopes and terrain characteristics | JAXA ALOS World 3D-30m | 30m |
| Land Cover Classification | Categorizes terrain into different surface types (forest, urban, etc.) | Copernicus Global Land Cover | 100m |

## Prerequisites

Before proceeding, ensure you have:

1. Installed the required dependencies as specified in the [Installation Requirements](installation-requirements.md)
2. Signed up for a Google Earth Engine account at [https://earthengine.google.com/](https://earthengine.google.com/)
3. Authenticated with Google Earth Engine using the `earthengine-api` package

## Google Earth Engine Authentication

When running the data acquisition workflow for the first time, you'll need to authenticate with Google Earth Engine:

```python
import ee

# Try to initialize Earth Engine
try:
    ee.Initialize()
    print("Already authenticated with Google Earth Engine")
except:
    # If initialization fails, authenticate first
    ee.Authenticate()
    ee.Initialize()
    print("Authentication successful")
```

The authentication process will open a browser window where you'll need to sign in with your Google account and authorize the Earth Engine application.

## Automatic UTM Projection Selection

For accurate distance measurements, the data is exported in the appropriate Universal Transverse Mercator (UTM) projection for the volcano's location. The workflow automatically determines the correct UTM zone based on the volcano's coordinates:

```python
def get_utm_epsg(latitude, longitude):
    """
    Determine the EPSG code for the UTM zone appropriate for the given coordinates.
    
    Args:
        latitude (float): Latitude in decimal degrees
        longitude (float): Longitude in decimal degrees
        
    Returns:
        str: EPSG code in the format "EPSG:xxxxx"
    """
    # Make sure longitude is between -180 and 180
    longitude = ((longitude + 180) % 360) - 180
    
    # Calculate UTM zone number
    zone_number = int(((longitude + 180) / 6) + 1)
    
    # Determine EPSG code
    if latitude >= 0:
        # Northern hemisphere
        epsg = f"EPSG:326{zone_number:02d}"
    else:
        # Southern hemisphere
        epsg = f"EPSG:327{zone_number:02d}"
    
    return epsg
```

## Step-by-Step Process

### 1. Define Area of Interest

First, define an area of interest (AOI) around your volcano's summit by creating a buffer:

```python
def define_aoi(coords, buffer_distance=20000):
    """
    Define an area of interest around a point.
    
    Args:
        coords (list): [longitude, latitude] of the point
        buffer_distance (int): Buffer distance in meters
        
    Returns:
        tuple: (ee.Geometry, list) - AOI and region coordinates
    """
    # Create a point from coordinates
    point = ee.Geometry.Point(coords)
    
    # Create a buffer around the point
    aoi = point.buffer(buffer_distance)
    
    # Get the region coordinates
    region_coords = aoi.bounds().getInfo()['coordinates']
    
    return aoi, region_coords
```

The buffer distance (default: 20 km) should be large enough to encompass potential evacuation routes and safe zones.

### 2. Download Digital Elevation Model

Next, download the DEM data for the defined area:

```python
def download_dem(aoi, region_coords, scale, description, utm_epsg, 
                collection="JAXA/ALOS/AW3D30/V3_2", band="DSM"):
    """
    Download DEM data for the specified area.
    """
    # Load DEM collection
    dem_collection = ee.ImageCollection(collection).select(band)
    
    # Create a mosaic and clip to AOI
    dem_mosaic = dem_collection.mosaic().clip(aoi)
    
    # Reproject to UTM with specified scale
    utm_projection = ee.Projection(utm_epsg).atScale(scale)
    dem_utm = dem_mosaic.reproject(utm_projection)
    
    # Export to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=dem_utm,
        description=f"{description}_{scale}m_Buffer_UTM",
        scale=scale,
        region=region_coords,
        crs=utm_epsg,
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    
    # Start the task
    task.start()
    
    return task
```

### 3. Download Land Cover Data

Similarly, download the land cover data:

```python
def download_landcover(aoi, region_coords, year, scale, description, utm_epsg):
    """
    Download land cover data for the specified area.
    """
    # Load land cover dataset for the specified year
    dataset = ee.Image(f'COPERNICUS/Landcover/100m/Proba-V-C3/Global/{year}').select('discrete_classification')
    
    # Clip to AOI and reproject
    clipped_dataset = dataset.clip(aoi)
    utm_projection = ee.Projection(utm_epsg).atScale(scale)
    dataset_utm = clipped_dataset.reproject(utm_projection)
    
    # Export to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=dataset_utm,
        description=f"{description}_{year}_{scale}m_Buffer_UTM",
        scale=scale,
        region=region_coords,
        crs=utm_epsg,
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    
    # Start the task
    task.start()
    
    return task
```

### 4. Combined Workflow Function

A consolidated function makes it easy to download all necessary data for a volcano:

```python
def download_volcano_data(volcano_name, lat, lon, buffer_distance=20000, 
                         scale=100, year=2019, utm_epsg=None):
    """
    Download DEM and land cover data for a volcano with automatic UTM projection detection.
    """
    # Get the proper UTM EPSG if not provided
    if utm_epsg is None:
        utm_epsg = get_utm_epsg(lat, lon)
    
    # Define area of interest
    coords = [lon, lat]  # GEE uses [longitude, latitude] order
    aoi, region_coords = define_aoi(coords, buffer_distance)
    
    # Download DEM
    dem_task = download_dem(
        aoi, region_coords, scale, f"{volcano_name}_DEM", utm_epsg
    )
    
    # Download land cover
    lc_task = download_landcover(
        aoi, region_coords, year, scale, f"{volcano_name}_LandCover", utm_epsg
    )
    
    return dem_task, lc_task
```

## Example: Downloading Data for Mount Marapi

Here's an example of downloading data for Mount Marapi in Indonesia:

```python
# Mount Marapi coordinates in Sumatra
MARAPI_LAT = -0.3775
MARAPI_LON = 100.4721

# Download data for Mount Marapi with automatic UTM detection
marapi_tasks = download_volcano_data(
    volcano_name="Marapi", 
    lat=MARAPI_LAT,
    lon=MARAPI_LON,
    buffer_distance=20000,  # 20 km buffer
    scale=100  # 100 m resolution
)
```

## Monitoring Export Progress

Google Earth Engine exports run asynchronously in the cloud. You can monitor the status using:

```python
def check_task_status(task):
    """Check the status of an Earth Engine export task."""
    status = task.status()
    if status['state'] == 'COMPLETED':
        print(f"Task {status['description']} completed successfully!")
    elif status['state'] == 'FAILED':
        print(f"Task {status['description']} failed: {status['error_message']}")
    else:
        print(f"Task {status['description']} is {status['state']}")
    return status

# Check both tasks
dem_status = check_task_status(marapi_tasks[0])
lc_status = check_task_status(marapi_tasks[1])
```

The export process may take several minutes to complete. Once finished, the files will be available in your Google Drive.

## Accessing Downloaded Files

After the export tasks complete:

1. Go to your Google Drive
2. Look for files named `[VolcanoName]_DEM_100m_Buffer_UTM.tif` and `[VolcanoName]_LandCover_2019_100m_Buffer_UTM.tif`
3. Download these files to your local project directory for further processing

## Data Validation

Before proceeding to the next step, it's important to validate the downloaded data:

1. Open the GeoTIFF files in a GIS software (QGIS, ArcGIS)
2. Check that the data covers the expected area around the volcano
3. Verify that there are no major gaps or artifacts in the data
4. Confirm that the data is projected in the correct UTM zone

## Next Steps

Once you have successfully downloaded and validated the required datasets, proceed to the [Cost Surface Generation](cost-surface.md) workflow to create cost surfaces for evacuation analysis.

## Troubleshooting

### Export Tasks Failing

If your export tasks fail, check the following:

1. **Area Size**: Very large areas may exceed GEE's processing limits. Try reducing the buffer size.
2. **Resolution**: Exporting at very high resolution can cause failures. Try increasing the scale parameter.
3. **Google Drive Space**: Ensure you have enough free space in your Google Drive.
4. **Authentication**: Verify your Earth Engine authentication is still valid.

### Missing or Incomplete Data

If the downloaded data has gaps or artifacts:

1. **Cloud Cover**: Some regions may have cloud coverage in the original imagery. Try using alternative DEM sources.
2. **Regional Availability**: Some datasets may have limited coverage in certain regions. Consider using alternative datasets.

### Alternative Data Sources

If Google Earth Engine doesn't provide suitable data for your area of interest, consider these alternatives:

1. **SRTM DEM**: Available from NASA Earth Data (https://earthdata.nasa.gov/)
2. **ASTER GDEM**: Available from USGS Earth Explorer (https://earthexplorer.usgs.gov/)
3. **Local Government Data**: Many countries provide national-level DEM and land cover datasets
