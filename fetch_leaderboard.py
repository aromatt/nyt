#!/usr/bin/env python3

import os
import json
import argparse

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
        name = div.find("p", class_='lbd-score__name').getText().strip().replace(' (you)', '')
        time = div.find("p", class_='lbd-score__time').getText()
        if time != '--':
            scores[name] = time
    return scores

parser = argparse.ArgumentParser(description='Fetch NYT Crossword Mini Leaderboard')
parser.add_argument('-f', '--format', default='json', help='Output format ("csv" or "json")')
args = parser.parse_args()
data = get_leaderboard()

if args.format == 'json':
    print(json.dumps(data, indent=2))
elif args.format == 'csv':
    print('name,time')
    for name,time in data.items():
        print(f'{name},{time}')
else:
    raise Exception(f'Unknown format {format}')
