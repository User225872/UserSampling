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
	global edge_list
	global node_dict
	global double_edge_number
	global edge_number

	cur_path = os.getcwd() + '/'
	graph = open(cur_path + "../Data/Edge/" + graph_name + ".txt", 'r')

	edge_list = []
	node_dict = dict()

	last_node = -1
	last_position = -1
	count = 0

	for line in graph.readlines():
		edge = line.rstrip().split('	')

		node = int(edge[1])

		edge_list.append(int(edge[2]))

		if node != last_node:
			node_dict[node] = count
			last_node = node
			last_position = count

		count += 1

	double_edge_number = len(edge_list)
	edge_number = int(double_edge_number / 2)
	node_dict[last_node + 1] = double_edge_number

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
	global tilde_edge_number

	tilde_edge_number = edge_number + LapNoise() * threshold / epsilon_pub
	check_edge_number = tilde_edge_number - threshold / epsilon_pub * math.log(1 / 2 / delta_pub)

	epsilon = math.log(check_edge_number / threshold * (math.e ** epsilon_sample - 1) + 1)

def CountSubgraph(src, dst):
	if subgraph_name == "Triangle":
		src_neighbors = edge_list[node_dict[src] : node_dict[src + 1]]
		dst_neighbors = edge_list[node_dict[dst] : node_dict[dst + 1]]

		return len(set(src_neighbors).intersection(set(dst_neighbors)))
	elif subgraph_name == "TwoPath":
		src_degree = node_dict[src + 1] - node_dict[src]
		dst_degree = node_dict[dst + 1] - node_dict[dst]

		return (src_degree + dst_degree - 2) / 2
	elif subgraph_name == "Star":
		src_degree = node_dict[src + 1] - node_dict[src]
		dst_degree = node_dict[dst + 1] - node_dict[dst]

		return (src_degree - 1) * (src_degree - 2) + (dst_degree - 1) * (dst_degree - 2)
	elif subgraph_name == "ThreePath":
		src_degree = node_dict[src + 1] - node_dict[src]
		dst_degree = node_dict[dst + 1] - node_dict[dst]

		return (src_degree - 1) * (dst_degree - 1)
	elif subgraph_name == "Rectangle":
		src_neighbors = edge_list[node_dict[src] : node_dict[src + 1]]
		dst_neighbors = edge_list[node_dict[dst] : node_dict[dst + 1]]

		count = 0

		for src_neighbor in src_neighbors:
			if src_neighbor != dst:
				src_neighbors_neighbors = edge_list[node_dict[src_neighbor] : node_dict[src_neighbor + 1]]
				count += len(set(src_neighbors_neighbors).intersection(set(dst_neighbors))) - 1

		return count
	elif subgraph_name == "TwoTriangle":
		src_neighbors = edge_list[node_dict[src] : node_dict[src + 1]]
		dst_neighbors = edge_list[node_dict[dst] : node_dict[dst + 1]]

		common_neighbors_number = len(set(src_neighbors).intersection(set(dst_neighbors)))

		return common_neighbors_number * (common_neighbors_number - 1)

def SampleAndExplore():
	answer = 0

	for i in range(iteration_number):
		sampled_src = edge_list[np.random.randint(0, double_edge_number)]
		sampled_src_pos = node_dict[sampled_src]
		sampled_src_degree = node_dict[sampled_src + 1] - sampled_src_pos

		sampled_dst = edge_list[sampled_src_pos + np.random.randint(0, sampled_src_degree)]

		answer += min(CountSubgraph(sampled_src, sampled_dst), clipping_threshold) + LapNoise() * clipping_threshold / epsilon

	return answer / iteration_number * tilde_edge_number * 2

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
		print("SampleAndExploreEdge.py -G <graph name> -S <subgraph name> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleAndExploreEdge.py -G <graph name> -S <subgraph name> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
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
	output_file = open(cur_path + "../Result/SampleAndExploreEdge_" + graph_name + "_" + subgraph_name + "_" + str(epsilon_total) + ".txt", 'w')
	
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