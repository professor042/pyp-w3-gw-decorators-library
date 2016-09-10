from decorators import *

@count_calls 
def my_func():
    pass

my_func()
my_func()
my_func()

print(my_func.counter())

count_calls.reset_counters()

print(my_func.counter())
