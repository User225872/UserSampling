import getopt
import math
import numpy as np
import os
import random
import sys
import time

def ReadGraph():
	global node_number

	cur_path = os.getcwd() + '/'
	node_file = open(cur_path + "../Data/Node/" + graph_name + ".txt", 'r')

	node_number = 0

	for line in node_file.readlines():
		node_number += 1

def SimpleSample(i):
	cur_path = os.getcwd() + '/'
	edge_file = open(cur_path + "../Data/Edge/" + graph_name + ".txt", 'r')
	sampled_node_file = open(cur_path + "../Temp/SimpleSampleNode_" + graph_name + "_" + str(sample_probability) + "_" + str(i) + "_Node.txt", 'w')
	sampled_edge_file = open(cur_path + "../Temp/SimpleSampleNode_" + graph_name + "_" + str(sample_probability) + "_" + str(i) + "_Edge.txt", 'w')

	sampled_users = np.random.binomial(1, sample_probability, node_number)

	for node in range(node_number):
		if sampled_users[node] == 1:
			sampled_node_file.write(str(node) + "\n")
	
	count = 0

	for line in edge_file.readlines():
		edge = line.rstrip().split('	')

		if sampled_users[int(edge[1])] == 1 and sampled_users[int(edge[2])] == 1:
			sampled_edge_file.write(str(count) + "	" + edge[1] + "	" + edge[2] + "\n")

			count += 1

def main(argv):
	global graph_name
	global sample_probability

	try:
		opts, args = getopt.getopt(argv,"h:G:p:", ["GraphName=", "SampleProbability="])
	except getopt.GetoptError:
		print("SimpleSampleNode.py -G <graph name> -p <sample probability>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SimpleSampleNode.py -G <graph name> -p <sample probability>")
			sys.exit()
		elif opt in ("-G", "--GraphName"):
			graph_name = str(arg)
		elif opt in ("-p", "--SampleProbability"):
			sample_probability = float(arg)
	
	test_number = 1

	ReadGraph()

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SimpleSampleNode_" + graph_name + "_" + str(sample_probability) + ".txt", 'w')

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