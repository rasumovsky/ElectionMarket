#!/usr/bin/env python
#

#import raw_input
from marketDB import *

def getPlayerPrice():
    current_price = raw_input("Specify price from $0 to $100 or 'MKT': ")
    if int(current_price) > 0 and int(current_price) < 100:
        print "current_price1 = ", current_price
        return current_price
    elif str(current_price) == 'MKT':
        print "current_price2 = ", current_price
        return current_price
    else: 
        print "current_price3 = ", current_price
        return getPlayerPrice()

def playTheGame():
    print "Welcome to the game!"
    
    # Use a while loop to stay in game playing mode:
    readyToExit = False
    player = 'Master'
    while not readyToExit:
        
        user_input = raw_input("Please type a command ('help' for options): ")
        
        # Check if user is ready to quit the program:
        if "quit" in user_input:
            readyToExit = True
            continue
        
        # User decides to add an election:
        elif "add election" in user_input:
            print "You want to add a new election to the game."
            contest = raw_input("What is the name of the election: ")
            opponent1 = raw_input("Who is the first candidate: ")
            opponent2 = raw_input("Who is the second candidate: ")
            addElection(contest, opponent1, opponent2)

        # User adds a player:
        elif "add player" in user_input:
            print "You want to add a player to the game."
            player = raw_input("What is the name of the new player: ")
            addPlayer(player, 200)

        # User starts as a character:
        elif "use player" in user_input:
            print "You want to use an existing player."
            player = raw_input("What is the username: ")

        # User adds an order:
        elif "trade" in user_input:
            print "You want to trade some shares."
            order = raw_input("'buy' or 'sell': ")
            candidate = raw_input("Which candidate: ")
            price = getPlayerPrice()

            quantity = raw_input("How many shares to trade? ")
            placeOrder(player, candidate, order, price, quantity)
        
        # Delete an order:
        elif "delete order" in user_input:
            print "You want to delete one of your trade orders."
            printPlayerOrders(player)
            order_id = raw_input("What is the order ID (see list above): ")
            deleteOrder(order_id)
        
        # Get information about the game:
        elif "show" in user_input:
            if user_input.find("players") > 0: showTable("players")
            elif user_input.find("orders") > 0: showTable("orders")
            elif user_input.find("elections") > 0: showTable("elections")
            else: print "I'm not sure what to show you."

        # Get information about the game:
        elif "clear table" in user_input:
            if user_input.find("players") > 0: clearATable("players")
            elif user_input.find("orders") > 0: clearATable("orders")
            elif user_input.find("elections") > 0: clearATable("elections")
            else: print "I'm not sure what to show you."

        # Get ranking:
        elif "ranking" in user_input:
            getPlayerStandings();
        
        # Get list of commands:
        elif "help" in user_input:
            print "A list of commands. Each will prompt for additional inputs."
            print "\tquit - quits the game"
            print "\tadd election - adds a new election market to the game"
            print "\tadd player - adds a player to the game"
            print "\tuse player - use an existing player"
            print "\ttrade - trade shares"
            print "\tdelete order - delete one of your orders"
            print "\tshow + players, orders, or elections - show information on players, orders, or elections"
            print "\tranking - rank the players by net worth."

        else:
            print "Input not recognized, please try again."

    # End of user input section.
    print "Thanks for playing, and have a nice day!"

playTheGame()

#if __name__ == ' __main__':
#    playTheGame()

