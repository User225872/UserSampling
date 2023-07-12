import math
import os
import sys
import time

queries = ["Triangle", "Rectangle", "TwoTriangle", "TwoPath", "Star", "ThreePath"]
databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]

ks = [8, 12, 10, 13]
answers = [[4002774, 25002584, 14122764, 19504372, 1713886716, 165970574],
			[1066920780, 211062353344, 157968389924, 8511536390, 24945845826432, 1560908466060],
			[724056, 2098712, 51476, 11990180, 35425764, 26451080],
			[2632824, 12857624, 86396, 102025442, 239601984, 183167066]]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		for j in range(len(queries)):
			a = answers[i][j]

			cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/SampleEdge.py -G " + databases[i] + " -S " + queries[j] + " -k " + str(ks[i]) + " -a " + str(a) 

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])