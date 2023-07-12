import getopt
import math
import numpy as np
import os
import random
import sys
import time

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

def Sample():
	answer = 0

	for i in range(iteration_number):
		sampled_src = edge_list[np.random.randint(0, double_edge_number)]
		sampled_src_pos = node_dict[sampled_src]
		sampled_src_degree = node_dict[sampled_src + 1] - sampled_src_pos

		sampled_dst = edge_list[sampled_src_pos + np.random.randint(0, sampled_src_degree)]

		answer += CountSubgraph(sampled_src, sampled_dst)

	return answer / iteration_number * edge_number * 2

def main(argv):
	global graph_name
	global subgraph_name
	global iteration_number
	global real_answer

	try:
		opts, args = getopt.getopt(argv,"h:G:S:k:a:", ["GraphName=", "SubgraphName=", "IterationNumber=", "RealAnswer="])
	except getopt.GetoptError:
		print("SampleEdge.py -G <graph name> -S <subgraph name> -k <iteration number> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleEdge.py -G <graph name> -S <subgraph name> -k <iteration number> -a <real answer>")
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
	output_file = open(cur_path + "../Result/SampleEdge_" + graph_name + "_" + subgraph_name + ".txt", 'w')
	
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