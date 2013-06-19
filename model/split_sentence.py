#coding:utf-8

import sys
import datetime
from mmseg import seg_txt
from consts import *


def split_line(text):
    tokenizer_list = [seg_txt, ]
    tokenizer = tokenizer_list[0]

    text = list(tokenizer(text))
    sentences = list()

    sentence_startnum = 0
    for i, term in enumerate(text):
        term = term.decode('utf-8')
        text[i] = term
        if len(term) == 1 and term[0] in cutlist:
            sentence = text[sentence_startnum:i]
            sentence_startnum = i + 1
            sentences.append(sentence)
    if sentence_startnum < len(text) - 1:
        sentences.append(text[sentence_startnum:])

    return sentences

def split(text):
    sentences = list()
    for line in text:
        sentences += split_line(line)

    return sentences

def demo():
    f = open(sys.argv[1])
   
    sentences = split(list(f))
    
    for sentence in sentences:
        for term in sentence:
            print term.encode('utf-8'),
        print 

if __name__ == '__main__':
    start = datetime.datetime.now()
    demo()
    end = datetime.datetime.now()
    print end - start
