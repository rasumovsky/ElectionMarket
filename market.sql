-- An SQL database for election market data
-- Author: Andrew Hard
-- Date: Sep. 23 2016

-- Connect to the market database:
\c market

CREATE TABLE players ( player_id SERIAL PRIMARY KEY, 
       	     	       username TEXT,
		       cash integer );

CREATE TABLE candidates ( candidate_id SERIAL PRIMARY KEY,
       	     	       	  candidate_name TEXT );

CREATE TABLE elections ( election_id SERIAL PRIMARY KEY,
       	     	       	 election_name TEXT, 
       	     	       	 candidate1 SERIAL REFERENCES candidates(candidate_id), 
		       	 candidate2 SERIAL REFERENCES candidates(candidate_id) );

CREATE TABLE transactions ( transaction_id SERIAL PRIMARY KEY, 
       	     		    buyer SERIAL REFERENCES players(player_id),
			    seller SERIAL REFERENCES players(player_id),
			    candidate REFERENCES candidates(candidate_id),
			    quantity integer,
			    price integer,
			    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

-- each player has 1 entry for each candidate
-- The price can be evaluated based on the most recent transaction for each market by timestamp.
CREATE TABLE positions ( position_id SERIAL PRIMARY KEY, 
       	     	       	 owner SERIAL REFERENCES players(player_id),
			 candidate SERIAL REFERENCES candidates(candidate_id), 
			 quantity integer );

-- only includes open orders
CREATE TABLE orders ( order_id SERIAL PRIMARY KEY,
       	     	      player SERIAL REFERENCES players(player_id),
		      candidate SERIAL REFERENCES candidates(candidate_id), 
		      order_type TEXT,
		      price integer,
		      quantity integer );
