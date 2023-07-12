import os
import sys
import time

test_number = 3

queries = ["Edge", "TwoPath", "Triangle", "Rectangle", "TwoTriangle", "Star", "ThreePath"]
databases = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]

queries = ["Edge_node", "TwoPath_node", "Triangle_node", "Rectangle_node", "TwoTriangle_node"]
databases = ["Amazon", "RoadnetCA", "USRN"]

def main(argv):
	cur_path = os.getcwd() + '/'
	output_file = open(cur_path + "../Result/ExtractInfoTime.txt", 'w')

	for database in databases:
		for query in queries:
			sum_time = []

			for i in range(test_number):
				cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/ExtractInfo.py -D " + database + " -Q ../Query/" + query + ".txt -O ../Information/" + database + "_" + query + ".txt"

				start = time.time()

				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

				end = time.time()
				sum_time.append(end - start)
	
			output_file.write(database + " " + query + " " + str(sum(sum_time) / test_number) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])