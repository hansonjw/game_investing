import random
import math
import time


class Transaction():
    def __init__(self, date, ticker, quantity, price, type):
        self.date = date
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.value = price * quantity
        self.type = type



class Player():


    def __init__(self, gameState):
        self.ledger = [] # ledger is a list of transaction objects...list = ordered
        # set up initial player ledger (dictionary) and set initial values of stocks to 0
        self.cashBalance = 1000000
        self.stockCounts = {}
        for ticker, stockObject in list(gameState.stocks.items()):
            self.stockCounts[ticker] = 0
    
        self.name = self.getName()
        self.tickerList = gameState.tickerList()


    def getName(self):
        print("Welcome player, what is your name?")
        playerName = input(">>> ")
        print(f"Very nice to meet you {playerName}")
        return playerName


    def tally(self, gameState):
        print(f"\nCash Balance: {self.cashBalance}")
        portfolioValue = self.cashBalance
        print("Stocks, quantities, and current values:")
        for ticker, count in list(self.stockCounts.items()):
            print(ticker, count, count*gameState.getPrice(ticker, gameState.date))
            portfolioValue += count*gameState.getPrice(ticker, gameState.date)
        print(f"Your total portfolio value is: {portfolioValue}\n")
        return portfolioValue


    def transact(self, transaction):
        print("\n\t","-"*50)
        print(f"\t\tProcessing transaction for {self.name}")
        print("\t","-"*50)
        print(f"\t\tDate of transaction: {transaction.date}")
        print(f"\t\tType of transaction: {transaction.type}")
        print(f"\t\tTicker Symbol: {transaction.ticker}")
        print(f"\t\tNumber of shares: {transaction.quantity}")
        print(f"\t\tTransaction price: {transaction.price}")
        print(f"\t\tTransaction value: {transaction.value}")
        print("\t","-"*50,"\n")

        if transaction.type == "buy":
            self.ledger.append(transaction)
            self.cashBalance -= transaction.value
            self.stockCounts[transaction.ticker] += transaction.quantity
        
        elif transaction.type == "sell":
            self.ledger.append(transaction)
            self.cashBalance += transaction.value
            self.stockCounts[transaction.ticker] -= transaction.quantity
        else:
            print("error")


    def buy(self, gameState):
        
        print("Which stock would you like to buy today?")
        stockChoice = self.userInput(gameState)
        while stockChoice not in gameState.tickerList():
            print("Come again, sorry I didn't catch that...please select a stock from the market")
            stockChoice = self.userInput(gameState)
        try:
            print("Great! how many shares would you like to purchase? ")
            quantity = int(self.userInput(gameState))
        except:
            print("let's try this agian...")
            self.buy(gameState)
        while quantity < 0:
            print("Sorry, I did not understand...please enter a positive integer quantity to purchase...let's try again")
            print("Again...how many shares would you like to purchase? ")
            quantity = int(self.userInput(gameState))

        currentTransaction = Transaction( gameState.date, stockChoice, quantity, gameState.getPrice(stockChoice, gameState.date), "buy")
        if currentTransaction.value > self.cashBalance:
            print("sorry, you don't have enough cash available to trade...let's try again")
            self.turn(gameState)
        else:
            self.transact(currentTransaction)



    def sell(self, gameState):

        if len(self.availableForSale()) < 1:
            print("Sorry, you do not have any stocks to sell, please try again...")
            return
        
        print("So you want to sell...here are your balances: ")
        self.tally(gameState)

        print("Which stock would you like to sell today (see list above from your available balances...")
        stockChoice = self.userInput(gameState)
        while stockChoice not in self.tickerList:
            print("Come again, sorry I didn't catch that...please select a stock from the list above")
            stockChoice = self.userInput(gameState)
        
        try:
            print("Great! how many shares would you like to sell today?")
            quantity = int(self.userInput(gameState))
        except:
            print("let's try try again...")
            self.turn(gameState)

        while quantity not in range(1, self.stockCounts[stockChoice]):
            print(f"sorry, that does not compute.  Please select an integer number of shares from 1 to {self.stockCounts[stockChoice]}")
            print("How many shares would you like to sell today?")
            quantity = int(self.userInput(gameState))

        currentTransaction = Transaction(gameState.date, stockChoice, quantity, gameState.getPrice(stockChoice, gameState.date), "sell")
        self.transact(currentTransaction)


    def turn(self, gameState):
        self.resetRobot()
        choice = ""
        while choice != "pass":
            print("What would you like to do today...buy or sell or pass?  ")
            choice = self.userInput(gameState)
            if choice == "buy":
                self.buy(gameState)
            elif choice == "sell":
                self.sell(gameState)
            elif choice == "pass":
                print("Ok, you want to pass, no problem.")
                print("As always it is a pleasure doing business with you, have a nice day!")
            else:
                print("Sorry that is not one of the options...please try again")
            self.resetRobot()

    
    def resetRobot(self):
        # ...a bit of a hacky way to do this
        # real version is in the Robot subclass...
        # couldn't avoid this without duplicating the turn function
        pass


    def availableForSale(self):
        tickersSell = []
        for ticker, count in list(self.stockCounts.items()):
            if count > 0:
                tickersSell.append(ticker)
            else:
                pass # ok, convention, don't like to leave single if statements without an else...
        return tickersSell

    
    #This method handles just the robot input, keep other functionality out of this...
    def userInput(self, gameState):

        return input(f"[{self.name}] >>> ")

    
    # Debugging tool to ensure transactions are posting
    def printLedger(self):
        print(self.ledger)
        for entry in self.ledger:
            print("\n#########")
            for key, val in list(entry.transactionData.items()):
                print(key, val)


class Robot(Player):

    def __init__(self, gameState):
        
        Player.__init__(self, gameState)
        
        #Robot Related decision
        self.turnOptions = [ "buy", "sell", "pass", "pass"] # added additional pass because robots are taking too many buy's and sell's
        self.robotDecision = {}
        self.resetRobot()

    
    def getName(self):
        robotName = random.choice( ["John P.", "Joe S.", "Steve M.", "John M.", "Geddy", "Alex", "Dave L.", "Paul", "John L.", "Ringo", "George"] )
        return robotName

    
    def resetRobot(self):
        self.robotDecision.clear()
        self.robotDecision["choice"] = ""
        self.robotDecision["ticker"] = ""
        self.robotDecision["quantity"] = 0


    def userInput(self, gameState):
        time.sleep(1)
        if self.robotDecision["choice"] == "":
            self.robotDecision["choice"] = random.choice(self.turnOptions)
            # print(f">>> {self.robotDecision["choice"]}")
            print(f"[{self.name}] >>> ", self.robotDecision["choice"])
            time.sleep(1)
            return self.robotDecision["choice"]
        elif (self.robotDecision["choice"] == "buy") and (self.robotDecision["ticker"] == ""):
            # need to return a random selection from available tickers...
            # could build more sophisticated market analysis based decision making, save for later...
            self.robotDecision["ticker"] = random.choice(self.tickerList)
            print(f"[{self.name}] >>> ", self.robotDecision["ticker"])
            time.sleep(1)
            return self.robotDecision["ticker"]
        elif (self.robotDecision["choice"] == "sell") and (self.robotDecision["ticker"] == ""):
            # return a random selection from stocks to sell, return ticker
            self.robotDecision["ticker"] = random.choice(self.availableForSale())
            print(f"[{self.name}] >>> ", self.robotDecision["ticker"])
            time.sleep(1)
            return self.robotDecision["ticker"]
        elif (self.robotDecision["choice"] == "buy") and (self.robotDecision["ticker"] != ""):
            self.robotDecision["quantity"] = random.randint( 1, math.floor(self.cashBalance / gameState.getPrice(self.robotDecision["ticker"], gameState.date)) )
            print(f"[{self.name}] >>> ", self.robotDecision["quantity"])
            time.sleep(1)
            return self.robotDecision["quantity"]
        elif (self.robotDecision["choice"] == "sell") and (self.robotDecision["ticker"] != ""):
            # need to return a quantity bounded by portfolio quantities
            self.robotDecision["quantity"] = random.randint(1, self.stockCounts[self.robotDecision["ticker"]])
            print(f"[{self.name}] >>> ", self.robotDecision["quantity"])
            time.sleep(1)
            return self.robotDecision["quantity"]