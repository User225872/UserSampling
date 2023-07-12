import math
import os
import sys
import time

test_number = 100

databases = ["Amazon", "RoadnetCA", "USRN"]
probabilities = [0.01, 0.02, 0.04, 0.08, 0.16]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for database in databases:
		output_file = open(cur_path + "../Result/ProcessGraphEdge_" + database + ".txt", 'w')

		for probability in probabilities:
			sum_time = []

			for i in range(test_number):
				start = time.time()

				cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/ProcessGraph.py -n ../Temp/SimpleSampleEdge_" + database + "_" + str(probability) + "_" + str(i) + "_Node.txt -e ../Temp/SimpleSampleEdge_" + database + "_" + str(probability) + "_" + str(i) + "_Edge.txt -D SimpleSampleEdge_" + database + "_" + str(probability) + "_" + str(i)

				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

				end = time.time()

				sum_time.append(end - start)

			output_file.write(str(probability) + " " + str(sum(sum_time) / test_number) + "\n")
			output_file.flush()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])