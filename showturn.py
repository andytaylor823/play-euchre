import random
import basicprogs as b
import boardstate_class as bsc

def show_turn(board):
		
	print('--------------------------------')
	print_partner_hand(board)
	print_opp_hand(board)
	print_dealer_hand(board)
	print('--------------------------------')
	print_extras(board)

def hand_suits_short(hand):
	
	suit_chars = []
	for card in hand:
		suit_chars.append(shorten_card_suit(card))
	return(suit_chars)

def shorten_card_suit(card):

	if card.suit == "null":	return("-")
	else:			return(card.suit[0].capitalize())

def hand_names_short(hand):

	shortnames = []
	for card in hand:
		if card.name == "null":	shortnames.append("--")
		else:			shortnames.append(shorten_card_name(card))
	return(shortnames)

def shorten_card_name(card):

	if card.name == "ten":		return("10")
	elif card.name == "nine":	return("9")
	else:				return(card.name[0].capitalize() + card.name[1])

def print_partner_hand(board):

	phand = board.pos_hand_dict['p']
	dhand = board.pos_hand_dict['d']
	line1 = "\t"
	line2 = line1

	pshortnames = hand_names_short(phand)
	pshortsuits = hand_suits_short(phand)
	
	for i in range(len(pshortnames)):
		pname = pshortnames[i]
		psuit = pshortsuits[i]
		
		if pname == "9":	line1 += "  " + pname
		else:			line1 += " " + pname
		line2 += "  " + psuit
	
	print(line1)
	print(line2)

def print_opp_hand(board):

	o1hand, phand, o2hand, dhand = [board.pos_hand_dict[pos] for pos in ['o1', 'p', 'o2', 'd']]
		
	fns = [hand_names_short]*2 + [hand_suits_short]*2
	hs = [o1hand, o2hand, o1hand, o2hand]
	shortnames1, shortnames2, shortsuits1, shortsuits2 = [fn(h) for fn, h in zip(fns, hs)]
	
	leader_pos = board.leader_pos
	trump_suit = board.trump_suit
	cards_played = board.cards_played
	print('')
	for i in range(len(o1hand)):
	
		name1 = shortnames1[i]
		name2 = shortnames2[i]
		suit1 = shortsuits1[i]
		suit2 = shortsuits2[i]
		
		line = opp_hand_first_half(name1, suit1) + "\t"
		
		if i == 0 and did_play_card(cards_played, "p", leader_pos):
			line += print_name_and_suit(cards_played, "p", leader_pos, phand, dhand)
		
		elif i == 2 and (did_play_card(cards_played, "o1", leader_pos) or did_play_card(cards_played, "o2", leader_pos)):
			
			if did_play_card(cards_played, "o1", leader_pos):
				line += print_name_and_suit(cards_played, "o1", leader_pos, phand, dhand)
			line += "\t    "
			if did_play_card(cards_played, "o2", leader_pos):
				line += print_name_and_suit(cards_played, "o2", leader_pos, phand, dhand)
			else:
				line += '\t'
		
		elif i == 4 and did_play_card(cards_played, "d", leader_pos):
			line += print_name_and_suit(cards_played, "d", leader_pos, phand, dhand)
		
		else:
			line += "\t\t"
		
		line += "  \t" + opp_hand_second_half(name2, suit2)
		print(line)
	print('')

def opp_hand_first_half(name, suit):
	line = name
	if name == "9":		line += "  "
	else:			line += " "
	line += suit
	return(line)

def opp_hand_second_half(name, suit):
	line = suit
	if name == "9":		line += "  "
	else:			line += " "
	line += name
	return(line)


def print_dealer_hand(board):
	
	dhand = board.pos_hand_dict['d']
	line1 = "\t"
	line2 = line1
	
	shortnames = hand_names_short(dhand)
	shortsuits = hand_suits_short(dhand)
	
	for i in range(len(dhand)):
		name = shortnames[i]
		suit = shortsuits[i]
		
		line1 += "  " + suit
		if name == "9":	line2 += "  " + name
		else:		line2 += " " + name
		
	print(line1)
	print(line2)

def did_play_card(cards_played, pos, leader_pos):

	if len(cards_played) == 0:	return(False)
	all_pos = ['o1', 'p', 'o2', 'd']
	start_idx = all_pos.index(leader_pos)
	played_pos = [all_pos[(i+start_idx)%4] for i in range(len(cards_played))]
	if pos in played_pos:
		return(True)
	return(False)

def get_played_card(cards_played, pos, leader_pos):

	if len(cards_played) == 0:	return(card("null", "null"))
	all_pos = ['o1', 'p', 'o2', 'd']
	start_idx = all_pos.index(leader_pos)
	now_idx = all_pos.index(pos)
	delta = (now_idx-start_idx+4) %4
	return(cards_played[delta])

def ns_spaces(partnerhand, dealerhand):

	line = ""
	pshortnames = hand_names_short(partnerhand)
	dshortnames = hand_names_short(dealerhand)
	for i in range(2):
		pname = pshortnames[i]
		dname = dshortnames[i]
		for j in range(max(len(pname), len(dname))):
			line += " "
		line += " "
		
	return(line)

def print_name_and_suit(cards_played, pos, leader_pos, partnerhand, dealerhand):
	
	line = ""
	thiscard = get_played_card(cards_played, pos, leader_pos)
	name = shorten_card_name(thiscard)
	suit = shorten_card_suit(thiscard)
	
	if pos == "p" or pos == "d":
		line += ns_spaces(partnerhand, dealerhand) + name + " " + suit + "\t"
	else:
		line += name + " " + suit
	
	return(line)	

def print_extras(board):

	line = 'NS score:  %i\t\t EW score:  %i\n' %(board.ns_score, board.ew_score)
	line += 'NS tricks: %i\t\t EW tricks: %i\n\n' %(board.ntricks_ns, board.ntricks_ew)
	line += 'Trump suit: **' + board.trump_suit.capitalize() + '**, called by: ' + board.caller_pos + '\n'
	if board.going_alone:	line += '***THIS PLAYER IS GOING ALONE***' + '\n'
	if board.called_first_round:	line += 'Called first round. ' 
	else:				line += 'Called second round. '
	line += 'Turn card was the ' + board.turn_card.name.capitalize() + ' of ' + board.turn_card.suit.capitalize() + '\n\n'
	line += board.leader_pos + ' led this trick, and ' + board.winner_pos + ' is winning right now.\n'
	line += '--------------------------------'
	print(line)
	

