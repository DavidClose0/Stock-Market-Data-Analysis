"""
This module downloads historical stock data for stock tickers passed as command line arguments.
The minimum, maximum, average, and median close prices are written to a JSON file.
"""

import requests
from datetime import date
import sys
import json

def download_data(ticker: str) -> dict:
    """
    Downloads stock data from the last 5 years for a given ticker from the Nasdaq API.
    Args: 
        ticker (str): The stock ticker to download data for.
    Returns:
        dict: A dictionary containing the historical stock data.
    """
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    # Pretend to be a browser
    headers = {
        "Accept-Language":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "User-Agent":"Java-http-client/"
    }

    try:
        request = requests.get(base_url + path, headers=headers)
        data = request.json()

        # Check if the API returned an error message
        if (data["status"]["bCodeMessage"] and "errorMessage" in data["status"]["bCodeMessage"][0]):
            raise Exception(data["status"]["bCodeMessage"][0]["errorMessage"])
        
        return data
    except Exception as e:
        print(f"Error retrieving {ticker} data: {e}")
        return {}

def extract_close_prices(data: dict) -> dict:
    """
    Extracts the minimum, maximum, average, and median close prices from historical stock data.
    Args:
        data (dict): The historical stock data.
    Returns:
        dict: A dictionary containing min, max, avg, and median close prices, plus ticker symbol.
    """
    # Extract numerical close prices and ticker symbol
    close_prices = [float(rows["close"][1:]) for rows in data["data"]["tradesTable"]["rows"]]
    ticker = data["data"]["symbol"]

    min_price = min(close_prices)
    max_price = max(close_prices)
    avg_price = sum(close_prices) / len(close_prices)
    close_prices.sort()
    median_price = close_prices[len(close_prices) // 2]

    return {
        "ticker": ticker,
        "min": min_price,
        "max": max_price,
        "avg": avg_price,
        "median": median_price
    }

if __name__ == "__main__":
    # Add close prices for each stock to a list
    stocks = []
    for ticker in sys.argv[1:]:
        data = download_data(ticker)
        if data:
            stocks.append(extract_close_prices(data))

    try :
        f = open("stocks.json", "w")
    except Exception as e:
        print(f"Error opening stocks.json: {e}")
        exit(1)
        
    with f:
        json.dump(stocks, f, indent=4)

    print("Stock data written to stocks.json")