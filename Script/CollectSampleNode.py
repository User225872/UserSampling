import math
import os
import sys
import time

queries = ["Edge", "TwoPath", "Triangle", "Rectangle", "TwoTriangle"]
databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]

ks = [8, 12, 10, 13]
answers = [[1851744, 19504372, 4002774, 25002584, 14122764],
			[69362378, 8511536390, 1066920780, 211062353344, 157968389924],
			[5533214, 11990180, 724056, 2098712, 51476],
			[57708624, 102025442, 2632824, 12857624, 86396]]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		for j in range(len(queries)):
			if databases[i] == "LiveJournal" and queries[j] == "Edge":
				continue
			if databases[i] == "LiveJournal" and queries[j] == "TwoPath":
				continue
			if databases[i] == "LiveJournal" and queries[j] == "Triangle":
				continue
			if databases[i] == "LiveJournal" and queries[j] == "Rectangle":
				continue
				
			a = answers[i][j]

			cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/SampleNode.py -G " + databases[i] + " -S " + queries[j] + " -k " + str(ks[i]) + " -a " + str(a) 

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])