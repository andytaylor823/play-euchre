import operator
import time

#arr = [10, 2, 6, 1, 26, 27, 18, 58, 189, 598, 18, 58, 0, 2, 85, 81, 891, 59]
arr = [10, 2, 6, 1, 26]
n = int(1e6)

# The Problem:
# Want to find the index of minimum in one array, then use that index to select out an element from another array

# The Answer:
# Method 1 (using arr.index) is better, seems like always better?

# Method 1:
# short array, so just use arr.index
t1 = time.time()
for i in range(n):
	min_idx = arr.index(min(arr))
	mn = arr[min_idx]
t2 = time.time()
print('Took %.2f seconds when using arr.index' %(t2-t1))


# Method 2:
# using operator.itemgetter seems neat
t3 = time.time()
for i in range(n):
	mindex, min_val = min(enumerate(arr), key = operator.itemgetter(1))
	mn = arr[mindex]
t4 = time.time()
print('Took %.2f seconds when using operator' %(t4-t3))
