import basicprogs as b
import play_card as pc

class boardstate:
	
	def __init__(self):
		self.all_pos, self.allpos = [['o1', 'p', 'o2', 'd'], ['o1', 'p', 'o2', 'd']]
		self.cards_played_and_stats, self.all_cards_played_and_stats = [[], []]
		self.cards_played, self.all_cards_played = [[], []]
		self.trump_suit = 'null'
		self.caller_pos = 'null'
		self.ns_score, self.ew_score = [0, 0]
		self.called_first_round = False
		self.turn_card = b.card('null', 'null', True)
		self.pos_hand_dict = {}
		self.pos_hand_dict_copy = {}
		self.ntricks_ns, self.ntricks_ew = [0, 0]
		self.leader_pos, self.winner_pos = ['o1', 'o1']
		self.winners = []
		self.all_pos = ['o1', 'p', 'o2', 'd']
		self.first_round_threshold = 70
		self.second_round_threshold = self.first_round_threshold
		self.going_alone_threshold = 120
		self.going_alone = False
		self.show_each_turn = True
		self.hand_result = 'null'
		self.alert_no_call = True
		self.reneg = [False, None]
	
	def run_quiet(self):
		self.show_each_turn = False
		self.alert_no_call = False
	
	def new_hand(self, hands):
#		self.o1hand, self.phand, self.o2hand, self.dhand = [hands[i] for i in range(4)]
		self.turn_card = hands[4][0].copy()
		self.turn_card.set_trump(self.turn_card.suit)
		for p, h in zip(['o1', 'p', 'o2', 'd'], hands[:4]):
			self.pos_hand_dict[p] = h
			
		self.pos_hand_dict_copy = dict(self.pos_hand_dict)
		self.cards_played_and_stats, self.all_cards_played_and_stats = [[], []]
		self.cards_played, self.all_cards_played = [[], []]
		self.trump_suit = 'null'
		self.caller_pos = 'null'
		self.called_first_round = False
		self.ntricks_ns, self.ntricks_ew = [0, 0]
		self.leader_pos, self.winner_pos = ['o1', 'o1']
		self.going_alone = False
		self.winners = []
	
	def new_trick(self, leader_pos):
		self.leader_pos = leader_pos
#		self.leader_pos, self.winner_pos = [leader_pos, leader_pos]
	
	# when this fn is called, all cards have been set to trump appropriately
	def call_trump(self, trump_suit, trump_caller, called_first_round, going_alone):
		self.trump_suit = trump_suit
		self.caller_pos = trump_caller
		self.called_first_round = called_first_round
		self.turn_card.set_trump(trump_suit)
		self.going_alone = going_alone
	
	def play_card(self, card, played_pos):
		self.cards_played_and_stats.append([card, played_pos])
		self.all_cards_played_and_stats.append([card, played_pos])
		self.cards_played.append(card)
		self.all_cards_played.append(card)
		
		# error checking
		if card not in self.pos_hand_dict[played_pos]:
			if not self.going_alone:
				print('Played error -- 1')
				raise(ValueError)
			if played_pos != b.partner(self.caller_pos):
				print('Played error -- 2')
				raise(ValueError)
		else:
			for c in self.pos_hand_dict[played_pos]:
				if c == card:
					c.set_null()
					break
			
		allpos = ['o1', 'p', 'o2', 'd']
		nextpos = allpos[(allpos.index(played_pos)+1)%4]
		dummy, winner_pos = pc.current_winner(nextpos, self)
		self.winner_pos = winner_pos
	
	def end_trick(self):
		# should be 4 cards played, so the leader_pos that pc.current_winner finds
		# should be the same as the input pos, so I feed it the actual leader_pos
		dummy, self.winner_pos = pc.current_winner(self.leader_pos, self)
		self.winners.append(self.winner_pos)
		self.cards_played = []
		self.cards_played_and_stats = []
		self.ntricks_ns += self.winner_pos in ['p', 'd']
		self.ntricks_ew += self.winner_pos in ['o1', 'o2']

	def add_points(self, ns_delta, ew_delta):
		self.ns_score += ns_delta
		self.ew_score += ew_delta
		self.set_result(ns_delta, ew_delta)
	
	def set_result(self, ns_delta, ew_delta):
	
		if self.reneg[0] == True:
			if self.reneg[1] in ['p', 'd']:	self.hand_result = 'reneg by p/d'
			else:					self.hand_result = 'reneg by o1/o2 (this is odd'
		elif ns_delta == 2:
			if self.caller_pos in ['o1', 'o2']:	self.hand_result = 'euchre by p/d'
			else:				self.hand_result = 'sweep by p/d'
		elif ew_delta == 2:
			if self.caller_pos in ['p', 'd']:	self.hand_result = 'euchre by o1/o2'
			else:				self.hand_result = 'sweep by o1/o2'
			
		elif ns_delta == 1:			self.hand_result = 'simple win by p/d'
		elif ew_delta == 1:			self.hand_result = 'simple win by o1/o2'
		elif ns_delta == 4:			self.hand_result = 'loner sweep by p/d'
		elif ew_delta == 4:			self.hand_result = 'loner sweep by o1/o2'
		else:
			print('error in hand result')
			exit(10)
	
	def done_with_hand(self):
	#	self.o1hand, self.phand, self.o2hand, self.dhand = [[], [], [], []]
		self.cards_played_and_stats, self.all_cards_played_and_stats = [[], []]
		self.cards_played, self.all_cards_played = [[], []]
		self.trump_suit = 'null'
		self.caller_pos = 'null'
		self.called_first_round = False
		self.turn_card = b.card('null', 'null', True)
		self.pos_hand_dict = {}
		self.ntricks_ns, self.ntricks_ew = [0, 0]
		self.leader_pos, self.winner_pos = ['o1', 'o1']
		self.winners = []
		self.reneg = [False, None]
	
	def set_null(self):
		self.done_with_hand()
		self.ns_score, self.ew_score = [0, 0]





