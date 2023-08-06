'''Various misc utils that do not fit elsewhere'''
from collections import Counter
from collections.abc import Iterable
def sum_dicts(dicts:Iterable):
    '''takes a list of dicts as input and returns one dict with all values summed togeher'''

    if len(dicts)==0:
        return {}

    counter_dicts = [Counter(d) for d in dicts]

    result_dict = counter_dicts[0]
    for d in counter_dicts[1:]:
        result_dict += d
    return result_dict

if __name__ == '__main__':

    a = {"apples":4,"beets":12}
    b = {"apple":2,"beets":1,"oranges":2}
    
    print(sum_dicts([a,b]))
