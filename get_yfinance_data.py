from yahooquery import Ticker

def get_current_price(tickers: list) -> dict:
    current_prices = {}
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    myDict = myInfo.price
    history_data = myInfo.history(period="2d")
    for ticker in tickers:
        current_prices[ticker] = {}
        try:
            current_prices[ticker]["price"] = float(myDict[ticker]["regularMarketPrice"])
            ticker_history = history_data.loc[ticker]
            if len(ticker_history) >= 2:
                close_yesterday = ticker_history["close"].iloc[-2]
                close_today = ticker_history["close"].iloc[-1]

                change_pct = (close_today - close_yesterday) / close_yesterday * 100
                current_prices[ticker]["change_percent"] = round(float(change_pct), 2)
            else:
                current_prices[ticker]["change_percent"] = None
        except (KeyError, TypeError, ValueError):
            current_prices[ticker] = None  # brak ceny zamiast rzucać wyjątek
    return current_prices
