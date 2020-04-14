# This file has been checked through, and it is compatible with the board and isleft/isright updates
# This file is also compatible with the "__eq__" and "__str__" updates.
# It is as efficient as I think it can be right now.
# Most recent check: 12/6/2019

import random
import basicprogs as b
import call
import lead
import play_card as pc
import showturn as s
import boardstate_class as bsc
import forced_hand as fh
import points
import lead_alone
import leading_logic
import leading_alone_logic

def play_a_hand(board, forced_hands = [], forced_hand_positions = [], prevent_firstround_callers = [], prevent_secondround_callers = [], enable_alone = True, only_accept_alone = False, pass_condition = None):

	# does all of the setup for one hand
	setup(board, forced_hands, forced_hand_positions, prevent_firstround_callers, prevent_secondround_callers, enable_alone)
	
	if pass_condition is not None:
		if pass_condition(board):
			board.trump_suit = 'pass'
			return
	if board.trump_suit == 'null':	return		# happens if no one calls it
	
	# allow this option
	if only_accept_alone:
		if not board.going_alone:
			return
	
	# play 5 tricks
	for i in range(5):
		play_a_trick(board)
	
	# add points
	points.add_points(board)
	if board.show_each_turn:	print(board.hand_result.capitalize())

def setup(board, forced_hands, forced_hand_positions, prevent_firstround_callers, prevent_secondround_callers, enable_alone):

	# create a deck and deal out the cards
	hands = fh.hands(forced_hands, forced_hand_positions)
	
	# do some "board" bookkeeping (create the pos_hand dictionary, reset all the lead/winner stats, etc.)
	# only the turn card has been set to trump
	board.new_hand(hands)
	
	# calls trump and sets all cards to trump accordingly
	# the dealer has not taken the turn card into their hand (yet)
	call_trump(board, prevent_firstround_callers, prevent_secondround_callers)
	if board.trump_suit == 'null':	return	# happens if no one calls it
	if not enable_alone:		board.going_alone = False
	
	if board.going_alone:	adjust_partner_hand(board)
	
	# show the board state before anyone plays a card
	show(board)
	
	# re-order all hands				
	for p in board.pos_hand_dict:
		b.order_hand(board.pos_hand_dict[p], trump_suit = board.trump_suit)
	
	if board.going_alone:
		if board.caller_pos == 'o2':
			board.leader_pos, board.winner_pos = ['p', 'p']

def play_a_trick(board):

	board.new_trick(board.winner_pos)
	idx = board.allpos.index(board.leader_pos)
	
	for i in range(4):
		k = (i + idx)%4
		play_a_card(board, board.allpos[k])
		show(board)
	
	board.end_trick()

# this function should be solely syntax
def play_a_card(board, pos):

	if len(board.cards_played) == 0:
		if board.going_alone and pos == board.caller_pos:
			c1 = leading_alone_logic.return_card(board, pos)
#			c1 = lead_alone.lead_alone(board, pos)
		else:
			c1 = leading_logic.return_card(board, pos)
#			c1 = lead.pick_lead_card(board, pos)	
	else:		
		c1 = pc.pick_nonlead_card(board, pos)
	
	board.play_card(c1.copy(), pos)


def call_trump(board, prevent_firstround_callers, prevent_secondround_callers):
	
	# call trump in the first round
	call_trump_first_round(board, prevent_firstround_callers)
	
	# add the turn card to the dealer's hand
	if board.called_first_round:
		board.pos_hand_dict['d'] = call.dealer_new_hand(board.pos_hand_dict['d'], board.turn_card.copy())
		return
	
	# if you made it to here, trump was not called in the first round
	board.turn_card.remove_trump()
	call_trump_second_round(board, prevent_secondround_callers)
	if board.trump_suit != 'null':	return
	
	# if you made it to here, trump was not called in the second round, either
	if board.alert_no_call:		print('No trump was called -- re-deal.')
	board.call_trump('null', 'd', False, False)

def call_trump_first_round(board, prevent_firstround_callers):
	
	# go through first round
	# loop over all players' positions
	for pos in board.all_pos:
		# see if their hand is good enough to order it up
		# call_first_round leaves only the turn card as trump
		if pos in prevent_firstround_callers:	continue
		trump_called, going_alone = call.call_first_round(pos, board)
		
		# if they order it up, then set all cards to trump accordingly
		if trump_called:
			for p in board.pos_hand_dict:
				for c in board.pos_hand_dict[p]:
					c.set_trump(board.turn_card.suit)
			# after all trump cards have been set, do some "board" class bookkeeping
			board.call_trump(board.turn_card.suit, pos, True, going_alone)
			return

def call_trump_second_round(board, prevent_secondround_callers):

	# now, loop over all players' positions again
	for pos in board.all_pos:
		# see if their hand is good enough to call trump in the 2nd round
		# "trump_suit": String, either a suit name or "null" if trump was not called
		if pos in prevent_secondround_callers:	continue
		trump_suit, going_alone = call.call_second_round(pos, board)
		
		# if so, then set all cards to trump accordingly
		if trump_suit != "null":
			for p in board.pos_hand_dict:
				for c in board.pos_hand_dict[p]:
					c.set_trump(trump_suit)
			# after all trump cards have been set, do some "board" class bookkeeping
			board.call_trump(trump_suit, pos, False, going_alone)
			return

# asks for input to slow down the display of each turn
def show(board):

	if board.show_each_turn:
		s.show_turn(board)
		wait = 'z'
		while wait.lower() != 'c':
			if wait.lower() == 'x':		exit(10)
			wait = input('enter "c" to continue, "x" to exit: ')

# if one player is going alone, their partner gets a dead hand
def adjust_partner_hand(board):

	partner_pos = b.partner(board.caller_pos)
	dead_card = b.card('null', 'null')
	board.pos_hand_dict[partner_pos] = [dead_card.copy() for i in range(5)]
	
	
