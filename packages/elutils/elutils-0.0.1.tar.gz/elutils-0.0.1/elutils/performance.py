# PERFORMANCE
import functools
from statistics import mean, stdev
import timeit

def compare_functions(func1,func2,*args,**kwargs):
    '''A small module to compare the speed of two functions.
    :param repeat : how many times to repeat the timer
    :param number : how many times to execute each function
    :params args : the args that you pass to the functions
    '''
    assert func1(*args) == func2(*args),"Functions must return the same output to be comparable!"

    if 'repeat' in kwargs:
        repeat = kwargs['repeat']
    else:
        repeat = 100
    if 'number' in kwargs:
        number = kwargs['number']
    else:
        number = 10_000

    timer = timeit.Timer(functools.partial(func1,*args))
    result_func1 = timer.repeat(repeat=repeat, number=number)
    timer = timeit.Timer(functools.partial(func2, *args))
    result_func2 = timer.repeat(repeat=repeat, number=number)

    print(f'"{func1.__name__}": Avg:{mean(result_func1):.5f} Min:{min(result_func1):.5f} Max:{max(result_func1):.5f} Stdev:{stdev(result_func1):.5f}')
    print(f'"{func2.__name__}": Avg:{mean(result_func2):.5f} Min:{min(result_func2):.5f} Max:{max(result_func2):.5f} Stdev:{stdev(result_func2):.5f}')
    print(f'"{func1.__name__}" relative to "{func2.__name__}" Avg: {mean(result_func1)/mean(result_func2):.2%} Min:{min(result_func1)/min(result_func2):.2%} Max: {max(result_func1)/max(result_func2):.2%}')


if __name__ == '__main__':
    def bad_concat(letters:list):
        returnstr = ""
        for letter in letters:
            returnstr += letter
        return returnstr

    def better_concat(letters):
        return "".join(letters)

    from string import ascii_letters
    compare_functions(better_concat,bad_concat,list(ascii_letters))