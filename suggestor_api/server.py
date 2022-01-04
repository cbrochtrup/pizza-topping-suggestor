"""
This basic example loads a pre-trained model from the web and uses it to
generate sentence embeddings for a given list of sentences.
"""

import logging
import random
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException

from sentiment_suggestion import build_sentiment_to_toppings_map, suggest_toppings
from predict import predict_toppings, node2id


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
async def generate_toppings(feelings: Optional[str] = Query("the the the the")):
    """
    Example request from python

    r = requests.get(
        'http://127.0.0.1:8000/top?' + urllib.parse.quote('I can not believe you would do this to me on the day of my wedding.')
    )

    javascript URI encoding
        const uri = 'https://mozilla.org/?x=шеллы';
        const encoded = encodeURI(uri);
        console.log(encoded);
    """
    toppings = suggest_toppings(feelings, TOPPING_MAP, 3)
    return {'toppings': toppings}

@api.get('/suggest')
async def recommend_toppings(topping: List[str] = Query(["mozzarella"])):
    for top in topping:
        if top not in node2id:
            HTTPException(status_code=422, detail="Invalid topping passed")
    suggested_toppings = predict_toppings(topping, 10)
    LOGGER.info(suggested_toppings)
    suggested_toppings = random.sample(suggested_toppings, 3)
    return {'toppings': suggested_toppings}
