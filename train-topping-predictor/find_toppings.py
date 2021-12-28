import json
import sys
import csv

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


def contains_topping(toppings_dict, top):
    for category, toppings in toppings_dict.items():
        # Consider making this more permissive if predictions bad
        if top.lower() in toppings:
            return True, category
    return False, None


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
        

if __name__ == '__main__':
    toppings_file = sys.argv[1]
    pizza_descriptions = sys.argv[2]
    t = load_topping_json(toppings_file)
    nodes = generate_nodes(t)
    write_csv(nodes, 'nodes.csv')
    # TODO: write edges file noting which toppings are in what graph