import re

import parsivar

from consts import *

stemmer = parsivar.FindStems()  # # delimiter
lemmatizer = hazm.Lemmatizer()  # & delimiter
tokenizer = hazm.WordTokenizer(
    replace_links=True,
    replace_hashtags=True,
    replace_emails=True,
    replace_IDs=True,
    join_verb_parts=False
)

pair_counting = {}


def stemming(token):
    stemmed_word = stemmer.convert_to_stem(lemmatizer.lemmatize(token)).replace('&', '#')
    if '#' in stemmed_word:
        past, present = stemmed_word.split('#')
        stemmed_word = past if past in token else present
    return stemmed_word


def tokenizing(sentence):
    # # # part 1
    # sentence = remove_numbers(sentence)
    # sentence = remove_english_characters(sentence)
    # sentence = remove_punctuations(sentence)
    #
    # words = sentence.split()
    # tokens = []
    # for word in words:
    #     if word not in stopwords:
    #         tokens.append(word)

    # # part 2
    sentence = remove_half_spaces(sentence)
    sentence = remove_numbers(sentence)
    sentence = remove_english_characters(sentence)
    sentence = remove_punctuations(sentence)
    sentence = remove_emojis(sentence)
    sentence = remove_diacritics(sentence)
    sentence = sentence.replace('  ', ' ')
    sentence = replace_multi_words_token(sentence)

    words = tokenizer.tokenize(sentence)
    tokens = []
    for word in words:
        stemmed_word = stemming(word)
        if word not in stopwords and stemmed_word not in stopwords:
            tokens.append(stemmed_word)

    return tokens


def remove_half_spaces(sentence):
    for half_space in half_spaces:
        sentence = sentence.replace(half_space, ' ')
    return sentence


def remove_numbers(sentence):
    for digit in digit_characters:
        sentence = sentence.replace(digit, '')
    return sentence


def remove_punctuations(sentence):
    for punctuation in punctuations:
        sentence = sentence.replace(punctuation, ' ')
    return sentence


def remove_diacritics(sentence):
    for diacritic in diacritics:
        sentence = sentence.replace(diacritic, '')

    for normalized_character, characters in character_mapping.items():
        for character in characters:
            sentence = sentence.replace(character, normalized_character)

    return sentence


def remove_emojis(sentence):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', sentence)


def remove_english_characters(sentence):
    for english_character in english_characters:
        sentence = sentence.replace(english_character, '')
    return sentence


def replace_multi_words_token(sentence):
    for multi_word_token in multi_words_token:
        sentence.replace(multi_word_token, multi_word_token.replace(' ', '_'))
    return sentence
