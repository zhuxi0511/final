import math

def normalise(vector, method='square'):
    if method=='square':
        square_sum = map(lambda x:x*x, vector)
        square_sum = math.sqrt(sum(square_sum))
    else:
        square_sum = sum(vector)

    if square_sum > 0:
        ret = map(lambda x:x/square_sum, vector)
        return ret
    else:
        return vector

def get_kth_min(data, p=0.2):
    data = sorted(data)
    return data[int(len(data) * p)]

def yu_normalise(sentence):
    square_sum = sum(map(lambda x:x[1], sentence))
    if square_sum > 0:
        return [[s[0],s[1]/square_sum] for s in sentence]
    else:
        return sentence

def yu_length(sentence):
    ret = 0.0
    for term in sentence:
        ret += term[1] * term[1]
    return ret ** 0.5


def yu_function(current_sentence, sentence):
    current_sentence = yu_normalise(current_sentence)
    sentence = yu_normalise(sentence)
    up = 0.0
    down = 0.0
    for current_term in current_sentence:
        for term in sentence:
            if current_term[0] == term[0]:
                up += current_term[1] * term[1]

    down = yu_length(current_sentence) * yu_length(sentence)
    try:
        return up / down
    except:
        return 0


