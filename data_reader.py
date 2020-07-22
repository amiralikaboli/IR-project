import json
import math

import pandas as pd
from bs4 import BeautifulSoup

from utils import tokenizing

inverted_index = {}
term_frequency = {}
doc_frequency = {}
champion_lists = {}


def generate_inverted_index_and_frequencies(tokens, doc_id):
    for token in set(tokens):
        if token not in inverted_index:
            inverted_index[token] = []
        inverted_index[token].append(doc_id)

        if token not in doc_frequency:
            doc_frequency[token] = 0
        doc_frequency[token] += 1

    for token in tokens:
        if token not in term_frequency:
            term_frequency[token] = {}
        if doc_id not in term_frequency[token]:
            term_frequency[token][doc_id] = 0
        term_frequency[token][doc_id] += 1


def vector_normalizing(vec):
    normalizing_factor = math.sqrt(sum([val ** 2 for val in vec.values()]))
    return {key: val / normalizing_factor for key, val in vec.items()}


def calc_tf_idf(term, doc_id):
    return (1 + math.log10(term_frequency[term][doc_id])) * math.log10(len(news_details) / doc_frequency[term])


if __name__ == '__main__':
    news_details = []
    for csv_index in range(6):
        data = pd.read_csv(f'../IR_project/IR-S19-project-data/ir-news-{2 * csv_index}-{2 * csv_index + 2}.csv')
        for ind in range(data.shape[0]):
            news_details.append({
                'title': data['title'][ind],
                'content': BeautifulSoup(data['content'][ind]).get_text()
            })

    champion_list_size = math.floor(math.sqrt(len(news_details)))

    with open('news_details.json', 'w') as json_file:
        json.dump(news_details, json_file, ensure_ascii=False)

    docs_tokens = []
    for doc in news_details:
        docs_tokens.append(tokenizing(doc['content']))

    for doc_id, doc_tokens in enumerate(docs_tokens):
        generate_inverted_index_and_frequencies(doc_tokens, doc_id)

    with open('inverted_index.json', 'w') as json_file:
        json.dump(inverted_index, json_file, ensure_ascii=False)
    with open('term_frequency.json', 'w') as json_file:
        json.dump(term_frequency, json_file, ensure_ascii=False)
    with open('doc_frequency.json', 'w') as json_file:
        json.dump(doc_frequency, json_file, ensure_ascii=False)

    tf_idf = [{} for _ in range(len(docs_tokens))]
    for doc_id, doc_tokens in enumerate(docs_tokens):
        terms = list(set(doc_tokens))
        for term in terms:
            tf_idf[doc_id][term] = calc_tf_idf(term, doc_id)

    with open('tf_idf.json', 'w') as json_file:
        json.dump(tf_idf, json_file, ensure_ascii=False)
    with open('normalized_tf_idf.json', 'w') as json_file:
        json.dump([vector_normalizing(doc_tf_idf) for doc_tf_idf in tf_idf], json_file, ensure_ascii=False)

    for term in inverted_index.keys():
        terms_tf_idf = [(tf_idf[doc_id][term], doc_id) for doc_id in inverted_index[term]]
        champion_lists[term] = [doc_id for _, doc_id in sorted(terms_tf_idf)[::-1][:champion_list_size]]

    with open('champion_lists.json', 'w') as json_file:
        json.dump(champion_lists, json_file, ensure_ascii=False)
