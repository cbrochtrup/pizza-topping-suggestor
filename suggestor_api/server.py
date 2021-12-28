"""
This basic example loads a pre-trained model from the web and uses it to
generate sentence embeddings for a given list of sentences.
"""

import logging

from fastapi import FastAPI
from sentiment_suggestion import build_sentiment_to_toppings_map, suggest_toppings


logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

LOGGER = logging.getLogger()
TOPPING_MAP = build_sentiment_to_toppings_map()

api = FastAPI()


@api.get('/')
async def root():
    return {"message": "Hello World"}


@api.get('/top')
async def generate_toppings():
    toppings = suggest_toppings(
        'My day was kind of rough, I could not find my blanket and my children all tried to kill me',
        TOPPING_MAP, 3
    )
    return {'toppings': toppings}