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
import sys
# -----


FORECAST = "Adj. Close"
OUTLIER_VALUE = -sys.maxsize


def get_data_frame():
    stock_data_frame = quandl.get('WIKI/GOOGL')
    adjusted_stock_data_frame = stock_data_frame[["Adj. Open", "Adj. Low", "Adj. High", "Adj. Close", "Adj. Volume"]]
    adjusted_stock_data_frame["Volatility"] = (adjusted_stock_data_frame["Adj. High"] - adjusted_stock_data_frame["Adj. Low"]) / adjusted_stock_data_frame["Adj. Low"] * 100.0
    adjusted_stock_data_frame["Change"] = (adjusted_stock_data_frame["Adj. Close"] - adjusted_stock_data_frame["Adj. Open"]) / adjusted_stock_data_frame["Adj. Open"] * 100.0
    # These are out features ( Adj. Close, Volatility, etc )
    used_stock_data_frame = adjusted_stock_data_frame[["Adj. Close", "Volatility", "Change", "Adj. Volume"]]
    used_stock_data_frame.fillna(value=OUTLIER_VALUE, inplace=True)
    return used_stock_data_frame


def get_forecast_out(days=0, data_frame=None):
    if data_frame is None:
        return 0
    if days == 0:
        return 0
    return int(math.ceil((1/days)*len(data_frame)))


def main():
    logging.info("Start.")
    used_stock_data_frame = get_data_frame()
    logging.info("Got a data frame that looks like this:\n\n" + str(used_stock_data_frame.head()) + "\n\n")
    forecast_out = get_forecast_out(days=100, data_frame=used_stock_data_frame)
    logging.info("Forecast out: " + str(forecast_out))

    # The forecast column ( Adj. Close, the price at closing ) will be shifted up ( hence the minus ).
    # This was, for each row, the label column will be adj. close 10 days in the future.
    used_stock_data_frame['Label'] = used_stock_data_frame[FORECAST].shift(-forecast_out)

    logging.info("[0] Data frame at this point:\n\n" + str(used_stock_data_frame.head()) + "\n\n")



if __name__ == "__main__":
    main()
