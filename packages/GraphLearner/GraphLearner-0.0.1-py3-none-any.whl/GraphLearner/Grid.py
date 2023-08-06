import math
import networkx
from matplotlib import pyplot as plt
from itertools import count


class Grid:
    def __init__(
            self,
            dimensions=None,
            with_diagonals=False,
            assignment=None,
            graph=None
    ):
        if dimensions:
            self.dimensions = dimensions
            self.graph = create_grid_graph(dimensions, with_diagonals)
            if not assignment:
                thresholds = tuple(math.floor(n / 2) for n in self.dimensions)
                assignment = {
                    node: color_quadrants(node, thresholds) for node in self.graph.nodes
                }
        else:
            raise Exception("Not a good way to create a Partition")

    def draw_grid(self, col_attr, x=12, y=12, cmap=plt.cm.coolwarm):
        plt.figure(figsize=(x, y))

        gtemp = networkx.Graph(self.graph)
        for edge in gtemp.edges: gtemp.edges[edge]['weight'] = 1

        cds = set(networkx.get_node_attributes(gtemp, col_attr).values())
        mapping = dict(zip(sorted(cds), count()))
        nodes = gtemp.nodes()
        colors = [mapping[gtemp.nodes[n][col_attr]] for n in nodes]
        pos = networkx.spring_layout(gtemp, iterations=2000)
        ec = networkx.draw_networkx_edges(gtemp, pos, alpha=0.2)
        nc = networkx.draw_networkx_nodes(gtemp, pos, nodelist=nodes, node_color=colors,
                                          with_labels=True, node_size=350, cmap=cmap)
        plt.axis('off')
        plt.show()

    def __str__(self):
        return "Welcome!  Your graph has {n} by {m} nodes.\n\n" \
               "Here are some useful functions/usages that assume you called your grid object G. \nEverything shown here translates to networkx usability. \n\n" \
               "\t * G.graph.nodes(data=True) will give you all of your nodes and the data that exists on each of them.\n" \
               "\t \t * Removing the (data=True) will simply print the node names, which are repsented by their coordinates if this were on a lattice.\n" \
               "\t \t * All nodes come pre-populated with population=1, area=1, their perimeter, and if they are a boundary node or not.\n\n" \
               "\t * G.graph.edges(data=True) will give you all of the edges and their associated data.\n" \
               "\t \t * Removing the (data=True will simply print the edge names.\n" \
               "\t \t * All edges come pre-populated their shared perimeter lengths.\n\n" \
               "\t * Here is how to loop over nodes while creating a new attribute on them.  The attribute we will create will be called CD.\n" \
               "\t \t - for node in G.graph.nodes:\n" \
               "\t \t \t G.graph.nodes(data=True)[node]['CD'] = 1\n\n" \
               "\t * Here is how to loop over edges while assigning them the networkx built in keyword 'weight'.\n" \
               "\t \t - for edge in G.graph.edges:\n" \
               "\t \t \t G.graph.edges[edge]['weight'] = 10\n\n" \
               "\t * To visualize the graph, which at least helps me in understanding what's happening, I have built a method that makes this easy.\n" \
               "\t \t * G.draw_grid(col_attribute)\n" \
               "\t \t \t * This has a number of attributes attributes: \n" \
               "\t \t \t \t - col_attr (String, required, one of the attributes that exists on all nodes you would like to color by)\n" \
               "\t \t \t \t -        x (int, default: 12, controls length of x-axis for matplotlib plot)\n" \
               "\t \t \t \t -        y (int, default: 12, controls length of y-axis for matplotlib plot)\n" \
               "\t \t \t \t -     cmap (plt.cm, default: plt.cm.coolwarm, specifies color scheme. A list of available options can be found here: https://matplotlib.org/tutorials/colors/colormaps.html)\n" \
               "\t \t * Here is an example using all default values passing in your attribute name.\n" \
               "\t \t \t * G.draw_grid('boundary_node')\n" \
               "\t \t * Here is an example setting all attributes. You need to import matplotlibs pyplot to use the cmap attribute.\n" \
               "\t \t \t * G.draw_grid('boundary_node', x=10, y=10, cmap=plt.cm.viridis)".format(n=self.dimensions[0], m=self.dimensions[1])


def create_grid_graph(dimensions, with_diagonals):
    if len(dimensions) != 2:
        raise ValueError("Dr. Mitchel... why are you trying to draw lines?")
    m, n = dimensions
    graph = networkx.generators.lattice.grid_2d_graph(m, n)

    networkx.set_edge_attributes(graph, 1, "shared_perim")

    if with_diagonals:
        nw_to_se = [
            ((i, j), (i + 1, j + 1)) for i in range(m - 1) for j in range(n - 1)
        ]
        sw_to_ne = [
            ((i, j + 1), (i + 1, j)) for i in range(m - 1) for j in range(n - 1)
        ]
        diagonal_edges = nw_to_se + sw_to_ne
        graph.add_edges_from(diagonal_edges)
        for edge in diagonal_edges:
            graph.edges[edge]["shared_perim"] = 0

    networkx.set_node_attributes(graph, 1, "population")
    networkx.set_node_attributes(graph, 1, "area")

    tag_boundary_nodes(graph, dimensions)

    return graph


def tag_boundary_nodes(graph, dimensions):
    m, n = dimensions
    for node in graph.nodes:
        if node[0] in [0, m - 1] or node[1] in [0, n - 1]:
            graph.nodes[node]["boundary_node"] = True
            graph.nodes[node]["boundary_perim"] = get_boundary_perim(node, dimensions)
        else:
            graph.nodes[node]["boundary_node"] = False


def get_boundary_perim(node, dimensions):
    m, n = dimensions
    if node in [(0, 0), (m - 1, 0), (0, n - 1), (m - 1, n - 1)]:
        return 2
    elif node[0] in [0, m - 1] or node[1] in [0, n - 1]:
        return 1
    else:
        return 0


def color_quadrants(node, thresholds):
    x, y = node
    x_color = 0 if x < thresholds[0] else 1
    y_color = 0 if y < thresholds[1] else 2
    return x_color + y_color

