import yfinance as yf
from datetime import datetime
import pandas as pd

class Stock:
    def __init__(self, ticker, start="2024-01-01"):
        self.ticker = ticker
        self.start_date = start
        self.current_date = self.get_current_date()
        self.data = self.get_stock_data()
        if self.data is None or self.data.empty:
            print("No vaid stock data")

        #self.news = self.get_recent_news()
    

    def get_current_date(self):
        current = datetime.now()
        return current.strftime("%Y-%m-%d")


    def get_stock_data(self): 
        data = yf.download(self.ticker, self.start_date, self.current_date)

        # Flatten multi-index if it exists
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [' '.join(col).strip() for col in data.columns.values]

        # Remove ticker suffix (e.g., "Close SPY" -> "Close")
        data.columns = [col.replace(f" {self.ticker}", "") for col in data.columns]

        print(f"\n[{self.ticker}] Final Cleaned Columns:\n{data.columns}")
        return data




    """"
    def get_recent_news(self):
        ticker = yf.Ticker(self.ticker)
        raw_news = ticker.get_news(count = 5)
        article_list = []
        for article in raw_news:
            if article["content"]: 
                article_list.append(
                    {"Title": article.get("content").get("title"),
                    "Summary": article.get("content").get("summary"), 
                    "url": article.get("content").get("clickThroughUrl").get("url")
                    })
            else: 
                article_list.append(
                    {"Title": article.get("title"),
                    "Summary": article.get("summary"), 
                    "url": article.get("clickThroughUrl").get("url")
                    })
        return article_list

"""


if __name__ == "__main__":
    test_stock = Stock("PLTR")
    print(test_stock.data)
    