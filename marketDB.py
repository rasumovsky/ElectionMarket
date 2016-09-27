#!/usr/bin/env python
# 
# Market Database Interactions

import psycopg2
from psycopg2.extensions import AsIs

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=market")

def getCandidateList():
    """Get a list of all of the candidates in the game database."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT candidate_name1 as candidate_name FROM elections UNION SELECT candidate_name2 as candidate_name FROM elections ORDER BY candidate_name;")
    candidates = c.fetchall()
    DB.close()
    return candidates

def addPlayer(username, cash):
    """Add a new player to the game."""
    DB = connect()
    c = DB.cursor()
    # The player is added to the database and given $100:
    c.execute("insert into players values (%s, %s);", 
              (username, cash,))
    
    # Give the player a holding in each candidate:
    candidates = getCandidateList()
    for candidate in candidates:
        c.execute("INSERT into positions (owner, candidate, quantity) values (%s, %s, %s);", (username, candidate[0], 1,))

    DB.commit()
    DB.close()

def addElection(election_name, candidate1, candidate2):
    """Add a new election to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT into elections (election_name, candidate_name1, candidate_name2) values (%s, %s, %s);", (election_name, candidate1, candidate2,))
    DB.commit()
    DB.close()

def printPlayerOrders(player):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * from orders where player = %s ORDER BY time DESC;",
              (player,))
    order_list = c.fetchall()
    DB.close()
    for order in order_list:
        print "ID = ", order[0], " \tCandidate = ", order[2], " \tType = ", order[3], " \tPrice = $", order[4], " \tQuantity = ", order[5], " shares."
    
def showTable(tableName):
    """Show the results of a given table"""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * from %s;", (AsIs(tableName),))
    results = c.fetchall()
    for result in results:
        print result
    DB.close()

def clearATable(tableName):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from %s;", (AsIs(tableName),))
    DB.commit()
    DB.close()

def getOpponent(candidate):
    """Retrieves the opposing candidate in an election"""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT candidate_name1 as candidate FROM elections where candidate_name2 = %s UNION SELECT candidate_name2 as candidate FROM elections where candidate_name1 = %s;", (candidate, candidate,))
    opponent_name = c.fetchone()[0]
    DB.close()
    return opponent_name

def getPosition(player, candidate):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT quantity from positions where owner = %s and candidate = %s limit 1;", (player,candidate,));
    position_size = c.fetchone()[0]
    DB.close()
    return int(position_size)

def playerCashValue(player): 
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT cash from players where username = %s limit 1;",
              (player,));
    cash_value = c.fetchone()
    DB.close()
    return int(cash_value[0])

def getLastPrice(candidate):
    """Use transaction history to get last price of a share"""
    opponent = getOpponent(candidate)
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT price FROM transactions where (candidate = %s) or (candidate = %s) ORDER BY time DESC limit 1;", (candidate, opponent,))
    history = c.fetchall()
    DB.close()
    if len(history) > 0:
        return int(history[0][0])
    else:
        # The default price will be 50/50 at the game beginning:
        return 50
    
def getMatchingOrderList(candidate, order):
    """ Get most highly ranked buy or sell orders"""
    opponent = getOpponent(candidate)
    DB = connect()
    c = DB.cursor()
    # Get list of offers on the other side of the trade: 
    if order == "buy":
        # rank seller asking prices from lower to highest and time:
        c.execute("SELECT * FROM orders where (candidate = %s and order_type = 'sell') or (candidate = %s and order_type = 'buy') ORDER BY price, time;", (candidate, opponent,))
    else:
        # rank buyer bidding prices from highest to lowest, and time:
        c.execute("SELECT * FROM orders where (candidate = %s and order_type = 'buy') or (candidate = %s and order_type = 'sell') ORDER BY price DESC, time;", (candidate, opponent,))
    orderList = c.fetchall()
    DB.close()
    return orderList

def getMarketPrice(candidate, order):
    """Look up the market price for a share, else return historical price."""
    # Get a list of orders:
    matching_orders = getMatchingOrderList(candidate, order)
    # Then return the best order price:
    if len(matching_orders) > 0:
        return matching_orders[0][2]
    else:
        return getLastPrice(candidate)
    
# This is the most important method.

def placeOrder(player, candidate, order, price, quantity, useMarketPrice):
    """
    Adding a new order to the database involves the following steps:
    0. Get the market price and historical asset price
    1. Check that the buyer and seller are in a position to do so
    2. Add new order to database.
    3. Check if there is a match for the order.
    4. Determine the possible price and size of the transaction
    5. Create a new transaction record
    6. Deduct or add to player cash piles
    7. Modify player holdings
    8. Delete the smaller order and modify the larger order. 
    9. check to see if remainder of order can be placed (recursive call)
    """

    # In case a follow-up order needs to be placed:
    incomplete_order = False
    incomplete_quantity = 0
    
    # Step 0: Get prices and potential matches for the trade:
    market_price = getMarketPrice(candidate, order)
    historical_price = getLastPrice(candidate)
    matching_orders = getMatchingOrderList(candidate, order)
    
    # Calculate the trade value:
    trade_value = (int(market_price) * int(quantity)) if useMarketPrice else (int(price) * int(quantity))
        
    # Check that buyer can afford to make this trade:
    if order == 'buy' and playerCashValue(player) < trade_value:
        print "You don't have enough money for the desired trade!"
        return
    
    # Check that seller actually had shares to sell:
    if order == 'sell' and getPosition(player, candidate) < quantity:
        print "You don't have that many shares to sell! Try a smaller order"
        return

    # Connect to the database:
    DB = connect()
    c = DB.cursor()
    
    # Set the current transaction price:
    current_price = market_price if useMarketPrice else price
    
    c.execute("INSERT into orders (player, candidate, order_type, price, quantity) values (%s, %s, %s, %s, %s) RETURNING order_id;", (player, candidate, order, current_price, quantity))
    current_order_id = c.fetchone()[0]
    print "Your order has been placed on the market."

    # Check for matches to this order:
    if len(matching_orders) < 1:
        # There are no orders on the other side of the bet.
        print "No matches for the current order were found."
        DB.commit()
        DB.close()
        return
    
    # There is at least one order on the other side of the bet.
    # The best_match contains a row of the 'orders' table.
    best_match = matching_orders[0]
    
    # Conditions for matching:
    order_matched = False
    if (order == "buy" and best_match[4] <= current_price) or \
       (order == "sell" and best_match[4] >= current_price): 
        order_matched = True

        # split the difference when both bids are too generous:
        trade_price = int(0.5 * (int(current_price) + int(best_match[4])))
        # Select the purchase quantity (minimum of the two orders):
        trade_quantity = min(int(quantity), int(best_match[5]))

        ########################################
        # Perform the trade where both people are trading the same candidate:
        if candidate == best_match[2]:
            
            buyer = player if (order == 'buy') else best_match[1]
            seller = best_match[1] if (order == 'sell') else player
            c.execute("INSERT into transactions (buyer, seller, candidate, quantity, price) values (%s, %s, %s, %s, %s);", (buyer, seller, candidate, trade_quantity, trade_price,))

            # Deduct from buyer's cash and add to seller's cash:
            c.execute("UPDATE players set cash = %s where username = %s;",
                      ((playerCashValue(buyer) - trade_price), buyer,))
            c.execute("UPDATE players set cash = %s where username = %s;",
                      ((playerCashValue(seller) + trade_price), seller,))

            # Change the positions of each player:
            position_buyer = getPosition(buyer, candidate) + trade_quantity
            position_seller = getPosition(seller, candidate) - trade_quantity
            c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (position_buyer, buyer, candidate,))
            c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (position_seller, seller, candidate,))
            
        ########################################
        # Players have executed the same order but on opposing candidates,
        # which is a bank-mediated position-neutral transaction. 
        else:
            opponent = getOpponent(candidate)

            # In this case, there will be two buy transactions and two cash 
            # additions or deductions:

            # Two buyers. Add transactions, positions, and deduct cash holdings:
            if order == 'buy':
                # First customer:
                c.execute("INSERT into transactions(buyer, seller, candidate, quantity, price) values (%s, 'Master', %s, %s, %s);", (player, candidate, trade_quantity, trade_price,))
                c.execute("UPDATE players set cash=%s where username=%s;", ((playerCashValue(player) - trade_price), player,))
                pos1 = getPosition(player, candidate) + trade_quantity
                c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (pos1, player, candidate,))
                
                # Second customer:
                c.execute("INSERT into transactions(buyer, seller, candidate, quantity, price) values (%s, 'Master', %s, %s, %s);", (best_match[1], opponent, trade_quantity, trade_price,))
                c.execute("UPDATE players set cash=%s where username=%s;", ((playerCashValue(best_match[1]) - trade_price), best_match[1],))
                pos2 = getPosition(best_match[1], opponent) + trade_quantity
                c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (pos2, best_match[1], opponent,))

            # Two sellers. Add transaction, cash, and deduct positions:
            else:
                # First customer:
                c.execute("INSERT into transactions(buyer, seller, candidate, quantity, price) values ('Master', %s, %s, %s, %s);", (player, candidate, trade_quantity, trade_price,))
                c.execute("UPDATE players set cash=%s where username=%s;", ((playerCashValue(player) + trade_price), player,))
                pos1 = getPosition(player, candidate) - trade_quantity
                c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (pos1, player, candidate,))

                # Second customer:
                c.execute("INSERT into transactions(buyer, seller, candidate, quantity, price) values ('Master', %s, %s, %s, %s);", (best_match[1], opponent, trade_quantity, trade_price,))
                c.execute("UPDATE players set cash=%s where username=%s;", ((playerCashValue(best_match[1]) + trade_price), best_match[1],))
                pos2 = getPosition(best_match[1], opponent) - trade_quantity
                c.execute("UPDATE positions set quantity = %s where owner = %s and candidate = %s;", (pos2, best_match[2], opponent,))


        # Then delete or modify the orders:
        if quantity < best_match[5]:
            # delete the current bid and modify the matched bid size
            c.execute("DELETE from orders where order_id = %s;", 
                      (current_order_id,))
            c.execute("UPDATE orders set quantity = %s where order_id = %s;",
                      ((best_match[5] - quantity), best_match[0],))

        elif quantity > best_match[5]:
            # delete the matched offer and only modify current offer
            c.execute("DELETE from orders where order_id = %s;", 
                      (best_match[0],))
            c.execute("DELETE from orders where order_id = %s;", 
                      (current_order_id,))
            incomplete_order = True
            incomplete_quantity = quantity - best_match[5]
        else:
            # delete both offers (perfect match)
            c.execute("DELETE from orders where order_id = %s;", 
                      (current_order_id,))
            c.execute("DELETE from orders where order_id = %s;",
                      (best_match[0],))
    else:
        print "Other market orders do not match your price at the moment"
    
    DB.commit()
    DB.close()

    # Then submit a new order:
    if incomplete_order:
        placeOrder(player, candidate, order, price, incomplete_quantity,
                   useMarketPrice)

def deleteOrder(order_id):
    """Remove an order that was placed."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from orders where order_id = %s;", (order_id,))
    DB.commit()
    DB.close()

def getPlayerStandings():
    """Rank the players using cash + market prices of all assets."""
    print "Needs to be defined..."
