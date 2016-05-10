#!/usr/bin/python
# -*- coding: utf-8 -*-

# Logging
import logging
logging.basicConfig(level=logging.INFO)
# -----

# Libs
import pandas as pd
import quandl
import math
import numpy as np
import sys
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
# -----


FORECAST = "Adj. Close"
OUTLIER_VALUE = -sys.maxsize


def get_data_frame():
    stock_data_frame = quandl.get('WIKI/GOOGL')
    adjusted_stock_data_frame = stock_data_frame[["Adj. Open", "Adj. Low", "Adj. High", "Adj. Close", "Adj. Volume"]]
    adjusted_stock_data_frame["Volatility"] = (adjusted_stock_data_frame["Adj. High"] - adjusted_stock_data_frame["Adj. Low"]) / adjusted_stock_data_frame["Adj. Low"] * 100.0
    adjusted_stock_data_frame["Change"] = (adjusted_stock_data_frame["Adj. Close"] - adjusted_stock_data_frame["Adj. Open"]) / adjusted_stock_data_frame["Adj. Open"] * 100.0
    used_stock_data_frame = adjusted_stock_data_frame[["Adj. Close", "Volatility", "Change", "Adj. Volume"]]
    used_stock_data_frame.fillna(value=OUTLIER_VALUE, inplace=True)
    return used_stock_data_frame


def get_forecast_out(days=0, data_frame=None):
    if data_frame is None:
        logging.error("[get_forecast_out] IMPORTANT: Using None as a data frame. Returning 0.")
        return 0
    if days <= 0:
        logging.error("[get_forecast_out] IMPORTANT: Using 0 as number of days. Returning 0.")
        return 0
    return int(math.ceil((1/days)*len(data_frame)))


def set_label(data_frame=None, forecast_out=0):
    if data_frame is None:
        logging.error("[set_label] IMPORTANT: Using None as a data frame. No label set.")
        return data_frame
    # The forecast column ( Adj. Close, the price at closing ) will be shifted up ( hence the minus ).
    # This was, for each row, the label column will be adj. close 10 days in the future.
    data_frame['Label'] = data_frame[FORECAST].shift(-forecast_out)
    data_frame.dropna(inplace=True)
    return data_frame


def preprocess(features=None, labels=None, data_frame=None, forecast_out=0):
    if features is None or labels is None:
        logging.error("[preprocess] IMPORTANT: Using None as a numpy array. Preprocessing failed.")
        return features, labels
    if data_frame is None:
        logging.error("[preprocess] IMPORTANT: Using None as a data frame. Preprocessing failed.")
        return features, labels
    if forecast_out <= 0:
        logging.error("[preprocess] IMPORTANT: Using 0 as forecast_out. Preprocessing failed.")
        return features, labels

    # Scale ( Normalize, in a way. Set it between -1 and 1 )
    features = preprocessing.scale(features)

    labels = np.array(data_frame['Label'])

    return features, labels

def main():
    logging.info("Start.")

    # Get a slightly processed data frame from Quandl.
    used_stock_data_frame = get_data_frame()
    logging.info("[main] Got a data frame that looks like this:\n\n" + str(used_stock_data_frame.head()) + "\n\n")

    # Get prediction offset.
    forecast_out = get_forecast_out(days=100, data_frame=used_stock_data_frame)
    logging.info("[main] Forecast out: " + str(forecast_out))

    # Set the label column.
    used_stock_data_frame = set_label(data_frame=used_stock_data_frame, forecast_out=forecast_out)
    logging.info("[main] Data frame at this point:\n\n" + str(used_stock_data_frame.head()) + "\n\n")

    # Define the Features and Labels.
    features = np.array(used_stock_data_frame.drop(['Label'], 1))  # Our features are everything except the label column.
    labels = np.array(used_stock_data_frame['Label'])  # Our labels are the label column.

    # Preprocess features and labels
    features, labels = preprocess(features=features,
                                  labels=labels,
                                  data_frame=used_stock_data_frame,
                                  forecast_out=forecast_out)

    logging.info("[main] Features:\n\n" + str(features) + "\n\n")
    logging.info("[main] Labels:\n\n" + str(labels) + "\n\n")

    logging.info("[main] Len of Features:\n\n" + str(len(features)) + "\n\n")
    logging.info("[main] Len Labels:\n\n" + str(len(labels)) + "\n\n")

    # 

if __name__ == "__main__":
    main()
