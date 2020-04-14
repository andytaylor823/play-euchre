import basicprogs as b

# this is just implementing the scoring
def add_points(board, just_return = False):

	if len(board.winners) != 5:
		print ('error in winners')
		exit(10)	
		
	allpos = ['o1', 'p', 'o2', 'd']
	num_tricks_ns = 0
	num_tricks_ew = 0
	for pos in board.winners:
		if pos == 'o1' or pos == 'o2':	num_tricks_ew += 1
		elif pos == 'p' or pos == 'd':	num_tricks_ns += 1
		else:
			print('error in scoring')
			exit(10)
	
	if board.going_alone:
		
		if board.caller_pos[0] == 'o':
			if num_tricks_ew == 5:
				p_ns = 0
				p_ew = 4
			elif num_tricks_ew >= 3:
				p_ns = 0
				p_ew = 1
			else:
				p_ns = 2
				p_ew = 0
		else:
			if num_tricks_ns == 5:
				p_ns = 4
				p_ew = 0
			elif num_tricks_ns >= 3:
				p_ns = 1
				p_ew = 0
			else:
				p_ns = 0
				p_ew = 2

		if just_return:	return(p_ns, p_ew)
		board.add_points(p_ns, p_ew)
		return
			
		

	if board.caller_pos[0] == 'o':
		if num_tricks_ew == 5:
			p_ns = 0
			p_ew = 2
		elif num_tricks_ew >= 3:
			p_ns = 0
			p_ew = 1
		else:
			p_ns = 2
			p_ew = 0	
		
	else:
		if num_tricks_ns == 5:
			p_ns = 2
			p_ew = 0
		elif num_tricks_ns >= 3:
			p_ns = 1
			p_ew = 0
		else:
			p_ns = 0
			p_ew = 2
			
	if just_return:	return(p_ns, p_ew)
	board.add_points(p_ns, p_ew)
