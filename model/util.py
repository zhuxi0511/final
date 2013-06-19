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
