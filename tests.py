from market import Stock
from market import Market
from player import Player
from player import Transaction

stocks = []

for n in range(1,25):
    stocks.append(Stock(10))

for stock in stocks:
    print(stock.prices)



