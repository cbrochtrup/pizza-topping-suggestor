import dgl
from dgl.data import DGLDataset
import pandas as pd
import torch
import numpy as np

class PizzaToppingDataset(DGLDataset):
    edge_data_ = None
    def __init__(self, edge_data=None):
        self.edge_data_ = edge_data
        super().__init__(name='pizza_toppings')

    def process(self):
        edges_data = pd.read_csv('edges.csv')
        if self.edge_data_ is not None:
          print('UUUUUUUUUUUUUUUUUUUU')
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
        print(edge_features.shape)

        nodes_data = pd.read_csv('nodes.csv')
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

dataset = PizzaToppingDataset()
graph = dataset[0]
