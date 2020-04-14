# This file has been checked through, and it is compatible with the board and isleft/isright updates
# It is also compatible with the "__str__" and "__eq__" updates
# Most recent check: 12/6/2019
#
# functions contained in here (assume no args unless stated otherwise):
# (1) "class card":		creates the entire card class
#	(1a) ---"set_trump":		takes trumpsuit as arg and only sets self to trump if suit
#					matches, or if it's the right/left. Sets isright/isleft appropriately
#
#	(1b) ---"copy":			makes an exact copy of the card, to avoid passing by reference errors
#
#	(1c) ---"remove_trump:		sets all trump-related attributes to False
#
#	(1d) ---"is_match":		compares another card with itself to see if name & suit match (not trump attributes tho)
#	^This is now obsolete, all else needs to be adjusted around this
#
#	(1e) ---"print_card":		just an easily accessible way to print out the card, e.g. "ace of clubs (not trump)"
#	^This is now obsolete, all else needs to be adjusted around this
#
#	(1f) ---"set_null":		sets name and suit to "null" and sets trump attributes to False
#
# (2) "create_deck": 		just makes a 24 card deck in order
#
# (3) "shuffle_deck":		takes a deck as arg, shuffles it in place
#
# (4) "deal":			calls the two deck args above, divides the shuffled deck into 4 hands and a kitty
#
# (5) "print_hand":		takes a card array as arg, prints each card out using the card.print_card fn
#
# (6) "same_color_suit":	takes a suit name as arg, returns the string of the suit of the same color
#
# (7) "order_hand":		takes a card array as required arg, trump suit as optional arg. Loops over all cards
#				in the array and puts them in descending order by power (ace, king, queen, etc., putting
#				the right and the left before the ace in the trump suit)
import random

class card:
	name = "eight"
	suit = "none"
	istrump = False
	isleft = False
	isright = False
	def __init__(self, cardname, cardsuit, istrump = False, isleft = False, isright = False):
		self.name = cardname
		self.suit = cardsuit
		self.istrump = istrump
		self.isleft = isleft
		self.isright = isright
	
	def __eq__(self, other):
		if isinstance(other, card):
			return(self.suit == other.suit and self.name == other.name)
		return(False)
	
	def __str__(self):
		line = self.name.capitalize() + ' of ' + self.suit.capitalize() + ' ('
		if not self.istrump:	line += 'not '
		line += 'trump)'
		return(line)
			
	def set_trump(self, trumpsuit):
		if trumpsuit == self.suit:
			self.istrump = True
			if self.name == 'jack':
				self.isright = True
		elif self.name == 'jack' and self.suit == same_color_suit(trumpsuit):
			self.istrump = True
			self.isleft = True
	
	def copy(self):
		c = card(self.name, self.suit, self.istrump, self.isleft, self.isright)
		return(c)		

	def remove_trump(self):
		self.istrump = False
		self.isleft = False
		self.isright = False
	
	def set_null(self):
		self.suit = "null"
		self.name = "null"
		self.istrump = False
		self.isright = False
		self.isleft = False

def create_deck():

	names = ["nine", "ten", "jack", "queen", "king", "ace"]
	suits = ["clubs", "diamonds", "hearts", "spades"]
	deck = []
	
	for n in names:
		for s in suits:
			c = card(n, s)
			deck.append(c)
	return(deck)

def shuffle(deck):	random.shuffle(deck)

def deal():
	
	deck = create_deck()
	shuffle(deck)
	
	hand1, hand2, hand3, hand4 = [deck[(5*i):(5*(i+1))] for i in range(4)]
	kitty = deck[20:]
	
	for hand in [hand1, hand2, hand3, hand4]:
		order_hand(hand)
	
	hands = [hand1, hand2, hand3, hand4, kitty]
	return(hands)

def print_hand(hand):
	for card in hand:
		print(card)
	print

def same_color_suit(suit):
	if suit == "clubs":	return("spades")
	if suit == "spades":	return("clubs")
	if suit == "hearts":	return("diamonds")
	if suit == "diamonds":	return("hearts")
	if suit == "null":	return("null")

def order_hand(hand, trump_suit = "null"):

	# if it's all null, return exactly the hand
	if sum([c.suit == 'null' for c in hand]) == 5:	return(hand)

	new_hand = []
	suits = ["clubs", "diamonds", "hearts", "spades"]
	names = ["ace", "king", "queen", "jack", "ten", "nine"]

	for s in suits:
		if s == trump_suit:
			for c in hand:
				if c.isright:	new_hand.append(c)
			for c in hand:
				if c.isleft:	new_hand.append(c)
			for n in names:
				for c in hand:
					if c.name == n:
						if c.suit == s:
							if c.name != "jack":
								new_hand.append(c)			
		else:
			for n in names:
				for c in hand:
					if c.name == n:
						if c.suit == s:
							if not c.isleft:
								new_hand.append(c)						
	for i in range(len(hand)):
		hand[i] = new_hand[i]

def partner(pos):
	if pos == 'o1':	return('o2')
	if pos == 'p':	return('d')
	if pos == 'o2':	return('o1')
	if pos == 'd':	return('p')
