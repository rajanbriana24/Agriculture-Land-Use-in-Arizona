import ee
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression

from data_collection import get_climate_data


def main():
    # Get data
    data = get_data()
    data = data[:-1] # Remove the last entry because it has big value.

    # Extract climate variables and dates
    y_tmin = np.array([entry['climate']['tmin'] for entry in data])
    y_tmax = np.array([entry['climate']['tmax'] for entry in data])
    y_prcp = np.array([entry['climate']['prcp'] for entry in data])
    X = np.array([[date_to_ordinal(entry['date'])] for entry in data])

    # Prepare dates for plotting
    X_dates = pd.to_datetime([datetime.fromordinal(int(ox)) for ox in X.flatten()])

    # Forecast future dates for prediction
    future_dates = [datetime(year, month, 15).toordinal()
                    for year in range(2024, 2029) for month in [1, 4, 7, 10]]
    future_dates_dt = pd.to_datetime([datetime.fromordinal(fd) for fd in future_dates])
    future_years = np.array(future_dates).reshape(-1, 1)

    # Convert numpy arrays to pandas Series with dates as index
    tmin_series = pd.Series(y_tmin, index=X_dates)
    tmax_series = pd.Series(y_tmax, index=X_dates)
    prcp_series = pd.Series(y_prcp, index=X_dates)

    # Calculate moving averages
    tmin_moving_avg = tmin_series.rolling(window=4).mean()
    tmax_moving_avg = tmax_series.rolling(window=4).mean()
    prcp_moving_avg = prcp_series.rolling(window=4).mean()

    # Train and predict with Linear Regression
    model_tmin = LinearRegression().fit(X, y_tmin)
    model_tmax = LinearRegression().fit(X, y_tmax)
    model_prcp = LinearRegression().fit(X, y_prcp)
    predictions_tmin = model_tmin.predict(future_years)
    predictions_tmax = model_tmax.predict(future_years)
    predictions_prcp = model_prcp.predict(future_years)

    # Plotting
    plt.figure(figsize=(14, 10))

    # Plot Tmin
    plt.subplot(3, 1, 1)
    plt.plot(tmin_series.index, tmin_series, label='Historical Tmin', marker='o', linestyle='-')
    plt.plot(future_dates_dt, predictions_tmin, label='Predicted Tmin', marker='x', linestyle='--')
    plt.plot(tmin_moving_avg.index, tmin_moving_avg, label='Tmin Moving Average', color='orange', linestyle='-')
    plt.ylabel('Tmin (°C)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Plot Tmax
    plt.subplot(3, 1, 2)
    plt.plot(tmax_series.index, tmax_series, label='Historical Tmax', marker='o', linestyle='-')
    plt.plot(future_dates_dt, predictions_tmax, label='Predicted Tmax', marker='x', linestyle='--')
    plt.plot(tmax_moving_avg.index, tmax_moving_avg, label='Tmax Moving Average', color='orange', linestyle='-')
    plt.ylabel('Tmax (°C)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Plot Prcp
    plt.subplot(3, 1, 3)
    plt.plot(prcp_series.index, prcp_series, label='Historical Prcp', marker='o', linestyle='-')
    plt.plot(future_dates_dt, predictions_prcp, label='Predicted Prcp', marker='x', linestyle='--')
    plt.plot(prcp_moving_avg.index, prcp_moving_avg, label='Prcp Moving Average', color='orange', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Prcp (mm)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout()
    plt.show()


def get_data():
    point = [-112.087198, 33.037128]
    xy_point = ee.Geometry.Point(point)
    data = []

    for year in range(1997, 2023):
        for month in [1, 4, 7, 10]:
            date_str = f'{str(year)}-{str(month)}-15'
            climate_result = get_climate_data(xy_point, date_str)

            year_result = {
              'date': date_str,
              'climate': climate_result
            }

            data.append(year_result)

    return data


def date_to_ordinal(date):
    return datetime.strptime(date, '%Y-%m-%d').toordinal()
