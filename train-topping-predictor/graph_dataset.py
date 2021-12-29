import dgl
from dgl.data import DGLDataset
import pandas as pd
import torch
import numpy as np

class PizzaToppingDataset(DGLDataset):
    def __init__(self):
        super().__init__(name='pizza_toppings')

    def process(self):
        edges_data = pd.read_csv('edges.csv')
        edges_src = torch.from_numpy(edges_data['Src'].to_numpy())
        edges_dst = torch.from_numpy(edges_data['Dst'].to_numpy())
        edges_that_exist = edges_data['Src'].unique()
        edge_features = torch.from_numpy(
            np.vstack(
                (edges_data['Weight1'].to_numpy(), edges_data['Weight2'].to_numpy())
            )
            # gedges_data['Weight1'].to_numpy()
        ).float().T
        print(f'edge_features are shape {edge_features.shape}')

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

        # If your dataset is a node classification dataset, you will need to assign
        # masks indicating whether a node belongs to training, validation, and test set.
        # n_nodes = nodes_data.shape[0]
        # n_train = int(n_nodes * 0.6)
        # n_val = int(n_nodes * 0.2)
        # train_mask = torch.zeros(n_nodes, dtype=torch.bool)
        # val_mask = torch.zeros(n_nodes, dtype=torch.bool)
        # test_mask = torch.zeros(n_nodes, dtype=torch.bool)
        # train_mask[:n_train] = True
        # val_mask[n_train:n_train + n_val] = True
        # test_mask[n_train + n_val:] = True
        # self.graph.ndata['train_mask'] = train_mask
        # self.graph.ndata['val_mask'] = val_mask
        # self.graph.ndata['test_mask'] = test_mask

    def __getitem__(self, i):
        return self.graph

    def __len__(self):
        return 1

dataset = PizzaToppingDataset()
graph = dataset[0]
