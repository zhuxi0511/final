#coding: utf-8

import sys
import os
import datetime

from model.split_sentence import split
from model.cluster import make_sentences_vectors, make_graph, page_rank
from model.read_xml import read_xml

root_dir = os.path.dirname(os.path.realpath(__file__))

def final(page_value, sentences, tags):
    data = zip(sentences, page_value, tags)
    data.sort(key=lambda x:x[1], reverse=True)
    return '\n'.join(map(lambda s:''.join([t[0] for t in s]), map(lambda x:x[0], data))[:len(sentences)/5])

def word_level_evaluate(sentences, page_value, tags, cut_level=10):
    #cut_level 向上取整
    data = zip(sentences, page_value, tags)
    data.sort(key=lambda x:x[1], reverse=True)

    precient_sum = set()
    recall_sum = set()
    match = set()

    for d in data:
        tag = 100
        if d[2][0]:
            tag = int(d[2][0][:-1])
        if (cut_level >= tag):
            precient_sum = precient_sum.union(d[0])
    
    good_len = int(len(data) * 10/100.0) + 1
    for i in range(good_len):
        d = data[i]
        recall_sum = recall_sum.union(d[0])
        match = match.union(precient_sum.intersection(d[0]))

    precient = len(match) / float(len(precient_sum))
    recall = len(match) / float(len(recall_sum))
    f = 0
    if precient + recall > 0.0001:
        f = 2 * precient * recall /(precient + recall)
    if f < 0.2:
        raise Exception

    """
    print 'precient_sum', len(precient_sum)
    print 'recall_sum', len(recall_sum)
    print 'match', len(match)
    print 'precient recall F', precient, recall, 2 * precient * recall /(precient + recall)
    """
    for d in data:
        print d[1], d[2]
    print 'precient recall F', precient, recall, f 
    return precient, recall, f


def deal_one_page(file_name, cut_level=10):
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
    #print final(page_value, sentences, tags)
    return word_level_evaluate(sentences, page_value, tags, cut_level)

def main(data_number):
    a = []
    precient, recall, f = 0, 0, 0
    os.system('mkdir -p result/%s' % data_number)
    os.chdir('./data/xml/%s' % data_number)
    for dir,filedir,filename in os.walk('.'):
        for file in filename:
            a.append((os.path.join(dir, file)).split("./")[1])
    l = 0
    for p in a:
        print p
        try:
            pp, rr, ff = deal_one_page(p, 20)
        except:
            continue
        l += 1
        precient += pp
        recall += rr
        f += ff
    print 'precient recall F', precient/l, recall/l, f/l 
    os.chdir(root_dir)
    print os.getcwd()
    out = open('./result/%s/%s' % (data_number, sys.argv[1]), 'w')
    out.write('precient recall F\n')
    out.write(str(precient/l) + '\n')
    out.write(str(recall/l) + '\n')
    out.write(str(f/l) + '\n')

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    start = datetime.datetime.now()
    for i in range(1, 6):
        main(i)
    end = datetime.datetime.now()
    print end - start
