import json

from utils import tokenizing


def posting_lists_intersection(posting_lists):
    if not posting_lists:
        return 'all tokens are probably in stopwords'
    result_set = set(posting_lists[0])
    for posting_list in posting_lists:
        result_set = result_set.intersection(posting_list)
    return sorted(list(result_set))


if __name__ == '__main__':
    with open('inverted_index.json', 'r') as json_file:
        inverted_index = json.load(json_file)

    while True:
        query = input()
        query_tokens = tokenizing(query)

        posting_lists = [
            inverted_index[query_token] if query_token in inverted_index else [] for query_token in query_tokens
        ]
        print(posting_lists_intersection(posting_lists))
