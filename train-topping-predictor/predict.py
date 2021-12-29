import torch
import json
from link_predict import model, pred, g

# TODO make a graph from very few toppings and get predicted links
# TODO? Figure out how to save and load dgl models

with open('node2id.json') as f:
    node2id = json.load(f)
id2node = {id: node for node, id in node2id.items()}

with torch.no_grad():
    h = model(g, g.ndata['feat'])
    score = pred(g, h)
    vals, indices = torch.topk(score, 50)
    print(indices)
    indices = indices[torch.hstack((indices.diff(), indices[-1])) > 1]
    print(indices)
    all_preds = set()
    for ind in indices:
        n1, n2 = map(lambda x: x.item(), g.find_edges(ind))
        all_preds.add((id2node[n1], id2node[n2]))
    print(all_preds)