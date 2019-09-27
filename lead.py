import basicprogs as b
import call

def tricknum(hand):	return(1+sum([c.name == 'null' for c in hand]))

# this is the logic part
# some rules, in order of what card to play:

# ---Always lead the right on 3
# ---Lead an offsuit ace if you have it
# ---If your partner called trump and you have a jack, lead it
# ---Lead your highest off-suit card, unless....
#	---The highest card is a 9 or 10, and
# 	---You have 4/5 or 3/4 trump
#    in which case, you play your lowest trump

# So far, we have no knowledge about what all has been played, though maybe I should update that?
# I'll leave it in the variable "known_excludes"
def pick_lead_card(hand, pos, caller_pos, known_excludes = []):
	tnum = tricknum(hand)

	if tnum == 3:
		for c in hand:
			if c.isright:
				return(c)
	
	for c in hand:
		if c.name == 'ace':
			if not c.istrump:
				return(c)
	
	if pos == 'd':		partner_pos = 'p'
	elif pos == 'p':	partner_pos = 'd'
	elif pos == 'o1':	partner_pos = 'o2'
	else:			partner_pos = 'o1'
	
	if caller_pos == partner_pos:
		for c in hand:
			if c.isright:	return(c)
			if c.isleft:	return(c)
	
	ntrump = sum([c.istrump for c in hand])
	ncards = 6-tnum
	frac_trump = ntrump/ncards
	if frac_trump >= 0.75:		# only lead trump if you have 3/4 or 4/5, not 3/5 or 2/4 or 2/3
		trumps = [c for c in hand if c.istrump]
		power = [call.card_power(c) for c in trumps]
		idx = power.index(min(power))
		return(trumps[idx])
	
	non_trumps = [c for c in hand if (not c.istrump and c.suit != 'null')]
	power = [call.card_power(c) for c in non_trumps]
	idx = power.index(max(power))
	return(non_trumps[idx])
	



