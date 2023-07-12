import getopt
import os
import psycopg2
import sys
import time

def CreateTables():
	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "CREATE TABLE " + relation_name + "(ID INTEGER NOT NULL, VALUE INTEGER NOT NULL);"
	cur.execute(code)

	con.commit()
	con.close()

def CopyTables():
	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	file = open(file_path, 'r')
	cur.copy_from(file, relation_name, sep='|')

	con.commit()
	con.close()

def IndexTables():
	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "CREATE INDEX " + relation_name + "_I on " + relation_name + "(ID);"
	cur.execute(code)
	code = "CLUSTER " + relation_name + " USING " + relation_name + "_I;"
	cur.execute(code)
	
	con.commit()
	con.close()

def DropTables():
	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "DROP TABLE " + relation_name + ";"
	cur.execute(code)

	con.commit()
	con.close()

def main(argv):
	global database_name
	global relation_name
	global file_path

	model = 0

	try:
		opts, args = getopt.getopt(argv, "h:d:D:n:m:", ["file_path=", "database=", "relation_name", "model="])
	except getopt.GetoptError:
		print("ProcessRandomSeed.py -d <file path> -D <database> -n <relation name> -m <model:0(import)/1(clean)>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ProcessRandomSeed.py -d <file path> -D <database> -n <relation name> -m <model:0(import)/1(clean)>")
			sys.exit()
		elif opt in ("-d", "--file"):
			file_path = arg
		elif opt in ("-D", "--Database"):
			database_name = arg
		elif opt in ("-n", "--relation"):
			relation_name = arg
		elif opt in ("-m", "--model"):
			model = int(arg)

	start = time.time()

	if model != 0:
		DropTables()
	else:
		cur_path = os.getcwd() + '/'
		file_path = cur_path + file_path

		CreateTables()
		CopyTables()
		IndexTables()

	end = time.time()

	print(end - start)

if __name__ == "__main__":
	main(sys.argv[1:])