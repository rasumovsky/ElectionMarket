#!/usr/bin/env python
# 
# Market Database Interactions

import psycopg2

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
    c.execute("insert into players values (%s, %f);", 
              (username, cash,))
    
    # Give the player a holding in each candidate:
    candidates = getCandidateList()
    for candidate in candidates:
        c.execute("insert into positions (owner, candidate, quantity) values (%d, %d, %d);", (username, candidate[0], 1,))

    DB.commit()
    DB.close()

def addElection(election_name, candidate1, candidate2):
    """Add a new election to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into elections (election_name, candidate1, candidate2) values (%s, %s, %s);", (election_name, candidate1, candidate2,))
    DB.commit()
    DB.close()

def showTable(tableName):
     """Show the results of a given table"""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * from %s;", (tableName,))
    DB.close()

def clearATable(tablename):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from %s;", (tableName,))
    DB.commit()
    DB.close()

def getPosition(player, candidate):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT quantity from positions where owner = %s and candidate = %s limit 1", (player,candidate,));
    position_size = c.fetchone()
    DB.close()
    return position_size

def playerCashValue(player): 
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT cash from players where username = %s limit 1",(player,));
    cash_value = c.fetchone()
    DB.close()
    return cash_value[0]

def getLastPrice(candidate):
    """Use transaction history to get last price of a share"""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT price FROM transactions where candidate = %s ORDER BY time DESC limit 1", (candidate,))
    history = c.fetchall()
    DB.close()
    if len(history) > 0:
        return history[0][0]
    else:
        # The default price will be 50/50 at the game beginning:
        return 50
    
def getMatchingOrderList(canddate, order):
    """ Get most highly ranked buy or sell orders"""
    DB = connect()
    c = DB.cursor()
    # Get list of offers on the other side of the trade: 
    if order == "buy":
        # rank seller asking prices from lower to highest and time:
        c.execute("SELECT order_id, player, price, quantity, time FROM orders where candidate = %s and order_type = 'sell' ORDER BY price, time", (candidate, other_order))
    else:
        # rank buyer bidding prices from highest to lowest, and time:
        c.execute("SELECT order_id, player, price, quantity, time FROM orders where candidate = %s and order_type = 'buy' ORDER BY price DESC, time", (candidate, other_order))
    orderList = c.fetchall()
    DB.close()
    return orderList

def getMarketPrice(candidate, order):
    """Look up the market price for a share, else return historical price."""
    # Get a list of orders:
    matching_orders = getMatchingOrderList(candidate, order)
    # Then return the best order price:
    if len(offers) > 0:
        return matching_orders[0][2]
    else:
        return getLastPrice(candidate)
    
# This is the most important method.

def placeOrder(player, candidate, order, price, quantity):
    """
    Add a new order to the database.
    0. Get the market price.
    1. Add new order to database.
    2. Check if there is a match.
    3. Determine the size of the possible transaction
    4. Check if both participants have enough cash for the transaction.
          - if not, the orders are withdrawn.
    5. Create a new transaction record
    6. Delete the smaller order and modify the larger order. 
    7. change the cash value in both player accounts. 
    8. check to see if remainder of order can be placed (recursive call)
    """

    # Step 0: Get prices and potential matches for the trade:
    market_price = getMarketPrice(candidate, order)
    historical_price = getLastPrice(candidate)
    matching_orders = getMatchingOrderList(canddate, order)
    
    # Calculate the trade value:
    trade_value = (price == "MKT") ? market_price * quantity : price * quantity
        
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
    
    # Add the order to the database:
    if price == "MKT": 
        price = market_price
    
    c.execute("INSERT into orders (player, candidate, order_type, price, quantity) values (%s, %s, %s, %d, %d) RETURNING order_id;", (player, candidate, order, price, quantity))
    current_order_id = c.fetchone()[0]
    print "Your order has been placed on the market."

    # Check for matches to this order:
    if len(matching_orders) < 1:
        # There are no orders on the other side of the bet.
        print "No matches for the current order were found."
        return
    
    # There is at least one order on the other side of the bet.
    best_match = matching_orders[0]
    
    # Conditions for matching:
    order_matched = False
    if (order == "buy" and best_match[2] <= price) or \
       (order == "sell" and best_match[2] >= price): 
        order_matched = True
        # split the difference when both bids are too generous:
        trade_price = int(0.5 * (price + best_match[2]))
        # Select the purchase quantity (minimum of the two orders):
        trade_quantity = min(quantity, best_match[3])

        # Perform the trade:
        buyer = (order == 'buy') ? player : best_match[1]
        seller = (order == 'sell') ? best_match[1] : player
        c.execute("INSERT into transactions (buyer, seller, candidate, quantity, price) values (%s, %s, %s, %d, %d);", (buyer, seller, candidate, trade_quantity, trade_price,))
        
        # Deduct from buyer's cash and add to seller's cash:
        c.execute("UPDATE players set cash = %d where username = %s",
                  ((playerCashValue(buyer) - trade_price), buyer,))
        c.execute("UPDATE players set cash = %d where username = %s",
                  ((playerCashValue(seller) + trade_price), seller,))
        
        # Change the positions of each player:
        position_buyer = getPosition(buyer, candidate) + trade_quantity
        position_seller = getPosition(seller, candidate) - trade_quantity
        c.execute("UPDATE positions set quantity = %d where owner = %s and candidate = %s", (position_buyer, buyer, candidate,))
        c.execute("UPDATE positions set quantity = %d where owner = %s and candidate = %s", (position_seller, seller, candidate,))
        
        # Then delete or modify the orders:
        if quantity < best_match[3]:
            # delete the current bid and modify the matched bid size
            c.execute("DELETE from orders where order_id = %d", 
                      (current_order_id,))
            c.execute("UPDATE orders set quantity = %d where order_id = %d",
                      ((best_match[3] - quantity), best_match[0],))
        elif quantity > best_match[3]:
            # delete the matched offer and only modify current offer
            c.execute("DELETE from orders where order_id = %d", 
                      (best_match[0],))
            c.execute("UPDATE orders set quantity = %d where order_id = %d",
                      ((quantity - best_match[3]), current_order_id,))
        else:
            # delete both offers (perfect match)
            c.execute("DELETE from orders where order_id = %d", 
                      (current_order_id,))
            c.execute("DELETE from orders where order_id = %d", 
                      (best_match[0],))

    else:
        print "Other market orders do not match your price at the moment"

    
#order_id, player, price, quantity, time 

    DB.commit()
    DB.close()







def deleteOrder(order_id):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from open_orders where order_id = %d;", (order_id,))
    DB.commit()
    DB.close()
