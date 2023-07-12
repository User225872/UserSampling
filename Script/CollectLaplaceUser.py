import math
import os
import random
import sys
import time

test_number = 100

queries = ["Q3", "Q18", "Q20", "Q9" , "Q5", "Q8", "Q7"]
databases = ['0.25','0.5', '1', '2', '4', '8', '16']
epsilons = [0.25, 0.5, 1, 2, 4, 8, 16]

answers = [[723372, 1444801, 2888656, 5766676, 11529780, 23062854, 46119454],
			[38275475, 76520242, 153078795, 305976330, 612025449, 1223811776, 2447794544],
			[1499579, 2999671, 6001215, 11997996, 23996604, 47989007, 95988640],
			[32673369.8391777, 67130708.1556679, 141514833.5740701, 282779746.4685628, 565545200.5046818, 1130870125.3764291, 2262124211.5376097],
			[60017, 120257, 239917, 479224, 960320, 1920585, 3835730],
			[2284365, 4571965, 9147090, 18227170, 36449620, 72917175, 145835675],
			[15821054.9127257, 32160537.9574971, 66481360.9057850, 132473422.5204555, 264880259.3924716, 529795443.1298605, 1059498349.8034907]]

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def ComputeGlobalSensitivity(query):
	if query == "Q3" or query == "Q20" or query == "Q5" or query == "Q8":
		return 1000
	elif query == "Q18" or query == "Q9" or query == "Q7":
		return 1000000

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		database = databases[i]

		output_file = open(cur_path + "../Result/LaplaceUser_" + database + ".txt", 'w')

		for j in range(len(queries)):
			query = queries[j]

			for epsilon in epsilons:
				sum_error = []
				sum_time = []

				for k in range(test_number):
					start = time.time()

					real_answer = answers[j][i]
					answer = real_answer + LapNoise() * ComputeGlobalSensitivity(query) / epsilon

					end = time.time()

					sum_error.append(abs(answer - real_answer))
					sum_time.append(end - start)

				sum_error.sort()
	
				output_file.write(query + " " + str(epsilon) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
				output_file.flush()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])