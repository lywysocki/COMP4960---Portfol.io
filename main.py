import Algorithm2 as a2
import arimaCpy as arima


def test_slope(ticker):
    # predicted returns the slope of the line 30 days from offset
    predicted = a2.main(ticker)
    # actual returns the change between the stock price 250 days ago and 220 days ago
    actual = a2.percent_change(ticker, 250, 220)
    print(ticker, "Predicted:", predicted, "Actual:", actual)
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

