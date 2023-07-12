import getopt
import math
import numpy as np
import os
import random
import sys
import time

def ReadGraph():
	global edge_list
	global edge_number

	cur_path = os.getcwd() + '/'
	graph_file = open(cur_path + "../Data/Graph/" + graph_name + ".txt", 'r')

	edge_list = []

	for line in graph_file.readlines():
		edge = line.rstrip().split('	')

		edge_list.append((int(edge[0]), int(edge[1])))

	edge_number = len(edge_list)

def SimpleSample(i):
	cur_path = os.getcwd() + '/'
	sampled_edge_file = open(cur_path + "../Temp/SimpleSampleEdge_" + graph_name + "_" + str(sample_probability) + "_" + str(i) + "_Edge.txt", 'w')
	sampled_node_file = open(cur_path + "../Temp/SimpleSampleEdge_" + graph_name + "_" + str(sample_probability) + "_" + str(i) + "_Node.txt", 'w')

	sampled_users = np.random.binomial(1, sample_probability, edge_number)

	sampled_nodes = set()

	count = 0

	for edge in range(edge_number):
		if sampled_users[edge] == 1:
			if edge_list[edge][0] not in sampled_nodes:
				sampled_nodes.add(edge_list[edge][0])

			if edge_list[edge][1] not in sampled_nodes:
				sampled_nodes.add(edge_list[edge][1])

			sampled_edge_file.write(str(count) + "	" + str(edge_list[edge][0]) + "	" + str(edge_list[edge][1]) + "\n")

			count += 1

			sampled_edge_file.write(str(count) + "	" + str(edge_list[edge][1]) + "	" + str(edge_list[edge][0]) + "\n")

	for node in sampled_nodes:
		sampled_node_file.write(str(node) + "\n")

def main(argv):
	global graph_name
	global sample_probability

	try:
		opts, args = getopt.getopt(argv,"h:G:p:", ["GraphName=", "SampleProbability="])
	except getopt.GetoptError:
		print("SimpleSampleEdge.py -G <graph name> -p <sample probability>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SimpleSampleEdge.py -G <graph name> -p <sample probability>")
			sys.exit()
		elif opt in ("-G", "--GraphName"):
			graph_name = str(arg)
		elif opt in ("-p", "--SampleProbability"):
			sample_probability = float(arg)
	
	test_number = 100

	ReadGraph()

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SimpleSampleEdge_" + graph_name + "_" + str(sample_probability) + ".txt", 'w')

	sum_time = []

	for i in range(test_number):
		start = time.time()

		SimpleSample(i)

		end = time.time()

		sum_time.append(end - start)
	
	output_file.write(str(sum(sum_time) / test_number) + "\n")
	output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1 : ])