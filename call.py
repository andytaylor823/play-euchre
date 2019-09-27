import random
import basicprogs as b
import showturn as s

first_round_threshold = 70
second_round_threshold = 65
power_trump = {'nine':12, 'ten':15, 'queen':20, 'king':25, 'ace':30, 'left':31, 'right':35}
power_nontrump = {'nine':1, 'ten':2, 'jack':3, 'queen':4, 'king':5, 'ace':10}

def call_first_round(hand, turn_card, pos):

	for card in hand:
		card.set_trump(turn_card.suit)
	turn_card.istrump = True
	if turn_card.name == 'jack':	turn_card.isright = True

	if pos == "d":
		new_hand = dealer_new_hand(hand, turn_card)
		power = hand_power(new_hand, pos, turn_card.suit)
	else:
		power = hand_power(hand, pos, turn_card.suit)
		
	for card in hand:
		card.remove_trump()
	
	# play around with these
	turn_card_power = card_power(turn_card)
	if pos == 'p':		power += 0.5*turn_card_power
	if pos == 'o1':		power += -0.4*turn_card_power
	if pos == 'o2':		power += -0.4*turn_card_power
	
	print(pos, ': ', power)
	if power > first_round_threshold:		return(True)
	else:						return(False)

def call_second_round(hand, turn_card, pos):
	
	# make an array of hand powers for each different suit of trump
	allsuits = ['clubs', 'diamonds', 'hearts', 'spades']
	powers = [hand_power(hand, pos, suit) for suit in allsuits]
	
	# trump cannot be what was turned down
	idx = allsuits.index(turn_card.suit)
	powers[idx] = 0
	
	# figure out the best trump suit
	idx = powers.index(max(powers))
	best_trump_suit = allsuits[idx]
	
	# stick the dealer
	if pos == 'd':
		return(best_trump_suit)
	
	# it's good to start off leading with an ace
	if pos == 'o1' and b.hand_contains(hand, "ace"):
		powers = [p+3 for p in powers]
	
	if max(powers) > second_round_threshold:	return(best_trump_suit)
	else:						return("null")


def hand_power(hand, pos, trump_suit):

	power = 0	
	for card in hand:
		power += card_power(card)
	return(power)
	
def card_power(card):

	power = -1
	n = card.name
	if card.istrump:
		if card.isleft:		n = 'left'
		elif card.isright:	n = 'right'
		else:			n = card.name
		return(power_trump[n])
	else:
		return(power_nontrump[card.name])
	
	# this is now defunct -- not as optimal
	if card.suit == trump_suit:
		if n == "nine":		power = 12
		if n == "ten":		power = 15
		if n == "queen":	power = 20
		if n == "king":		power = 25
		if n == "ace":		power = 30
		if n == "jack":		power = 35
	elif n == "jack" and card.suit == b.same_color_suit(trump_suit):
		power = 31
	else:
		if n == "nine":		power = 1
		if n == "ten":		power = 2
		if n == "jack":		power = 3
		if n == "queen":	power = 4
		if n == "king":		power = 5
		if n == "ace":		power = 10
	return(power)

def dealer_new_hand(hand, turn_card):

	cd = find_weakest_card(hand, turn_card.suit)
	new_hand = [turn_card]
	for c in hand:
		if not c.is_match(cd):
			new_hand.append(c)
#	for i in range(len(hand)):
#		if i != idx:
#			new_hand.append(hand[i])
	return(new_hand)	

# TODO:
# sometimes I want to short myself in a suit, but not always
# if I have no trump in my hand, I don't want to short myself
# if I am the dealer, I will short myself a queen and below, but will I short myself a king?
# I am much less likely to want to short myself a king if I'm not picking up trump right now
# for now, hotfix by just saying "don't ever throw off an ace or king"
def find_weakest_card(hand, trump_suit):

	discardable_hand = []
	for card in hand:
		card.set_trump(trump_suit)
		if card.istrump == False:
			discardable_hand.append(card)
			
	c = cards_of_a_suit(discardable_hand, "clubs")
	d = cards_of_a_suit(discardable_hand, "diamonds")
	h = cards_of_a_suit(discardable_hand, "hearts")
	s = cards_of_a_suit(discardable_hand, "spades")
	
	c1 = False
	d1 = False
	h1 = False
	s1 = False
	
	a = [c, d, h, s]
	a1 = [c1, d1, h1, s1]
	shortable_suits = []
	
	# check if can shorten self in any suit, but not an ace
	# do I want to short myself in a king? most of the time, no
	for i in range(len(a)):
		if len(a[i]) == 1:
			if a[i][0].name not in ["ace", "king"]:
				shortable_suits.append(a[i][0])

	if len(shortable_suits) == 1:
		return(shortable_suits[0])
	if len(shortable_suits) > 1:
		powers = [card_power(card) for card in shortable_suits]
		idx = powers.index(min(powers))
		return(shortable_suits[idx])
	
	# now, unable to short self in any suits
	# does this mean just play lowest possible card? I'll go with that for now
	sub_hand = [c for c in hand if c.suit != 'null']
	powers = [card_power(c) for c in sub_hand]
	idx = powers.index(min(powers))
	return(sub_hand[idx])	
		

def cards_of_a_suit(hand, suit, trumpsuit='null'):

	card_arr = []
	if trumpsuit == 'null':
		for c in hand:
			if c.istrump:
				if not c.isleft:	trumpsuit = c.suit
				else:			trumpsuit = b.same_color_suit(c.suit)
				break
	for card in hand:
		if card.suit == suit:
			card_arr.append(card)
		elif suit == trumpsuit:
			if card.isleft:
				card_arr.append(card)
	return(card_arr)



