import getopt
import os
import psycopg2
import sys

def CreateTables():
	global database_name

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "CREATE TABLE region (R_REGIONKEY INTEGER NOT NULL, R_NAME CHAR(25) NOT NULL, R_COMMENT VARCHAR(152));"
	cur.execute(code)
	code = "CREATE TABLE nation (N_NATIONKEY INTEGER NOT NULL, N_NAME CHAR(25) NOT NULL, N_REGIONKEY INTEGER NOT NULL, N_COMMENT VARCHAR(152));"
	cur.execute(code)
	code = "CREATE TABLE supplier (S_SUPPKEY INTEGER NOT NULL, S_NAME CHAR(25) NOT NULL, S_ADDRESS VARCHAR(40) NOT NULL, S_NATIONKEY INTEGER NOT NULL, S_PHONE CHAR(15) NOT NULL, S_ACCTBAL DECIMAL(15,2) NOT NULL, S_COMMENT VARCHAR(101) NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE customer (C_CUSTKEY INTEGER NOT NULL, C_NAME VARCHAR(25) NOT NULL, C_ADDRESS VARCHAR(40) NOT NULL, C_NATIONKEY INTEGER NOT NULL, C_PHONE CHAR(15) NOT NULL, C_ACCTBAL DECIMAL(15,2) NOT NULL, C_MKTSEGMENT CHAR(10) NOT NULL, C_COMMENT VARCHAR(117) NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE part (P_PARTKEY INTEGER NOT NULL, P_NAME VARCHAR(55) NOT NULL, P_MFGR CHAR(25) NOT NULL, P_BRAND CHAR(10) NOT NULL, P_TYPE VARCHAR(25) NOT NULL, P_SIZE INTEGER NOT NULL, P_CONTAINER CHAR(10) NOT NULL, P_RETAILPRICE DECIMAL(15,2) NOT NULL, P_COMMENT VARCHAR(23) NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE partsupp (PS_PARTKEY INTEGER NOT NULL, PS_SUPPKEY INTEGER NOT NULL, PS_AVAILQTY INTEGER NOT NULL, PS_SUPPLYCOST DECIMAL(15,2) NOT NULL, PS_COMMENT VARCHAR(199) NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE orders (O_ORDERKEY INTEGER NOT NULL, O_CUSTKEY INTEGER NOT NULL, O_ORDERSTATUS CHAR(1) NOT NULL, O_TOTALPRICE DECIMAL(15,2) NOT NULL, O_ORDERDATE DATE NOT NULL, O_ORDERPRIORITY CHAR(15) NOT NULL, O_CLERK CHAR(15) NOT NULL, O_SHIPPRIORITY INTEGER NOT NULL, O_COMMENT VARCHAR(79) NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE lineitem (L_ORDERKEY INTEGER NOT NULL, L_PARTKEY INTEGER NOT NULL, L_SUPPKEY INTEGER NOT NULL, L_LINENUMBER INTEGER NOT NULL, L_QUANTITY DECIMAL(15,2) NOT NULL, L_EXTENDEDPRICE DECIMAL(15,2) NOT NULL, L_DISCOUNT DECIMAL(15,2) NOT NULL, L_TAX DECIMAL(15,2) NOT NULL, L_RETURNFLAG CHAR(1) NOT NULL, L_LINESTATUS CHAR(1) NOT NULL, L_SHIPDATE DATE NOT NULL, L_COMMITDATE DATE NOT NULL, L_RECEIPTDATE DATE NOT NULL, L_SHIPINSTRUCT CHAR(25) NOT NULL, L_SHIPMODE CHAR(10) NOT NULL, L_COMMENT VARCHAR(44) NOT NULL);"
	cur.execute(code)

	con.commit()
	con.close()

def CopyTables():
	global database_name
	global dataset
	global data_path
	global relations

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	for element in relations:
		element_file_path = data_path + element.lower() + ".csv"

		element_file = open(element_file_path, 'r')
		cur.copy_from(element_file, element.lower(), sep='|')

	con.commit()
	con.close()

def IndexTables():
	global database_name

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "CREATE INDEX R_I on region(R_REGIONKEY);"
	cur.execute(code)
	code = "CLUSTER region USING R_I;"
	cur.execute(code)
	code = "CREATE INDEX N_I on nation(N_NATIONKEY);"
	cur.execute(code)
	code = "CLUSTER nation USING N_I;"
	cur.execute(code)
	code = "CREATE INDEX S_I on supplier(S_SUPPKEY);"
	cur.execute(code)
	code = "CLUSTER supplier USING S_I;"
	cur.execute(code)
	code = "CREATE INDEX C_I on customer(C_CUSTKEY);"
	cur.execute(code)
	code = "CLUSTER customer USING C_I;"
	cur.execute(code)
	code = "CREATE INDEX P_I on part(P_PARTKEY);"
	cur.execute(code)
	code = "CLUSTER part USING P_I;"
	cur.execute(code)
	code = "CREATE INDEX PS_I on partsupp(PS_PARTKEY,PS_SUPPKEY);"
	cur.execute(code)
	code = "CLUSTER partsupp USING PS_I;"
	cur.execute(code)
	code = "CREATE INDEX O_I on orders(O_ORDERKEY);"
	cur.execute(code)
	code = "CLUSTER orders USING O_I;"
	cur.execute(code)
	code = "CREATE INDEX L_I on lineitem(L_PARTKEY,L_SUPPKEY);"
	cur.execute(code)
	code = "CLUSTER lineitem USING L_I;"
	cur.execute(code)

	con.commit()
	con.close()

def AddKeys():
	global database_name

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "ALTER TABLE region ADD PRIMARY KEY (R_REGIONKEY);"
	cur.execute(code)
	code = "ALTER TABLE nation ADD PRIMARY KEY (N_NATIONKEY);"
	cur.execute(code)
	code = "ALTER TABLE supplier ADD PRIMARY KEY (S_SUPPKEY);"
	cur.execute(code)
	code = "ALTER TABLE customer ADD PRIMARY KEY (C_CUSTKEY);"
	cur.execute(code)
	code = "ALTER TABLE part ADD PRIMARY KEY (P_PARTKEY);"
	cur.execute(code)
	code = "ALTER TABLE partsupp ADD PRIMARY KEY (PS_PARTKEY,PS_SUPPKEY);"
	cur.execute(code)
	code = "ALTER TABLE orders ADD PRIMARY KEY (O_ORDERKEY);"
	cur.execute(code)
	code = "ALTER TABLE lineitem ADD PRIMARY KEY (L_ORDERKEY,L_LINENUMBER);"
	cur.execute(code)
	code = "COMMIT WORK;"
	cur.execute(code)

	code = "ALTER TABLE nation ADD FOREIGN KEY (N_REGIONKEY) references region;"
	cur.execute(code)
	code = "ALTER TABLE supplier ADD FOREIGN KEY (S_NATIONKEY) references nation;"
	cur.execute(code)
	code = "ALTER TABLE customer ADD FOREIGN KEY (C_NATIONKEY) references nation;"
	cur.execute(code)
	code = "ALTER TABLE partsupp ADD FOREIGN KEY (PS_SUPPKEY) references supplier;"
	cur.execute(code)
	code = "ALTER TABLE partsupp ADD FOREIGN KEY (PS_PARTKEY) references part;"
	cur.execute(code)
	code = "ALTER TABLE orders ADD FOREIGN KEY (O_CUSTKEY) references customer;"
	cur.execute(code)
	code = "ALTER TABLE lineitem ADD FOREIGN KEY (L_ORDERKEY) references orders;"
	cur.execute(code)
	code = "ALTER TABLE lineitem ADD FOREIGN KEY (L_PARTKEY,L_SUPPKEY) references partsupp;"
	cur.execute(code)
	code = "COMMIT WORK;"
	cur.execute(code)

	con.commit()
	con.close()

def DropTables():
	global database_name
	global relations

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	for element in reversed(relations):
		code = "DROP TABLE " + element.lower() + ";"
		cur.execute(code)

	con.commit()
	con.close()

def main(argv):
	global database_name
	global dataset
	global data_path
	global relations

	datasets = ["0.25", "0.5", "1", "2", "4", "8", "16"]
	dataset = ''
	database_name = ''
	model = 0

	relations = ["REGION", "NATION", "SUPPLIER", "CUSTOMER", "PART", "PARTSUPP", "ORDERS", "LINEITEM"]

	try:
		opts, args = getopt.getopt(argv, "h:d:D:m:", ["dataset=", "database=", "model="])
	except getopt.GetoptError:
		print("ProcessTPCH.py -d <dataset> -D <database> -m <model:0(import)/1(clean)>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ProcessTPCH.py -d <dataset> -D <database> -m <model:0(import)/1(clean)>")
			sys.exit()
		elif opt in ("-d", "--dataset"):
			dataset = arg
		elif opt in ("-D", "--Database"):
			database_name = arg
		elif opt in ("-m", "--model"):
			model = int(arg)

	if model != 0:
		DropTables()
	else:
		if dataset not in datasets:
			print("Invalid dataset.")
			sys.exit()

		cur_path = os.getcwd() + '/'
		data_path = cur_path + "../Data/TPCH/" + dataset + "/"

		CreateTables()
		CopyTables()
		IndexTables()
		AddKeys()

if __name__ == "__main__":
	main(sys.argv[1:])