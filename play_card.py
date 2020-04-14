import basicprogs as b
import call
import lead
import showturn as s

all_pos = ['o1', 'p', 'o2', 'd']
def tricknum(hand):	return(1+sum([c.name == 'null' for c in hand]))

def find_leader_pos(pos, cards_played):
	nc = len(cards_played)
	idx_me = all_pos.index(pos)
	idx_leader = (idx_me - nc) % 4
	return(all_pos[idx_leader])

# finds the current winner of a trick
def current_winner(pos, board):

	# the leader is winning, and it's up to everyone else to beat them
	winning_pos = board.leader_pos
	winning_card = board.cards_played[0]

	# look at the rest of the cards
	for i in range(1, len(board.cards_played)):
		c = board.cards_played[i]
		# a card that (isn't trump) and (isn't the same suit as the winning card) can win
		if not c.istrump and c.suit != winning_card.suit:
			continue
		
		# get this card's position
		p = all_pos[(all_pos.index(board.leader_pos)+i)%4]
		
		# compare the power of the two cards, knowing now that
		# the two cards are actually comparable (both of the same suit,
		# or the non-winning card trumps the winning card)
		cpower = call.card_power(c)
		wpower = call.card_power(winning_card)
		if cpower > wpower:
			winning_card = c
			winning_pos = p
	
	return(winning_card, winning_pos)

# this is the logic part
def pick_nonlead_card(board, pos):

	# if your partner is going alone, you must play a trash card
	if board.going_alone:
		if board.caller_pos == b.partner(pos):
			c = partner_going_alone(board)
			return(c)

	hand = board.pos_hand_dict[pos]
	winning_card, dummy = current_winner(pos, board)
	legal_hand = cards_allowed_to_play(hand, board)
	
	teamwinner, led_card, team_pos, have_highest_trump, followsuit, have_trump, n_tricks_won_team, n_tricks_remaining = current_state(board, pos, legal_hand)
	n, have_2_above, have_3_above, c_2_above, c_3_above = trump_spot_winning_card(teamwinner, winning_card, legal_hand, board)
	
	can_win, highest, lowest, lowest_winning = key_cards(pos, board, legal_hand)
	if not can_win:						return(lowest)
	if not teamwinner:
		if led_card.istrump:
			if board.caller_pos in team_pos:			return(highest)
			else:							return(lowest_winning)
		elif highest.suit == led_card.suit:				return(highest)
		else:								return(lowest_winning)
	
	# If you can't win the trick, play your lowest legal card
	
	# If your teammate **doesn't** have it:
		# If trump was led:
			# If your team called trump       			:	highest
			# If your team did not call trump 			:	lowest winning
		# If you're following an off-suit	  			:	highest
		# If you're trumping an off-suit	  			:	lowest winning
	
	else:
		if len(board.cards_played) == 3:				return(lowest)
		if led_card.istrump:
			if have_highest_trump:
				if n != 2:					return(highest)
				else:						return(lowest)
			else:
				if have_2_above:				return(c_2_above)
				elif have_3_above:				return(c_3_above)
				else:						return(lowest)
				
	# If your teammate **does** have it:
		# If you're the last person		  			:	lowest
		# If trump was led:
			# If you have the top card:
				# If your partner can be beat			:	highest
				# If your partner can't be beat			:	lowest
			# If you don't have the top card:
				# If you have the one two above your partner	:	that one
				# If you have the one three above your partner	:	that one
				# Else						:	lowest
		
		else:
			if winning_card.name == 'ace':				return(lowest)
			else:
				if followsuit:					return(highest)
				else:
					if not have_trump:			return(lowest)
					else:
						if n_tricks_won_team + n_tricks_remaining >= 3:		return(lowest_winning)
						else:				return(lowest)
			
		# If an off-suit was led:
			# If your partner is     winning it with an ace		:	lowest
			# If your partner is not winning it with an ace:
				# If you have to follow suit			:	highest
				# If you don't have to follow suit:
					# If you can't trump it			: 	lowest
					# If you can trump it:
						# If n_tricks_won + n_trump_in_hand >= 3:	lowest winning
						# If you need that king to win the trick:	lowest


def cards_allowed_to_play(hand, board):

	# check if you have to follow suit
	must_follow_suit = follow_suit(hand, board)
	lead_card = board.cards_played[0]
	
	legal_cards = []
	if must_follow_suit:
		if lead_card.istrump:	legal_cards = [c for c in hand if c.istrump]
		else:			legal_cards = [c for c in hand if c.suit == lead_card.suit and not c.isleft]
	else:
		legal_cards = hand[:]
	return(legal_cards)

def follow_suit(hand, board):

	led_card = board.cards_played[0]
	if led_card.istrump:
		for c in hand:
			if c.istrump:					return(True)
	else:
		for c in hand:
			if c.suit == led_card.suit and not c.isleft:	return(True)
	return(False)

def key_cards(pos, board, legal_hand):

	# get the lowest card
	lowest = call.find_weakest_card(legal_hand, board.trump_suit)
	
	# see if you even have the right suits to beat the winning card
	winning_card, winning_pos = current_winner(pos, board)
	if not has_winnable_suit(legal_hand, winning_card):
		return(False, None, lowest, None)
	
	# get the highest card and the lowest winning card
	highest, lowest_winning = highest_and_lowest_winning(legal_hand, winning_card)
	can_win = call.card_power(highest) > call.card_power(winning_card)
	return(can_win, highest, lowest, lowest_winning)

def has_winnable_suit(hand, winning_card):

	if winning_card.isleft:		winning_suit = b.same_color_suit(winning_card.suit)
	else:				winning_suit = winning_card.suit
	
	for c in hand:
		if c.istrump:			return(True)
		if c.suit == winning_suit:	return(True)
	return(False)

def current_state(board, pos, legal_hand):

	team_pos = [pos, b.partner(pos)]
	teamwinner = board.winner_pos in team_pos
	led_card = board.cards_played[0]
	team_pos = [pos, b.partner(pos)]
	c, have_highest_trump = lead.nth_highest_remaining_trump(legal_hand, board, n = 1)
	followsuit = follow_suit(legal_hand, board)
	have_trump = sum([c.istrump for c in legal_hand])
	
	n_tricks_won_team = sum([p == pos or p == b.partner(pos) for p in board.winners])
	n_tricks_remaining = 5-len(board.winners)
	
	return(teamwinner, led_card, team_pos, have_highest_trump, followsuit, have_trump, n_tricks_won_team, n_tricks_remaining)

def trump_spot_winning_card(teamwinner, winning_card, legal_hand, board):
	
	if teamwinner:
		if winning_card.istrump:
			c_2_above = None
			c_3_above = None
			for i in range(7):
				c1, dummy = lead.nth_highest_remaining_trump(legal_hand, board, n = i+1)
				n = i
				if c1 == winning_card:	break
			if n == 1 or n == 2:
				have_2_above = False
				have_3_above = False
			elif n == 3:
				c_2_above, have_2_above = lead.nth_highest_remaining_trump(legal_hand, board, n = n-2)
				have_3_above = False
			else:
				c_2_above, have_2_above = lead.nth_highest_remaining_trump(legal_hand, board, n = n-2)
				c_3_above, have_3_above = lead.nth_highest_remaining_trump(legal_hand, board, n = n-3)
			return(n, have_2_above, have_3_above, c_2_above, c_3_above)
	return([0]*5)

def get_hand_power(hand, winning_card):

	hand_power = []
	# by this point, we know that there is at least one card of the right suit to beat the winning card
	# find the power of each card in your hand
	for c in hand:
		if c.istrump or (c.suit == winning_card.suit and not c.isleft):
			hand_power.append(call.card_power(c))
		else:
			hand_power.append(-1)
	return(hand_power)

def highest_and_lowest_winning(hand, winning_card):

	hand_power = get_hand_power(hand, winning_card)
	max_idx = hand_power.index(max(hand_power))
	highest = hand[max_idx]

	# find the power of the winning card
	win_power = call.card_power(winning_card)
	# these cards are either all trump or none trump
	# can't have a mix, or else you would have to follow suit
	better_cards = [hand[i] for i in range(len(hand)) if hand_power[i] > win_power]
	if len(better_cards) == 0:		return(highest, None)
	
	hand_power = [call.card_power(c) for c in better_cards]
	min_idx = hand_power.index(min(hand_power))
	lowest_winning = better_cards[min_idx]

	return(highest, lowest_winning)
	
# if you can win with an off-suit ace, do that
# if you can play a nine on an off-suit ace, do that	
def proper_winning_card(hand, winning_card, trump_suit):	
	
	# from the beginning, we know that these are only cards which are legal under following suit, so there can
	# never be a mix of trump and follow-suit cards in this hand
	# there can still be a mix of trump and non-trump cards, though
	if winning_card.istrump:	winning_suit = trump_suit
	else:				winning_suit = winning_card.suit
	
	# check if you can even possibly win (if you have any trump or any of the led suit)
	hand_power = []
	can_beat = False
	for c in hand:
		if c.istrump:
			can_beat = True
			break
		if c.suit == winning_suit:
			can_beat = True
			break
	if not can_beat:
		return(call.find_weakest_card(hand, trump_suit))
	
	# by this point, we know that there is at least one card of the right suit to beat the winning card
	# find the power of each card in your hand
	for c in hand:
		if c.istrump or (c.suit == winning_card.suit and not c.isleft):
			hand_power.append(call.card_power(c))
		else:
			hand_power.append(-1)
		
	
	# find the power of the winning card
	win_power = call.card_power(winning_card)
	
	# these cards are either all trump or none trump
	better_cards = [hand[i] for i in range(len(hand)) if hand_power[i] > win_power]
	if len(better_cards) == 0:		return(call.find_weakest_card(hand, trump_suit))
	
	hand_power = [call.card_power(c) for c in better_cards]
	if better_cards[0].istrump:	# means they are all trump -- play the lowest trump that wins
		idx = hand_power.index(min(hand_power))
		return(better_cards[idx])	
	else:				# means none are trump -- play the highest card that wins
		idx = hand_power.index(max(hand_power))
		return(better_cards[idx])
		
def partner_going_alone(board):
	
	led_card = board.cards_played[0]
	if led_card.istrump:	suit = board.trump_suit
	else:			suit = led_card.suit
	trash_card = b.card('nine', suit)
	trash_card.set_trump(board.trump_suit)
	return(trash_card)
	
	

		

