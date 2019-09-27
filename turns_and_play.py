import random
import basicprogs as b
import call
import lead
import play_card as pc
import showturn as s

def play_a_hand(ns_score, ew_score):

	hands = b.deal()
	s.show_turn(hands, 'o1', trump_suit = 'null')
	trump_suit, caller_pos, called_first_round, turn_card = call_trump(hands)
	if called_first_round:
		hands[3] = call.dealer_new_hand(hands[3], hands[-1][0])
		b.order_hand(hands[3], trump_suit = trump_suit)
	print(trump_suit, called_first_round, caller_pos)

	for hand in hands:
		for card in hand:
			card.set_trump(trump_suit)

	allhands = [hands[i] for i in range(4)]
	winner_pos = 'o1'
	winners = []
	for i in range(5):
		allhands, winner_pos = play_a_trick(allhands, trump_suit, winner_pos, caller_pos)
		winners.append(winner_pos)
	
	delta_ns, delta_ew = points(winners, caller_pos)
	ns_score += delta_ns
	ew_score += delta_ew
	
	return(ns_score, ew_score)


def play_a_trick(allhands, trump_suit, leader_pos, caller_pos):

	allpos = ['o1', 'p', 'o2', 'd']
	idx = allpos.index(leader_pos)
	
	# need to check this
	cards_played = []
	for i in range(4):
		k = (i + idx)%4
		allhands[k], card_to_play = play_a_card(allhands[k], allpos[k], caller_pos, trump_suit, cards_played)
		cards_played.append(card_to_play)
		s.show_turn(allhands, leader_pos, trump_suit = trump_suit, cards_played = cards_played)
		wait = 'z'
		while wait != 'c':
			if wait.lower() == 'x':		exit(10)
			wait = input('enter "c" to continue, "x" to exit: ')
	
#	winner_pos = find_winner(leader_pos, cards_played)
	# should be 4 cards played, so the leader_pos that pc.current_winner finds
	# should be the same as the input pos, so I feed it the actual leader_pos
	dummy, winner_pos = pc.current_winner(leader_pos, cards_played)
	return(allhands, winner_pos)

# this function should be solely syntax
def play_a_card(hand, pos, caller_pos, trump_suit, cards_played = []):

	if len(cards_played) == 0:
		c1 = lead.pick_lead_card(hand, pos, caller_pos)
		card_to_play = b.make_copy(c1)
		for card in hand:
			if card.is_match(card_to_play):
				card.set_null()
	
	else:
		c1 = pc.pick_nonlead_card(hand, pos, caller_pos, cards_played, trump_suit)
		card_to_play = b.make_copy(c1)
		for card in hand:
			if card.is_match(card_to_play):
				card.set_null()

	return(hand, card_to_play)

# returns:  trump_suit, caller_pos, called_first_round, turn_card
def call_trump(hands):

	[o1hand, phand, o2hand, dhand, kitty] = hands
	allhands = [o1hand, phand, o2hand, dhand]
	allpos = ['o1', 'p', 'o2', 'd']
	
	turn_card = kitty[0]
	trump_suit = turn_card.suit
	turn_card.print_card()
	
	# go through first round
	for i in range(len(allpos)):
		trump_called = call.call_first_round(allhands[i], turn_card, allpos[i])
		if trump_called:
			for h in hands:
				for c in h:
					c.remove_trump()
					c.set_trump(trump_suit)
			return(turn_card.suit, allpos[i], True, turn_card)
	
	for h in hands:
		for c in h:
			c.remove_trump()
	# if you made it to here, trump was not called in the first round
	for i in range(len(allpos)):
		trump_suit = call.call_second_round(allhands[i], turn_card, allpos[i])
		if trump_suit != "null":
			for h in hands:
				for c in h:
					c.set_trump(trump_suit)
			return(trump_suit, allpos[i], False, turn_card)
	



# this is syntax
# TODO:
# this does the same thing as a function in "play_card" -- make one the best and kill the other
def find_winner(leader_pos, cards_played):

	for card in cards_played:
		if card.istrump == True:
			powers = [call.card_power(x) for x in cards_played]
			idx = powers.index(max(powers))
			break

		lead_card = cards_played[0]
		idx = 0
		for card in cards_played:
			if card.suit == lead_card.suit and call.card_power(card) > call.card_power(cards_played[idx]):
				idx = cards_played.index(card)	
		
	allpos = ['o1', 'p', 'o2', 'd']
	leader_idx = allpos.index(leader_pos)
	winner_pos = allpos[(leader_idx + idx)%4]
	return(winner_pos)


# this is just implementing the scoring
def points(winners, caller_pos):

	if len(winners) != 5:
		print ('error in winners')
		exit(10)
		
	allpos = ['o1', 'p', 'o2', 'd']
	num_tricks_ns = 0
	num_tricks_ew = 0
	for pos in winners:
		if pos == 'o1' or pos == 'o2':	num_tricks_ew += 1
		elif pos == 'p' or pos == 'd':	num_tricks_ns += 1
		else:
			print('error in scoring')
			exit(10)
	
	
	if caller_pos == 'o1' or caller_pos == 'o2':
		if num_tricks_ew == 5:
			p_ns = 0
			p_ew = 2
		elif num_tricks_ew >= 3 and num_tricks_ew < 5:
			p_ns = 0
			p_ew = 1
		else:
			p_ns = 2
			p_ew = 0	
		
	else:
		if num_tricks_ns == 5:
			p_ns = 2
			p_ew = 0
		elif num_tricks_ns >= 3 and num_tricks_ns < 5:
			p_ns = 1
			p_ew = 0
		else:
			p_ns = 0
			p_ew = 2

	return(p_ns, p_ew)



