-- An SQL database for election market data
-- Author: Andrew Hard
-- Date: Sep. 22 2016

-- Connect to the market database:
\c market

CREATE TABLE players ( player_id SERIAL PRIMARY KEY, 
       	     	       username TEXT, 
		       cash integer );

CREATE TABLE candidates ( candidate_id SERIAL PRIMARY KEY,
       	     		  candidate_name TEXT );

CREATE TABLE markets ( market_id SERIAL PRIMARY KEY,
       	     	       candidate1 SERIAL REFERENCES candidates(candidate_id),
		       candidate2 SERIAL REFERENCES candidates(candidate_id) );

CREATE TABLE transactions ( transaction_id SERIAL PRIMARY KEY, 
       	     		    buyer SERIAL REFERENCES players(player_id),
			    seller SERIAL REFERENCES players(player_id),
			    candidate SERIAL REFERENCES candidates(candidate_id), 
			    quantity integer,
			    price integer,
			    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

-- maybe better to have holdings than shares table
CREATE TABLE holdings ( holding_id SERIAL PRIMARY KEY, 
       	     	      	owner_id SERIAL REFERENCES players(player_id),
			candidate_id SERIAL REFERENCES candidates(candidate_id),
			quantity integer );
		      
CREATE TABLE orders ( order_id SERIAL PRIMARY KEY,
       	     	      player SERIAL REFERENCES players(player_id),
		      order_type TEXT,
		      price integer );
