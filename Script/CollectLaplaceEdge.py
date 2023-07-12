import math
import os
import random
import sys
import time

test_number = 100

queries = ["Triangle", "Rectangle", "TwoTriangle", "TwoPath", "Star", "ThreePath"]
databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]
epsilons = [0.25, 0.5, 1, 2, 4, 8, 16]

Ts = [1024, 16384, 16, 16]
answers = [[4002774, 25002584, 14122764, 19504372, 1713886716, 165970574],
			[1066920780, 211062353344, 157968389924, 8511536390, 24945845826432, 1560908466060],
			[724056, 2098712, 51476, 11990180, 35425764, 26451080],
			[2632824, 12857624, 86396, 102025442, 239601984, 183167066]]

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def ComputeGlobalSensitivity(query, degree_bound):
	if query == "TwoPath":
		return (degree_bound - 1) * 2
	elif query == "Triangle":
		return (degree_bound - 1) * 6
	elif query == "Rectangle":
		return (degree_bound - 1) * (degree_bound - 1) * 8
	elif query == "TwoTriangle":
		return (degree_bound - 1) * (degree_bound - 2) * 2
	elif query == "Star":
		return (degree_bound - 1) * (degree_bound - 2) * 12
	elif query == "ThreePath":
		return (degree_bound - 1) * (degree_bound - 1) * 3

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		database = databases[i]

		output_file = open(cur_path + "../Result/LaplaceEdge_" + database + ".txt", 'w')

		for j in range(len(queries)):
			query = queries[j]

			for epsilon in epsilons:
				sum_error = []
				sum_time = []

				for k in range(test_number):
					start = time.time()

					real_answer = answers[i][j]
					answer = real_answer + LapNoise() * ComputeGlobalSensitivity(query, Ts[i]) / epsilon

					end = time.time()

					sum_error.append(abs(answer - real_answer))
					sum_time.append(end - start)

				sum_error.sort()
	
				output_file.write(query + " " + str(epsilon) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
				output_file.flush()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])