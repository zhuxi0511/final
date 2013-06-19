# -*- coding: utf-8 -*-

import nltk
from math import log

class TF_IDF():
    def __init__(self, texts):
        self.texts = texts

        self._texts_num = len(self.texts)
        self._terms_index = self._index_and_cal_terms_num()

        self.terms_set = self._terms_index.keys()
        self._terms_num = len(self.terms_set)
        print 'terms_num ', self._terms_num
        self._terms_match_texts = self._cal_terms_match_texts()

    def _index_and_cal_terms_num(self):
        index = 0
        terms_index = dict()
        for text in self.texts:
            for term in text:
                if terms_index.get(term) is None:
                    terms_index[term] = index
                    index += 1
        return terms_index

    def _cal_terms_match_texts(self):
        terms_match_texts = [0 for i in range(self._terms_num)]

        for text in self.texts:
            has_match_text = [False for i in range(self._terms_num)]
            for term in text:
                term_index = self._terms_index[term]
                if not has_match_text[term_index]:
                    has_match_text[term_index] = True
                    terms_match_texts[term_index] += 1
        
        return [log(self._terms_num/float(term)) for term in terms_match_texts]

    def tf(self, term, text):
        return float(text.count(term)) / len(text)

    def idf(self, term):
        return self._terms_match_texts[self._terms_index[term]]

    def tf_idf(self, term, text):
        return self.tf(term, text) * self.idf(term)

    def get_terms_set(self):
        return self.terms_set


