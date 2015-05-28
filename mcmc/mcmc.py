# Ryan Baltenberger
# CS 463G
# Program 6 - MCMC

import random
import numpy as np
import matplotlib.pyplot as plt

# setting up the conditional probability tables for the network
table_B = np.array([[(1,-1,-1,-1), 0.8], [(0,-1,-1,-1), 0.2]])
table_E = np.array([[(-1,-1,1,-1), 0.2], [(-1,-1,0,-1), 0.6]])
table_A = np.array([[(-1,1,1,-1), 0.9574], [(-1,1,0,-1), 0.9375], [(-1,0,1,-1), 0.5844], [(-1,0,0,-1), 0.4839]])
table_D = np.array([[(1,-1,-1,1), 0.2404], [(1,-1,-1,0), 0.6849], [(0,-1,-1,1), 0.1923], [(0,-1,-1,0), 0.5479]])

# mcmc
# Runs mcmc on the network over the 
# given probability tables
def mcmc():
	# generate random assignment
	assignment = (int(round(random.random())), int(round(random.random())), int(round(random.random())), int(round(random.random())))

	# set up matrix to hold data for P(B|C=T)
	data = np.zeros(20)

	# variable to hold the number of instances
	# where node B is true
	true_b = 0

	# run 800 instances
	for ix in xrange(0,800):
		# assign new A
		if assignment[1] == 1 and assignment[2] == 1:
			prob = table_A[0,1]
		elif assignment[1] == 1 and assignment[2] == 0:
			prob = table_A[1,1]
		elif assignment[1] == 0 and assignment[2] == 1:
			prob = table_A[2,1]
		elif assignment[1] == 0 and assignment[2] == 0:
			prob = table_A[3,1]

		# select new value for A
		if random.random() < prob:
			new_A = 1
		else:
			new_A = 0

		# assign new D
		if assignment[0] == 1 and assignment[3] == 1:
			prob = table_D[0,1]
		elif assignment[0] == 1 and assignment[3] == 0:
			prob = table_D[1,1]
		elif assignment[0] == 0 and assignment[3] == 1:
			prob = table_D[2,1]
		elif assignment[0] == 0 and assignment[3] == 0:
			prob = table_D[3,1]

		# select new value for D
		if random.random() < prob:
			new_D = 1
		else:
			new_D = 0

		# assign new B
		if assignment[0] == 1:
			prob = table_B[0,1]
		elif assignment[0] == 0:
			prob = table_B[1,1]

		# select new value for B
		if random.random() < prob:
			new_B = 1
		else:
			new_B = 0

		# assign new E
		if assignment[3] == 1:
			prob = table_E[0,1]
		elif assignment[3] == 0:
			prob = table_E[1,1]

		# select new value for E
		if random.random() < prob:
			new_E = 1
		else:
			new_E = 0

		# check if new assignment has B=T
		if new_B == 1:
			true_b = true_b + 1

		# add a new data point every 40 instances
		if (ix+1) % 40 == 0:
			data[((ix+1)/40)-1] = (float(true_b) / (ix+1)) 

		# load the new assignment
		assignment = (new_A, new_B, new_D, new_E)

	return data

def main():
	# gather data
	run1 = mcmc()
	run2 = mcmc()
	run3 = mcmc()
	run4 = mcmc()
	run5 = mcmc()

	# plot data
	fig = plt.figure()
	ax2 = fig.add_subplot(111)	
	ax2.plot(run1)
	ax2.plot(run2)
	ax2.plot(run3)
	ax2.plot(run4)
	ax2.plot(run5)
	ax2.set_xlabel('Instance (sets of 40)')
	ax2.set_ylabel('Probability')
	ax2.set_title('P(B|C=T)')
	ax2.axis([0, 19, 0, 1])
	plt.show()

if __name__ == "__main__":
	main()

