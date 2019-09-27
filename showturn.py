import random
import basicprogs as b

def show_turn(hands, leader_pos, trump_suit, cards_played = []):
	opphand1 = hands[0]
	partnerhand = hands[1]
	opphand2 = hands[2]
	dealerhand = hands[3]
	
	print('--------------------------------')
	print_partner_hand(hands)
	print_opp_hand(hands, leader_pos, trump_suit, cards_played)
	print_dealer_hand(hands)
	print('--------------------------------')
	#print_extras(trump_suit, ns_score, ew_score, caller_pos)

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

def print_partner_hand(hands):

	partnerhand = hands[1]
	dealerhand = hands[3]
	line1 = "\t"
	line2 = line1
	
	shortnames = hand_names_short(partnerhand)
	shortsuits = hand_suits_short(partnerhand)
	dshortnames = hand_names_short(dealerhand)
	dshortsuits = hand_suits_short(dealerhand)
	
	for i in range(len(shortnames)):
		name = shortnames[i]
		suit = shortsuits[i]
		dname = dshortnames[i]
		dsuit = dshortsuits[i]
		
		if name == "9":	line1 += "  " + name
		else:		line1 += " " + name
		line2 += "  " + suit
	
	print(line1)
	print(line2)

def print_opp_hand(hands, leader_pos, trump_suit = 'null', cards_played = []):

	opphand1 = hands[0]
	partnerhand = hands[1]
	opphand2 = hands[2]
	dealerhand = hands[3]
	
	shortnames1 = hand_names_short(opphand1)
	shortnames2 = hand_names_short(opphand2)
	shortsuits1 = hand_suits_short(opphand1)
	shortsuits2 = hand_suits_short(opphand2)
	
	print('')
	for i in range(len(opphand1)):
	
		name1 = shortnames1[i]
		name2 = shortnames2[i]
		suit1 = shortsuits1[i]
		suit2 = shortsuits2[i]
		
		line = opp_hand_first_half(name1, suit1) + "\t"
		
		if i == 0 and did_play_card(cards_played, "p", leader_pos):
			line += print_name_and_suit(cards_played, "p", leader_pos, partnerhand, dealerhand)
		
		elif i == 2 and (did_play_card(cards_played, "o1", leader_pos) or did_play_card(cards_played, "o2", leader_pos)):
			
			if did_play_card(cards_played, "o1", leader_pos):
				line += print_name_and_suit(cards_played, "o1", leader_pos, partnerhand, dealerhand)
			line += "\t    "
			if did_play_card(cards_played, "o2", leader_pos):
				line += print_name_and_suit(cards_played, "o2", leader_pos, partnerhand, dealerhand)
			else:
				line += '\t'
		
		elif i == 4 and did_play_card(cards_played, "d", leader_pos):
			line += print_name_and_suit(cards_played, "d", leader_pos, partnerhand, dealerhand)
		
		else:
			line += "\t\t"
		
		line += "  \t" + opp_hand_second_half(name2, suit2)
		if i == 2:		line += "\tTrump = " + trump_suit.capitalize()
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


def print_dealer_hand(hands):
	
	partnerhand = hands[1]
	dealerhand = hands[3]
	line1 = "\t"
	line2 = line1
	
	shortnames = hand_names_short(dealerhand)
	shortsuits = hand_suits_short(dealerhand)
	pshortnames = hand_names_short(partnerhand)
	pshortsuits = hand_suits_short(partnerhand)	
	
	for i in range(len(dealerhand)):
		name = shortnames[i]
		suit = shortsuits[i]
		pname = pshortnames[i]
		psuit = pshortsuits[i]
		
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

# TODO:
# write this -- just add extra stuff at the bottom of each showturn
# also add who the winner is
def print_extras(trump_suit, ns_score, ew_score, caller_pos):
	print('add in later')
