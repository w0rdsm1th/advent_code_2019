#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd

import utils

# part 1
"""
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
"""

# search space: 353096-843212

def filter_inp(inp):
    found_repeated = False
    prev_rightmost = inp % 10

    while inp:
        inp = inp // 10
        next_rightmost = inp % 10

        if next_rightmost == prev_rightmost:
            found_repeated = True

        if next_rightmost > prev_rightmost:
            return False

        prev_rightmost = next_rightmost

    return found_repeated

# pt1 test cases
filter_inp(111111) == True
filter_inp(223450) == False
filter_inp(123789) == False


# part 2

def filter_inp_pt2(inp):
    found_double = False
    prev_rightmost = inp % 10
    exponent = 1
    iter_inp = inp

    while iter_inp:
        iter_inp = inp // (10**exponent)
        next_rightmost = iter_inp % 10

        if next_rightmost == prev_rightmost and \
                (prev_rightmost != (inp // (10 ** (exponent - 2))) % 10 or exponent == 1) and \
                (next_rightmost != (inp // (10 ** (exponent + 1))) % 10):  #  or exponent ==
            found_double = True

        if next_rightmost > prev_rightmost:
            return False

        prev_rightmost = next_rightmost
        exponent += 1

    return found_double


if __name__ == "__main__":
    # Lesson learned: own test case - identified that pt2 fails when the repeated double is at start of the number
    filter_inp_pt2(223456) == True

    # pt1 test cases
    # filter_inp_pt2(111111) == False
    # filter_inp_pt2(223450) == False
    # filter_inp_pt2(123789) == False


    # filter_inp_pt2(112233)
    # filter_inp_pt2(123444)
    # filter_inp_pt2(111122)

    print(sum([filter_inp_pt2(_) for _ in range(353096, 843212)]))
    print(sum([filter_inp(_) for _ in range(353096, 843212)]))
