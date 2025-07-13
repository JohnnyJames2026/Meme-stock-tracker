import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from stock import Stock
from plotting import *

spy = Stock("SPY")
stock2 = Stock("BBAI")
stock3 = Stock("negg")
stock4 = Stock("joby")

stocks_list = [spy, stock2, stock3, stock4]


#get one stock chart
get_stock_chart(spy)

#compare multiple stock charts
compare_charts_interactive_enhanced(stocks_list)
