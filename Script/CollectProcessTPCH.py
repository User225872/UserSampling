import math
import os
import sys
import time

databases = ["0.25", "0.5", "1", "2", "4", "8", "16"]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for database in databases:
		cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/ProcessTPCH.py -d " + database + " -D " + database + " -m 0"

		shell = os.popen(cmd, 'r')
		shell.read()
		shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])