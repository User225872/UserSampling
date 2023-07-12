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

def CreateTables(relation_name):
	con = psycopg2.connect(database=database)
	cur = con.cursor()

	code = "CREATE TABLE " + relation_name + "(VALUE INTEGER NOT NULL);"
	cur.execute(code)

	con.commit()
	con.close()

def CopyTables(file_path, relation_name):
	con = psycopg2.connect(database=database)
	cur = con.cursor()
	con.autocommit = True

	file = open(file_path, 'r')
	cur.copy_from(file, relation_name, sep='|')

	con.commit()
	con.close()

def DropTables(relation_name):
	con = psycopg2.connect(database=database)
	cur = con.cursor()

	code = "DROP TABLE " + relation_name + ";"
	cur.execute(code)

	con.commit()
	con.close()

def Compute():
	if query == "Q3":
		sql_query = "select count(*) from seed, customer, orders, lineitem where orders.o_custkey = customer.c_custkey and lineitem.l_orderkey = orders.o_orderkey and o_orderdate < date'1997-01-01' and l_shipdate > date'1994-01-01' and seed.value = c_custkey;"
	elif query == "Q18":
		if users == "c":
			sql_query = "select sum(l_quantity) from seed, customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey and seed.value = c_custkey;"
		elif users == "cs":
			sql_query = "select sum(l_quantity) from customer_seed, supplier_seed, customer, orders, lineitem, supplier where c_custkey = o_custkey and o_orderkey = l_orderkey and lineitem.l_suppkey = supplier.s_suppkey and customer_seed.value = c_custkey and supplier_seed.value = s_suppkey;"
	elif query == "Q20":
		sql_query = "select count(*) from seed, supplier, partsupp, lineitem where l_partkey = ps_partkey and l_suppkey = ps_suppkey and s_suppkey = ps_suppkey and seed.value = s_suppkey;"
	elif query == "Q9":
		sql_query = "select sum((l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000) from seed, supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and seed.value = s_suppkey;"
	elif query == "Q5":
		sql_query = "select count(*) from customer_seed, supplier_seed, region, nation, customer, supplier, orders, lineitem where r_regionkey=n_regionkey and n_nationkey=c_nationkey and n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and customer_seed.value = c_custkey and supplier_seed.value = s_suppkey;"
	elif query == "Q8":
		sql_query = "select count(*) from customer_seed, supplier_seed, customer, orders, lineitem, supplier, region where customer.c_custkey = orders.o_custkey and orders.o_orderkey = lineitem.l_orderkey and lineitem.l_suppkey = supplier.s_suppkey and o_orderdate >= date'1995-01-01' and o_orderdate <= date'1996-12-31' and customer_seed.value = c_custkey and supplier_seed.value = s_suppkey;"
	elif query == "Q7":
		sql_query = "select sum(l_extendedprice * (1 - l_discount)/1000) from customer_seed, supplier_seed, customer, supplier, orders, lineitem where c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' and customer_seed.value = c_custkey and supplier_seed.value = s_suppkey;"

	con = psycopg2.connect(database=database)
	cur = con.cursor()

	cur.execute(sql_query)
	results = cur.fetchall()

	con.commit()
	con.close()

	if users == "c" or users == "s":
		DropTables("seed")
	elif users == "cs":
		DropTables("customer_seed")
		DropTables("supplier_seed")

	return float(results[0][0])

def Scale(number):
	if users == "c" or users == "s":
		return number / sample_probability
	elif users == "cs":
		return number / (sample_probability ** 2)

def GlobalSensitivity():
	if users == "c" or users == "s":
		if query == "Q3" or query == "Q20" or query == "Q5" or query == "Q8":
			return 1000
		elif query == "Q18" or query == "Q9" or query == "Q7":
			return 1000000
	elif users == "cs":
		if query == "Q3" or query == "Q20" or query == "Q5" or query == "Q8":
			return 1000 * sample_probability * 2
		elif query == "Q18" or query == "Q9" or query == "Q7":
			return 1000000 * sample_probability * 2

def SimpleSample():
	cur_path = os.getcwd() + '/'

	if users == "c":
		write_file_path = cur_path + "../Temp/" + database + "_" + query + "_" + users + "_" + str(sample_probability) + ".csv"
		write_file = open(write_file_path, 'w')

		sampled_users = np.random.binomial(1, sample_probability, customer_number)

		for i in range(customer_number):
			if sampled_users[i] > 0:
				write_file.write(str(i+1) + "\n")

		write_file.close()

		CreateTables("seed")
		CopyTables(write_file_path, "seed")
	elif users == "s":
		write_file_path = cur_path + "../Temp/" + database + "_" + query + "_" + users + "_" + str(sample_probability) + ".txt"
		write_file = open(write_file_path, 'w')

		sampled_users = np.random.binomial(1, sample_probability, supplier_number)

		for i in range(supplier_number):
			if sampled_users[i] > 0:
				write_file.write(str(i+1) + "\n")

		write_file.close()

		CreateTables("seed")
		CopyTables(write_file_path, "seed")
	elif users == "cs":
		write_file_path_customer = cur_path + "../Temp/" + database + "_" + query + "_" + users + "_" + str(sample_probability) + "_customer.txt"
		write_file_customer = open(write_file_path_customer, 'w')

		sampled_users = np.random.binomial(1, sample_probability, customer_number)
		
		for i in range(customer_number):
			if sampled_users[i] > 0:
				write_file_customer.write(str(i+1) + "\n")

		write_file_customer.close()

		CreateTables("customer_seed")
		CopyTables(write_file_path_customer, "customer_seed")

		write_file_path_supplier = cur_path + "../Temp/" + database + "_" + query + "_" + users + "_" + str(sample_probability) + "_supplier.txt"
		write_file_supplier = open(write_file_path_supplier, 'w')

		sampled_users = np.random.binomial(1, sample_probability, supplier_number)
		
		for i in range(supplier_number):
			if sampled_users[i] > 0:
				write_file_supplier.write(str(i+1) + "\n")

		write_file_supplier.close()

		CreateTables("supplier_seed")
		CopyTables(write_file_path_supplier, "supplier_seed")

	return Compute()

def main(argv):
	global database
	global query
	global users
	global sample_probability
	global real_answer

	global customer_number
	global supplier_number

	try:
		opts, args = getopt.getopt(argv,"h:D:Q:p:a:", ["Database=", "Query=", "sampleProbability=", "RealAnswer="])
	except getopt.GetoptError:
		print("SimpleSampleCountUser.py -D <database> -Q <query> -p <sample probability> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SimpleSampleCountUser.py -D <database> -Q <query> -p <sample probability> -a <real answer>")
			sys.exit()
		elif opt in ("-D", "--Database"):
			database = str(arg)
		elif opt in ("-Q", "--Qeury"):
			query_users = str(arg)
			query_users = query_users.split('_')
			query = query_users[0]
			users = query_users[1]
		elif opt in ("-p", "--SampleProbability"):
			sample_probability = float(arg)
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)
	
	test_number = 100
	epsilons = [0.25, 0.5, 1, 2, 4, 8, 16]

	customer_number = int(float(database) * 150000)
	supplier_number = int(float(database) * 10000)
	
	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SimpleSampleCountUser_" + database + "_" + query + "_" + users + "_" + str(sample_probability) +".txt", 'w')

	sum_error = dict()
	sum_error[0] = []

	for epsilon_total in epsilons:
		sum_error[epsilon_total] = []

	sum_time_sample = []
	sum_time_noise = []

	for i in range(test_number):
		start = time.time()

		sample_answer = SimpleSample()
		answer = Scale(sample_answer)

		end = time.time()

		sum_error[0].append(abs(answer - real_answer))
		sum_time_sample.append(end - start)

		for epsilon_total in epsilons:
			start = time.time()

			epsilon = epsilon_total / sample_probability

			global_sensitivity = GlobalSensitivity()

			answer = sample_answer + LapNoise() * global_sensitivity / epsilon
			answer = Scale(answer)

			end = time.time()

			sum_error[epsilon_total].append(abs(answer - real_answer))
			sum_time_noise.append(end - start)

	sum_error[0].sort()
	
	output_file.write(str(0) + " " + str(sum(sum_error[0][int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time_sample) / test_number) + "\n")

	for epsilon_total in epsilons:
		sum_error[epsilon_total].sort()

		output_file.write(str(epsilon_total) + " " + str(sum(sum_error[epsilon_total][int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time_sample) / test_number + sum(sum_time_noise) / test_number / len(epsilons)) + "\n")

if __name__ == "__main__":
	main(sys.argv[1 : ])