import requests
from datetime import date

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
    