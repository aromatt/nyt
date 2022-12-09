#!/usr/bin/env python3

import argparse
import json
import os
import sys

import requests
from bs4 import BeautifulSoup

PUZZLE_BASE_URL = 'https://www.nytimes.com/svc/crosswords/v6/puzzle/mini'

if 'NYT_COOKIE' not in os.environ:
    raise Exception('Set env var NYT_COOKIE to your "NYT-S" cookie.')


def get_puzzle(date_str):
    return requests.get(f'{PUZZLE_BASE_URL}/{date_str}.json',
                        cookies={'NYT-S': os.environ['NYT_COOKIE']}).json()


def extract_clues(puzzle):
    cells = {i: c['answer']
             for i,c in enumerate(puzzle['body'][0]['cells'])
             if 'answer' in c}
    out = []
    for clue in puzzle['body'][0]['clues']:
        out.append({
            'text': clue['text'][0]['plain'],
            'answer': ''.join(cells[x] for x in clue['cells'])
        })
    return out


puzzle = get_puzzle(sys.argv[1])
clues = extract_clues(puzzle)
print(json.dumps(clues))
