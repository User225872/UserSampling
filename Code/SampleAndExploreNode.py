import getopt
import math
import numpy as np
import os
import random
import sys
import time

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def AddEdge(node, edge):
	if node in adjacency_list.keys():
		adjacency_list[node].append(edge)
	else:
		adjacency_list[node] = [edge]

def BinarySearch(epsilon_sample_k, delta_0):
	left = 0
	right = epsilon_sample_k
	accuracy = 10 ** -5

	while right - left > accuracy:
		mid = (left + right) / 2

		if math.sqrt(2 * iteration_number * math.log(1 / delta_0)) * mid + iteration_number * mid * (math.e ** mid - 1) > epsilon_sample_k:
			right = mid
		else:
			left = mid

	return left

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

def ComputeEpsilonsBefore():
	global epsilon_sample
	global epsilon_pub
	global delta_pub

	epsilon_sample_k = 0.8 * epsilon_total
	epsilon_pub = 0.2 * epsilon_total

	delta_0 = 0.8 * delta_total
	delta_pub = 0.2 * delta_total

	epsilon_sample = BinarySearch(epsilon_sample_k, delta_0)

def ComputeEpsilonsAfter():
	global epsilon
	global tilde_node_number

	tilde_node_number = node_number + LapNoise() * threshold / epsilon_pub
	check_node_number = tilde_node_number - threshold / epsilon_pub * math.log(1 / 2 / delta_pub)

	epsilon = math.log(check_node_number / threshold * (math.e ** epsilon_sample - 1) + 1)

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

def SampleAndExplore():
	answer = 0

	for i in range(iteration_number):
		sampled_user = np.random.randint(0, node_number)
		answer += min(CountSubgraph(sampled_user), clipping_threshold) + LapNoise() * clipping_threshold / epsilon

	return answer / iteration_number * tilde_node_number

def main(argv):
	global graph_name
	global subgraph_name
	global iteration_number
	global threshold
	global clipping_threshold
	global epsilon_total
	global delta_total
	global real_answer

	try:
		opts, args = getopt.getopt(argv,"h:G:S:k:T:C:e:d:a:", ["GraphName=", "SubgraphName=", "IterationNumber=", "Threshold=", "ClippingThreshold=", "EpsilonTotal=", "DeltaTotal=", "RealAnswer="])
	except getopt.GetoptError:
		print("SampleAndExploreNode.py -G <graph name> -S <subgraph name> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleAndExploreNode.py -G <graph name> -S <subgraph name> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
			sys.exit()
		elif opt in ("-G", "--GraphName"):
			graph_name = str(arg)
		elif opt in ("-S", "--SubgraphName"):
			subgraph_name = str(arg)
		elif opt in ("-k", "--IterationNumber"):
			max_iteration_number = int(arg)
		elif opt in ("-T", "--Threshold"):
			threshold = int(arg)
		elif opt in ("-C", "--ClippingThreshold"):
			max_clipping_threshold = int(arg)
		elif opt in ("-e", "--EpsilonTotal"):
			epsilon_total = float(arg)
		elif opt in ("-d", "--DeltaTotal"):
			delta_total = float(arg)
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)
	
	test_number = 100

	ReadGraph()

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SampleAndExploreNode_" + graph_name + "_" + subgraph_name + "_" + str(epsilon_total) + ".txt", 'w')

	for i in range(max_iteration_number):
		iteration_number = int(100 * math.pow(2, i))

		for j in range(max_clipping_threshold):
			clipping_threshold = int(math.pow(2, j))

			sum_error = []
			sum_time = []

			for k in range(test_number):
				start = time.time()

				ComputeEpsilonsBefore()
				ComputeEpsilonsAfter()

				answer = SampleAndExplore()

				end = time.time()

				sum_error.append(abs(answer - real_answer))
				sum_time.append(end - start)

			sum_error.sort()
	
			output_file.write(str(iteration_number) + " " + str(clipping_threshold) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1 : ])