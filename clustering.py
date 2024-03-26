from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

import geemap
import ee

# Read the data from the CSV file into a DataFrame
df = pd.read_csv('Dataset.csv')

# Assuming you have latitude and longitude values stored in latitudes and longitudes arrays
# You can read your data into these arrays from your source, such as a CSV file
latitudes = df['lat'].values
longitudes = df['lon'].values
# Combine latitudes and longitudes into a single array
coordinates = np.column_stack((latitudes, longitudes))

# Define bounding box coordinates for filtering data within a specific area
minLon, minLat = -112.6, 32.5
maxLon, maxLat = -111.5, 33.5

# Count the number of points within the specified bounding box
count = np.sum((coordinates[:, 0] > minLat) & (coordinates[:, 0] < maxLat) &
               (coordinates[:, 1] > minLon) & (coordinates[:, 1] < maxLon))
print("Count: ", count)

# Specify the epsilon (maximum distance between two samples) and minimum samples for DBSCAN
epsilon = 0.15  # Adjust as needed
min_samples = 10  # Adjust as needed

# Create a DBSCAN model
dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)

# Fit the model to the data
dbscan.fit(coordinates)

# Get the cluster labels for each point
labels = dbscan.labels_

# Group the DataFrame by cluster labels
grouped = df.groupby('cluster_label')

# Dictionary to store boundary coordinates of each cluster
cluster_boundaries = {}

# Iterate over each cluster
for cluster_label, cluster_data in grouped:
    # Compute minimum and maximum latitude and longitude values for the cluster
    min_lat = cluster_data['lat'].min()
    max_lat = cluster_data['lat'].max()
    min_lon = cluster_data['lon'].min()
    max_lon = cluster_data['lon'].max()

    # Store boundary coordinates of the cluster in the dictionary
    cluster_boundaries[cluster_label] = {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lon': min_lon,
        'max_lon': max_lon
    }

# Print boundary coordinates of each cluster
for cluster_label, boundaries in cluster_boundaries.items():
    print(f"Cluster {cluster_label} Boundary Coordinates:")
    print(f"Min Latitude: {boundaries['min_lat']}, Max Latitude: {boundaries['max_lat']}")
    print(f"Min Longitude: {boundaries['min_lon']}, Max Longitude: {boundaries['max_lon']}")
    print()

# Initialize Earth Engine
ee.Initialize()

# Latitude and longitude coordinates of Phoenix
phoenix_coords = [33.4484, -112.0740]

# Create a Map object centered on Phoenix
Map = geemap.Map(center=phoenix_coords, zoom=8)

# Define a list of colors
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'cyan', 'magenta', 'lime']

# Add each cluster boundary geometry to the map with a different color
for cluster_label, boundaries in cluster_boundaries.items():
    min_lat = boundaries['min_lat']
    max_lat = boundaries['max_lat']
    min_lon = boundaries['min_lon']
    max_lon = boundaries['max_lon']
    geometry = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
    color = colors[cluster_label % len(colors)]  # Cycle through colors if more clusters than colors
    Map.addLayer(geometry, {'color': color}, f'Cluster {cluster_label} Boundary')

# Display the map
Map.addLayerControl()
Map
