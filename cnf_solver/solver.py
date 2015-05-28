# Ryan Baltenberger
# CS 463G
# Program 3 - CNF Solver
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import csv
import os


# Reads in the CNF from the passed
# in file into a NumPy matrix. 
# Slices off the 0 at the end of each
# line and the space at the beginning.
# Returns the CNF matrix along with the
# number of variables in the formula
def read_formula(filename):
	cnfreader = csv.reader(open(filename, 'r'), delimiter=' ')
	formula = list(cnfreader)

	num_vars = int(formula[0][2])	
	num_clauses = int(formula[0][3])

	temp = formula[1:(num_clauses+1)]
	for el in temp:
		del el[0]
		del el[-1]
	cnf = np.array(temp).astype(int)

	return (cnf, num_vars)

# Generates a random truth assignment for
# a CNF with a length of the passed in value
def generate_assignment(num_vars):
	assign = np.zeros(num_vars)
	for ix in xrange(0, num_vars):
		assign[ix] = round(random.random())

	return assign


# Evaluates how many clauses in the passed in
# CNF are satisfied based on the passed in
# truth assignment.
def evaluate(assignment, clauses):
	clauses_satisfied = 0
	for i in xrange(0, np.size(clauses, 0)):
		for j in xrange(0, np.size(clauses, 1)):
			if cmp(clauses[i][j], 0) == 1:
				if assignment[clauses[i][j] - 1] == 1:
					clauses_satisfied += 1
					break
			else:
				if assignment[abs(clauses[i][j]) - 1] == 0:
					clauses_satisfied += 1
					break

	return clauses_satisfied

# Implementation of local search (hill climbing)
def local_search(clauses, assignment, num_vars):
	child = 0
	c = np.size(clauses, 0)
	satisfied = evaluate(assignment, clauses)

	# Generate and evaluate the children of the
	# current truth assignment.  Take the next
	# best one
	next_assignment = np.copy(assignment)
	next_satisfied = satisfied	
	for k in xrange(0, num_vars):
		temp_assign = np.copy(assignment)
		temp_assign[k] = (temp_assign[k] + 1) % 2
		
		temp_sat = evaluate(temp_assign, clauses)
		if temp_sat > satisfied:
			child = 1
			next_satisfied = temp_sat
			next_assignment = np.copy(temp_assign)
	
	# Goal test
	if next_satisfied == c:
		return (next_assignment, next_satisfied)
	
	# Recursively call local search if a child
	# truth assignment is produced. Else return
	# the best truth assignment seen
	if child == 1:
		return local_search(clauses, next_assignment, num_vars)
	else:
		return (assignment, satisfied)


# Implementation of a genetic algorithm
def genetic(clauses, num_vars, p, r, m, s):
	k = 0

	# Create the first generation
	old_generation = []
	for a in xrange(0, p):
		old_generation = np.append(old_generation, generate_assignment(num_vars), axis=0)
	old_generation = np.reshape(old_generation, (p, num_vars))
	
	# Calculate the fitness of each
	# element of the first generation
	old_fitness = np.zeros(p)
	for b in xrange(0, p):
		old_fitness[b] = evaluate(old_generation[b], clauses)
	
	# Loop for passed in number of generations
	for c in xrange(0, s):
		new_generation = []
		
		# Sort the fitness of the last generation
		# to be able to find the most fit elements
		# of the generation
		fitness_sorted = np.argsort(old_fitness)

		# Reproduce
		for d in xrange(0, r):
			parent1 = fitness_sorted[-1 + d]
			parent2 = fitness_sorted[-2 + d]
			new_generation = np.append(new_generation, np.concatenate((old_generation[parent1][0:(num_vars/2)], old_generation[parent2][(num_vars/2):num_vars]), axis=1), axis=0)
		
		# Copy to fill generation
		for e in xrange(r, p):
			selection = round(random.random() * (np.size(old_generation, 0) - 1))
			new_generation = np.append(new_generation, old_generation[selection], axis=0)
			old_generation = np.delete(old_generation, selection, axis=0)
		
		new_generation = np.reshape(new_generation, (p, num_vars))
		
		# Mutate
		for f in xrange(0, m):
			entity = round(random.random() * (np.size(new_generation, 0) - 1))	
			gene = round(random.random() * (np.size(new_generation, 1) - 1))
			new_generation[entity][gene] = (new_generation[entity][gene] + 1) % 2

		# Calculate fitness of new generation
		new_fitness = np.zeros(p)
		for g in xrange(0, p):
			new_fitness[g] = evaluate(new_generation[g], clauses)
			if new_fitness[g] == np.size(clauses, 0):
				return new_fitness[g]

		# Make the new generation the old generation
		k += 1
		old_generation = np.copy(new_generation)
		old_fitness = np.copy(new_fitness)
		
	return np.max(new_fitness)


# Implementation of WalkSat
def walksat(clauses, num_vars):
	c = np.size(clauses, 0)
	assignment = generate_assignment(num_vars)
	if evaluate(assignment, clauses) == c:
		return c

	max_satisfied = 0

	# Loop for specified number of iterations.
	# This is a sort of way to cut off the run
	# time of the algorithm.  Usually finds a
	# close to optimal, if not optimal, truth
	# assignment for the CNF
	for ix in xrange(0, 5000):
		chosen_clause = round(random.random() * (np.size(clauses, 0) - 1))
		temp_max = 0
		temp_index = 0
		for iy in xrange(0, np.size(clauses, 1)):
			temp_clauses = np.copy(clauses)
			temp_clauses[chosen_clause][iy] *= -1
			new_sat = evaluate(assignment, temp_clauses)
			if new_sat > temp_max:
				temp_max = new_sat
				clauses = np.copy(temp_clauses)
		if temp_max > max_satisfied:
			max_satisfied = temp_max
		if max_satisfied == c:
			return c

	return max_satisfied


def run_algorithms(path):
	var_cnfs = os.listdir(path)
	
	file_num = 0
	hill_max = []
	hill_time = []
	genetic_max = []
	genetic_time = []
	walksat_max = []
	walksat_time = []
	
	# Loop over each file in the passed in
	# directory path
	for filename in var_cnfs:
		file_num += 1
		print filename, file_num, "of", len(var_cnfs)
		print

		cnf_cur, total_vars = read_formula(path + filename)		

		# Run hill climbing
		hill_avg = 0
		hill_time_avg = 0
		for x in xrange(0,10):
			start = time.clock()
			assignment = generate_assignment(total_vars)
			sat_assign, num_satisfied = local_search(cnf_cur, assignment, total_vars)
			end = time.clock()

			hill_avg += num_satisfied
			hill_time_avg += (end - start)
			print "Hill Climbing", x, "in", end-start, "seconds"

		hill_max = np.append(hill_max, round(hill_avg / 10))
		hill_time = np.append(hill_time, hill_time_avg / 10)		

		print

		# Run the genetic algorithm
		genetic_avg = 0
		genetic_time_avg = 0
		for y in xrange(0,10):
			start = time.clock()
			cs = genetic(cnf_cur, total_vars, 100, 15, 5, 100)
			end = time.clock()

			genetic_avg += cs
			genetic_time_avg += (end - start)
			print "Genetic", y, "in", end-start, "seconds"
		
		genetic_max = np.append(genetic_max, round(genetic_avg / 10))
		genetic_time = np.append(genetic_time, genetic_time_avg / 10)
	
		print

		# Run WalkSat
		walksat_avg = 0
		walksat_time_avg = 0
		for x in xrange(0,10):
			start = time.clock()
			sat = walksat(cnf_cur, total_vars)
			end = time.clock()

			walksat_avg += sat
			walksat_time_avg += (end - start)
			print "WalkSat", x, "in", end-start, "seconds"

		walksat_max = np.append(walksat_max, round(walksat_avg / 10))
		walksat_time = np.append(walksat_time, walksat_time_avg / 10)		

		print

	# Create the two figures comparing each
	# algorithm's runtime and maximum number
	# of clauses satisfied
	fig1 = plt.figure()
	ax = fig1.add_subplot(111)
	ind = np.arange(len(var_cnfs))
	width = 0.30

	rects1_max = ax.bar(ind, hill_max, width, color='red')
	rects2_max = ax.bar(ind + width, genetic_max, width, color='blue')
	rects3_max = ax.bar(ind + width * 2, walksat_max, width, color='green')
	ax.set_xlim(-width*2, len(ind)+width*2)
	ax.set_xticks(ind + width)
	ax.set_xlabel('CNF')
	ax.set_ylabel('Clauses Satisfied')
	ax.set_title('Maximum Clauses Satisfied for each Algorithm')
	xtickNames = ax.set_xticklabels(var_cnfs)
	plt.setp(xtickNames, rotation=45, fontsize=10)
	ax.legend( (rects1_max[0], rects2_max[0], rects3_max[0]), ('Hill Climbing', 'Genetic Algorithm', 'WalkSat'))

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111)	
	rects1_time = ax2.bar(ind, hill_time, width, color='red')
	rects2_time = ax2.bar(ind + width, genetic_time, width, color='blue')
	rects3_time = ax2.bar(ind + width * 2, walksat_time, width, color='green')
	ax2.set_xlim(-width*2, len(ind)+width*2)
	ax2.set_xticks(ind + width)
	ax2.set_xlabel('CNF')
	ax2.set_ylabel('Time Elapsed (s)')
	ax2.set_title('Time To Maximum Satisfied Clauses for each Algorithm')
	xtickNames = ax2.set_xticklabels(var_cnfs)
	plt.setp(xtickNames, rotation=45, fontsize=10)
	ax2.legend( (rects1_time[0], rects2_time[0], rects3_time[0]), ('Hill Climbing', 'Genetic Algorithm', 'WalkSat'))
	
	plt.show()

	return


# Main function
def main():
	random.seed()

	run_algorithms('formulas/10_var/')
	#run_algorithms('forumlas/100_var/')
	
	print "Done"


if __name__ == "__main__":
	main()

