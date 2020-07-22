import heapq
import json
import math

from utils import tokenizing

result_size = 10


def calc_query_vec(query_tokens):
    term_frequency = {}
    for token in query_tokens:
        if token not in term_frequency:
            term_frequency[token] = 0
        term_frequency[token] += 1

    return {
        term: (1 + math.log10(term_frequency[term])) * math.log10(len(news_details) / doc_frequency[term])
        for term in set(query_tokens)
    }


def vector_normalizing(vec):
    normalizing_factor = math.sqrt(sum([val ** 2 for val in vec.values()]))
    return {key: val / normalizing_factor for key, val in vec.items()}


def similarity(doc_vec, query_vec):
    dot_ans = 0
    for key in query_vec.keys():
        if key in doc_vec:
            dot_ans += doc_vec[key] * query_vec[key]
    return dot_ans


if __name__ == '__main__':
    with open('news_details.json', 'r') as json_file:
        news_details = json.load(json_file)
    with open('inverted_index.json', 'r') as json_file:
        inverted_index = json.load(json_file)
    with open('champion_lists.json', 'r') as json_file:
        champion_lists = json.load(json_file)
    with open('doc_frequency.json', 'r') as json_file:
        doc_frequency = json.load(json_file)
    with open('normalized_tf_idf.json', 'r') as json_file:
        normalized_tf_idf = json.load(json_file)

    while True:
        query = input()
        query_tokens = tokenizing(query)

        normalized_query_vec = vector_normalizing(calc_query_vec(query_tokens))

        candidates = []
        for token in set(query_tokens):
            # candidates.extend(inverted_index[token])
            candidates.extend(champion_lists[token])
        candidates = list(set(candidates))

        candidates_similarity = [
            (similarity(normalized_tf_idf[doc_id], normalized_query_vec), doc_id)
            for doc_id in candidates
        ]
        top_similar_docs = [
            news_details[candidate_similarity[1]]
            for candidate_similarity in heapq.nlargest(result_size, candidates_similarity)
        ]

        for news in top_similar_docs:
            print(f"title: {news['title']}")
            print(f"content: {news['content']}")
            print('#' * 100)
