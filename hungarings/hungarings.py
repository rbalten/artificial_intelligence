# Ryan Baltenberger
# CS 463G Project 1 Parts I & II
# Hungarian Rings
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import heapq

# move function
# pass in ring and direction to rotate
def move(rings, direction, ring_to_move):
	# counter clockwise = 0. add the last value to the front and remove the
	# old value from the array.  change the shared ball positions in the
	# other ring
	if direction == 0:
		temp_ring = np.insert(rings[ring_to_move], [0], rings[ring_to_move][19], axis=0)
		rings[ring_to_move] = temp_ring[0:20]	

		rings[(ring_to_move + 1) % 2, 0] = rings[ring_to_move, 0]
		rings[(ring_to_move + 1) % 2, 15] = rings[ring_to_move, 15]
	else:
		temp_ring = np.append(rings[ring_to_move], rings[ring_to_move][0])
		rings[ring_to_move] = temp_ring[1:21]	

		rings[(ring_to_move + 1) % 2, 0] = rings[ring_to_move, 0]
		rings[(ring_to_move + 1) % 2, 15] = rings[ring_to_move, 15]

	# Code for visualizing the randomization
	#plt.clf()
	#visualize(rings)

	return rings

# randomizer function
# pass in number of moves, randomly choose ring and
# move to make, checking to make sure previous move
# is not undone and not to make 10 of the same moves
# in a row
def randomize(rings, moves):
	prev_ring = -1
	prev_dirc = -1
	repeats = 0

	# iterate for the number of moves, check that the previous move is
	# not undone and there aren't ten of the same move in a row. 
	for ix in xrange(0, moves):
		ring_to_move = round(random.random())
		direction = round(random.random())
		while (ring_to_move == prev_ring) and (direction == ((prev_dirc + 1) % 2)):
			ring_to_move = round(random.random())
			direction = round(random.random())

		if (ring_to_move == prev_ring) and (direction == prev_dirc):
			repeats += 1
		if repeats > 9:
			ring_to_move = round(random.random())
			direction = round(random.random())

		rings = move(rings, direction, ring_to_move)

		prev_ring = ring_to_move
		prev_dirc = direction

	return rings

# visualize the rings
def visualize(rings):
	# the position of each ball is found using the equation of a circle
	theta = 2 * math.pi / 20
	radius = 5	
	xdata_left = np.zeros(20)
	ydata_left = np.zeros(20)
	xdata_right = np.zeros(20)
	ydata_right = np.zeros(20)
	plt.clf()	

	# get the positions for the left and right rings
	for ix in xrange(0,20):
		xdata_left[ix] = 5 + (radius * math.cos((ix + 5 * math.pi / 6) * theta))
		ydata_left[ix] = 5 + (radius * math.sin((ix + 5 * math.pi / 6) * theta))
	
		xdata_right[ix] = 12.08 + (radius * math.cos((ix + 63 * math.pi / 16) * -theta))
		ydata_right[ix] = 5.3 + (radius * math.sin((ix + 63 * math.pi / 16) * -theta))

	# set up the colors for the left and right ring
	colors_left = np.chararray(20)
	colors_right = np.chararray(20)
	for ix in xrange(0,20):
		if rings[0][ix] == 0:
			colors_left[ix] = 'r'
		elif rings[0][ix] == 1:
			colors_left[ix] = 'b'
		elif rings[0][ix] == 2:
			colors_left[ix] = 'y'
		elif rings[0][ix] == 3:
			colors_left[ix] = 'k'
		
		if rings[1][ix] == 0:
			colors_right[ix] = 'r'
		elif rings[1][ix] == 1:
			colors_right[ix] = 'b'
		elif rings[1][ix] == 2:
			colors_right[ix] = 'y'
		elif rings[1][ix] == 3:
			colors_right[ix] = 'k'

	# plot each ball individually to get the correct color
	for ix in xrange(0,20):
		plt.scatter(xdata_left[ix], ydata_left[ix], 1500, colors_left[ix])	
		plt.scatter(xdata_right[ix], ydata_right[ix], 1500, colors_right[ix])	

	plt.axis('equal')
	plt.show()
	plt.draw()

# Implementation of the heuristic
# Counts the number of color changes in each ring, subtracts three
# from the value for each ring (a solved puzzle has three color changes)
# and takes the max of the two values
def heuristic(rings):
	return max(np.sum(np.logical_not(rings[0][0:19] == rings[0][1:20])) - 3, np.sum(np.logical_not(rings[1][0:19] == rings[1][1:20])) - 3)
	
# Implementation of IDA*
# Works for puzzles below a randomization of 20,
# after that, it does not finish (also runs 
# slowly for some puzzle randomizations)
def ida(rings, goal):
	# Set up the initial variables and the queue
	g = 0
	count = 0
	expanded = 0
	f_next = float('inf')
	f_limit = g + heuristic(rings)

	priorq = []
	heapq.heapify(priorq)
	heapq.heappush(priorq, (f_limit, count, rings, g, rings))

	# Main loop 
	# Runs until a solution is found
	while (1):	
		expanded += 1
		next_state = heapq.heappop(priorq)
		
		# Returns if the next state is the goal state
		# Generates the children for the next state if not
		if np.array_equal(next_state[2], goal):
			return expanded
		else:
			move1 = np.copy(move(np.copy(next_state[2]), 0, 0))
			move2 = np.copy(move(np.copy(next_state[2]), 0, 1))
			move3 = np.copy(move(np.copy(next_state[2]), 1, 0))
			move4 = np.copy(move(np.copy(next_state[2]), 1, 1))		
			moves = (move1, move2, move3, move4)

		# Loop over each of the generated children
		# Ignore the one that undoes the previous move
		# Add them to the queue if they have a smaller
		# f value, change the next f limit if not
		for ix in xrange(0,4):
			f_val = heuristic(moves[ix]) + next_state[3] + 1
			if np.array_equal(moves[ix], next_state[4]):
				continue
			if f_val <= f_limit:
				count += 1
				heapq.heappush(priorq, (f_val, count, moves[ix], next_state[3] + 1, next_state[2]))
			else:
				f_next = min(f_next, f_val)
		
		# When the queue is empty, reset everything
		# and start over with a new f limit
		if priorq == []:
			count = 0
			expanded = 0
			f_limit = f_next
			f_next = float('inf')
			heapq.heappush(priorq, (f_limit, count, rings, g, rings))	


# Main part of the script
random.seed()

# show the initial plot
#plt.axis([0, 15, 0, 15])
#plt.ion()
#plt.show()

# hardcoded in initial state
# r = 0, u = 1, y = 2, b = 3
rings = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2,
								  2, 2, 2], [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3,
								  3, 2, 1, 1, 1, 1]])
# Copy over the initial state as the goal
goal = np.copy(rings)

# Set up the container for running IDA*
nodes = np.zeros(6)

# Generate and solve five randomized puzzles for
# each of the steps 
for c in xrange(10, 16):
	node_avg = 0
	for d in xrange(0,5):
		rings_scrambled = randomize(np.copy(goal), c)
		node_avg += ida(np.copy(rings_scrambled), goal)
	nodes[c-10] = node_avg / 5
	print nodes	

# Plot the average number of nodes
# expanded for each of the steps
xdata = xrange(10, 16)
plt.plot(xdata, nodes)
plt.xlabel('Actual Depth')
plt.ylabel('Nodes Expanded')
plt.title('Nodes Expanded vs. Actual Depth for IDA*')
plt.show()
visualize(rings)
