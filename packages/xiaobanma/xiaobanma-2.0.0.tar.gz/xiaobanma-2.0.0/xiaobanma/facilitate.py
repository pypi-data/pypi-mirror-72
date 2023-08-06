import time
def time_count(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func, time.time() - start)
        return res
    return wrapper