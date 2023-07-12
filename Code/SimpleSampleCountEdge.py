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

def ReadGraph():
	global edge_list
	global edge_number

	cur_path = os.getcwd() + '/'
	graph = open(cur_path + "../Data/Graph/" + graph_name + ".txt", 'r')

	edge_list = []

	for line in graph.readlines():
		edge = line.rstrip().split('	')

		edge_list.append((int(edge[0]), int(edge[1])))

	edge_number = len(edge_list)

def CountSubgraph(src, dst):
	if subgraph_name == "Triangle":
		src_neighbors = sampled_edge_list[sampled_node_dict[src] : sampled_node_dict[src + 1]]
		dst_neighbors = sampled_edge_list[sampled_node_dict[dst] : sampled_node_dict[dst + 1]]

		return len(set(src_neighbors).intersection(set(dst_neighbors)))
	elif subgraph_name == "TwoPath":
		src_degree = sampled_node_dict[src + 1] - sampled_node_dict[src]
		dst_degree = sampled_node_dict[dst + 1] - sampled_node_dict[dst]

		return (src_degree + dst_degree - 2) / 2
	elif subgraph_name == "Star":
		src_degree = sampled_node_dict[src + 1] - sampled_node_dict[src]
		dst_degree = sampled_node_dict[dst + 1] - sampled_node_dict[dst]

		return (src_degree - 1) * (src_degree - 2) + (dst_degree - 1) * (dst_degree - 2)
	elif subgraph_name == "ThreePath":
		src_degree = sampled_node_dict[src + 1] - sampled_node_dict[src]
		dst_degree = sampled_node_dict[dst + 1] - sampled_node_dict[dst]

		return (src_degree - 1) * (dst_degree - 1)
	elif subgraph_name == "Rectangle":
		src_neighbors = sampled_edge_list[sampled_node_dict[src] : sampled_node_dict[src + 1]]
		dst_neighbors = sampled_edge_list[sampled_node_dict[dst] : sampled_node_dict[dst + 1]]

		count = 0

		for src_neighbor in src_neighbors:
			if src_neighbor != dst:
				src_neighbors_neighbors = sampled_edge_list[sampled_node_dict[src_neighbor] : sampled_node_dict[src_neighbor + 1]]
				count += len(set(src_neighbors_neighbors).intersection(set(dst_neighbors))) - 1

		return count
	elif subgraph_name == "TwoTriangle":
		src_neighbors = sampled_edge_list[sampled_node_dict[src] : sampled_node_dict[src + 1]]
		dst_neighbors = sampled_edge_list[sampled_node_dict[dst] : sampled_node_dict[dst + 1]]

		common_neighbors_number = len(set(src_neighbors).intersection(set(dst_neighbors)))

		return common_neighbors_number * (common_neighbors_number - 1)

def Scale(number):
	if subgraph_name == "TwoPath":
		return number / (sample_probability ** 2)
	elif subgraph_name == "Triangle" or subgraph_name == "Star" or subgraph_name == "ThreePath":
		return number / (sample_probability ** 3)
	elif subgraph_name == "Rectangle":
		return number / (sample_probability ** 4)
	elif subgraph_name == "TwoTriangle":
		return number / (sample_probability ** 5)

def SampledThreshold():
	if graph_name == "Amazon" or graph_name == "LiveJournal":
		return threshold * sample_probability / 2
	elif graph_name == "RoadnetCA" or graph_name == "USRN":
		return threshold

def GlobalSensitivity(degree_bound):
	if subgraph_name == "TwoPath":
		return (degree_bound - 1) * 2
	elif subgraph_name == "Triangle":
		return (degree_bound - 1) * 6
	elif subgraph_name == "Rectangle":
		return (degree_bound - 1) * (degree_bound - 1) * 8
	elif subgraph_name == "TwoTriangle":
		return (degree_bound - 1) * (degree_bound - 2) * 2
	elif subgraph_name == "Star":
		return (degree_bound - 1) * (degree_bound - 2) * 12
	elif subgraph_name == "ThreePath":
		return (degree_bound - 1) * (degree_bound - 1) * 3

def SimpleSample():
	global sampled_users
	global sampled_edge_list
	global sampled_node_dict

	answer = 0

	sampled_users = np.random.binomial(1, sample_probability, edge_number)

	sampled_nodes = {}
	sampled_edges = set()

	id_num = 0

	for i in range(edge_number):
		if sampled_users[i] == 1:
			node_1 = edge_list[i][0]
			node_2 = edge_list[i][1]

			if node_1 in sampled_nodes.keys():
				node_id_1 = sampled_nodes[node_1]
			else:
				sampled_nodes[node_1] = id_num
				node_id_1 = id_num
				id_num += 1

			if node_2 in sampled_nodes.keys():
				node_id_2 = sampled_nodes[node_2]
			else:
				sampled_nodes[node_2] = id_num
				node_id_2 = id_num
				id_num += 1

			sampled_edges.add((node_id_1, node_id_2))
			sampled_edges.add((node_id_2, node_id_1))

	sampled_nodes = sorted(sampled_nodes.values())

	sampled_edges = list(sampled_edges)
	sampled_edges = sorted(sampled_edges, key=lambda item: item[1])
	sampled_edges = sorted(sampled_edges, key=lambda item: item[0])

	sampled_edge_list = []
	sampled_node_dict = dict()

	last_node = -1
	last_position = -1
	count = 0

	for sampled_edge in sampled_edges:
		sampled_node = int(sampled_edge[0])

		sampled_edge_list.append(int(sampled_edge[1]))

		if sampled_node != last_node:
			sampled_node_dict[sampled_node] = count
			last_node = sampled_node
			last_position = count

		count += 1

	sampled_double_edge_number = len(sampled_edge_list)
	sampled_edge_number = int(sampled_double_edge_number / 2)
	sampled_node_dict[last_node + 1] = sampled_double_edge_number

	current_src = 0
	current_count = 0
	
	while current_count < sampled_double_edge_number:
		if current_count >= sampled_node_dict[current_src + 1]:
			current_src += 1
		
		current_dst = sampled_edge_list[current_count]

		answer += CountSubgraph(current_src, current_dst)
		current_count += 1

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
		print("SimpleSampleCountEdge.py -G <graph name> -S <subgraph name> -p <sample probability> -T <threshold> -e <epsilon total> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SimpleSampleCountEdge.py -G <graph name> -S <subgraph name> -p <sample probability> -T <threshold> -e <epsilon total> -a <real answer>")
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
	output_file = open(cur_path + "../Result/SimpleSampleCountEdge_" + graph_name + "_" + subgraph_name + "_" + str(sample_probability) + ".txt", 'w')

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