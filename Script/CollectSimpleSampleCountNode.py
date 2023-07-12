import math
import os
import sys
import time

queries = ["Edge", "TwoPath", "Triangle", "Rectangle", "TwoTriangle"]
databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]
probabilities = [0.01, 0.02, 0.04, 0.08, 0.16]

Ts = [1024, 16384, 16, 16]
answers = [[1851744, 19504372, 4002774, 25002584, 14122764],
			[69362378, 8511536390, 1066920780, 211062353344, 157968389924],
			[5533214, 11990180, 724056, 2098712, 51476],
			[57708624, 102025442, 2632824, 12857624, 86396]]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		for j in range(len(queries)):
			for probability in probabilities:
				a = answers[i][j]

				cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/SimpleSampleCountNode.py -G " + databases[i] + " -S " + queries[j] + " -p " + str(probability) + " -T " + str(Ts[i]) + " -a " + str(a)

				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])