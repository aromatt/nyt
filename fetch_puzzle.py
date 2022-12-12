#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

PUZZLE_BASE_URL = 'https://www.nytimes.com/svc/crosswords/v6/puzzle/mini'

if 'NYT_COOKIE' not in os.environ:
    raise Exception('Set env var NYT_COOKIE to your "NYT-S" cookie.')


def date_generator(start_date: str) -> str:
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    current_date = datetime.datetime.now()
    next_date = start_date
    while next_date <= current_date:
        yield next_date.strftime('%Y-%m-%d')
        next_date += datetime.timedelta(days=1)


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


for date in date_generator(sys.argv[1]):
    puzzle = get_puzzle(date)
    clues = extract_clues(puzzle)
    print(json.dumps({'date': date, 'clues': clues}))
    time.sleep(1)
