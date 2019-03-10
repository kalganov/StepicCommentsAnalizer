# -*- coding: utf-8 -*-
import pickle
import re

from nltk.stem.snowball import RussianStemmer

comment_model = open('comment_model.pickle', 'rb')
tweeter_model = open('tweet_model.pickle', 'rb')
tokenizer_model = open('tokenizer_comment.pickle', 'rb')
stem_cache_model = open('stem_cache_comment.pickle', 'rb')
stem_count_model = open('stem_count_comment.pickle', 'rb')

comment_classifier = pickle.load(comment_model)
tweeter_classifier = pickle.load(tweeter_model)
stem_cache = pickle.load(stem_cache_model)
stem_count = pickle.load(stem_count_model)
tokenizer = pickle.load(tokenizer_model)
stemer = RussianStemmer()
regex = re.compile('[^а-яА-Я ]')

comment_model.close()
tokenizer_model.close()
stem_cache_model.close()
stem_count_model.close()


def get_stem(token):
    stem = stem_cache.get(token, None)
    if stem:
        return stem
    token = regex.sub('', token).lower()
    stem = stemer.stem(token)
    stem_cache[token] = stem
    return stem


def comment_to_feachure(tweet, show_unknowns=False):
    vector = []
    for token in tokenizer.tokenize(tweet):
        stem = get_stem(token)
        if stem:
            vector.append(stem)
        elif show_unknowns:
            print("Unknown token: {}".format(token))
    res = dict([('contains-word(%s)' % w, True) for w in vector])
    print(res)
    return res


def classify(s):
    return "Tweeter analyze:" + tweeter_classifier.classify(comment_to_feachure(s)) + '\n' + \
           "Stepic analyze:" + comment_classifier.classify(comment_to_feachure(s))
