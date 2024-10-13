import yfinance as yf

msft = yf.Ticker("MSFT")
print(msft.info)
print()
print(msft.balance_sheet)
print()
print(msft.history(period="1mo"))
print()
print(msft.balance_sheet)
print()
print(msft.income_stmt)

