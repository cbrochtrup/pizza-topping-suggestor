import dgl
from dgl.data import DGLDataset
import pandas as pd
import torch
import networkx as nx
import numpy as np

class PizzaToppingDataset(DGLDataset):
    edge_data_ = None
    def __init__(self, edge_data=None):
        self.edge_data_ = edge_data
        super().__init__(name='pizza_toppings')

    def process(self):
        nodes_data = pd.read_csv('nodes.csv')
        edges_data = pd.read_csv('edges.csv')

        if self.edge_data_ is not None:
          edges_data = self.edge_data_
        edges_src = torch.from_numpy(edges_data['Src'].to_numpy())
        edges_dst = torch.from_numpy(edges_data['Dst'].to_numpy())
        edges_that_exist = edges_data['Src'].unique()
        edge_features = torch.from_numpy(
            np.vstack(
                (edges_data['Weight1'].to_numpy(), edges_data['Weight2'].to_numpy())
            )
            # gedges_data['Weight1'].to_numpy()
        ).float().T

        # nodes_data = nodes_data[nodes_data.isin(edges_that_exist)]

        # node_labels = torch.from_numpy(nodes_data['Club'].astype('category').cat.codes.to_numpy())
        node_cat = nodes_data['category'].astype('category').cat.codes.to_numpy()
        node_features = torch.from_numpy(
            np.vstack((nodes_data['length'].to_numpy(), node_cat))
        ).float().T
        self.graph = dgl.graph((edges_src, edges_dst), num_nodes=nodes_data.shape[0])
        self.graph.ndata['feat'] = node_features
        # self.graph.ndata['label'] = torch.from_numpy(node_cat).long()
        self.graph.edata['weight'] = edge_features

    def __getitem__(self, i):
        return self.graph

    def __len__(self):
        return 1


def get_connected_toppings(to_start):
    nx_G = graph.to_networkx().to_undirected()
    nx_G = nx.relabel_nodes(nx_G, id2node)
    return list(nx_G.neighbors(start_node))


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import json
    import sys

    dataset = PizzaToppingDataset()
    graph = dataset[0]

    start_node = sys.argv[1]
    with open('node2id.json') as f:
        node2id = json.load(f)
    id2node = {id: node for node, id in node2id.items()}
    
    # Since the actual graph is undirected, we convert it for visualization
    # purpose.
    nx_G = graph.to_networkx().to_undirected()
    nx_G = nx.relabel_nodes(nx_G, id2node)
    to_plot = list(nx_G.neighbors(start_node))
    to_plot += [start_node]
    nx_G = nx_G.subgraph(to_plot)
    # to_plot = list(nx_G.neighbors(0))
    # Kamada-Kawaii layout usually looks pretty for arbitrary graphs
    pos = nx.kamada_kawai_layout(nx_G)
    nx.draw(
        nx_G, pos,
        with_labels=True,
        node_color=[[.7, .7, .7]],
        nodelist=to_plot,
        font_color='blue'
    )
    plt.savefig('graph.png')
