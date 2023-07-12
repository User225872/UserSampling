import getopt
import math
import numpy as np
import os
import random
import sys
import time

def AddEdge(node, edge):
	if node in adjacency_list.keys():
		adjacency_list[node].append(edge)
	else:
		adjacency_list[node] = [edge]

def ReadGraph():
	global adjacency_list
	global node_number

	cur_path = os.getcwd() + '/'
	graph = open(cur_path + "../Data/Edge/" + graph_name + ".txt", 'r')

	adjacency_list = dict()

	for line in graph.readlines():
		edge = line.rstrip().split('	')

		AddEdge(int(edge[1]), int(edge[2]))

	node_number = int(line.rstrip().split('	')[1]) + 1

def CountSubgraph(node):
	if subgraph_name == "Edge":
		node_degree = len(adjacency_list[node])

		return node_degree
	elif subgraph_name == "Triangle":
		neighbors = adjacency_list[node]

		count = 0

		for neighbor in neighbors:
			neighbors_neighbors = adjacency_list[neighbor]

			count += len(set(neighbors).intersection(set(neighbors_neighbors)))

		return count
	elif subgraph_name == "TwoPath":
		node_degree = len(adjacency_list[node])

		return node_degree * (node_degree - 1)
	elif subgraph_name == "Rectangle":
		neighbors = adjacency_list[node]
		neighbors_number = len(neighbors)

		count = 0

		for i in range(neighbors_number):
			for j in range(i + 1, neighbors_number):
				count += 2 * (len(set(adjacency_list[neighbors[i]]).intersection(set(adjacency_list[neighbors[j]]))) - 1)

		return count
	elif subgraph_name == "TwoTriangle":
		neighbors = adjacency_list[node]

		count = 0

		for neighbor in neighbors:
			neighbors_neighbors = adjacency_list[neighbor]

			common_neighbors_number = len(set(neighbors).intersection(set(neighbors_neighbors)))
			count += common_neighbors_number * (common_neighbors_number - 1)

		return count

def Sample():
	answer = 0

	for i in range(iteration_number):
		sampled_user = np.random.randint(0, node_number)
		answer += CountSubgraph(sampled_user)

	return answer / iteration_number * node_number

def main(argv):
	global graph_name
	global subgraph_name
	global iteration_number
	global real_answer

	try:
		opts, args = getopt.getopt(argv,"h:G:S:k:a:", ["GraphName=", "SubgraphName=", "IterationNumber=", "RealAnswer="])
	except getopt.GetoptError:
		print("SampleNode.py -G <graph name> -S <subgraph name> -k <iteration number> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleNode.py -G <graph name> -S <subgraph name> -k <iteration number> -a <real answer>")
			sys.exit()
		elif opt in ("-G", "--GraphName"):
			graph_name = str(arg)
		elif opt in ("-S", "--SubgraphName"):
			subgraph_name = str(arg)
		elif opt in ("-k", "--IterationNumber"):
			max_iteration_number = int(arg)
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)
	
	test_number = 100

	ReadGraph()

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SampleNode_" + graph_name + "_" + subgraph_name + ".txt", 'w')

	for i in range(max_iteration_number):
		iteration_number = int(100 * math.pow(2, i))

		sum_error = []
		sum_time = []

		for j in range(test_number):
			start = time.time()

			answer = Sample()

			end = time.time()

			sum_error.append(abs(answer - real_answer))
			sum_time.append(end - start)

		sum_error.sort()

		output_file.write(str(iteration_number) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
		output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1 : ])