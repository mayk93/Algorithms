#!/usr/bin/python
# -*- coding: utf-8 -*-

# Logging
import logging
logging.basicConfig(level=logging.INFO)
# -----

# Libs
import pandas as pd
import quandl
# -----

def main():
    stock_data_frame = quandl.get('WIKI/GOOGL')
    # logging.info("Got a data frame that looks like this: " + str(stock_data_frame.head()))
    adjusted_stock_data_frame = stock_data_frame[["Adj. Open", "Adj. Low", "Adj. High", "Adj. Close", "Adj. Volume"]]
    adjusted_stock_data_frame["Volatility"] = (adjusted_stock_data_frame["Adj. High"] - adjusted_stock_data_frame["Adj. Low"]) / adjusted_stock_data_frame["Adj. Low"] * 100.0
    adjusted_stock_data_frame["Change"] = (adjusted_stock_data_frame["Adj. Close"] - adjusted_stock_data_frame["Adj. Open"]) / adjusted_stock_data_frame["Adj. Open"] * 100.0
    used_stock_data_frame = adjusted_stock_data_frame[["Adj. Close", "Volatility", "Change", "Adj. Volume"]]
    logging.info("Got a data frame that looks like this: " + str(used_stock_data_frame.head()))

if __name__ == "__main__":
    main()
