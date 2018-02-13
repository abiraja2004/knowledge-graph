import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from heapq import nlargest
from collections import defaultdict

#nltk.download("stopwords")
#nltk.download('punkt')

class FrequenySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') +
                              list(string.punctuation) +
                              [u"'s",""])

    def _compute_frequencies(self, word_sent, customStopWords=None):
        freq = defaultdict(int)
        if customStopWords is None:
            stopwords = set(self._stopwords)
        else:
            stopwords = set(customStopWords).union(self._stopwords)
        for sentence in word_sent:
            for word in sentence:
                if word not in stopwords:
                    freq[word] +=1
        m = float(max(freq.values()))
        for word in list(freq): #freq.keys():
            freq[word] = freq[word]/m
            if freq[word] >= self._max_cut or freq[word] <= self._min_cut:
                del freq[word]
        return freq

    def summarize(self, desc, n):
        sentences = sent_tokenize(desc)
        word_sent = [word_tokenize(s.lower()) for s in sentences]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sentence in enumerate(word_sent):
            for word in sentence:
                if word in self._freq:
                    ranking[i] += self._freq[word]

        sentences_index = nlargest(n, ranking, key=ranking.get)
        return [sentences[j] for j in sentences_index], len(sentences)

