import arima as arima


ticker = "NVDA"
df = arima.get_data(ticker, "01-01-2021", 0)
test_df = arima.get_data(ticker, "01-01-2021", 90)
arima.forcast(df, test_df, 90, "NVDA")

# arima.forcast("AAPL", "01-01-2020", 365)
# arima.forcast("WMT", "01-01-2020", 365)
# arima.forcast("SNAP", "01-01-2020", 365)
# arima.forcast("SCHW", "01-01-2020", 365)
# arima.forcast("AMD", "01-01-2020", 365)
# arima.forcast("NVDA", "01-01-2020", 365)
# arima.forcast("MSFT", "01-01-2020", 365)
# arima.forcast("GRRR", "01-01-2020", 365)
# arima.forcast("NXT", "01-01-2020", 365)


# arima.forcast("AAPL", "01-01-2020", 91)
# arima.forcast("WMT", "01-01-2020", 91)
# arima.forcast("SNAP", "01-01-2020", 91)
# arima.forcast("SCHW", "01-01-2020", 91)
# arima.forcast("AMD", "01-01-2020", 91)
# arima.forcast("NVDA", "01-01-2020", 91)
# arima.forcast("MSFT", "01-01-2020", 91)
# arima.forcast("GRRR", "01-01-2020", 91)
# arima.forcast("NXT", "01-01-2020", 91)


arima.forcast("AAPL", "03-23-2020", 182)
# arima.forcast("WMT", "01-01-2008", 182)
# arima.forcast("SNAP", "01-01-2008", 182)
# arima.forcast("SCHW", "01-01-2008", 182)
# arima.forcast("AMD", "01-01-2008", 182)
# arima.forcast("NVDA", "01-01-2008", 182)
# arima.forcast("MSFT", "01-01-2008", 182)
# arima.forcast("GRRR", "01-01-2008", 182)
arima.forcast("NXT", "01-01-2008", 182)

# arima.forcast("AAPL", "01-01-2017", 30)
# arima.forcast("WMT", "01-01-2017", 30)
# arima.forcast("SNAP", "01-01-2017", 30)
# arima.forcast("SCHW", "01-01-2017", 30)
# arima.forcast("AMD", "01-01-2017", 30)
# arima.forcast("NVDA", "01-01-2017", 30)
# arima.forcast("MSFT", "01-01-2017", 30)
# arima.forcast("GRRR", "01-01-2017", 30)
# arima.forcast("NXT", "01-01-2017", 30)
