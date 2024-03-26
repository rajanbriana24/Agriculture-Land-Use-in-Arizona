# visualization.py

import geemap

def visualize_clusters(clusters):
    # Initialize Earth Engine
    ee.Initialize()

    # Define a list of colors
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'cyan', 'magenta', 'lime']

    # Create a Map object
    Map = geemap.Map()

    # Add each cluster boundary geometry to the map with a different color
    for cluster_label, color in zip(set(clusters), colors):
        cluster_indices = np.where(clusters == cluster_label)[0]
        cluster_latitudes = df.iloc[cluster_indices]['lat'].values
        cluster_longitudes = df.iloc[cluster_indices]['lon'].values
        geometry = ee.Geometry.MultiPoint(list(zip(cluster_longitudes, cluster_latitudes)))
        Map.addLayer(geometry, {'color': color}, f'Cluster {cluster_label} Boundary')

    # Display the map
    Map.addLayerControl()
    Map
