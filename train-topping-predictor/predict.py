import torch
import itertools
import pandas as pd
import json
import sys
from link_predict import model, pred
from find_toppings import build_edge
from graph_dataset import PizzaToppingDataset
import dgl

with open('node2id.json') as f:
    node2id = json.load(f)
id2node = {id: node for node, id in node2id.items()}

# TODO? Figure out how to save and load dgl models
# TODO: visualize toppings graph? https://docs.dgl.ai/en/0.6.x/tutorials/basics/1_first.html
def predict_toppings(toppings_found):
    edges_fw = [
        build_edge(top1, top2, node2id)
        for top1, top2 in itertools.combinations(toppings_found, 2)
    ]
    edges_bw = [
        build_edge(top2, top1, node2id)
        for top1, top2 in itertools.combinations(toppings_found, 2)
    ]
    # We want to consider all possible edges
    possible_edges = [
        dict(
            Src=node2id[top],
            Dst=i,
            Weight1=0,
            Weight2=0
        )
        for top in toppings_found
        for i in range(len(node2id))
    ]
    input_edges = edges_fw + edges_bw + possible_edges
    edge_df = pd.DataFrame.from_dict(input_edges)

    d = PizzaToppingDataset()
    g_orig = d[0]
    dataset = PizzaToppingDataset(edge_data=edge_df)
    g = dataset[0]

    node_ids = [node2id[_] for _ in toppings_found]

    with torch.no_grad():
        h = model(g_orig, g_orig.ndata['feat'])
        score = pred(g, h)
        vals, indices = torch.topk(score, min(30, score.numel()))
        valid_inds = [
            g.edges()[1][ind.item()].item()
            for ind in indices if ind not in node_ids
        ]
        # Don't select input toppings
        toppings = set(id2node[_] for _ in valid_inds)
        return toppings


"""
import networkx as nx
# Since the actual graph is undirected, we convert it for visualization
# purpose.
nx_G = G.to_networkx().to_undirected()
# Kamada-Kawaii layout usually looks pretty for arbitrary graphs
pos = nx.kamada_kawai_layout(nx_G)
nx.draw(nx_G, pos, with_labels=True, node_color=[[.7, .7, .7]])
"""


if __name__ == '__main__':
    toppings_found = sys.argv[1:]
    print(predict_toppings(toppings_found))
