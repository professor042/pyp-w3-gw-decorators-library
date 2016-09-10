# implement your decorators here.

import functools
import logging

# def logged(level, name=None, message=None):
#     '''
#     Add logging to function.  Level is logging level and name and message are
#     optional arguments.  They default to function's module and name
    
#     Adapted from:
#     http://chimera.labs.oreilly.com/books/1230000000393/ch09.html#_problem_147
#     '''
#     def decorate(func):
#         logname = name if name else func.__module__
#         log = logging.getLogger(logname)
#         logmsg = message if message else func.__name__
        
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             log.log(level, logmsg)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorate
    
def debug(fn, logger=None):
    lvl = logging.DEBUG
    debug_log = logging.getLogger(logger)
    # Logger.log(lvl, msg, *args, **kwargs)
    def log_wrapper(*args, **kwargs):
        # Message before execution
        pre_msg = "Executing {} with params: {}, {}".format(fn.__name__, 
            *args, **kwargs)
        debug_log.log(lvl, pre_msg)
        
        # Execute and store result
        result = fn(*args, **kwargs)
        
        # Message after execution
        post_msg = "Finished {} execution with result: {}".format(fn.__name__, 
            result)
        debug_log.log(lvl, post_msg)    
        return result
    return log_wrapper


#COUNT_CALLS ----------------------------------------------------------------
class count_calls(object):
    counter_dict = {}
    
    @staticmethod
    def reset_counters():
        count_calls.counter_dict = {}
        # for key in count_calls.counter_dict.keys():
        #     count_calls.counter_dict[key] = 0
        # Reset counters actually needs to clear the entire dictionary to 
        # pass test_count_no_calls rather than just reset the count of each
        # function to zero (clear_functions or something might be better name)
    
    @staticmethod
    def counters():
        return count_calls.counter_dict
    
    def __init__(self, func):
        self.func = func
        count_calls.counter_dict[self.func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        '''Allows class to be called like a function'''
        # print("Got here test 1")
        # if self.func.__name__ in count_calls.counter_dict:
        count_calls.counter_dict[self.func.__name__] += 1
        return self.func(*args, **kwargs)
        
    def counter(self):
        # print("count={}".format(count_calls.counter_dict[self.func.__name__]))
        return count_calls.counter_dict[self.func.__name__]

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
        
    def __get__(self, obj, objtype):
        '''Support instance methods'''
        return functools.partial(self.__call__, obj)
        
        
#MEMOIZED ------------------------------------------------------------------
def memoized(fn):
    '''
    Adapted from:
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    '''
    cache = fn.cache = {}
    
    @functools.wraps(fn)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = fn(*args, **kwargs)
            # print(cache)
        return cache[args]
    return memoizer
    