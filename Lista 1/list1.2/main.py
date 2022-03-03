import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import sys


class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def add(self, node):
        if self.head is None:
            self.head = Node(node)
        else:
            tmp = Node(node)
            tmp.next = self.head
            self.head = tmp

    def print_list(self):
        if self.head is None:
            return
        else:
            tmp = self.head
            while tmp.next is not None:
                print(tmp.data)
                tmp = tmp.next


def add_prop_dfs(graph):
    for n in range(graph.number_of_nodes()):
        graph.nodes[n]['id'] = n
        graph.nodes[n]['color'] = 'white'
        graph.nodes[n]['dis'] = float('inf')
        graph.nodes[n]['fi'] = None


def dfs(direction, number_of_nodes, number_of_edges, edges):
    global llist
    llist = LinkedList()

    if len(edges) > 0:
        if direction:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()
        for i in range(number_of_nodes):
            graph.add_node(i)
        graph.add_edges_from(edges)
    else:
        graph = nx.gnm_random_graph(number_of_nodes, number_of_edges, directed=direction, seed=100)
        # graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)])

    print_graph(graph, "graph_dfs10000.pdf", direction)

    add_prop_dfs(graph)
    # print(nx.find_cycle(graph,orientation='original'))
    for i in range(number_of_nodes):
        graph.nodes[i]['color'] = 'white'
        graph.nodes[i]['pi'] = None

    global time
    global array_visited, stack
    array_visited = [False] * (number_of_nodes)
    stack = [False] * (number_of_nodes)
    time = 0

    for i in range(number_of_nodes):
        if graph.nodes[i]['color'] == 'white':
            dfs_search(graph, i)

    # tree = nx.Graph()
    # for i in range(graph.number_of_nodes()):
    #     if graph.nodes[i]['pi'] is not None:
    #         tree.add_edge(i, graph.nodes[i]['pi'])
    #
    # print_graph(tree, "tree_dfs.pdf", type=False)

    llist.print_list()


def dfs_search(graph, node):
    global llist
    global time
    global stack
    global array_visited

    array_visited[node] = True
    stack[node] = True

    time = time + 1
    graph.nodes[node]['dis'] = time
    graph.nodes[node]['color'] = 'gray'

    for v in graph.adj[node]:
        if graph.nodes[v]['color'] == 'white':
            graph.nodes[v]['pi'] = graph.nodes[node]['id']
            print("Odwiedzam wierzcholek " + str(graph.nodes[v]['id']))
            dfs_search(graph, v)
        if stack[graph.nodes[v]['id']]:
            print("Cykliczny")
            sys.exit(0)

    stack[node] = False
    graph.nodes[node]['color'] = 'black'
    time = time + 1
    graph.nodes[node]['fi'] = time
    llist.add(graph.nodes[node])
    # print(str(graph.nodes[node]['id']) + " id ->" + str(graph.nodes[node]['dis']) + "/" + str(graph.nodes[node]['fi']))


def print_graph(graph, name, type):
    plt.figure(num=None, figsize=(30, 40), dpi=300)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, arrows=type)
    nx.draw_networkx_labels(graph, pos)

    plt.savefig(name, bbox_inches="tight")
    pylab.close()
    del fig


def begin(data):
    # direction = True
    # number_of_nodes = 6
    # number_of_edges = 0
    # edges = [(0, 1), (1, 2), (2, 3), (4, 5), (1, 4), (5, 3)]

    edges = []
    for i in range(int(data[2])):
        edges.append((input()))
        if edges[0] == '-1':
            edges = []
            break

    edges = [tuple(map(int, element.split(' '))) for element in edges]
    dfs(data[0] == 'D', int(data[1]), int(data[2]), edges)


if __name__ == '__main__':

    data = []
    sys.setrecursionlimit(150000)
    for line in sys.argv:
        if '\n' == line.rstrip():
            break
        data.append(line)

    data.pop(0)
    begin(data)
