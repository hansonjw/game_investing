from market import Stock
from market import Market
from player import Player
from player import Transaction

# I feel like I need to create some sort of matrix for the 'game state'...maybe getting a little ahead of myself
# game state = dictionary of lists...{players: , stocks: , days:}

# set up the game...get user inputs, etc....consider this as a function
# rounds, number of stocks, number of players
# def __init__(self, rounds=10, numberOfStocks = 5, numberOfPlayers = 3):

game = Market(rounds=2, numberOfStocks = 5, numberOfPlayers = 3)

game.start()

# for player in game.players:
#     print(player, player.name)

# print("should see Player, Robot, Robot")

while game.date <= game.rounds:
    game.turn()

# Instead of a generic 'status' method, do a clear 'end'
game.end()


