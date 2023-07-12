import math
import os
import sys
import time

queries = [0, 1, 2, 3]
databases = ["Amazon", "RoadnetCA", "USRN"]
answers = [[4002774, 19504372, 25002584, 14122764],
			[724056, 11990180, 2098712, 51476],
			[2632824, 102025442, 12857624, 86396]]

def main(argv):
	cur_path = os.getcwd() + '/'
	
	for i in range(len(databases)):
		for j in range(len(queries)):
			a = answers[i][j]

			cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "/../Code/Residual.py -D" + databases[i] + " -T " + str(queries[j]) + " -a " + str(a)

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

if __name__ == "__main__":
	main(sys.argv[1:])