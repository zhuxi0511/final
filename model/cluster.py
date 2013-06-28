#coding:utf-8

import sys
import datetime

from math import log
import numpy as np

from consts import *

from nltk.cluster import KMeansClusterer, euclidean_distance
from tfidf import TF_IDF
from util import normalise, get_kth_min
from nltk.cluster import KMeansClusterer, euclidean_distance

def make_sentences_vectors(sentences):
    data = TF_IDF(sentences)
    feature_set = set()

    for text in data.texts:
        vector = list()
        feature_set = feature_set.union(set(text))

    print 'len of feature_set: ', len(feature_set)

    sentences = list()
    for text in data.texts:
        sentence = list()
        for term in text:
            sentence.append((term, data.tf_idf(term, text)))
        if sentence:
            sentences.append(sentence)
    return sentences

def make_graph(sentences):
    graph = []
    for i, current_sentence in enumerate(sentences):
        out_row = []
        current_value_list = map(lambda x:x[1], current_sentence)
        current_useful_term_limit = get_kth_min(current_value_list, p=0.0)
        current_sentence_length = len(current_sentence)
        current_sentence = [term for term in current_sentence 
                if term[1] >= current_useful_term_limit]
        for j, sentence in enumerate(sentences):
            if i == j:
                out_row.append(0)
            else:
                same_term_count = 0
                for current_term in current_sentence:
                    for term in sentence:
                        if current_term[0] == term[0]:
                            same_term_count += 1
                            break
                out_row.append(
                        float(same_term_count) /
                        ( current_sentence_length + len(sentence) )
                )
        out_row = normalise(out_row, method='normal')
        graph.append(out_row)
    graph = np.array(graph)
    count = 0
    while count < len(graph):
        if sum(graph[count]) > 1 - 0.01:
            count += 1
        else:
            """
            choose_list = [True] * len(graph) 
            choose_list[count] = False
            choose_list = np.array(choose_list)
            graph = graph[choose_list]
            graph = graph[:, choose_list]
            sentences = sentences[:count] + sentences[count+1:]
            """
            graph[count] = 1.0/len(graph)
    return sentences, graph.T

def page_rank(graph, page_value, iteration=100, threshold=1e-6):
    graph = np.array(graph)
    page_value = np.array(page_value)
    new_page_value = np.zeros_like(page_value)

    for iter_time in range(iteration):
        print 'the %s iter' % (iter_time + 1), 
        new_page_value = graph.dot(page_value)
        distance = euclidean_distance(new_page_value, page_value)
        print 'distance %s' % distance,
        print 'sum %s' % sum(new_page_value)
        if distance < threshold:
            print 'good convergence'
            break
        page_value = new_page_value
    return page_value



