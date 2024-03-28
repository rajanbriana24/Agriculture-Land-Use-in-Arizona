import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import geemap
import ee
from data_collection import collect_data
from clustering import perform_clustering
from machine_learning import train_models
from visualization import visualize_clusters
from machine_learning_linear_regression import train_linear_regression_and_plot

def main():
    # Initialize Earth Engine
    ee.Initialize()

    # Collect and preprocess data
    df = collect_data('Dataset.csv')

    # Perform clustering
    clusters = perform_clustering(df)

    # Train machine learning models
    models = train_models(df)

    # Visualize clusters
    visualize_clusters(clusters)

    # Train linear regression and plot
    train_linear_regression_and_plot()

if __name__ == "__main__":
    main()
