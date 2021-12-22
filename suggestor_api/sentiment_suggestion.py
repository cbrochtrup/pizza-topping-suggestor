import json
import random
from pathlib import Path
from collections import defaultdict

from transformers import pipeline
import numpy as np
 
file_dir = Path(__file__).parent
scores_file = file_dir / "pizza_ingredient_scores.json"
with open(file_dir / "pizza_ingredients.json") as f:
    ingredients = json.load(f)

def get_polarity(score_dict):
    label = score_dict['label']
    score = score_dict['score']
    if label == 'NEGATIVE':
        # 1 -> -0.5 and 0.5 -> 0
        return -score + 0.5
    elif label == 'POSITIVE':
        # 1 -> 0.5 and 0.5 -> 0
        return score - 0.5
    else:
        raise Exception(f'We got an unexpcted label {label}')

def generate_scores_json():
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
    return_dict = {}
    for category, ing_list in ingredients.items():
        scores = sentiment_analysis(ing_list)
        return_dict[category] = {ing: get_polarity(score) for ing, score in zip(ing_list, scores)}
    with open(scores_file, "w") as f:
        json.dump(return_dict, f, indent=2, sort_keys=True)


def build_sentiment_to_toppings_map(invalid_topping_groups=None):
    if invalid_topping_groups is None:
        invalid_topping_groups = []
    bin_size = 0.1
    with open(scores_file) as f:
        dict_scores = json.load(f)
    all_scores = [
        dict_scores[k] for k in dict_scores.keys()
        if k not in invalid_topping_groups
    ]
    all_scores = {k: v for d in all_scores for k, v in d.items()}
    binned_scores = defaultdict(list)
    bin_edges = np.linspace(-0.5, 0.5, int(1/bin_size) + 1)
    for bin_start, bin_stop in zip(bin_edges, bin_edges[1:]):
        for k, v in all_scores.items():
            if v > bin_start and v <= bin_stop:
                binned_scores[bin_start].append(k)
    return binned_scores


def choose_toppings(score, toppings_map):
    bins = sorted(list(toppings_map.keys()))
    bin = next(b for b in bins if score > b)
    appropriate_toppings = toppings_map[bin]
    topping = random.choice(appropriate_toppings)
    return topping
    

def suggest_toppings(query, toppings_map, n_toppings):
    words = query.split()
    split_length = int(len(words)/n_toppings)
    sentence_words = [" ".join(words[i:i+split_length]) for i in range(0, len(words), split_length)]
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
    scores = sentiment_analysis(sentence_words, padding='longest')
    toppings = [choose_toppings(get_polarity(score), toppings_map) for score in scores]
    return toppings


if __name__ == "__main__":
    m = build_sentiment_to_toppings_map()
    suggest_toppings(
        'My day was kind of rough, I could not find my blanket and my children all tried to kill me',
        m, 3
    )
    print('hi')