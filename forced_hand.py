import basicprogs as b

def hands(forced_hands = [], forced_hand_positions = []):

	# if normal hand, just deal regularly
	if len(forced_hands) == 0:	return(b.deal())
	
	# do all of the error checking on the input
	em = error_checking(forced_hands, forced_hand_positions)
	if em != '':
		print(em)
		exit(10)
	
	# create your own deck
	deck = b.create_deck()
	b.shuffle(deck)
	
	# create an empty position:hand dictionary
	pos_hand_dict = {pos:[] for pos in ['o1', 'p', 'o2', 'd', 'kitty']}
	
	# add in the known forced hands
	for p, h in zip(forced_hand_positions, forced_hands):
		pos_hand_dict[p] = h

	# create a dictionary containing each card and if it has been used or not
	# e.g. {"acehearts":0, "kinghearts:0", ... , "nineclubs":0}
	# set the cards in the forced hand(s) to 1
	used_cards = {c.name+c.suit:0 for c in deck}
	for h in forced_hands:
		for c in h:
			used_cards[c.name+c.suit] = 1
	
	# loop over each card in the deck, check if it's already been used
	# if not, add it to the first hand that hasn't already been set	
	# kitty is last, so it's fine that its length is not 5
	for c in deck:
		has_been_used = used_cards[c.name+c.suit]
		if has_been_used:	continue
		used_cards[c.name+c.suit] = 1	
		for p in pos_hand_dict:
			hand = pos_hand_dict[p]
			if len(hand) != 5:
				hand.append(c)
				break
	
	# return the hands, kitty is last
	all_hands = [pos_hand_dict[p] for p in pos_hand_dict]
	return(all_hands)
	
	
	
def error_checking(fh, fhpos):
	
	# error checking -- length of hand(s)
	for h in fh:
		if len(h) != 5:
			return('Forced hand error -- 5')
	
	# error checking -- equal number of hands and positions
	if len(fh) != len(fhpos):
		return('Forced hand error -- 1')
	
	# error checking -- appropriate position labels
	for p in fhpos:
		if p not in ['o1', 'p', 'o2', 'd']:
			return('Forced hand error -- 4')

	# error checking -- making sure each element in hand is of type card
	for h in fh:
		for c in h:
			if type(c) != b.card:
				return('Forced hand error -- 2')
	
	return('')




