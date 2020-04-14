import basicprogs as b
import boardstate_class as bsc
from inspect import signature  # use this to check the "condition" argument

class rule:

	def __init__(self, condition, rule_type, name='rule'):
		if not callable(condition):
			print('Error: condition argument must be a callable function')
			raise(ValueError)
		sig = signature(condition)
		if len(sig.parameters) != 2:
			print('Error: condition argument can only take two arguments')
			raise(ValueError)
		if not isinstance(rule_type, str):
			print('Error: rule_type argument must be a string')
			raise(ValueError)
		if rule_type.lower() not in ['lead', 'follow', 'call']:
			print('Error: rule_type argument can only be "lead", "follow", or "call"')
			raise(ValueError)
			
		self.type = rule_type
		self.condition = condition
		self.name = name
	
	def is_satisfied(self, board, pos):
		if not isinstance(board, bsc.boardstate):
			print('Error: improper board argument')
			raise(ValueError)
		if not isinstance(pos, str):
			print('Error: position argument not a string')
			raise(ValueError)
		if pos.lower() not in ['o1', 'o2', 'p', 'd']:
			print('Error: invalid position choice given')
			raise(ValueError)
		
		c, have = self.condition(board, pos)
		if have:	return(c)
		else:	return(None)

		
		
		
