-- An SQL database for election market data
-- Author: Andrew Hard
-- Date: Sep. 22 2016

-- Connect to the market database:
\c market

CREATE TABLE players ( player_id SERIAL PRIMARY KEY, 
       	     	       username TEXT, 
		       cash numeric );

CREATE TABLE candidates ( candidate_id SERIAL PRIMARY KEY, 
       	     		  candidate_name TEXT, 
			  office TEXT,
			  odds numeric );
			 
CREATE TABLE shares ( share_id SERIAL PRIMARY KEY,
       	     	      candidate_id SERIAL REFERENCES candidates(candidate_id),
		      owner_id SERIAL REFERENCES players(player_id) );

CREATE TABLE transactions ( transaction_id SERIAL PRIMARY KEY, 
       	     		    buyer_id SERIAL REFERENCES players(player_id),
			    seller_id SERIAL REFERENCES players(player_id),
			    share_id SERIAL REFERENCES shares(share_id), 
			    price numeric,
			    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

CREATE TABLE open_orders ( order_id SERIAL PRIMARY KEY,
       	     	       	   player_id SERIAL REFERENCES players(player_id), 
		       	   trade_type TEXT,
			   number_shares integer,
			   price numeric,
			   time TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

-- maybe better to have holdings than shares table
CREATE TABLE holdings ( holding_id SERIAL PRIMARY KEY, 
       	     	      	owner_id SERIAL REFERENCES players(player_id),
			candidate_id SERIAL REFERENCES candidates(candidate_id) );
		      
