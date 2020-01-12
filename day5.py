#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

lessons learned
    - missed comprehension when to adjust pointer for opcodes 5 and 6

"""

import numpy as np
import pandas as pd

import utils


raw_inp = utils.get_daily_input("day5_input.txt")
day5_inp = [int(_) for _ in raw_inp[0].split(",")]


def interpret_opcode_parameter_modes(inp_opcode):

    opcode = inp_opcode % 100
    inp_opcode //= 100
    out_instr = [opcode, ]

    # remove instructions from Right to Left
    while inp_opcode > 0:
        out_instr.append(inp_opcode % 10)
        inp_opcode //= 10

    # zero pad if inp_opcode doesnt have leading 0s
    while len(out_instr) < 4:
        out_instr.append(0)

    return out_instr


def position_immediate_mode_switch(inp, mode, param):
    if mode == 0:
        return inp[param]
    elif mode == 1:
        return param
    else:
        return None


# part 1
def process_int_code_pt1(inp, op3_input=None):

    pointer = 0

    while True:
        if inp[pointer] == 99:
            print("halted")
            return inp

        raw_opcode = inp[pointer]
        opcode = interpret_opcode_parameter_modes(raw_opcode)

        if opcode[0] in {1, 2}:
            p1 = position_immediate_mode_switch(inp, opcode[1], inp[pointer+1])
            p2 = position_immediate_mode_switch(inp, opcode[2], inp[pointer+2])
            p3 = inp[pointer+3]  # Parameters that an instruction writes to will never be in immediate mode.

            # Opcode 1 adds together numbers read from two positions and stores the result in a third position.
            if opcode[0] == 1:
                inp[p3] = p1 + p2

            # Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
            elif opcode[0] == 2:
                inp[p3] = p1 * p2

            pointer += 4

        elif opcode[0] in {3, 4}:
            p1 = inp[pointer+1]  # Parameters that an instruction writes to will never be in immediate mode.

            # Opcode 3: takes a single integer as input and saves it to the position given by its only parameter.
            # For example, the instruction 3,50 would take an input value and store it at address 50.
            if opcode[0] == 3:
                inp[p1] = op3_input

            # Opcode 4 outputs the value of its only parameter.
            # For example, the instruction 4,50 would output the value at address 50.
            elif opcode[0] == 4:
                print(f"output instruction: {inp[p1]}")
            pointer += 2





# test cases
# interpret_opcode_parameter_modes(1002)
# print(process_int_code([3, 0, 4, 0, 99], op3_input=1))  # should output whatever it gets as input and then halt
# print(process_int_code([1002, 4, 3, 4, 33]))
# print(process_int_code([1101, 100, -1, 4, 0]))

# part 2

def process_int_code_pt2(inp: list, op3_input:int, pointer=0, amp_key=""):

    while True:
        if inp[pointer] == 99:
            print("halted")
            return None, inp, pointer+1, True

        raw_opcode = inp[pointer]
        opcode = interpret_opcode_parameter_modes(raw_opcode)

        if opcode[0] in {1, 2}:
            p1 = position_immediate_mode_switch(inp, opcode[1], inp[pointer+1])
            p2 = position_immediate_mode_switch(inp, opcode[2], inp[pointer+2])
            p3 = inp[pointer+3]  # Parameters that an instruction writes to will never be in immediate mode.

            # Opcode 1 adds together numbers read from two positions and stores the result in a third position.
            if opcode[0] == 1:
                inp[p3] = p1 + p2

            # Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
            elif opcode[0] == 2:
                inp[p3] = p1 * p2

            pointer += 4

        elif opcode[0] in {3, 4}:
            # Opcode 3: takes a single integer as input and saves it to the position given by its only parameter.
            # For example, the instruction 3,50 would take an input value and store it at address 50.
            if opcode[0] == 3:
                p1 = inp[pointer+1]  # Parameters that an instruction writes to will never be in immediate mode.
                inp[p1] = op3_input.pop(0)

            # Opcode 4 outputs the value of its only parameter.
            # For example, the instruction 4,50 would output the value at address 50.
            elif opcode[0] == 4:
                p1 = position_immediate_mode_switch(inp, opcode[1], inp[pointer+1])
                print(f"output instruction: {p1}, amplifier: {amp_key}")
                return p1, inp, pointer+2, False

            pointer += 2

        elif opcode[0] in {5, 6}:
            p1 = position_immediate_mode_switch(inp, opcode[1], inp[pointer+1])
            p2 = position_immediate_mode_switch(inp, opcode[2], inp[pointer+2])

            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the
            # value from the second parameter. Otherwise, it does nothing.
            if opcode[0] == 5:
                if p1:
                    pointer = p2
                else:
                    pointer += 3

            # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
            # from the second parameter. Otherwise, it does nothing.
            elif opcode[0] == 6:
                if not p1:
                    pointer = p2
                else:
                    pointer += 3

        elif opcode[0] in {7, 8}:
            p1 = position_immediate_mode_switch(inp, opcode[1], inp[pointer+1])
            p2 = position_immediate_mode_switch(inp, opcode[2], inp[pointer+2])
            p3 = inp[pointer+3]  # Parameters that an instruction writes to will never be in immediate mode.

            # Opcode 7 is less than: if the first parameter is less than the second parameter,
            # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
            if opcode[0] == 7:
                inp[p3] = 1 if p1 < p2 else 0

            # Opcode 8 is equals: if the first parameter is equal to the second parameter,
            # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
            elif opcode[0] == 8:
                inp[p3] = 1 if p1 == p2 else 0

            pointer += 4





# test cases
# each_inp = 5
# for each_inp in [5, 8, 9]:
#     print(f"each_inp: {each_inp}")
#     print(process_int_code_pt2([3,9,8,9,10,9,4,9,99,-1,8], op3_input=each_inp))
#     print(process_int_code_pt2([3,9,7,9,10,9,4,9,99,-1,8],  op3_input=each_inp))
#     print(process_int_code_pt2([3,3,1108,-1,8,3,4,3,99], op3_input=each_inp))
#     print(process_int_code_pt2([3,3,1107,-1,8,3,4,3,99], op3_input=each_inp))
#     print("-0"*20, "\n")
#
#
# # jump tests
# for each_inp in [0, 1, 8, 69]:
#     print(f"each_inp: {each_inp}")
#     print(process_int_code_pt2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], op3_input=each_inp))  # position mode
#     print(process_int_code_pt2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], op3_input=each_inp))  # immediate mode
#
#     # larger example
#     print(process_int_code_pt2([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], op3_input=each_inp))
#     # The above example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
#     print("-0"*20, "\n")



if __name__ == "__main__":
    # process_int_code_pt1(day5_inp, 1)
    process_int_code_pt2(day5_inp, 5)
