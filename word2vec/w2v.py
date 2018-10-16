from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews

b = Word2Vec(brown.sents())
mr = Word2Vec(movie_reviews.sents())

print(b.wv.most_similar('money', topn=5))
print(mr.wv.most_similar('money', topn=5))

print(b.wv.most_similar('great', topn=5))
print(mr.wv.most_similar('great', topn=5))

print(b.wv.most_similar('company', topn=5))
print(mr.wv.most_similar('company', topn=5))
