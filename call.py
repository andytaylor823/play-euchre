# This file has been checked through, and it is compatible with the board and isleft/isright updates
# This file is also compatible with the "__eq__" and "__str__" updates.
# It is as efficient as I think it can be right now.
# Most recent check: 12/3/2019
#
# functions contained in here (assume no args unless stated otherwise):
#
# (1) "call_first_round":	Takes position and board as args. Returns True if the player's hand
#				has a power greater than the threshold required to call trump, based
#				on the turn card's suit. All cards (except the turn card) are assumed
#				non-trump before being fed into this function, and all cards (except
#				the turn card) have trump removed after being fed into this function.
#
# (2) "call_second_round":	Takes position and board as args. Returns the trump suit the player will
#				call if the hand's power in that suit is greater than the required threshold,
#				otherwise returns "null". All cards are assumed non-trump before being 
#				fed into this function, and all cards have trump removed after being
#				fed into this function.
#
# (3) "hand_power":		Takes hand, position, and trump suit as required args. Returns the sum power
#				of the hand. This power includes the power of each individual card, as
#				well as the additional power by being short-suited.
#
# (4) "card_power":		Takes one card as an arg. Returns the power associated with the card in a vacuum.
#
# (5) "dealer_new_hand":	Takes a hand and the turn_card as args. Returns a new hand, given by
#				substituting the turn card in place of the weakest card in the dealer's hand.
#
# (6) "find_weakest_card":	Takes a hand as a required arg and trump_suit as an optional arg. Returns a 
#				single card, the weakest card in the hand. It first tries to short the hand in a
#				non-trump suit (though it will not do this if there is no trump in the hand).
#				If there are no shortable suits, it returns the card with the lowest raw power.
#				Right now, it does not return a short-suit ace or king.
#
# (7) "absolute_weakest_card":	Helper function for the "find_weakest_card" function. Takes a hand as an arg.
#				Returns the card with the minimum raw power in the hand. This function
#				does not take short-suits or anything else into consideration -- just raw card power.
#
# (8) "cards_of_a_suit":	Takes a hand and suit as required args and the trump_suit as an optional arg. Returns
#				a subset of the input hand, containing only cards that belong to the given suit.
#				First searches for a trump card in the hand to determine the trump_suit if not
#				provided. If the trump_suit is known, then the left may be appropriately considered
#				when determining which suit a card belongs to.

import random
import basicprogs as b
import showturn as s
import numpy as np

short3, short2, short1 = [40, 20, 10]
power_trump = {'nine':12, 'ten':15, 'queen':20, 'king':25, 'ace':30, 'left':31, 'right':35}
power_nontrump = {'nine':1, 'ten':2, 'jack':3, 'queen':4, 'king':5, 'ace':10}

# Given a player's position, access the board to determine whether they should order it up or not
def call_first_round(pos, board):

	# first set all cards in the hand to trump, according to the turn card's suit
	hand = board.pos_hand_dict[pos]
	for c in hand:	c.set_trump(board.turn_card.suit)

	# if you're the dealer, get a new hand including the turn card
	# get the power of your (possibly new) hand
	if pos == "d":	power = hand_power(dealer_new_hand(hand, board.turn_card), 	pos, board.turn_card.suit)
	else:		power = hand_power(hand,					pos, board.turn_card.suit)
	
	# remove trump from all cards (except the turn card)
	for c in hand:	c.remove_trump()
	
	# get more or less power based on the turn card and where you're sitting
	# play around with these
	turn_card_power = card_power(board.turn_card)
	if pos == 'p':		power += 0.5*turn_card_power
	if pos == 'o1':		power += -0.4*turn_card_power
	if pos == 'o2':		power += -0.4*turn_card_power
	
	# print your hand power
	if board.show_each_turn:
		print(pos, ': ', power, '\t\tFirst Round')

	# return whether you call trump or not, and if you're going alone
	return(power > board.first_round_threshold, power > board.going_alone_threshold)

# Given a player's position, access the board to determine whether or not they can call trump in the 2nd round of calling
def call_second_round(pos, board):

	hand = board.pos_hand_dict[pos]
	
	# make an array of hand powers for each different suit of trump
	allsuits = ['clubs', 'diamonds', 'hearts', 'spades']
	powers = [0,0,0,0]
	for i in range(4):
		s = allsuits[i]
		
		# trump cannot be what was turned down
		if s == board.turn_card.suit:
			powers[i] = 0
			continue
		
		# set each card as trump, get the hand power for that suit, then remove all trump
		for c in hand:	c.set_trump(s)
		powers[i] = hand_power(hand, pos, s)
		for c in hand:	c.remove_trump()
			
	# figure out the best trump suit
	idx = powers.index(max(powers))
	best_trump_suit = allsuits[idx]
	
	# print your 2nd-round power
	if board.show_each_turn:
		print(pos, ': ', max(powers), '\t\tSecond Round')
	
	# it's good to lead off with an off-suit ace
	if pos == 'o1':
		ace_suits = [c.suit for c in hand if c.name == 'ace']
		# always have an offsuit ace
		if len(ace_suits) >= 2:	powers = [p+5 for p in powers]
		# have an offsuit ace only if the one suit is not trump
		if len(ace_suits) == 1:	powers = [powers[i]+5 for i in range(len(powers)) if allsuits[i] != ace_suits[0]]	
	
	mp = max(powers)
	# stick the dealer
	if pos == 'd':				return(best_trump_suit, mp > board.going_alone_threshold)
	
	# possibly return the trump suit
	if mp > board.second_round_threshold:	return(best_trump_suit, mp > board.going_alone_threshold)
	else:					return("null", False)

# returns the power of an entire hand
# tries to account for being short in suits
def hand_power(hand, pos, trump_suit):

	# power of a hand just associated with the cards alone
	power = 0	
	for card in hand:
		power += card_power(card)
	
	# power of a hand due to being short-suited
	n_of_suits = []
	suits_have = {}
	for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
		nc = len(cards_of_a_suit(hand, suit, trump_suit))
		if nc != 0:	suits_have[suit] = nc
		n_of_suits.append(nc)
	
	# if you're short in trump, the benefit of being short-suited is gone
	n_suits = sum(np.array(n_of_suits) != 0)
	scale = int(trump_suit in suits_have)
	
	# check these numbers?
	if n_suits == 1:	power += short3*scale
	elif n_suits == 2:	power += short2*scale
	elif n_suits == 3:	power += short1*scale
	else:			power += 0
	
	return(power)

def n_suits(hand, trump_suit):
	n_of_suits = []
	suits_have = {}
	for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
		nc = len(cards_of_a_suit(hand, suit, trump_suit))
		n_of_suits.append(nc)
	
	# if you're short in trump, the benefit of being short-suited is gone
	n_suits = sum(np.array(n_of_suits) != 0)
	return(n_suits)


# returns the power of a single card -- assumes it is already labelled as trump	
def card_power(c):

	if c.suit == 'null':		return(0)
	if c.istrump:
		if c.isleft:		n = 'left'
		elif c.isright:		n = 'right'
		else:			n = c.name
		return(power_trump[n])
	else:
		return(power_nontrump[c.name])

# finds the weakest card in the dealer's hand and replaces it with the turn card
def dealer_new_hand(hand, turn_card):

	weakest = find_weakest_card(hand, turn_card.suit)
	new_hand = [c for c in hand if c != weakest]
	new_hand.append(turn_card)
	return(new_hand)	

# TODO:
# For now, just say that I won't throw off an ace, but I'll throw off everything else
def find_weakest_card(hand, trump_suit = 'null'):


	# first look to throw off some non-trump
	if trump_suit != 'null':
		for c in hand:	c.set_trump(trump_suit)
	discardable_hand = [c for c in hand if not c.istrump]

	# if we have no trump, then we don't really want to throw off a suit -- just play lowest card
	ntrump = sum([c.istrump for c in hand])
	if ntrump == 0:			return(absolute_weakest_card(hand))
	
	# check if there's only 0 or 1 possible cards to discard
	if len(discardable_hand) == 0:	return(absolute_weakest_card(hand))
	if len(discardable_hand) == 1:	return(discardable_hand[0])
	
	# sort the cards according to their suit
	c, d, h, s = [cards_of_a_suit(discardable_hand, s) for s in ['clubs', 'diamonds', 'hearts', 'spades']]
	shortable_cards = []
	
	# check if can shorten self in any suit, but not an ace
	# do I want to short myself in a king? most of the time, yes
	for suit_hand in [c, d, h, s]:
		if len(suit_hand) == 1:
			if suit_hand[0].name not in ['ace']:
				shortable_cards.append(suit_hand[0])

	# if only one shortable suit, return that card
	if len(shortable_cards) == 1:
		return(shortable_cards[0])
	
	# if several options, pick the one with the weakest card to throw off
	if len(shortable_cards) > 1:
		powers = [card_power(c) for c in shortable_cards]
		idx = powers.index(min(powers))
		return(shortable_cards[idx])
	
	# now, unable to short self in any suits
	# does this mean just play lowest possible card? I'll go with that for now
	return(absolute_weakest_card(hand))

# simple function to get the card with the lowest power, regardless of shorting suits
# this method is 5x faster than using numpy to look at 
def absolute_weakest_card(hand):
	sub_hand = [c for c in hand if c.suit != 'null']
	if len(sub_hand) == 0:
		print('ahhh, no non-null cards')
		[print(c) for c in hand]
	powers = [card_power(c) for c in sub_hand]
	
	idx = powers.index(min(powers))
	return(sub_hand[idx])

# returns the cards in a hand belonging to a given suit -- accounts for trump
def cards_of_a_suit(hand, suit, trumpsuit='null'):

	card_arr = []
	# if the trump suit is not given, we must find out ourselves to see if we're stepping on any trump
	# e.g. if we're looking for spades, but we have the jack of clubs in our hand
	# The selection criteria are different if we're looking at trump or not
	if trumpsuit == 'null':
		for c in hand:
			if c.istrump:
				if not c.isleft:	trumpsuit = c.suit
				else:			trumpsuit = b.same_color_suit(c.suit)
				break
		
	if suit == trumpsuit:	card_arr = [c for c in hand if c.istrump]
	else:			card_arr = [c for c in hand if c.suit == suit and not c.isleft]
	return(card_arr)



