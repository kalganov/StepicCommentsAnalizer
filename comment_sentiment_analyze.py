import re
import pickle
from nltk.stem.snowball import RussianStemmer

tweet_model = open('models/tweet_model.pickle', 'rb')
comment_model = open('models/comment_model.pickle', 'rb')
tokenizer_model = open('models/tokenizer_comment.pickle', 'rb')
stem_cache_model = open('models/stem_cache_comment.pickle', 'rb')
stem_count_model = open('models/stem_count_comment.pickle', 'rb')

tweet_classifier = pickle.load(tweet_model)
comment_classifier = pickle.load(comment_model)
stem_cache = pickle.load(stem_cache_model)
stem_count = pickle.load(stem_count_model)
tokenizer = pickle.load(tokenizer_model)
stemer = RussianStemmer()
regex = re.compile('[^а-яА-Я ]')

tweet_model.close()
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
    return dict([('contains-word(%s)' % w, True) for w in vector])


while True:
    s = input()
    print('comments_classifier: {}'.format(comment_classifier.classify(comment_to_feachure(s))))
    print('tweet_classifier: {}'.format(tweet_classifier.classify(comment_to_feachure(s))))
