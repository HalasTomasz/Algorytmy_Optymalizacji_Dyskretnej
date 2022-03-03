import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import sys
import scipy as sp


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
        graph = nx.gnm_random_graph(number_of_nodes, number_of_edges, directed=direction,seed=100)

    print_graph(graph, "graph_dfs10000.pdf", direction)

    add_prop_dfs(graph)

    for i in range(number_of_nodes):
        graph.nodes[i]['color'] = 'white'
        graph.nodes[i]['pi'] = None

    global time
    time = 0
    for i in range(number_of_nodes):
        if graph.nodes[i]['color'] == 'white':
            dfs_search(graph, i)

    tree = nx.Graph()
    for i in range(graph.number_of_nodes()):
        if graph.nodes[i]['pi'] is not None:
            tree.add_edge(i, graph.nodes[i]['pi'])

    print_graph(tree, "tree_dfs10000.pdf", type=False)

    return graph


def dfs_search(graph, node):
    global time
    time = time + 1
    graph.nodes[node]['dis'] = time
    graph.nodes[node]['color'] = 'gray'

    for v in graph.adj[node]:
        if graph.nodes[v]['color'] == 'white':
            graph.nodes[v]['pi'] = graph.nodes[node]['id']
            #print("Odwiedzam wierzcholek " + str(graph.nodes[v]['id']))
            dfs_search(graph, v)

    graph.nodes[node]['color'] = 'black'
    time = time + 1
    graph.nodes[node]['fi'] = time
    #print(str(graph.nodes[node]['id']) + " id ->" + str(graph.nodes[node]['dis']) + "/" + str(graph.nodes[node]['fi']))


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


def dfs_T(graph,number_of_nodes):

    for n in range(graph.number_of_nodes()):
        graph.nodes[n]['id'] = n
        graph.nodes[n]['color'] = 'white'
        graph.nodes[n]['dis'] = float('inf')
        graph.nodes[n]['pi'] = None

    global time
    time = 0
    tmp = [(graph.nodes[i]["fi"],graph.nodes[i]["id"]) for i in range (number_of_nodes)]
    tmp.sort(key=lambda x:x[0],reverse=True)

    for i in tmp:
        if graph.nodes[i[1]]['color'] == 'white':
            dfs_search(graph, i[1])

  #   for i in range(number_of_nodes):
  #        print(graph.nodes[i])

    tree = nx.Graph()
    for i in range(graph.number_of_nodes()):
        if graph.nodes[i]['pi'] is not None:
            tree.add_edge(i, graph.nodes[i]['pi'])
        else:
            tree.add_node((i))

    print_graph(tree, "tree_dfsT10000.pdf", type=False)

    return graph

def dfs_search(graph, node):
    global time
    time = time + 1
    graph.nodes[node]['dis'] = time
    graph.nodes[node]['color'] = 'gray'

    for v in graph.adj[node]:
        if graph.nodes[v]['color'] == 'white':
            graph.nodes[v]['pi'] = graph.nodes[node]['id']
            print("Odwiedzam wierzcholek " + str(graph.nodes[v]['id']))
            dfs_search(graph, v)

    graph.nodes[node]['color'] = 'black'
    time = time + 1
    graph.nodes[node]['fi'] = time
    #print(str(graph.nodes[node]['id']) + " id ->" + str(graph.nodes[node]['dis']) + "/" + str(graph.nodes[node]['fi']))

def begin(data):

    # number_of_nodes = 8
    # number_of_edges = 14
    # edges = [(0, 1), (1, 2), (2, 3), (3, 2), (1, 4), (1, 5), (2, 6), (3, 7), (4, 0),(4,5),(5,6),(6,5),(6,7),(7,7)]

    edges = []
    for i in range(int(data[2])):
        edges.append((input()))
        if edges[0] == '-1':
            edges = []
            break

    edges = [tuple(map(int, element.split(' '))) for element in edges]

    graph = dfs(data[0] == 'D', int(data[1]), int(data[2]), edges)
    graph = graph.reverse()
    print_graph(graph, "graph_rev10000.pdf", data[0] == 'D')
    dfs_T(graph, int(data[1]))


if __name__ == '__main__':

    data = []
    sys.setrecursionlimit(150000)
    for line in sys.argv:
        if '\n' == line.rstrip():
            break
        data.append(line)

    data.pop(0)
    begin(data)

