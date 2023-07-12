import getopt
import math
import numpy as np
import os
import psycopg2
import random
import sys
import time

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def BinarySearch(epsilon_sample_k, delta_0):
	left = 0
	right = epsilon_sample_k
	accuracy = 10 ** -5

	while right - left > accuracy:
		mid = (left + right) / 2

		if math.sqrt(2 * iteration_number * math.log(1 / delta_0)) * mid + iteration_number * mid * (math.e ** mid - 1) > epsilon_sample_k:
			right = mid
		else:
			left = mid

	return left

def ComputeEpsilonsBefore():
	global epsilon_sample
	global epsilon_pub
	global delta_pub

	epsilon_sample_k = 0.8 * epsilon_total
	epsilon_pub = 0.2 * epsilon_total

	delta_0 = 0.8 * delta_total
	delta_pub = 0.2 * delta_total

	epsilon_sample = BinarySearch(epsilon_sample_k, delta_0)

def ComputeEpsilonsAfter():
	global epsilon
	global tilde_user_number

	tilde_user_number = user_number + LapNoise() * threshold / epsilon_pub
	check_user_number = tilde_user_number - threshold / epsilon_pub * math.log(1 / 2 / delta_pub)

	epsilon = math.log(check_user_number / threshold * (math.e ** epsilon_sample - 1) + 1)

def Compute(k):
	first_user = k * iteration_number
	last_user = (k + 1) * iteration_number

	if query == "Q3":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select count(*) as num from sae_seed_customer, customer, orders, lineitem where orders.o_custkey = customer.c_custkey and lineitem.l_orderkey = orders.o_orderkey and o_orderdate < date'1997-01-01' and l_shipdate > date'1994-01-01' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + " group by customer.c_custkey) as a;"
	elif query == "Q18":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select sum(l_quantity) as num from sae_seed_customer, customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + " group by customer.c_custkey) as a;"
	elif query == "Q20":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select count(*) as num from sae_seed_supplier, supplier, partsupp, lineitem where l_partkey = ps_partkey and l_suppkey = ps_suppkey and s_suppkey = ps_suppkey and supplier.s_suppkey = sae_seed_supplier.value and sae_seed_supplier.id > " + str(first_user) + " and sae_seed_supplier.id <= " + str(last_user) + " group by supplier.s_suppkey) as a;"
	elif query == "Q9":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select sum((l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000) as num from sae_seed_supplier, supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and supplier.s_suppkey = sae_seed_supplier.value and sae_seed_supplier.id > " + str(first_user) + " and sae_seed_supplier.id <= " + str(last_user) + " group by supplier.s_suppkey) as a;"
	elif query == "Q5":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select count(*) as num from sae_seed_customer, region, nation, customer, supplier, orders, lineitem where r_regionkey=n_regionkey and n_nationkey=c_nationkey and n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + " group by customer.c_custkey) as a;"
	elif query == "Q8":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select count(*) as num from sae_seed_customer, customer, orders, lineitem, supplier, region where customer.c_custkey = orders.o_custkey and orders.o_orderkey = lineitem.l_orderkey and lineitem.l_suppkey = supplier.s_suppkey and o_orderdate >= date'1995-01-01' and o_orderdate <= date'1996-12-31' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + " group by customer.c_custkey) as a;"
	elif query == "Q7":
		sql_query = "select sum(least(" + str(clipping_threshold) + ", num)) from (select sum(l_extendedprice * (1 - l_discount)/1000) as num from sae_seed_customer, customer, supplier, orders, lineitem where c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + " group by customer.c_custkey) as a;"

	con = psycopg2.connect(database=database)
	cur = con.cursor()

	cur.execute(sql_query)
	results = cur.fetchall()

	return float(results[0][0])

def SampleAndExplore(k):
	answer = Compute(k)

	for i in range(iteration_number):
		answer += LapNoise() * clipping_threshold / epsilon

	return answer / iteration_number * tilde_user_number

def main(argv):
	global database
	global query
	global users
	global iteration_number
	global threshold
	global clipping_threshold
	global epsilon_total
	global delta_total
	global real_answer

	global user_number

	try:
		opts, args = getopt.getopt(argv,"h:D:Q:k:T:C:e:d:a:", ["Database=", "Query=", "IterationNumber=", "Threshold=", "ClippingThreshold=", "EpsilonTotal=", "DeltaTotal=", "RealAnswer="])
	except getopt.GetoptError:
		print("SampleAndExploreUserQuery.py -D <database> -Q <query> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleAndExploreUserQuery.py -D <database> -Q <query> -k <iteration number> -T <threshold> -C <clipping threshold> -e <epsilon total> -d <delta total> -a <real answer>")
			sys.exit()
		elif opt in ("-D", "--Database"):
			database = str(arg)
		elif opt in ("-Q", "--Qeury"):
			query_users = str(arg)
			query_users = query_users.split('_')
			query = query_users[0]
			users = query_users[1]
		elif opt in ("-k", "--IterationNumber"):
			max_iteration_number = int(arg)
		elif opt in ("-T", "--Threshold"):
			threshold = int(arg)
		elif opt in ("-C", "--ClippingThreshold"):
			max_clipping_threshold = int(arg)
		elif opt in ("-e", "--EpsilonTotal"):
			epsilon_total = float(arg)
		elif opt in ("-d", "--DeltaTotal"):
			delta_total = float(arg)
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)
	
	test_number = 100

	supplier_number = float(database) * 10000
	if users == "s":
		user_number = supplier_number
	elif users == "c":
		user_number = supplier_number * 15

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SampleAndExploreUserQuery_" + database + "_" + query + "_" + users + "_" + str(epsilon_total) + "_" + str(threshold) + ".txt", 'w')

	for i in range(max_iteration_number):
		iteration_number = int(100 * math.pow(2, i))

		for j in range(max_clipping_threshold - 5, max_clipping_threshold):
			clipping_threshold = int(math.pow(2, j))

			sum_error = []
			sum_time = []

			for k in range(test_number):
				start = time.time()

				ComputeEpsilonsBefore()
				ComputeEpsilonsAfter()

				answer = SampleAndExplore(k)
				print(answer)

				end = time.time()

				sum_error.append(abs(answer - real_answer))
				sum_time.append(end - start)

			sum_error.sort()
	
			output_file.write(str(iteration_number) + " " + str(clipping_threshold) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1 : ])