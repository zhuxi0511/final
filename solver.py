#coding: utf-8

import sys
import datetime

from model.split_sentence import split
from model.cluster import make_sentences_vectors, make_graph, page_rank
from model.read_xml import read_xml

def final(page_value, sentences):
    data = zip(page_value, sentences)
    data.sort(key=lambda x:x[0], reverse=True)
    return '\n'.join(map(lambda s:''.join([t[0] for t in s]), map(lambda x:x[1], data))[:len(sentences)/5])

def deal_one_page(file_name):
    sentences, tags = read_xml(file_name)

    sentences = make_sentences_vectors(sentences)
    sentences, graph = make_graph(sentences)
    page_value = [1.0/len(sentences)] * len(sentences)
    page_value = page_rank(graph, page_value, 10000)
    """
    page_value = page_rank([[0, 0.5, 0, 0.5], 
        [1.0/3, 0, 0, 1.0/2], [1.0/3, 1.0/2, 0, 0], 
        [1.0/3, 0, 1, 0]], [1.0/4] * 4)
        """
    print final(page_value, sentences)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    start = datetime.datetime.now()
    print deal_one_page('data/xml/abs1.xml')
    end = datetime.datetime.now()
    print end - start
