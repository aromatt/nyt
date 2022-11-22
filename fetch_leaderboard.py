#!/usr/bin/env python3

import os
import json

import requests
from bs4 import BeautifulSoup

LEADERBOARD_URL = 'https://www.nytimes.com/puzzles/leaderboards'

if 'NYT_COOKIE' not in os.environ:
    raise Exception('Set env var NYT_COOKIE to your "NYT-S" cookie.')

def get_leaderboard():
    html = requests.get(LEADERBOARD_URL,
                        cookies={'NYT-S': os.environ['NYT_COOKIE']}).text
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", class_='lbd-score')
    scores = {}
    for div in divs:
        name = div.find("p", class_='lbd-score__name').getText()
        time = div.find("p", class_='lbd-score__time').getText()
        if time != '--':
            scores[name] = time
    return scores

print(json.dumps(get_leaderboard(), indent=2))
