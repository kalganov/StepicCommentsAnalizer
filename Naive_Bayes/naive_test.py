import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews


def document_features(document):
    return dict([('contains-word(%s)' % w, True) for w in document])


negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(document_features(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(document_features(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats) * 3 / 4
poscutoff = len(posfeats) * 3 / 4

trainfeats = negfeats[:int(negcutoff)] + posfeats[:int(poscutoff)]
testfeats = negfeats[int(negcutoff):] + posfeats[int(poscutoff):]
print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

classifier = NaiveBayesClassifier.train(trainfeats)
print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
classifier.show_most_informative_features()
