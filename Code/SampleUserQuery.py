import getopt
import math
import numpy as np
import os
import psycopg2
import random
import sys
import time

def Compute(k):
	first_user = k * iteration_number
	last_user = (k + 1) * iteration_number

	if query == "Q3":
		sql_query = "select count(*) as num from sae_seed_customer, customer, orders, lineitem where orders.o_custkey = customer.c_custkey and lineitem.l_orderkey = orders.o_orderkey and o_orderdate < date'1997-01-01' and l_shipdate > date'1994-01-01' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + ";"
	elif query == "Q18":
		sql_query = "select sum(l_quantity) as num from sae_seed_customer, customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + ";"
	elif query == "Q20":
		sql_query = "select count(*) as num from sae_seed_supplier, supplier, partsupp, lineitem where l_partkey = ps_partkey and l_suppkey = ps_suppkey and s_suppkey = ps_suppkey and supplier.s_suppkey = sae_seed_supplier.value and sae_seed_supplier.id > " + str(first_user) + " and sae_seed_supplier.id <= " + str(last_user) + ";"
	elif query == "Q9":
		sql_query = "select sum((l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000) as num from sae_seed_supplier, supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and supplier.s_suppkey = sae_seed_supplier.value and sae_seed_supplier.id > " + str(first_user) + " and sae_seed_supplier.id <= " + str(last_user) + ";"
	elif query == "Q5":
		sql_query = "select count(*) as num from sae_seed_customer, region, nation, customer, supplier, orders, lineitem where r_regionkey=n_regionkey and n_nationkey=c_nationkey and n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + ";"
	elif query == "Q8":
		sql_query = "select count(*) as num from sae_seed_customer, customer, orders, lineitem, supplier, region where customer.c_custkey = orders.o_custkey and orders.o_orderkey = lineitem.l_orderkey and lineitem.l_suppkey = supplier.s_suppkey and o_orderdate >= date'1995-01-01' and o_orderdate <= date'1996-12-31' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + ";"
	elif query == "Q7":
		sql_query = "select sum(l_extendedprice * (1 - l_discount)/1000) as num from sae_seed_customer, customer, supplier, orders, lineitem where c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' and customer.c_custkey = sae_seed_customer.value and sae_seed_customer.id > " + str(first_user) + " and sae_seed_customer.id <= " + str(last_user) + ";"

	con = psycopg2.connect(database=database)
	cur = con.cursor()

	cur.execute(sql_query)
	results = cur.fetchall()

	return float(results[0][0])

def SampleAndExplore(k):
	answer = Compute(k)

	return answer / iteration_number * user_number

def main(argv):
	global database
	global query
	global users
	global iteration_number
	global real_answer

	global user_number

	try:
		opts, args = getopt.getopt(argv,"h:D:Q:k:a:", ["Database=", "Query=", "IterationNumber=", "RealAnswer="])
	except getopt.GetoptError:
		print("SampleUserQuery.py -D <database> -Q <query> -k <iteration number> -a <real answer>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("SampleUserQuery.py -D <database> -Q <query> -k <iteration number> -a <real answer>")
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
		elif opt in ("-a", "--RealAnswer"):
			real_answer = int(arg)
	
	test_number = 100

	supplier_number = float(database) * 10000
	if users == "s":
		user_number = supplier_number
	elif users == "c":
		user_number = supplier_number * 15

	cur_path = os.getcwd() + "/"
	output_file = open(cur_path + "../Result/SampleUserQuery_" + database + "_" + query + "_" + users + ".txt", 'w')

	for i in range(max_iteration_number):
		iteration_number = int(100 * math.pow(2, i))

		sum_error = []
		sum_time = []

		for k in range(test_number):
			start = time.time()

			answer = SampleAndExplore(k)

			end = time.time()

			sum_error.append(abs(answer - real_answer))
			sum_time.append(end - start)

		sum_error.sort()
	
		output_file.write(str(iteration_number) + " " + str(sum(sum_error[int(test_number * 0.2) : int(test_number * 0.8)]) / int(test_number * 0.6) / real_answer) + " " + str(sum(sum_time) / test_number) + "\n")
		output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1 : ])