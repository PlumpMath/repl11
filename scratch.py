
import gc

census = {}
def count(obj):
    _t = type(obj)
    if _t not in census:
        census[_t] = 0
    census[_t] += 1
map(count, gc.get_objects());

sorted(census.items(), key=lambda kv:kv[1], reverse=True)

census[type(count)]

fns = filter(lambda obj: type(obj)==type(count), gc.get_objects())

[f.func_code.co_filename for f in fns if f.__name__ == 'count']

count.func_code.co_filename


