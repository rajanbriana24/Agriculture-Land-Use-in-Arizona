import ee
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='crypto-pulsar-418018')

# Define datasets
irrigation_dataset = ee.Image("USGS/GFSAD1000_V1")
climate_dataset = ee.ImageCollection('NASA/ORNL/DAYMET_V4')
crop_dataset = ee.ImageCollection('USDA/NASS/CDL')
elevation_dataset = ee.Image("CGIAR/SRTM90_V4")

# Select variables
selected_variables_irrigation = ['landcover']
selected_variables_climate = ['prcp', 'tmin', 'tmax']

# Helper functions
def get_day_values(data, date, xy_point):
    day_data = data.filterDate(date, date.advance(1, 'day'))

    if day_data.size().getInfo() == 0:
        print(f"No data available for {date.format().getInfo()}")
        return None

    first_image = day_data.first()
    day_values = first_image.reduceRegion(reducer=ee.Reducer.first(), geometry=xy_point)
    return day_values.getInfo()

def get_climate_data(xy_point, date_str):
    date = ee.Date(date_str)
    daily_value = get_day_values(climate_dataset, date, xy_point)
    return daily_value

def get_crop_data(xy_point, date_str):
    date = ee.Date(date_str)
    day_value = get_day_values(crop_dataset, date, xy_point)
    return day_value['cropland']

def get_elevation_data(xy_point):
    elevation_for_point = elevation_dataset.reduceRegion(reducer=ee.Reducer.first(), geometry=xy_point)
    return elevation_for_point.getInfo()['elevation']

def get_results(coordinates):
    xy_point = ee.Geometry.Point(coordinates)

    irrigation_result = irrigation_data.reduceRegion(reducer=ee.Reducer.first(), geometry=xy_point).getInfo()['landcover']
    climate_result = get_climate_data(xy_point)
    crop_result = get_crop_data(xy_point)
    elevation_result = get_elevation_data(xy_point)

    return {
        "irrigation_result": irrigation_result,
        "tmin": climate_result['tmin'],
        "tmax": climate_result["tmax"],
        "prcp": climate_result["prcp"],
        "cropland": crop_result,
        "elevation_result": elevation_result
    }

# Define coordinates for Arizona bounding box
minLon, minLat, maxLon, maxLat = -114.931, 31.332, -109.045, 37.004
bounding_box = ee.Geometry.Rectangle([minLon, minLat, maxLon, maxLat])
# Collect random point samples 
random_points = ee.FeatureCollection.randomPoints(region=bounding_box, points=10)
coordinates = random_points.geometry().coordinates().getInfo()

# Output CSV file
output_csv = 'Dataset.csv'
columns = ['lat', 'lon', 'irrigation_result', 'tmin', 'tmax', 'prcp', 'cropland', 'elevation_result']

# Write results to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    for coord in coordinates:
        result = get_results(coord)
        result['lon'], result['lat'] = coord[0], coord[1]
        writer.writerow(result)
