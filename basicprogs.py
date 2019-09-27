import random

class card:
	name = "eight"
	suit = "none"
	istrump = False
	isleft = False
	isright = False
	def __init__(self, cardname, cardsuit, cardistrump = False):
		if cardname == "nine" or cardname == "ten" or cardname == "jack" or cardname == "queen" or cardname == "king" or cardname == "ace" or cardname == "null":
			self.name = cardname
		else:
			print("error in card name")
			exit(10)
		if cardsuit == "clubs" or cardsuit == "diamonds" or cardsuit == "hearts" or cardsuit == "spades" or cardsuit == "null":
			self.suit = cardsuit
		else:
			print("error in card suit")
			exit(10)
			
	def set_trump(self, trumpsuit):
		if trumpsuit == self.suit:
			self.istrump = True
			if self.name == 'jack':
				self.isright = True
		elif self.name == 'jack' and self.suit == same_color_suit(trumpsuit):
			self.istrump = True
			self.isleft = True
			

	def remove_trump(self):
		self.istrump = False
			
	def is_match(self, card):
		if card.name == self.name and card.suit == self.suit:
			return(True)
		else:
			return(False)

	def print_card(self):
		line = self.name + " of " + self.suit
		if self.istrump:	line += " (trump)"
		else:			line += " (not trump)"
		print(line)
	
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
	for name in names:
		for suit in suits:
			thiscard = card(name, suit)
			deck.append(thiscard)
	return(deck)

def shuffle(deck):
	random.shuffle(deck)

def deal():

	hand1 = []
	hand2 = []
	hand3 = []
	hand4 = []
	kitty = []
	
	deck = create_deck()
	shuffle(deck)
	
	hand1 = deck[0:5]
	hand2 = deck[5:10]
	hand3 = deck[10:15]
	hand4 = deck[15:20]
	kitty = deck[20:]
	
	for hand in [hand1, hand2, hand3, hand4]:
		order_hand(hand)
	
	hands = [hand1, hand2, hand3, hand4, kitty]
	return(hands)

def print_hand(hand):
	for card in hand:
		card.print_card()
	print

def same_color_suit(suit):
	if suit == "clubs":	return("spades")
	if suit == "spades":	return("clubs")
	if suit == "hearts":	return("diamonds")
	if suit == "diamonds":	return("hearts")
	if suit == "null":	return("null")

def order_hand(hand, trump_suit = "null"):
	new_hand = []
	suits = ["clubs", "diamonds", "hearts", "spades"]
	names = ["ace", "king", "queen", "jack", "ten", "nine"]
	
	
	theright = card("jack", trump_suit)
	theleft = card("jack", same_color_suit(trump_suit))

	for suit in suits:
		if suit == trump_suit:
			for acard in hand:
				if acard.is_match(theright):
					new_hand.append(acard)
			for acard in hand:
				if acard.is_match(theleft):
					new_hand.append(acard)
			for name in names:
				for acard in hand:
					if acard.name == name and acard.suit == suit and acard.name != "jack":
						new_hand.append(acard)
			
		else:
			for name in names:
				for acard in hand:
					if acard.name == name and acard.suit == suit and not (acard.name == "jack" and acard.suit == same_color_suit(trump_suit)):
						new_hand.append(acard)
						
	for i in range(len(hand)):
		hand[i] = new_hand[i]

def hand_contains(hand, string, trump_suit = "null"):

	suits = ['clubs', 'diamonds', 'hearts', 'spades']
	cards = ['nine', 'ten', 'jack', 'queen', 'king', 'ace']
	
	if string in cards:
		for card in hand:
			if card.name == string:
				return(True)
		return(False)
		
	if string in suits:
		for card in hand:
			if card.suit == string:
				return(True)
		return(False)
		
	if string == 'right':
		for card in hand:
			if card.name == "jack" and card.suit == trump_suit:
				return(True)
		return(False)	
	
	if string == 'left':
		for card in hand:
			if card.name == "jack" and card.suit == same_color_suit(trump_suit):
				return(True)
		return(False)
	
	# non-trump ace
#	if string == 'nta':
	
	print('invalid "contains" parameter')
	exit(10)

def make_copy(old_card):

	c1 = card(old_card.name, old_card.suit)
	if old_card.istrump:
		c1.istrump = True
		if old_card.isleft:	c1.isleft = True
		if old_card.isright:	c1.isright = True
	return(c1)
	
	

