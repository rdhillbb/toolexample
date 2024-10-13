import datetime
import os
import subprocess

import yfinance as yf
"""
In this section, the data schemas based on the OpenAI function structure 
will be defined in this section of the code.
"""
from typing import List, Optional, Type
from langchain_community.tools import format_tool_to_openai_function
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


def getyahootools():
    tools = [
        StockGetNewsTool(),
        StockPriceTool(),
        StockPercentageChangeTool(),
        StockGetBestPerformingTool(),
    ]
    return tools 


class StockPriceCheckInput(BaseModel):

    """Input for Stock price check."""

    stockticker: str = Field(..., description="Ticker symbol for stock or index")


class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    #description = "Useful for when you need to find out the price of stock. You should input the stock ticker used on the yfinance API"
    description = "This variable retrieves stock prices via the yfinance API. Input the required stock ticker symbol to obtain current financial data, essential for investment and market analysis."

    def _run(self, stockticker: str):
        # print("i'm running")
        price_response = get_stock_price(stockticker)

        return price_response

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput


class StockChangePercentageCheckInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stockticker: str = Field(..., description="Ticker symbol for stock or index")
    days_ago: int = Field(..., description="Int number of days to look back")


class StockPercentageChangeTool(BaseTool):
    name = "get_price_change_percent"
    #description = "Useful for when you need to find out the percentage change in a stock's value. You should input the stock ticker used on the yfinance API and also input the number of days to check the change over"
    description ="This function calculates the percentage change in a stock's value over a specified number of days. Input the stock ticker symbol recognized by the yfinance API and the duration in days to receive the desired financial analysis."

    def _run(self, stockticker: str, days_ago: int):
        price_change_response = get_price_change_percent(stockticker, days_ago)

        return price_change_response

    def _arun(self, stockticker: str, days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput


# the best performing


class StockBestPerformingInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stocktickers: List[str] = Field(
        ..., description="Ticker symbols for stocks or indices"
    )
    days_ago: int = Field(..., description="Int number of days to look back")


class StockGetBestPerformingTool(BaseTool):
    name = "get_best_performing"
    #description = "Useful for when you need to the performance of multiple stocks over a period. You should input a list of stock tickers used on the yfinance API and also input the number of days to check the change over"
    description = "This function evaluates the performance of multiple stocks over a specified period. Input a list of stock tickers recognized by the yfinance API and the number of days for which you want to track changes. This tool provides a comprehensive analysis of stock trends, helping you make informed investment decisions."
    def _run(self, stocktickers: List[str], days_ago: int):
        price_change_response = get_best_performing(stocktickers, days_ago)

        return price_change_response

    def _arun(self, stockticker: List[str], days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockBestPerformingInput


# This seciton defines the public functions
class YahooToolObject:
    def __init__(self, tools: List[BaseTool] = None, functions: List = None):
        self.tools = tools if tools else []
        self.functions = functions if functions else []


from datetime import datetime, timedelta


def get_price_change_percent(symbol, days_ago):
    ticker = yf.Ticker(symbol)

    # Get today's date
    end_date = datetime.now()

    # Get the date N days ago
    start_date = end_date - timedelta(days=days_ago)

    # Convert dates to string format that yfinance can accept
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    # Get the historical data
    historical_data = ticker.history(start=start_date, end=end_date)

    # Get the closing price N days ago and today's closing price
    old_price = historical_data["Close"].iloc[0]
    new_price = historical_data["Close"].iloc[-1]

    # Calculate the percentage change
    percent_change = ((new_price - old_price) / old_price) * 100
    respons = f"Stock Price {days_ago} days ago was {old_price}. Current Price is {new_price} "
    respons +=str(round(percent_change, 2)) + "%"
    return respons
    return round(percent_change, 2)



def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    historical_data = ticker.history(start=start_date, end=end_date)
    old_price = historical_data["Close"].iloc[0]
    new_price = historical_data["Close"].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)


def get_best_performing(stocks, days_ago):
    best_stock = None
    best_performance = None
    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if best_performance is None or performance > best_performance:
                best_stock = stock
                best_performance = performance
        except Exception as e:
            print(f"Could not calculate performance for {stock}: {e}")
    return best_stock, best_performance


def blankScreen():
    subprocess.call("clear", shell=True)


class StockGetNewsInput(BaseModel):
    """Input for to receive yahoo news on stock"""

    ticker: str = Field(..., description="Ticker symbols for stocks or indices")


class StockGetNewsTool(BaseTool):
    name = "get_stock_news"
    #description = "market news and insights on stocks and indices, providing comprehensive coverage and global perspective for informed decision-making."
    description  ="This function offers market news and insights on stocks and indices, providing comprehensive coverage from a global perspective. It enables informed decision-making by delivering up-to-date information on market trends and financial data. Utilize this tool to gain a deeper understanding of market dynamics and enhance your investment strategies."
    def _run(self, ticker: str):
        news = get_stock_news(ticker)

        return news

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockGetNewsInput


def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return round(todays_data["Close"].iloc[0], 2)


# use the function
# stock = yf.Ticker("RandolphHill")
# print(stock.news)


def get_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_array = process_json_data(stock.news)
    long_string = ""

    for article in news_array:
        long_string += "Title: " + article.title + "\n"
        long_string += "Publisher: " + article.publisher + "\n"
        long_string += "Link: " + article.link + "\n"
        long_string += "Time Published: " + article.time_published + "\n"
        long_string += "Related Tickers: " + ", ".join(article.related_tickers) + "\n"
        long_string += "\n"
    return long_string


class Article:
    def __init__(self, title, publisher, link, time_published, related_tickers):
        self.title = title
        self.publisher = publisher
        self.link = link
        self.time_published = time_published
        self.related_tickers = related_tickers


def process_json_data(json_data):
    processed_data = []

    for item in json_data:
        title = item["title"]
        publisher = item["publisher"]
        link = item["link"]

        # Convert Unix timestamp to human-readable format
        timestamp = item["providerPublishTime"]
        datetime_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = datetime_object.strftime("%Y-%m-%d %H:%M")

        related_tickers = item["relatedTickers"]

        article = Article(title, publisher, link, formatted_time, related_tickers)
        processed_data.append(article)

    return processed_data


Article_prompt = 'When you see the tag ## Stock Article ###, that indicates the start of the data to process. You will process the data as follows: If the Related Tickers do not have {STOCK_TICKER}, ignore those articles. You are to pull out only those articles related to {STOCK_TICKER}. Replace "{{STOCK_TICKER}}" with the desired stock ticker you want to filter the articles for. For example, if you want to filter articles related to Apple (AAPL), you would use: When you see the tag ## Stock Article ###, that indicates the start of the data to process. You will process the data as follows: If the Related Tickers do not have AAPL, ignore those articles. You are to pull out only those articles related to AAPL.'


def process_json_data(json_data):
    processed_data = []

    for item in json_data:
        title = item["title"]
        publisher = item["publisher"]
        link = item["link"]

        # Convert Unix timestamp to human-readable format
        timestamp = item.get("providerPublishTime", [])
        if not timestamp:
            timestamp = "1672444800"
        datetime_object = datetime.fromtimestamp(timestamp)
        formatted_time = datetime_object.strftime("%Y-%m-%d %H:%M")

        # related_tickers = item['relatedTickers']
        related_tickers = item.get("relatedTickers", [])
        article = Article(title, publisher, link, formatted_time, related_tickers)
        processed_data.append(article)

    return processed_data


# Added try block to access to the file system without permissions and catch any possible error while opening and saving the file. The function returns an exception message. The file path is now provided as a return value. Hedged against changing directory paths
def save_stockinfo(symbol: str, text: str) -> str:
    try:
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{symbol}_{current_datetime}.txt"

        with open(filename, "w") as file:
            file.write(text)

        path_to_file = os.path.abspath(filename)
        return f"Content saved to {path_to_file}"
    except Exception as e:
        print(f"An error occurred while saving the file {e}")
        return "Cannot save information"


# DOES NOT WORK
def getperiodDaysfin(symb: str, perd: str) -> str:
    apple = yf.Ticker("APPL")
    print(apple)
    return apple.history(period="1mo")
    tic = yf.Ticker(symbol)
    return tic.history(period=perd)


# blankScreen()

# print(get_stock_news('TSL'))
