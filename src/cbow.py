# http://www.thushv.com/natural_language_processing/word2vec-part-2-nlp-with-deep-learning-with-tensorflow-cbow/#why-cbow?

import fasttext


# CBOW model
#model = fasttext.cbow('./fastText/data/enwik9', 'model')

model = fasttext.load_model('model.bin')
print(model.words[0:100]) # list of words in dictionary

print(model['king']) # get the vector of the word 'king'
