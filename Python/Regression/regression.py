#!/usr/bin/python
# -*- coding: utf-8 -*-

# Logging
import logging
logging.basicConfig(level=logging.INFO)
# -----

# Libs
import quandl
import math
import sys
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
# -----


FORECAST = "Adj. Close"
OUTLIER_VALUE = -sys.maxsize
UNIX_DAY = 86400
style.use('ggplot')


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
    features_no_label = features[-forecast_out:]
    features = features[:-forecast_out:]
    data_frame.dropna(inplace=True)
    labels = np.array(data_frame['Label'])

    return features, labels, features_no_label


def get_data():
    # Get a slightly processed data frame from Quandl.
    used_stock_data_frame = get_data_frame()
    logging.info("[get_data] Got a data frame that looks like this:\n\n" + str(used_stock_data_frame.head()) + "\n\n")

    # Get prediction offset.
    forecast_out = get_forecast_out(days=100, data_frame=used_stock_data_frame)
    logging.info("[get_data] Forecast out: " + str(forecast_out))

    # Set the label column.
    used_stock_data_frame = set_label(data_frame=used_stock_data_frame, forecast_out=forecast_out)
    logging.info("[get_data] Data frame at this point:\n\n" + str(used_stock_data_frame.head()) + "\n\n")

    # Define the Features and Labels.
    features = np.array(used_stock_data_frame.drop(['Label'], 1))  # Our features are everything except the label
    labels = np.array(used_stock_data_frame['Label'])  # Our labels are the label column.

    # Preprocess features and labels
    features, labels, features_no_label = preprocess(features=features,
                                                     labels=labels,
                                                     data_frame=used_stock_data_frame,
                                                     forecast_out=forecast_out)

    logging.info("[get_data] Features:\n\n" + str(features) + "\n\n")
    logging.info("[get_data] Labels:\n\n" + str(labels) + "\n\n")

    logging.info("[get_data] Len of Features:\n" + str(len(features)) + "\n")
    logging.info("[get_data] Len Labels:\n" + str(len(labels)) + "\n")

    # Get training and testing data.
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features,
                                                                                                 labels,
                                                                                                 test_size=0.3)

    return features_train, features_test, labels_train, labels_test, features_no_label, used_stock_data_frame


def train(features_train=None, features_test=None, labels_train=None, labels_test=None):
    if None in [features_train, features_test, labels_train, labels_test]:
        logging.error("[train] IMPORTANT: Using None as training or test data. Training failed.")
        return None
    classifier = LinearRegression()
    classifier.fit(features_train, labels_train)  # Fit means train
    accuracy = classifier.score(features_test, labels_test)  # Score means test

    logging.info("Accuracy score: " + str(accuracy))

    return classifier


def plot(data_frame=None, forecast=None):
    if data_frame is None:
        logging.error("[plot] IMPORTANT: Using None as data frame. Plot failed.")
        return
    if forecast is None:
        logging.error("[plot] IMPORTANT: Using None as forecast. Plot failed.")
        return
    data_frame["Forecast"] = np.nan
    last_date = data_frame.iloc[-1].name
    last_unix = last_date.timestamp()
    next_unix = last_unix + UNIX_DAY
    for forecast_value in forecast:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += UNIX_DAY
        data_frame.loc[next_date] = [np.nan for _ in range(len(data_frame.columns)-1)] + [forecast_value]
    data_frame['Adj. Close'].plot()
    data_frame['Forecast'].plot()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

def main():
    logging.info("Start.")

    # Get data.
    features_train, features_test, labels_train, labels_test, features_no_label, data_frame = get_data()

    # Train a classifier using data.
    trained_classifier = train(features_train, features_test, labels_train, labels_test)

    # Predict.
    forecast_set = trained_classifier.predict(features_no_label)

    # Plot
    plot(data_frame=data_frame, forecast=forecast_set)


if __name__ == "__main__":
    main()
