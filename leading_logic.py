import basicprogs as b
import boardstate_class as bsc
import rule_class as rc
import call

def return_card(board, pos):
	for r in leading_logic:
		c = r.is_satisfied(board, pos)
		if c is not None:	return(c)
	print('Error: no card returned to lead!')
	raise(ValueError)


def right_on_3(board, pos):
	hand = board.pos_hand_dict[pos]
	tnum = 1+sum([c.name == 'null' for c in hand])
	if tnum == 3:
		for c in hand:
			if c.isright:
				return(c, True)
	return(None, False)

def offsuit_ace(board, pos):

	hand = board.pos_hand_dict[pos]
	# start by looking at suits that have not yet been led
	led_cards = board.all_cards_played[::4]
	led_suits = [c.suit for c in led_cards]
	for c in hand:
		if c.name == 'ace':
			if not c.istrump:
				if c.suit not in led_suits:
					return(c, True)
	
	# it's still okay to lead an ace in a suit that's already been led?
	for c in hand:
		if c.name == 'ace':
			if not c.istrump:
				return(c, True)
	return(None, False)

def caller_awkward_spot(board, pos):

	hand = board.pos_hand_dict[pos]
	tnum = 1+sum([c.name == 'null' for c in hand])

	# make sure it's not the first trick
	if tnum == 1:	return(None, False)
	
	# check if the one who called trump is sitting to my left
	my_pos = board.leader_pos
	left_of_me_pos = board.all_pos[(board.all_pos.index(my_pos) + 1)%4]
	if left_of_me_pos != board.caller_pos:
		return(None, False)
	
	# create arrays of all cards/suits that have been led (but not trump)
	led_cards = board.all_cards_played[::4]
	led_suits = [c.suit for c in led_cards if not c.istrump]

	# one way I could do this is loop over card names (starting from ace, then to king,
	# then to queen, etc.) and also loop over all cards in the hand that match led suits
	# to see if I have an ace that meets the suit reqs, or if I have a king, or...etc.
	# this feels inefficient though, so I would like to see if I can do it better

	# "led_suits" should be max 3 items long, so seeing if an item is in that array is pretty fast
	have = False
	return_card = None
	min_priority = 7
	card_names = {'ace':1, 'king':2, 'queen':3, 'jack':4, 'ten':5, 'nine':6}
	
	# goes through each card in hand and each suit in led_suits
	# approx 5x2 processes
	for c in hand:
		# see if the criteria is met
		if c.istrump:				continue
		if c.suit not in led_suits:		continue
		if card_names[c.name] > min_priority:	continue
		
		# if it is met, store that it's met, 
		# the "strength" of the highest card that meets the criteria,
		# and the card itself
		have = True
		min_priority = card_names[c.name]
		return_card = c
		
	if have:	return(return_card, True)
	else:		return(None, False)

def partners_jack(board, pos):
	hand = board.pos_hand_dict[pos]
	if pos == 'd':		partner_pos = 'p'
	elif pos == 'p':	partner_pos = 'd'
	elif pos == 'o1':	partner_pos = 'o2'
	else:			partner_pos = 'o1'
	
	if board.caller_pos == partner_pos:
		for c in hand:
			if c.isright:	return(c, True)
			if c.isleft:	return(c, True)
	return(None, False)

def offsuit_king(board, pos):

	hand = board.pos_hand_dict[pos]
	# start by looking at suits that have not yet been led
	led_cards = board.all_cards_played[::4]
	led_suits = [c.suit for c in led_cards]
	for c in hand:
		if c.name == 'king':
			if not c.istrump:
				if c.suit not in led_suits:
					return(c, True)
	
	# it's still okay to lead an ace in a suit that's already been led?
	for c in hand:
		if c.name == 'king':
			if not c.istrump:
				return(c, True)
	return(None, False)

def highest_remaining_trump(board, pos):
	
	hand = board.pos_hand_dict[pos]
	ntrump = sum([c.istrump for c in hand])
	if ntrump == 0:		return(None, False)
	
	# finding the best card in hand first
	max_hand_power = 0
	top_card = hand[0]
	for c in hand:
		if not c.istrump:	continue
		if call.card_power(c) > max_hand_power:
			max_hand_power = call.card_power(c)
			top_card = c
	
	# find all the trump cards that have been played
	played_powers = {call.card_power(c) for c in board.all_cards_played if c.istrump}
	
	# go in descending order to see if the card has (1) been played or (2) is in hand
	trump_powers = [35, 31, 30, 25, 20, 15, 12]
	for p in trump_powers:
		if p in played_powers:	continue
		else:
			if p == max_hand_power:
				return(top_card, True)
			else:
				return(None, False)

# if you as the partner took 2 tricks already and your partner has zero (or even 1), lead trump to let them get the trick
def carry_the_team(board, pos):

	hand = board.pos_hand_dict[pos]
	# only works if the partner of the caller is leading
	if board.leader_pos != b.partner(board.caller_pos):	return(None, False)

	# only after the partner has taken 2 tricks (though maybe just one is fine?)
	if board.winners.count(board.leader_pos) < 2:		return(None, False)
	
	# gotta lead trump
	if sum([c.istrump for c in hand]) == 0:			return(None, False)
	
	trump_hand = [c for c in hand if c.istrump]
	powers = [call.card_power(c) for c in trump_hand]
	idx = powers.index(min(powers))
	return(trump_hand[idx], True)

# only lead trump if you have 3/4 or 4/5 trump, not 3/5 or 2/4 or 2/3
# or if your highest card is a 9 or 10?
def lead_trump(board, pos):

	hand = board.pos_hand_dict[pos]
	tnum = 1+sum([c.name == 'null' for c in hand])
	ntrump = sum([c.istrump for c in hand])
	ncards = 6-tnum
	frac_trump = ntrump/ncards
	if frac_trump < 0.75:
		return(None, False)
		
	trumps = [c for c in hand if c.istrump]
	power = [call.card_power(c) for c in trumps]
	idx = power.index(min(power))
	return(trumps[idx], True)
		
# best card from hand, specifically not trump
def highest_card(board, pos):

	hand = board.pos_hand_dict[pos]	
	non_trumps = [c for c in hand if (not c.istrump and c.suit != 'null')]
	power = [call.card_power(c) for c in non_trumps]
	idx = power.index(max(power))
	
	return(non_trumps[idx], True)


# returns the nth highest (1st, 2nd, etc.) unplayed trump card and whether that card is in your hand
def nth_highest_remaining_trump(board, pos, n=1):

	hand = board.pos_hand_dict[pos]
	played_trump_powers = {call.card_power(c) for c in board.all_cards_played if c.istrump}
	trump_powers = [35, 31, 30, 25, 20, 15, 12]
	
	# need to time this to see which is faster
	# The Problem: Want to compare the played powers with the possible powers of trump cards
	#	       Want to find the nth power that has not been played so far
	#	       Want to transform that into a card, then return that card
	
	# Method 1:
	# Look at all the powers, then turn the power into a card by making use of call's power_trump dictionary
	# I would need to loop through the power_trump dictionary to find the right name
	
	# As I'm writing this out, I can see that Method 1 is just clearly the best, so I won't even write out Method 2.
	
	for p in trump_powers:
		if p in played_trump_powers:	n -= 1
		if n == 0:
			for key in call.power_trump:
				if call.power_trump[key] == p:
					if key == 'right':		c = b.card('jack', board.trump_suit, istrump = True, isright = True)
					elif key == 'left':		c = b.card('jack', board.trump_suit, istrump = True, isleft = True)
					else:				c = b.card(key,    board.trump_suit, istrump = True)
					return(c, c in hand)
			
	c = b.card('nine', board.trump_suit, istrump = True)
	return(c, False) # why not None instead of c?


# this is the logic part
# some rules, in order of what card to play:

# ---Always lead the right on 3
# ---Lead an offsuit ace if you have it
# ---If the person on your left called it and you can lead a suit that has already been led, do it
# ---If your partner called trump and you have a jack, lead it
# ---Lead an off-suit king if you have it
# ---Lead the right / highest remaining card if you have it
# ---Pass off the lead back to your partner if you've carried the team so far
# ---Lead your highest off-suit card, unless....
# 	---You have 4/5 or 3/4 trump
#    in which case, you play your lowest trump


r3_rule = rc.rule(right_on_3, 'lead', 'right on 3')
off_ace_rule = rc.rule(offsuit_ace, 'lead', 'offsuit ace')
awkward_spot_rule = rc.rule(caller_awkward_spot, 'lead', 'caller in an awkward spot')
partners_jack_rule = rc.rule(partners_jack, 'lead', 'lead a jack when your partner called it')
off_king_rule = rc.rule(offsuit_king, 'lead', 'offsuit king')
highest_trump_rule = rc.rule(highest_remaining_trump, 'lead', 'highest remaining trump')
carried_team_rule = rc.rule(carry_the_team, 'lead', 'pass the lead back to your partner if you\'ve taken 2 so far')
lead_trump_rule = rc.rule(lead_trump, 'lead', 'lead trump if your highest off card sucks or you have a lot')
highest_card_rule = rc.rule(highest_card, 'lead', 'highest card')

leading_logic = [r3_rule,
			off_ace_rule,
			awkward_spot_rule,
			partners_jack_rule,
			off_king_rule,
			highest_trump_rule,
			carried_team_rule,
			lead_trump_rule,
			highest_card_rule]	

