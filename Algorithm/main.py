from Algorithm import Algorithm2 as a2
# import arimaCpy as arima
from Database.query import fetch_close_from_date
from Database.database import retrieve_stock_prices

'''
def test_slope(ticker):
    # predicted returns the slope of the line 30 days from offset
    predicted = a2.prediction_slope(ticker)
    # actual returns the change between the stock price 250 days ago and 220 days ago

    actual = a2.percent_change(ticker, 50, 0)
    print(ticker, "Predicted:", predicted, "Actual:", actual)
    #print(ticker, "Predicted:", predicted)
    print(" ")

    # Actual is this percent off the prediction
    # print("Error %:", predicted / actual * 100, "\n")


test_slope("MSFT")
test_slope("AMD")
test_slope("SPY")
test_slope("SNAP")
test_slope("META")
test_slope("COST")
test_slope("BTI")
'''

df = fetch_close_from_date("AMD", "01-01-2020")

print(df)

df1 = retrieve_stock_prices("AMD", "01-01-2020", 0)

print(df)

