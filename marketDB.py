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
        c.execute("insert into positions (owner, candidate, quantity) values (%d, %d, %d);", (username, candidate, 1,))

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
    DB.commit()
    DB.close()

def clearATable(tablename):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from %s;", (tableName,))
    DB.commit()
    DB.close()

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
    
    """
    
    DB = connect()
    c = DB.cursor()
    
    # Step 0: Get list of offers on the other side of the trade: 
    if order == "buy":
        c.execute("SELECT order_id, player, price, quantity, time FROM orders where candidate = %s and order_type = 'sell' ORDER BY price, time", (candidate, other_order))
    else:
        c.execute("SELECT order_id, player, price, quantity, time FROM orders where candidate = %s and order_type = 'buy' ORDER BY price DESC, time", (candidate, other_order))
    offers = c.fetchall()
    
    # If the offers list size is zero, then there are no open bids.
    if len(offers) < 1:
        
        # What to do about market price?

        # Try looking up value of last transaction:
        
        # Otherwise complain and say impossible...



    # Step 1: Add the new order into the database:
    c.execute("insert into orders (player, candidate, order_type, price, quantity) values (%s, %s, %s, %d, %d);", (player, candidate, order, price, quantity))
    
    # Then check for matches in the orders, etc.

    # If there is a match, then add a transaction.
    
    # Also need to check that players have enough cash for the transaction.

    DB.commit()
    DB.close()



#### WAIT, ALL WE NEED TO DO IS MATCH ORDERS...
def addTransaction(buy_order, sell_order, quantity):
    """Add a new share to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into transactions (buyer, seller, candidate, quantity, price) values (%d, %d, %d, %d, %d);", 
              (buyer_id, seller_id, candidate_id, quantity, price,))

    # ASLO MODIFY POSITIONS...
    # buyer should have cash deducted added/modified
    # seller should have cash added and position removed/modified

    DB.commit()
    DB.close()





def deleteOrder(order_id):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from open_orders where order_id = %d;", (order_id,))
    DB.commit()
    DB.close()
