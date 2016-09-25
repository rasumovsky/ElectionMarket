#!/usr/bin/env python
# 
# Market Database Interactions

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=market")


def addPlayer(username, cash):
    """Add a new player to the game."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (username) values (%s, %f);", 
              (username, cash,))
    DB.commit()
    DB.close()

def addCandidate(candidate):
    """Add a new candidate to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into candidates (candidate_name) values (%s);", 
              (username))
    DB.commit()
    DB.close()

def addElection(election_name, candidate_id1, candidate_id2):
    """Add a new candidate to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into elections (election_name, candidate1, candidate2) values (%s, %d, %d);", 
              (election_name, candidate_id1, candidate_id2,))
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

def addPosition(owner_id, candidate_id, quantity):
    """Add a new position (holding) to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into positions (owner, candidate, quantity) values (%d, %d, %d);", 
              (owner_id, candidate_id, quantity,))
    DB.commit()
    DB.close()

def addOrder(player_id, candidate_id, order_type, price, quantity):
    """Add a new order to the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("insert into orders (player, candidate, order_type, price, quantity) values (%d, %d, %s, %d, %d);", 
              (player_id, candidate_id, order_type, price, quantity))
    DB.commit()
    DB.close()

def clearATable(tablename):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from %s;", (tableName,))
    DB.commit()
    DB.close()

def deleteOrder(order_id):
    """Remove all rows from a given table."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from open_orders where order_id = %d;", (order_id,))
    DB.commit()
    DB.close()



#################################

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players;")
    result = (c.fetchone())[0]
    DB.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (player_name) values (%s);", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""
            SELECT players.player_id, players.player_name,
           (select count(*) from matches
            where matches.winner_id = players.player_id) as matches_won,
           (select count(*) from matches
            where players.player_id in (matches.winner_id, matches.loser_id)) as matches_played
            FROM players
            ORDER BY matches_won DESC
            """)
    
    result = c.fetchall()
    DB.close()
    return result

    """
    get wins for each player:
    select matches.winner_id, count(*) as num from matches group by matches.winner_id

    get total matches for each player:
    select players.player_id, count(*) as num2 from players left join matches where (players.player_id = matches.winner_id) or (players.player_id = matches.loser_id) group by players.player_id
    """

    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into matches (winner_id, loser_id) values (%s, %s);", (winner, loser,))
    DB.commit()
    DB.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    result = []
    standings = playerStandings()
    for index in range(0, len(standings), 2) :
        result.append([standings[index][0], standings[index][1], standings[index+1][0], standings[index+1][1]])

    return result
