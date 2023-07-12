import math
import os
import sys
import time

repeat_times = 10

# queries = ["Edge_node", "TwoPath_node", "Triangle_node", "TwoTriangle_node", "Rectangle_node"]
# databases = ["Amazon", "RoadnetCA", "USRN"]
# epsilons = [0.25, 0.5, 1, 2, 4, 8, 16]

# upper_bounds = [1024, 16, 16]

queries = ["Q5_cs", "Q18_cs", "Q7_cs", "Q8_cs"] 
databases = ['0.25','0.5', '1', '2', '4', '8', '16']
epsilons = [4, 8]

GS = ["1000", "1000000", "1000", "1000000"]

p = 10

def main(argv):
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/R2T_3.txt", 'w')

	for j in range(len(databases)):
		for i in range(len(queries)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "/../Code/R2T.py -I ../Information/" + databases[j] + "_" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -G " + GS[i] + " -p " + str(p)

				for k in range(repeat_times):
					start = time.time()

					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()
		
					errors.append(float(res[0]))

					shell.close()

					end = time.time()

					sum_time += end - start

				errors.sort()

				output_file.write(databases[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])