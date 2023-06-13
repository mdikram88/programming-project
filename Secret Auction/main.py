from additionals import *

bidders = {}
more_bids = 'yes'

print(logo
      )
print("Welcome to Secret Auction Program")

while more_bids == 'yes':

    name = input("What's Your Name? \n")
    bid = int(input("What's Your Bid? \n"))
    more_bids = input("Are there any other bidders? Type 'Yes' or 'No': ").lower()
    bidders[name] = bid

flag = True
for name in bidders:
    if flag:
        winner_name = name
        winner_bid = bidders[name]
        flag = False
    if winner_bid < bidders[name]:
        winner_bid = bidders[name]
        winner_name = name

print()
print(f"The Winner is {winner_name} with a bid of ${winner_bid}")
