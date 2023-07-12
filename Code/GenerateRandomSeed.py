import os
import numpy as np
import sys
	
def main(argv):
	cur_path = os.getcwd() + '/'
	databases = ['0.25','0.5', '1', '2', '4', '8', '16']

	databases = ['1']

	for database in databases:
		customer_number = int(float(database) * 150000)
		supplier_number = int(float(database) * 10000)

		test_customer_number = customer_number * 10
		test_supplier_number = supplier_number * 10

		write_file = open(cur_path + "../Temp/" + database + "_customer.txt", 'w')

		for i in range(test_customer_number):
			sampled_user = np.random.randint(0, customer_number) + 1
			write_file.write(str(i) + "|" + str(sampled_user) + "\n")

		write_file.close()

		write_file = open(cur_path + "../Temp/" + database + "_supplier.txt", 'w')

		for i in range(test_supplier_number):
			sampled_user = np.random.randint(0, supplier_number) + 1
			write_file.write(str(i) + "|" + str(sampled_user) + "\n")

		write_file.close()

if __name__ == "__main__":
	main(sys.argv[1 : ])
