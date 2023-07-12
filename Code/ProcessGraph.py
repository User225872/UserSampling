import getopt
import os
import psycopg2
import sys

def main(argv):
	node_file_path = ''
	edge_file_path = ''
	database_name = ''

	try:
		opts, args = getopt.getopt(argv, "h:n:e:D:m:", ["nodefile=", "edgefile=", "database="])
	except getopt.GetoptError:
		print("ProcessGraph.py -n <nodefile> -e <edgefile> -D <database>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ProcessGraph.py -n <nodefile> -e <edgefile> -D <database>")
			sys.exit()
		elif opt in ("-n", "--nodefile"):
			node_file_path = arg
		elif opt in ("-e", "--edgefile"):
			edge_file_path = arg
		elif opt in ("-D", "--Database"):
			database_name = arg

	con = psycopg2.connect(database="jfangad")
	cur = con.cursor()
	con.autocommit = True

	cur_path = os.getcwd() + '/'

	node_file = open(cur_path + node_file_path, 'r')
	edge_file = open(cur_path + edge_file_path, 'r')

	code = "CREATE Database \"" + database_name + "\";"
	cur.execute(code)

	con.commit()
	con.close()

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	code = "CREATE TABLE node (ID INTEGER NOT NULL);"
	cur.execute(code)
	code = "CREATE TABLE edge (ID INTEGER NOT NULL, FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);"
	cur.execute(code)
	code = "CREATE INDEX on node using hash (ID);"
	cur.execute(code)
	code = "CREATE INDEX on edge using hash (FROM_ID);"
	cur.execute(code)
	code = "CREATE INDEX on edge using hash (TO_ID);"
	cur.execute(code)

	con.commit()
	con.close()

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	cur.copy_from(node_file, "node")
	cur.copy_from(edge_file, "edge", sep='	')

	con.commit()
	con.close()

if __name__ == "__main__":
	main(sys.argv[1:])