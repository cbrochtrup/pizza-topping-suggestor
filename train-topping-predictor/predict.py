import torch
import itertools
import pandas as pd
import json
import sys
from link_predict import model, pred
from find_toppings import build_edge
from graph_dataset import PizzaToppingDataset

with open('node2id.json') as f:
    node2id = json.load(f)
id2node = {id: node for node, id in node2id.items()}

# TODO? Figure out how to save and load dgl models
toppings_found = sys.argv[1:]
# TODO abstract this out in find_toppings
edges_fw = [
    build_edge(top1, top2, node2id)
    for top1, top2 in itertools.combinations(toppings_found, 2)
]
# Bidirectional edges becaues I don't know what I'm doing
edges_bw = [
    build_edge(top2, top1, node2id)
    for top1, top2 in itertools.combinations(toppings_found, 2)
]
input_edges = edges_fw + edges_bw
edge_df = pd.DataFrame.from_dict(input_edges)

dataset = PizzaToppingDataset(edge_data=edge_df)
g = dataset[0]

with torch.no_grad():
    h = model(g, g.ndata['feat'])
    score = pred(g, h)
    vals, indices = torch.topk(score, 10)
    print(indices)
    indices = indices[torch.hstack((indices.diff(), indices[-1])) > 1]
    print(indices)
    all_preds = set()
    for ind in indices:
        n1, n2 = map(lambda x: x.item(), g.find_edges(ind))
        all_preds.add((id2node[n1], id2node[n2]))
    print(all_preds)
