import yfinance as yf
from datetime import datetime

class Stock:
    def __init__(self, ticker, start="2023-01-01"):
        self.ticker = ticker
        self.start_date = start
        self.current_date = self.get_current_date()
        self.data = self.get_stock_data()
        self.news = self.get_recent_news()
    

    def get_current_date(self):
        current = datetime.now()
        return current.strftime("%Y-%m-%d")


    def get_stock_data(self):
        #returns date, close price, day's high, day's low, open price, volume
        return yf.download(self.ticker, self.start_date, self.current_date)
    
    
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




if __name__ == "__main__":
    test_stock = Stock("PLTR")
    print(test_stock.data)
    print(test_stock.get_recent_news())
    