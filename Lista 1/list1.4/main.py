import networkx as nx
import sys
from matplotlib import pylab
import matplotlib.pyplot as plt


def add_prop_dfs(graph):
    for n in range(graph.number_of_nodes()):
        graph.nodes[n]['id'] = n
        graph.nodes[n]['color'] = 'white'
        graph.nodes[n]['dis'] = float('inf')
        graph.nodes[n]['fi'] = None


def dfs(direction, number_of_nodes, number_of_edges, edges):
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

    print_graph(graph, "graph_dfs10000.pdf", direction)
    add_prop_dfs(graph)

    for i in range(number_of_nodes):
        graph.nodes[i]['color'] = 'white'
        graph.nodes[i]['pi'] = None

    global time
    global color
    color = [0 for i in range(number_of_nodes)]
    time = 0
    for i in range(number_of_nodes):
        if graph.nodes[i]['color'] == 'white':
            dfs_search(graph, i)

    V1 = []
    V2 = []
    for i in range(number_of_nodes):
        if int(graph.nodes[i]['color']):
            V1.append(graph.nodes[i]['id'])
        else:
            V2.append(graph.nodes[i]['id'])
    print("Pierwsze rozbicie:" + str(V1) + "\n")
    print("Drugie rozbicie:" + str(V2))


def dfs_search(graph, node):
    global time
    global color
    time = time + 1
    graph.nodes[node]['dis'] = time
    graph.nodes[node]['color'] = 'gray'

    for v in graph.adj[node]:
        if graph.nodes[v]['color'] == 'white':
            color[graph.nodes[v]['id']] = not color[graph.nodes[node]['id']]
            graph.nodes[v]['pi'] = graph.nodes[node]['id']
            print("Odwiedzam wierzcholek " + str(graph.nodes[v]['id']))
            dfs_search(graph, v)
        elif color[graph.nodes[v]['id']] == color[graph.nodes[node]['id']]:
            print("Nie jest dzuwdzielny")
            sys.exit(0)

    graph.nodes[node]['color'] = str(time % 2)
    time = time + 1
    graph.nodes[node]['fi'] = time


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


# print(str(graph.nodes[node]['id']) + " id ->" + str(graph.nodes[node]['dis']) + "/" + str(graph.nodes[node]['fi']))


def begin(data):
    # direction = False
    # number_of_nodes = 5
    # number_of_edges = 5/6
    # edges = [(0, 1), (1, 2), (1, 3), (0, 4), (4, 2)]
    # edges = [(0, 1), (1, 2), (1, 3), (0, 4), (4, 2),(2,3)] Nie jest
    edges = []
    for i in range(int(data[2])):
        edges.append(input())
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
