from functools import reduce
from typing import List, Sized


def balance(a_list: List[List], max_length=10) -> List[List]:
    too_long_found = True
    while too_long_found:
        too_long_found = False
        for i, l in enumerate(a_list):
            if len(l) > max_length:
                too_long_found = True
                # Replace with split list
                a_list[i:i + 1] = split_list(l)
    return a_list


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


def batches(l: Sized, n: int):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]
