import getopt
import os
import psycopg2
import sys
import time

def ReadQuery():
	global query_path
	global query

	cur_path = os.getcwd() + '/'

	query = ""
	query_file = open(cur_path + query_path, 'r')

	for line in query_file.readlines():
		query = query + line
		if ";" in query:
			query = query.replace('\n', " ")
			break

def ExtractInformation():
	global database_name
	global output_path
	global query

	con = psycopg2.connect(database=database_name)
	cur = con.cursor()

	cur.execute(query)
	results = cur.fetchall()

	cur_path = os.getcwd() + '/'

	output_file = open(cur_path + output_path, 'w')

	for i in range(len(results)):
		result = results[i]

		for j in range(len(result)):
			output_file.write(str(result[j]) + " ")

		output_file.write("\n")

	con.commit()
	con.close()

def main(argv):
	global database_name
	global query_path
	global output_path

	try:
		opts, args = getopt.getopt(argv,"h:D:Q:O:",["Database=", "QueryPath=", "Output="])
	except getopt.GetoptError:
		print("ExtractInfo.py -D <database name> -Q <query path> -O <output path>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ExtractInfo.py -D <database name> -Q <query path> -O <output path>")
			sys.exit()
		elif opt in ("-D", "--Database"):
			database_name = arg
		elif opt in ("-Q","--QueryPath"):
			query_path = arg
		elif opt in ("-O","--Output"):
			output_path = arg

	ReadQuery()
	ExtractInformation()
	
if __name__ == "__main__":
   main(sys.argv[1:])