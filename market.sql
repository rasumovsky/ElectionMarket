-- An SQL database for election market data
-- Author: Andrew Hard
-- Date: Sep. 23 2016

-- Connect to the market database:
\c market

CREATE TABLE players ( username TEXT PRIMARY KEY,
		       cash integer );

CREATE TABLE elections ( election_id SERIAL PRIMARY KEY,
       	     	       	 election_name TEXT, 
       	     	       	 candidate_name1 TEXT,
		       	 candidate_name2 TEXT );

CREATE TABLE transactions ( transaction_id SERIAL PRIMARY KEY, 
       	     		    buyer TEXT REFERENCES players(username),
			    seller TEXT REFERENCES players(username),
			    candidate TEXT,
			    quantity integer,
			    price integer,
			    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

-- each player has 1 entry for each candidate
-- The price can be evaluated based on the most recent transaction for each market by timestamp.
CREATE TABLE positions ( position_id SERIAL PRIMARY KEY, 
       	     	       	 owner TEXT REFERENCES players(username),
			 candidate TEXT,
			 quantity integer );

-- only includes open orders
CREATE TABLE orders ( order_id SERIAL PRIMARY KEY,
       	     	      player TEXT REFERENCES players(username),
		      candidate TEXT,
		      order_type TEXT,
		      price integer,
		      quantity integer,
		      time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );
