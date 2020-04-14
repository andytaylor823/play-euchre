import basicprogs as b
import numpy as np
import time
import call

n = int(1e5)
c = b.card('nine', 'hearts')
c1 = b.card('nine', 'hearts')
c2 = b.card('jack', 'clubs')
cn = b.card('null', 'null')

# this is 5x longer than the other way
# uses numpy arrays to allow null cards to have -99 value
t1 = time.time()
for i in range(n):
	powers = np.array([call.card_power(c) for c in hand])
	testcard = np.array(hand)[powers == min(abs(powers))][0]
t2 = time.time()
print('Took %.2f seconds using abs method' %(t2-t1))

# this is the better way
# creates a sub_hand that specifically ignores null cards
t3 = time.time()
for i in range(n):
	sub_hand = [c for c in hand if c.suit != 'null']
	powers = [call.card_power(c) for c in sub_hand]
	idx = powers.index(min(powers))
	testcard = sub_hand[idx]
t4 = time.time()
print('Took %.2f seconds using sub_hand method' %(t4-t3))
