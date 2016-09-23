# ElectionMarket
A market-based game for guessing the outcome of an election.

## Game overview
Players start out with $100 in cash and $100 in the form of shares. During 
gameplay, players buy and sell shares in candidates for the purpose of 
maximizing their net worth. 

### Winning the game
After the election is held and share valuations are made, player rankings are
determined by net worth. The highest net-worth player is the winner.

### Shares in candidates
Each share has a price range of $0-$100. During the game, and prior to the 
election, share prices are determined by the bid and ask prices of players 
wanting to buy and sell candidate shares, respectively. The market is closed
once the electoral outcome is decided, and further trades are prohibited. At
that time, shares of losing candidates are valued at $0 while shares of winning 
candidates are valued at $100. 

While holding shares in candidates that are expected to win is a good way to 
gain money, larger profits (and losses) can be made in the short term by 
trading on stock price fluctuations. One strategy is to buy shares that you view
as undervalued. For example, a $10 share could be considered undervalued if it
represented a candidate with a 40% chance of winning. The expected return on 
your $10 investment would be $40.

### Trading
The market functions by matching buyers and sellers. Trades do not occur if 
there are no buyers and sellers willing to "meet in the middle". 

#### Buying shares
There are several ways to buy shares:
 - buy at market price: purchase shares at the lowest (or last) asking price,
 - buy at specified price: specify a maximum price you will pay for shares.

Note that neither buy order is guaranteed to go through. If there are no sellers
willing to meet your prices, no transaction can occur. One way to increase the
likelihood that someone will sell you shares is to increase your bid price.

#### Selling shares
There are two ways to sell shares as well:
 - sell at market price: sell shares at the highest (or last) bid price,
 - sell at specified price: specify a minimum sales price for your shares. 

As with buy orders, sell orders are not guaranteed to go through. There must be
someone in the market willing to buy your shares. One way to increase the 
probability that someone will buy your shares is to decrease your asking price.

#### Partial transactions:
Note that in cases where the number of shares for sale is not equal to the 
number of shares for purchase, only part of the larger transaction will occur. 

