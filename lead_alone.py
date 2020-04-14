import basicprogs as b
import lead
import call

# (1) First, lead the top card if you have it
# (2) Next, try an off-suit ace
# (3) Then, lead your highest trump
# (4) Then, lead your highest card

# come back to this order -- (3) and (4) feel imprecise
# maybe keep (3) if there's only one card that beats your top card, less likely to get euchred
# something to play around with -- optimal leading strategies when going alone
# is there something I can do about "knowing" that cards that beat my top one are gone?
def lead_alone(board, pos):
	
	hand = board.pos_hand_dict[pos]
	
	# see if you've got the top trump card
	if sum([c.istrump for c in hand]) > 0:
		top_card, n_ahead = num_trumps_beating(hand, board)
		if n_ahead == 0:	return(top_card)
	
	# if you've got an offsuit ace, lead it next
	for c in hand:
		if c.name == 'ace':
			if not c.istrump:
				return(c)
	
	# next, just play your best card
	powers = [call.card_power(c) for c in hand]
	idx = powers.index(max(powers))
	return(hand[idx])
	
def num_trumps_beating(hand, board):

	# finding the best card in hand first
	max_hand_power = 0
	top_card = hand[0]
	for c in hand:
		if not c.istrump:	continue
		if call.card_power(c) > max_hand_power:
			max_hand_power = call.card_power(c)
			top_card = c

	if top_card.name == 'null' or top_card.suit == 'null':
		print(top_card)
		print()
		for c in hand:
			print(c, call.card_power(c))
		exit(10)
			
	# find all the trump cards that have been played
	played_powers = set()
	for c in board.all_cards_played:
		played_powers.add(call.card_power(c))
	trump_powers = [35, 31, 30, 25, 20, 15, 12]
	
	n_possible_ahead = sum([p > max_hand_power for p in trump_powers])
	n_played_ahead = sum([p > max_hand_power for p in played_powers])
	return(top_card, n_possible_ahead - n_played_ahead)
	
