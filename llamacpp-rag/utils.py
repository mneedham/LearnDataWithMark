from itertools import islice


def chunk(arr_range, chunk_size): 
    arr_range = iter(arr_range) 
    return iter(lambda: list(islice(arr_range, chunk_size)), []) 