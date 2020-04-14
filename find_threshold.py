import turns_and_play as t
import boardstate_class as bsc

def play_hand_no_ordering_up(CallingThreshold, board = None)

	if board == None:	board = bsc.boardstate()
	board.run_quiet()
	board.first_round_threshold = CallingThreshold
	board.second_round_threshold = CallingThreshold
	
	t.play_a_hand(board, prevent_first_round = ['o1', 'p', 'o2'])

