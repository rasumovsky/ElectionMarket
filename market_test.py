#!/usr/bin/env python
#

import raw_input
from marketDB import *

if __name__ == ' __main__':
        
    # Use a while loop to stay in game playing mode:
    readyToExit = False
    player = 'Master'
    while not readyToExit:
        
        user_input = raw_input("next command please: ")

        # Check if user is ready to quit the program:
        if user_input.Contains("quit"):
            readyToExit = True
            continue
        
        # User decides to add an election:
        elif user_input.find("add election") > 0:
            print "You want to add a new election to the game."
            contest = raw_input("What is the name of the election: ")
            opponent1 = raw_input("Who is the first candidate: ")
            opponent2 = raw_input("Who is the second candidate: ")
            addElection(contest, opponent1, opponent2)

        # User adds a player:
        elif user_input.find("add player") > 0:
            print "You want to add a player to the game."
            player = raw_input("What is the name of the new player: ")
            addPlayer(player, 200)

        # User starts as a character:
        elif user_input.find("use player") > 0:
            print "You want to use an existing player."
            player = raw_input("What is the username: ")

        # User adds an order:
        elif user_input.find("trade") > 0:
            print "You want to trade some shares."
            order = raw_input("'buy' or 'sell': ")
            candidate = raw_input("Which candidate: ")
            price = raw_input("Specify price or type 'MKT' for market value: ")
            while ((price <= 0 or price >= 100) and price != "MKT"):
                price = raw_input("Please specify price between $0 and $100 or 'MKT': ")
            quantity = raw_input("How many shares to trade? ")
            placeOrder(player, candidate, order, price, quantity):
        
        # Delete an order:
        elif user_input.find("delete order") > 0:
            print "You want to delete one of your trade orders."
            printPlayerOrders(player)
            order_id = raw_input("What is the order ID (see list above): ")
            deleteOrder(order_id)
            
        # Get information about the game:
        elif user_input.find("show") > 0:
            if user_input.find("players") > 0:
                showTable("players")
            elif user_input.find("orders") > 0:
                showTable("orders")
            elif user_input.find("elections") > 0:
                showTable("elections")
            else:
                print "I'm not sure what to show you."

        # Get ranking:
        elif user_input.find("ranking") > 0:
            getPlayerStandings();

        else:
            print "Input not recognized, please try again."

    # End of user input section.
    print "Thanks for playing, and have a nice day!"
