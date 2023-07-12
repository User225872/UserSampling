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
		node_degree = len(sampled_adjacency_list[node])

		return node_degree
	elif subgraph_name == "Triangle":
		neighbors = sampled_adjacency_list[node]

		count = 0

		for neighbor in neighbors:
			if neighbor in sampled_adjacency_list.keys():
				neighbors_neighbors = sampled_adjacency_list[neighbor]

				count += len(set(neighbors).intersection(set(neighbors_neighbors)))

		return count
	elif subgraph_name == "TwoPath":
		node_degree = len(sampled_adjacency_list[node])

		return node_degree * (node_degree - 1)
	elif subgraph_name == "Rectangle":
		neighbors = sampled_adjacency_list[node]
		neighbors_number = len(neighbors)

		count = 0

		for i in range(neighbors_number):
			for j in range(i + 1, neighbors_number):
				count += 2 * (len(set(sampled_adjacency_list[neighbors[i]]).intersection(set(sampled_adjacency_list[neighbors[j]]))) - 1)

		return count
	elif subgraph_name == "TwoTriangle":
		neighbors = sampled_adjacency_list[node]

		count = 0

		for neighbor in neighbors:
			neighbors_neighbors = sampled_adjacency_list[neighbor]

			common_neighbors_number = len(set(neighbors).intersection(set(neighbors_neighbors)))
			count += common_neighbors_number * (common_neighbors_number - 1)

		return count

def Scale(number):
	if subgraph_name == "Edge":
		return number / (sample_probability ** 2)
	elif subgraph_name == "Triangle" or subgraph_name == "TwoPath":
		return number / (sample_probability ** 3)
	elif subgraph_name == "Rectangle" or subgraph_name == "TwoTriangle":
		return number / (sample_probability ** 4)

def SampledThreshold():
	if graph_name == "Amazon" or graph_name == "LiveJournal":
		return threshold * sample_probability / 2
	elif graph_name == "RoadnetCA" or graph_name == "USRN":
		return threshold

def GlobalSensitivity(degree_bound):
	if subgraph_name == "Edge":
		return degree_bound
	elif subgraph_name == "TwoPath":
		return degree_bound * (degree_bound - 1) * 3
	elif subgraph_name == "Triangle":
		return degree_bound * (degree_bound - 1) * 3
	elif subgraph_name == "Rectangle":
		return degree_bound * (degree_bound - 1) * (degree_bound - 1) * 8
	elif subgraph_name == "TwoTriangle":
		return degree_bound * (degree_bound - 1) * (degree_bound - 2) * 2

def SimpleSample():
	global sampled_users
	global sampled_adjacency_list

	answer = 0

	sampled_users = np.random.binomial(1, sample_probability, node_number)
	sampled_adjacency_list = dict()

	for node in range(node_number):
		if sampled_users[node] == 1:
			sampled_adjacency_list[node] = [neighbor for neighbor in adjacency_list[node] if sampled_users[neighbor] == 1]

	for node in sampled_adjacency_list.keys():
		answer += CountSubgraph(node)

	return answer

def main(argv):
	global graph_name
	global subgraph_name
	global sample_probability
	global threshold
	global real_answer

	try:
		opts, args = getopt.getopt(argv,"h:G:S:k:p:T:e:a:", ["GraphName=", "SubgraphName=", "IterationNumber=", "SampleProbability=", "Threshold=", "EpsilonTotal=", "RealAnswer="])
	except getopt.GetoptError:
		print("SimpleSampleCountNode.py -G <graph name> -S <subgraph name> -p <sample probability> -T <threshold> -e <epsilon total> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SimpleSampleCountNode.py -G <graph name> -S <subgraph name> -p <sample probability> -T <threshold> -e <epsilon total> -a <real answer>")
			sys.exit()
		elif opt in ("-G", "--GraphName"):
			graph_name = str(arg)
		elif opt in ("-S", "--SubgraphName"):
			subgraph_name = str(arg)
		elif opt in ("-p", "--SampleProbability"):
			sample_probability = float(arg)
		elif opt in ("-T", "--Threshold"):
			threshold = int(arg)
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)

	test_number = 100
	epsilons = [0.25, 0.5, 1, 2, 4, 8, 16]
	
	ReadGraph()

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SimpleSampleCountNode_" + graph_name + "_" + subgraph_name + "_" + str(sample_probability) + ".txt", 'w')

	sum_error = dict()
	sum_error[0] = []

	for epsilon_total in epsilons:
		sum_error[epsilon_total] = []

	sum_time_sample = []
	sum_time_noise = []

	for i in range(test_number):
		start = time.time()

		sample_answer = SimpleSample()
		answer = Scale(sample_answer)

		end = time.time()

		sum_error[0].append(abs(answer - real_answer))
		sum_time_sample.append(end - start)

		for epsilon_total in epsilons:
			start = time.time()

			epsilon = epsilon_total / sample_probability

			sampled_threshold = SampledThreshold()
			global_sensitivity = GlobalSensitivity(sampled_threshold)

			answer = sample_answer + LapNoise() * global_sensitivity / epsilon
			answer = Scale(answer)

			end = time.time()

			sum_error[epsilon_total].append(abs(answer - real_answer))
			sum_time_noise.append(end - start)

	sum_error[0].sort()		
	
	output_file.write(str(0) + " " + str(sum(sum_error[0][int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time_sample) / test_number) + "\n")

	for epsilon_total in epsilons:
		sum_error[epsilon_total].sort()

		output_file.write(str(epsilon_total) + " " + str(sum(sum_error[epsilon_total][int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time_sample) / test_number + sum(sum_time_noise) / test_number / len(epsilons)) + "\n")

if __name__ == "__main__":
	main(sys.argv[1 : ])