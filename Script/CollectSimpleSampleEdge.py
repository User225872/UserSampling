import math
import os
import sys
import time

databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]
probabilities = [0.01, 0.02, 0.04, 0.08, 0.16]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		for j in range(len(probabilities)):
			cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/SimpleSampleEdge.py -G " + databases[i] + " -p " + str(probabilities[j])

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])