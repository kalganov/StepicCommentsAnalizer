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


def standardize_text(df, text_field):
    df[text_field] = re.sub(r'@[a-zA-Zа-яА-Я]*[_[a-zA-Zа-яА-Я]*]*', '', df[text_field])
    df[text_field] = re.sub(r'[^а-яА-Я ]', '', df[text_field])
    df[text_field] = re.sub(r'http\S+', '', df[text_field])
    df[text_field] = re.sub(r'http', '', df[text_field])
    df[text_field] = re.sub(r'@\S+', '', df[text_field])
    df[text_field] = re.sub(r'(<(/?[^>]+)>)', '', df[text_field])
    df[text_field] = re.sub(r'[-.?!)(,:]', '', df[text_field])
    df[text_field] = df[text_field].lower()
    df[text_field] = df[text_field].strip()
    return df


def get_stem(token):
    stem = stem_cache.get(token, None)
    if stem:
        return stem
    token = regex.sub('', token).lower()
    stem = stemer.stem(token)
    stem_cache[token] = stem
    return stem


def comment_to_feachure(tweet, show_unknowns=False):
    text = standardize_text(tweet, 'text')['text']

    vector = []
    for token in tokenizer.tokenize(text):
        stem = get_stem(token)
        if stem:
            vector.append(stem)
        elif show_unknowns:
            print("Unknown token: {}".format(token))
    res = dict([('contains-word(%s)' % w, True) for w in vector])
    return res


def classify(s):
    return ((tweeter_classifier.prob_classify(comment_to_feachure(s)).prob('pos'),
             tweeter_classifier.prob_classify(comment_to_feachure(s)).prob('neg')),
            (comment_classifier.prob_classify(comment_to_feachure(s)).prob('pos'),
             comment_classifier.prob_classify(comment_to_feachure(s)).prob('neg')))
