import os
import sys

graph_names = ["Amazon", "LiveJournal", "RoadnetCA", "USRN"]

def Preprocess(graph_name):
	cur_path = os.getcwd() + '/'
	file = open(cur_path + "../Data/Graph/" + graph_name + ".txt", 'r')

	nodes = {}
	edges = set()

	id_num = 0

	for line in file.readlines():
		data = line.rstrip().split('	')

		node_1 = data[0]
		node_2 = data[1]

		if node_1 in nodes.keys():
			node_id_1 = nodes[node_1]
		else:
			nodes[node_1] = id_num
			node_id_1 = id_num
			id_num += 1

		if node_2 in nodes.keys():
			node_id_2 = nodes[node_2]
		else:
			nodes[node_2] = id_num
			node_id_2 = id_num
			id_num += 1

		if node_id_1 != node_id_2:
			tuple_1 = (node_id_1, node_id_2)
			tuple_2 = (node_id_2, node_id_1)

			edges.add(tuple_1)
			edges.add(tuple_2)

	nodes = sorted(nodes.values())

	edges = list(edges)
	edges = sorted(edges, key=lambda item: item[1])
	edges = sorted(edges, key=lambda item: item[0])

	write_file_node = open(cur_path + "../Data/Node/" + graph_name + ".txt", 'w')
	write_file_edge = open(cur_path + "../Data/Edge/" + graph_name + ".txt", 'w')

	for i in nodes:
		write_file_node.write(str(i) + '\n')

	l = len(edges)

	for i in range(l):
		write_file_edge.write(str(i) + '	' + str(edges[i][0]) + '	' + str(edges[i][1]) + '\n')

def main(argv):
	for graph_name in graph_names:
		Preprocess(graph_name)

if __name__ == "__main__":
	main(sys.argv[1 : ])
