import basicprogs as b
import call

all_pos = ['o1', 'p', 'o2', 'd']
def tricknum(hand):	return(1+sum([c.name == 'null' for c in hand]))

# TODO:
# these two are similar to a function in turns_and_play -- make one the best and kill the other
def find_leader_pos(pos, cards_played):
	nc = len(cards_played)
	idx_me = all_pos.index(pos)
	idx_leader = (idx_me + nc) % 4
	return(all_pos[idx_leader])

def current_winner(pos, cards_played):
	leader_pos = find_leader_pos(pos, cards_played)
	winning_pos = leader_pos
	winning_card = cards_played[0]
	for i in range(1, len(cards_played)):
		c = cards_played[i]
		p = all_pos[(all_pos.index(leader_pos)+i)%4]
		
		cpower = call.card_power(c)
		wpower = call.card_power(winning_card)
		if cpower > wpower:
			winning_card = c
			winning_pos = p
	
	return(winning_card, winning_pos)

# this is the logic part
def pick_nonlead_card(hand, pos, caller_pos, cards_played, trump_suit):

	teamwinner = False
	winning_card, winning_pos = current_winner(pos, cards_played)
	if pos[0] == 'o' and winning_pos[0] == 'o':	teamwinner = True
	elif pos[0] == 'o' or winning_pos[0] == 'o':	teamwinner = False
	else:						teamwinner = True
	
	followsuit = False
	if cards_played[0].isleft:	lead_suit = trump_suit
	else:				lead_suit = cards_played[0].suit
	
	for c in hand:
		if c.suit == lead_suit and not c.isleft:
			followsuit = True
			break
		elif lead_suit == trump_suit and c.isleft:
			followsuit = True
			break
	
	legal_cards = []
	if followsuit:
		for c in hand:
			if c.isleft:
				if lead_suit == trump_suit:	legal_cards.append(c)
			elif c.suit == lead_suit:		legal_cards.append(c)
	else:		legal_cards = hand[:]
		
	if teamwinner:
		weakest_card = call.find_weakest_card(legal_cards, trump_suit)
		return(weakest_card)
	else:
		card_to_play = proper_winning_card(legal_cards, winning_card, trump_suit)
		return(card_to_play)

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
#	print('len better cards = ', len(better_cards))
#	print(hand[0].name, hand[0].suit, ' this is my first card')
	if len(better_cards) == 0:		return(call.find_weakest_card(hand, trump_suit))
	
	hand_power = [call.card_power(c) for c in better_cards]
	if better_cards[0].istrump:	# means they are all trump -- play the lowest trump that wins
		idx = hand_power.index(min(hand_power))
		return(better_cards[idx])	
	else:				# means none are trump -- play the highest card that wins
		idx = hand_power.index(max(hand_power))
		return(better_cards[idx])
		
		
		

