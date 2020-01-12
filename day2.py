#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import utils

raw_inp = utils.get_daily_input("day2_input.txt")
day2_inp = [int(_) for _ in raw_inp[0].split(",")]

# To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.


def process_int_code(inp, noun=None, verb=None):
    # instructions
    # 1, 2, or 99
    if noun:
        inp[1] = noun
    if verb:
        inp[2] = verb

    # Once you're done processing an opcode, move to the next one by stepping forward 4 positions.
    # for pointer, instruction in enumerate(inp[::4]):  # Lesson learned: pointer only increments by 1
    # for pointer, instruction in zip(range(0, len(inp), 4), (inp[::4]):  # Lesson learned: fixes the pointer values so dont get updated by the instructions
    # while pointer <= len(inp):  # Lesson learned: not working, sometimes processes incorrect idxs
    for pointer in range(0, len(inp), 4):
        opcode = inp[pointer]

        if opcode == 99:
            # The halt instruction would increase the instruction pointer by 1, but it halts the program instead.
            # print(f"halting, returning! noun: {noun} verb: {verb}")
            # print(inp)
            return inp

        # Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        elif opcode == 1:
            inp[inp[pointer+3]] = inp[inp[pointer+1]] + inp[inp[pointer+2]]

        # Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        elif opcode == 2:
            inp[inp[pointer+3]] = inp[inp[pointer+1]] * inp[inp[pointer+2]]
            # inp[instruction[3]] = inp[instruction[1]] * inp[instruction[2]]

        # except IndexError:
            # print(f"index error! noun: {noun} verb: {verb}")
            # return [None]

# if __name__ == '__main__':
#     process_int_code([1,0,0,0,99])
#     process_int_code([2,3,0,3,99])
#     process_int_code([2,4,4,5,99,0])
#     process_int_code([1,1,1,4,99,5,6,0,99])
#     answer = process_int_code(day2_inp[:], noun=12, verb=2)
    # print(answer[0])



##################################################################################
# part 2
##################################################################################
if __name__ == '__main__':
    target = 19690720
    for noun in range(100):
        for verb in range(100):
            iter_out = process_int_code(day2_inp[:], noun, verb)
            if iter_out[0] == target:
                print(f"found! noun: {noun} verb: {verb}")
                print(f"answer {100*noun + verb}")
                break

    print("completed search space, didnt find target")
