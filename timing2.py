import basicprogs as b
import time

n = int(1e5)
deck = b.create_deck()
b.shuffle(deck)

h1 = [deck[i] for i in [5, 1, 8, 14, 23]]
h2 = [deck[i] for i in [7, 18, 12, 9, 2]]
fh = [h1, h2]

# This is 2x worse than the other way
# uses an array and checks if a card is "in" the array
t1 = time.time()
for i in range(n):
	pos_hand_dict = {pos:[] for pos in ['o1', 'p', 'o2', 'd', 'kitty']}
	used_cards = []						# this is the key line
	for h in fh:
		for c in h:
			used_cards.append(c)
	for c in deck:
		if c in used_cards:	continue
		used_cards.append(c)				# this line is also key
		for p in pos_hand_dict:
			hand = pos_hand_dict[p]
			if len(hand) != 5:
				hand.append(c)
t2 = time.time()
print('Took %.2f seconds for the "in" method' %(t2-t1))	

# this is the better way
# creates the dictionary {"acehearts":0, "kinghearts":0, ...} and turns them to 1 if the card has been "used"
t3 = time.time()
for i in range(n):
	pos_hand_dict = {pos:[] for pos in ['o1', 'p', 'o2', 'd', 'kitty']}
	used_cards = {c.name+c.suit:0 for c in deck}		# this is the key line
	for h in fh:
		for c in h:
			used_cards[c.name+c.suit] = 1
			
	for c in deck:
		has_been_used = used_cards[c.name+c.suit]
		if has_been_used:	continue
		used_cards[c.name+c.suit] = 1			# this line is also key
		for p in pos_hand_dict:
			hand = pos_hand_dict[p]
			if len(hand) != 5:
				hand.append(c)
t4 = time.time()
print('Took %.2f seconds for the dictionary method' %(t4-t3))
exit(10)
