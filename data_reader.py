import json

import pandas as pd
from bs4 import BeautifulSoup

from utils import tokenizing

inverted_index = {}


def generate_inverted_index(tokens, doc_id):
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = [doc_id]
        else:
            inverted_index[token].append(doc_id)


if __name__ == '__main__':
    doc_id = 0
    for csv_index in range(6):
        data = pd.read_csv(f'IR-S19-project-data/ir-news-{2 * csv_index}-{2 * csv_index + 2}.csv')
        for content in data['content']:
            text = BeautifulSoup(content).get_text()
            tokens = list(set(tokenizing(text)))
            generate_inverted_index(tokens, doc_id)
            doc_id += 1

    with open('inverted_index.json', 'w') as json_file:
        json.dump(inverted_index, json_file, ensure_ascii=False)
