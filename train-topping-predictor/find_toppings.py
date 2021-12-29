import json
import sys
import csv
import string
import itertools

# Import toppings JSON
# Create node CSV, each node is a topping
# Create edge CSV noting toppings in each pizza description


def write_csv(list_of_dicts, csv_name):
    with open(csv_name, 'w', newline='') as csvfile:
        fieldnames = list_of_dicts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in list_of_dicts:
            writer.writerow(row)


def load_topping_json(file_json):
    with open(file_json) as f:
        toppings = json.load(f)
    # Normalize toppings
    toppings = {
        cat: list(map(lambda x: x.lower(), t)) for cat, t in toppings.items()
    }
    return toppings


def load_pizza_descriptions(file_descriptions):
    with open(file_descriptions) as f:
        descriptions = [_.strip() for _ in f.readlines()]
    # Remove weird 'comma' text
    # toppings = {
    #     cat: list(map(lambda x: x.replace('commaa',''), t)) for cat, t in toppings.items()
    # }
    descriptions = map(
        lambda s: s.translate(str.maketrans('', '', string.punctuation)),
        descriptions
    )
    descriptions = map(
        lambda s: s.lower(),
        descriptions
    )
    descriptions = map(
        lambda x: x.replace('comma',''),
        descriptions
    )
    descriptions = map(
        lambda x: x.replace('amp ',''),
        descriptions
    )
    return list(_ for _ in descriptions if _)


def contains_topping(toppings_dict, top):
    for category, toppings in toppings_dict.items():
        # Consider making this more permissive if predictions bad
        # ie, checking if top is a substring of any topping
        if top.lower() in toppings:
            return category
    return None


def generate_nodes(toppings_dict):
    nodes = []
    i = 0
    for category, toppings in toppings_dict.items():
        for top in toppings:
            nodes.append(
                dict(
                    id=i,
                    name=top,
                    length=len(top),
                    category=category
                )
            )
            i += 1
    return nodes


def build_edge(top1, top2, node2id):
    return dict(
        Src=node2id[top1],
        Dst=node2id[top2],
        Weight1=len(top1),
        Weight2=len(top2)
    )


def find_topping_edges(pizza_descriptions, toppings_dict, node2id):
    out_list_dict = []
    for desc in pizza_descriptions:
        toppings_found = [
            word for word in desc.split()
            if contains_topping(toppings_dict, word)
        ]
        if len(toppings_found) == 0:
            continue
        # We need at least two toppings for an edge to form
        elif len(toppings_found) == 1:
            toppings_found.append(toppings_dict['cheese'][0])

        edges_fw = [
            build_edge(top1, top2, node2id)
            for top1, top2 in itertools.combinations(toppings_found, 2)
        ]
        # Bidirectional edges becaues I don't know what I'm doing
        edges_bw = [
            build_edge(top2, top1, node2id)
            for top1, top2 in itertools.combinations(toppings_found, 2)
        ]
        out_list_dict.extend(edges_fw + edges_bw)
    return out_list_dict


if __name__ == '__main__':
    # toppings_file = '/home/colin/projects/pizza-topping-suggestor/suggestor_api/pizza_ingredients.json'
    # pizza_descriptions = '/home/colin/projects/pizza-topping-suggestor/train-topping-predictor/pizza_descriptions.csv'
    toppings_file = sys.argv[1]
    pizza_descriptions = sys.argv[2]
    
    t = load_topping_json(toppings_file)
    nodes = generate_nodes(t)
    node2id = {node['name']: node['id'] for node in nodes}
    write_csv(nodes, 'nodes.csv')
    with open('node2id.json', 'w') as f:
        json.dump(node2id, f, indent=2, sort_keys=True)
    descriptions = load_pizza_descriptions(pizza_descriptions)
    edges = find_topping_edges(descriptions, t, node2id)
    write_csv(edges, 'edges.csv')
