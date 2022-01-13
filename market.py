import random
import string
from player import Player, Robot
import time
import math

class Market():

    def __init__(self, rounds=10, numberOfStocks = 5, numberOfPlayers = 3):

        # A lot of this might need to be in the "start" method...or perhaps this is the start method...or perhaps the 'start' is a different class altogether???
        self.rounds = rounds
        self.date = 1
        self.numberOfStocks = numberOfStocks
        self.numberOfPlayers = numberOfPlayers
        self.stocks = {} # Set as a dictionary such that each stock can be called by it's ticker symbol
        self.players = [] ### This should also be a dictionary...well maybe not

        for n in range(0, self.numberOfStocks):
            new_stock = Stock(self.rounds)
            self.stocks[new_stock.ticker] = new_stock

        for n in range(0, self.numberOfPlayers):
            if n == 0:
                self.players.append(Player(self))
            else:
                self.players.append(Robot(self))


    def start(self):
        print("\n")
        print("Welcome the stock market simulation game!")
        print(f"This is a turn based game with {self.numberOfPlayers} players.")
        print("You begin the game with a sum of cash and an empty portfolio.")
        print(f"There will be {self.numberOfStocks} stocks in the market for you to choose from each day.")
        print("During each turn you will be presented with the list of stocks and the current prices for the day.")
        print("When it is your turn you will be presented with the options to buy and/or sell stocks.")
        print("The prices will shift and change each day.")
        print("The player with the most valuable portfolio at the end of the game wins.")
        print(f"There will be {self.rounds} rounds, or trading days, in the game.")
        print("\n")
        print("Are you ready to get started?")
        answer = input(">>> ")
        if answer != "no":
            print("Great, good luck!")
        else:
            print("ok, well, we'll be here when you're ready to play")
            quit()
        # lots of print statements, etc...import text??  Just to keep stuff clean?  also, might be a good exercise in modules??
        # Write out the code now then modulurize later if it makes sense to do so
        # Feel like there is a whole world of possiblitiy in definining a new Class to print out messages to the user...user interface...
        # This is a good start...refactor, refactor...wait until you get some other user interfaces going before you decide to 'consolidate'


    # More of a debugging tool than a game function at this point...
    def status(self):
        print(f"Rounds in the game: {self.rounds}")
        print(f"The current date or round is: {self.date}")
        print(f"Number of Players: {self.numberOfPlayers}")
        print(f"Size of the Market: {self.numberOfStocks} stocks in the market")
        print("The stock market prices are:")
        
        for ticker, stock in list(self.stocks.items()):
            stock.printData()
        
        for player in self.players:
            print(player.name)
    
    
    def end(self):
        # set the date back to the last day of trading to summarize statistics...
        # Current strategy is for main game play loop to be guided by date and rounds
        # self.date -= 1
        print('\n')
        print('*'*50)
        print("That is the end of trading!")
        print('*'*50)
        print('\n')
        print("Here are the results:")

        resultsUnranked = [] #list of tuples, unsorted
        resultsValues = [] #list of numbers, to be sorted later
        resultsRanked = [] #list of tuples, sorted...

        # add data to resultsUnranked and resultsValues
        for player in self.players:
            # This just prints each player's result utlizing player.tally() method
            print("\n")
            print(f"{player.name}, your portfolio is as follows:")

            playerResult = player.tally(self)   # I really don't like this method(self)/gameState approach...need to factor all of that out of player
            resultsUnranked.append( (player.name, playerResult) ) #tuple
            resultsValues.append(playerResult)
        
        # sort the resultsValues
        resultsValues.sort(reverse=True)
        
        # now compare each element in resultsUnranked to sorted resultsValues and append to resultsRanked
        for result in resultsValues:
            for player in resultsUnranked:
                if (player[1] == result) and (player not in resultsRanked):
                    resultsRanked.append(player)
                else:
                    pass
        
        # This is good enough for now, however, I should get more sophisticated with the output        
        print("Ranked results as follows:")
        print(resultsRanked)
        print(f"And the winner is: {resultsRanked[0][0]}!!  Congratulations!!")
        print("Thank you for playing")
        

    def turn(self):
        # loop through each player and execute a game turn...
        print('\n')
        print('*'*50)
        print(f"Welcome to day {self.date} of {self.rounds} on the trading floor...")
        print('*'*50)
        print('\n')
        time.sleep(1)
        for player in self.players:
            # consider some white space and * to make the output clearer that it's a player's turn...
            playerSignal = f"It is {player.name}'s turn..."
            playerSignalLength = len(playerSignal)
            playerSignalStar = 3
            playerSignalWhite = int(math.floor( (50 - playerSignalLength) / 2 ) - playerSignalStar)
            playerSignalRemainder = 50 - 2*playerSignalStar - 2*playerSignalWhite - playerSignalLength
            
            print("\n")
            print("-"*50)
            print( ("*"*playerSignalStar)+(" "*playerSignalWhite)+(f"It is {player.name}'s turn...")+(" "*(playerSignalWhite + playerSignalRemainder))+("*"*playerSignalStar) )
            print("-"*50)
            time.sleep(1)

            # print out player portfolio
            print(f"{player.name}, here is your portfolio summary:")
            #player.someMethodToDisplayPortfolio...
            player.tally(self)
            time.sleep(1)

            # print out prices for each stock
            print("Here are the market prices and trends:")
            for ticker in self.tickerList():
                self.stocks[ticker].printPrices(self.date)  
            print("")  #printing one blank line (not two)
        
            player.turn(self)
            print("\n")

          
        self.date += 1


    def tickerList(self):
        list_of_tickers = []
        for ticker, stock in list(self.stocks.items()):
            list_of_tickers.append(ticker)
        return list_of_tickers


    def getPrice(self, ticker, day):
        return self.stocks[ticker].prices[day]




class Stock():

    def __init__(self, tradingDays):

        self.ticker = ""
        for n in range(0, 3):
            self.ticker += random.choice(string.ascii_uppercase)
        self.prices = self.priceMatrix(tradingDays)


    def printData(self):
        print(f"\n#####\nHere are the prices for {self.ticker}")
        for day, price in list(self.prices.items()):
            print(f"Day {day} price: {price}")
        print("\n")
    
    def printPrices(self, date):
        print(f"**{self.ticker}** ", end = '')
        for day in range (1, date+1):
            print(f"day {day}: {self.prices[day]}  ", end = '')
        print("")


    def priceMatrix(self, tradingDays):
        # Ok, now get into the shape and gaming aspects of the price curve...need to brainstorm...don't stare at code

        baseCurveRate = 0.05
        baseCurveRates = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
        startPrice = random.randint(1, 100)
        eventWinner = random.randint(1, tradingDays)

        # just for testing and debugging, can add this to the return statement
        eventLog = {}

        matrix = {}

        # generate base curve, keep in mind range() excludes last number, it's exclusive, this trips me up a lot
        for day in range(1,tradingDays+2): # +2 needed to generate a list of 1 greater than the number of rounds, so there is a final price, remember range() is exclusive
            if day == 1:
                matrix[day] = startPrice
            else:
                # roll dice on event...this logic is wrong...well, perhaps not...the idea is to have ~one shock per stock in the course of the game on average
                if random.randint(1, tradingDays) == eventWinner:
                    upOrDownEvent = random.choice( [-1, 1] )
                    dayPrice = matrix[day-1] + upOrDownEvent * matrix[day-1] * random.random()

                    # reset baseline...50/50 chance when event occurs
                    if random.choice(['yes', 'no']) == 'yes':
                        baseCurveRate = random.choice(baseCurveRates) * upOrDownEvent
                    else:
                        pass

                    eventLog[day] = ["yes", round( 100 * (dayPrice - matrix[day-1])/matrix[day-1], 0), baseCurveRate]
                
                else:
                    dayPrice = matrix[day-1] * (1 + baseCurveRate)

                matrix[day] = round( dayPrice, 4 )
                
        #layer on noise here, utilize list of keys for matrix dictionary...this always seems to trip me up

        return matrix