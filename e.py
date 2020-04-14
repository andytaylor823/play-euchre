import basicprogs as b
import turns_and_play as t
import call
import showturn as s
import boardstate_class as bsc
import time
import numpy as np

# TODO:
# have some fun :)
# look over everything to make sure it is all compatible with "board" and "isleft/isright"
# add in going alone
# add in forcing hand(s)
# plan out which numbers you are going to use statistics to calculate
# figure out those numbers (BIG)




# columns of data to print out:
# names and suits of each player's hand 					(40 cols)
# trump suit, called_first_round, caller_pos, turn_card (name and suit)		(+5 cols)
# n_tricks ns/ew, result ("simple", "euchre", "sweep"), by whom			(+3 cols)
# pts ns/ew (redundant, but nice)						(+2 cols)





board = bsc.boardstate()
board.run_quiet()

n = int(1e4)
t1 = time.time()
for i in range(n):
	t.play_a_hand(board)
t2 = time.time()
print('Took %.2f seconds to do %i hands' %(t2-t1, n))
exit(10)










i = 0
board = bsc.boardstate()
t0 = time.time()
while board.ns_score+board.ew_score == 0:
	i += 1
	print(i, board.ns_score, board.ew_score)
	t.play_a_hand(board, only_accept_alone = True)

print(i, board.going_alone, board.ns_score, board.ew_score)
exit(10)







c1 = b.card('jack', 'clubs')
c2 = b.card('jack', 'spades')
c3 = b.card('ace', 'clubs')
c4 = b.card('king', 'clubs')
c5 = b.card('ace', 'hearts')
hand = [c1, c2, c3, c4, c5]
pos = 'o1'
board = bsc.boardstate()
t.play_a_hand(board, forced_hands = [hand], forced_hand_positions = [pos], prevent_firstround_callers = ['o1', 'p', 'o2', 'd'])
exit(10)











c1, c2, c3, c4 = [b.card('jack', s) for s in ['clubs', 'hearts', 'diamonds', 'spades']]
c5 = b.card('ten', 'diamonds')
hand = [c1, c2, c3, c4, c5]
pos = 'o2'

board = bsc.boardstate()
t.play_a_hand(board, [hand], [pos])
exit(10)







t1 = time.time()

n_simple = np.array([0,0])
n_euchre = np.array([0,0])
n_sweep = np.array([0,0])
n_nsCall = 0
n_games = 100

board = bsc.boardstate()
board.run_quiet()
for i in range(n_games):
	board = t.play_a_hand(board)
#	print(board.ns_score, board.ew_score, '\t' + board.hand_result)

	if 'simple' in board.hand_result:
		if 'p/d' in board.hand_result:	n_simple[0] += 1
		else:				n_simple[1] += 1
	elif 'sweep' in board.hand_result:
		if 'p/d' in board.hand_result:	n_sweep[0] += 1
		else:				n_sweep[1] += 1
	elif 'euchre' in board.hand_result:
		if 'p/d' in board.hand_result:	n_euchre[0] += 1
		else:				n_euchre[1] += 1
	if board.caller_pos in ['p', 'd']:
		n_nsCall += 1
#	print(board.caller_pos, '\t', board.called_first_round)
	
p_sweep, p_euchre, p_simple = [arr/n_games for arr in [n_sweep, n_euchre, n_simple]]
sd_sweep, sd_euchre, sd_simple = [np.sqrt(arr*(1-arr)/n_games) for arr in [p_sweep, p_euchre, p_simple]]



print('Fraction sweeps:')
print('   NS: %.3f +/- %.3f     EW: %.3f +/- %.3f' %(p_sweep[0], sd_sweep[0], p_sweep[1], sd_sweep[1]))
print('Fraction euchres:')
print('   NS: %.3f +/- %.3f     EW: %.3f +/- %.3f' %(p_euchre[0], sd_euchre[0], p_euchre[1], sd_euchre[1]))
print('Fraction simple wins:')
print('   NS: %.3f +/- %.3f     EW: %.3f +/- %.3f' %(p_simple[0], sd_simple[0], p_simple[1], sd_simple[1]))
print('Expected points:')
print('   NS: %.2f                EW: %.2f' %(2*p_sweep[0]+p_simple[0]+2*p_euchre[0]-2*p_euchre[1], 2*p_sweep[1]+p_simple[1]+2*p_euchre[1]-2*p_euchre[0]))
print('Fraction of times called:')
print('   NS: %.3f               EW: %.3f' %(n_nsCall/n_games, 1-n_nsCall/n_games))

t2 = time.time()
print(t2 - t1)


exit(10)












hands = b.deal()
print('------------------------')

trump_suit, caller_pos, called_first_round, turn_card = t.call_trump(hands)
if called_first_round:
	hands[3] = call.dealer_new_hand(hands[3], hands[-1][0])
	b.order_hand(hands[3], trump_suit = trump_suit)
print(trump_suit, called_first_round, caller_pos)
h, w = t.play_a_trick(hands, trump_suit, 'o1', caller_pos)


exit(10)


o1hand, phand, o2hand, dhand, kitty = b.deal()
hands = [o1hand, phand, o2hand, dhand, kitty]

trump_suit, caller_pos, called_first_round, turn_card = t.call_trump(hands)






s.show_turn(hands, cards_played = [[phand[0],"p"], [o1hand[0], "o1"], [dhand[0], "d"], [o2hand[0], "o2"]])
#s.show_turn(hands)
kitty[0].print_card()
print('')

for hand in hands[0:4]:
	if call.call_first_round(hand, kitty[0]):
		b.print_hand(hand)






