#coding: utf-8

import sys
import os
import datetime

from lxml import etree

def read_xml(file_name):
    sentences = []
    tags = []
    tree = etree.parse(file_name)

    paras_tree = tree.xpath('//para')
    for sentences_tree in paras_tree:
        for sentence_tree in sentences_tree:
            tag = sentence_tree.xpath('@tag')
            sentence = sentence_tree.xpath('word/@cont')
            sentences.append(sentence)
            tags.append(tag)
    return sentences, tags

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    read_xml('%s/data/abs1.xml' % root_dir)

