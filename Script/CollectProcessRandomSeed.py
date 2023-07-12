import math
import os
import sys
import time

databases = ["0.25", "0.5", "1", "2", "4", "8", "16"]
relations = ["customer", "supplier"]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for database in databases:
		for relation in relations:
			cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/ProcessRandomSeed.py -d ../Temp/" + database + "_" + relation + ".txt" + " -D " + database + " -n " + "sae_seed_" + relation + " -m 0"

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])