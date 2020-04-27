import basicprogs as b
import rule_class as rc
import boardstate_class as bc
import call
import leading_logic

def return_card(board, pos):
	
	for r in leading_alone_logic:
		try:
			c = r.is_satisfied(board, pos)
		except(TypeError):
			print(r.name, r.rule_type, r.condition)
			c = None
			exit(10)
		if c is not None:	return(c)
	print('Error: no card returned to lead (alone)!')
	raise(ValueError)

def top_card(board, pos):

	hand = board.pos_hand_dict[pos]
	powers = [call.card_power(c) for c in hand]
	idx = powers.index(max(powers))
	return(hand[idx], True)


# (1) First, lead the top card if you have it
# (2) Next, try an off-suit ace
# (3) Then, lead your highest trump
# (4) Then, lead your highest card

# come back to this order -- (3) and (4) feel imprecise
# maybe keep (3) if there's only one card that beats your top card, less likely to get euchred
# something to play around with -- optimal leading strategies when going alone

top_card_rule = rc.rule(leading_logic.highest_remaining_trump, 'lead', 'alone -- top card')
off_ace_rule = rc.rule(leading_logic.offsuit_ace, 'lead', 'alone -- off ace')
best_card_rule = rc.rule(top_card, 'lead', 'alone -- top card')

leading_alone_logic = [top_card_rule,
					off_ace_rule,
					best_card_rule]

