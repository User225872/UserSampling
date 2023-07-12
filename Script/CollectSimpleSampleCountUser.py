import math
import os
import sys
import time

queries = ["Q3_c", "Q18_c", "Q20_s", "Q9_s", "Q5_cs", "Q8_cs", "Q18_cs", "Q7_cs"]
databases = ['0.25', '0.5', '1', '2', '4', '8', '16']
probabilities = [0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16]

answers = [[723372, 1444801, 2888656, 5766676, 11529780, 23062854, 46119454],
			[38275475, 76520242, 153078795, 305976330, 612025449, 1223811776, 2447794544],
			[1499579, 2999671, 6001215, 11997996, 23996604, 47989007, 95988640],
			[32673369, 67130708, 141514833, 282779746, 565545200, 1130870125, 2262124211],
			[60017, 120257, 239917, 479224, 960320, 1920585, 3835730],
			[2284365, 4571965, 9147090, 18227170, 36449620, 72917175, 145835675],
			[38275475, 76520242, 153078795, 305976330, 612025449, 1223811776, 2447794544],
			[15821054, 32160537, 66481360, 132473422, 264880259, 529795443, 1059498349]]

def CollectResult():
	cur_path = os.getcwd() + '/'

	for i in range(len(databases)):
		for j in range(len(queries)):
			for probability in probabilities:
				a = answers[j][i]

				cmd = "../../anaconda3/envs/test/bin/python " + cur_path + "../Code/SimpleSampleCountUser.py -D " + databases[i] + " -Q " + queries[j] + " -p " + str(probability) + " -a " + str(a)

				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

def main(argv):
	CollectResult()

if __name__ == "__main__":
	main(sys.argv[1:])