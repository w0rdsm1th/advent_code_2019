#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# LESSONS LEARNED
1) comprehension what was meant by
"The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a negative address, though.)"
assumed meant memory address, not memory value.

2) missed a comprehension that relative mode params can be read AND written
p1 = self.read(inp, self.pointer, 1)  # Parameters that an instruction writes to will never be in immediate mode.
p1 = self.position_relative_mode_switch(inp, opcode[1], self.read(inp, self.pointer, 1), self.rel_base)

3) missed a comprehension that:
"address a relative mode parameter refers to is itself plus the current relative base"

4) missed a comprehension:
"starts at value 0" doesnt mean that values at a memory address start at 0 and then increment with length
instead refers to all memory address location's initial default values

"""

import numpy as np
import pandas as pd
import functools

import utils


raw_inp = utils.get_daily_input(f"{__file__.strip('.py')}_input.txt")
clean_inp = [int(_) for _ in raw_inp[0].split(",")]  # if want to convert to int

# part 1
class IntcodeComputer:
    def __init__(self, inp, pointer=0, rel_base=0):
        self.inp = {k: v for k, v in enumerate(inp)}
        self.inp_len = len(inp)
        self.pointer = pointer
        self.rel_base = rel_base
        self.halted = False

    # run method to accept new op3_input
    def run(self, op3_input):
        # while not self.halted:
        out = self.process_int_code(inp=self.inp,
                                    op3_input=op3_input,
                                    )
        return out

    def read(self, inp, pointer, pointer_offset=0):

        combined_pointer = pointer + pointer_offset

        # (It is invalid to try to access memory at a negative address, though.)
        if combined_pointer < 0:
            raise ValueError(f"negative pointer address passed to read(), pointer val: {combined_pointer}")

        # Memory beyond the initial program starts with the value 0 and can be read or written like any other memory.
        if combined_pointer not in inp.keys():
            return 0
        else:
            return inp[combined_pointer]

    # TODO - just use the full method? writing params should never be in relative mode anyway
    def position_relative_mode_switch(self, inp, mode, param, offset, rel_base) -> int:
        if mode == 0:  # position mode
            return self.read(inp, param, offset)
        elif mode == 2:  # relative mode
            return self.read(inp, param, offset) + rel_base
        else:
            return None

    def position_immediate_relative_mode_switch(self, inp, mode, param, offset, rel_base) -> int:
        if mode == 0:  # position mode
            return self.read(inp, param, offset)
        elif mode == 1:  # immediate mode
            return param + offset
        elif mode == 2:  # relative mode
            return self.read(inp, param, offset) + rel_base
        else:
            return None

    @staticmethod
    def interpret_opcode_parameter_modes(inp_opcode: int) -> list:

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

    def process_int_code(self, inp: dict, op3_input: list):

        loop_counter = 0
        while True:
            loop_counter += 1

            raw_opcode = self.read(inp, self.pointer)

            if raw_opcode == 99 or self.pointer > self.inp_len:
                print("halted")
                self.pointer += 1
                self.halted = True
                return inp

            opcode = self.interpret_opcode_parameter_modes(raw_opcode)

            p1 = self.read(inp, self.position_immediate_relative_mode_switch(inp, opcode[1], self.pointer, 1, self.rel_base))
            p2 = self.read(inp, self.position_immediate_relative_mode_switch(inp, opcode[2], self.pointer, 2, self.rel_base))
            if opcode[0] in {1, 2}:
                p3 = self.position_relative_mode_switch(inp, opcode[3], self.pointer, 3, self.rel_base)  # never in immediate mode

                # Opcode 1 adds together numbers read from two positions and stores the result in a third position.
                if opcode[0] == 1:
                    inp[p3] = p1 + p2

                # Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
                elif opcode[0] == 2:
                    inp[p3] = p1 * p2

                self.pointer += 4

            elif opcode[0] in {3, 4}:
                # Opcode 3: takes a single integer as input and saves it to the position given by its only parameter.
                # For example, the instruction 3,50 would take an input value and store it at address 50.
                if opcode[0] == 3:
                    p1 = self.position_relative_mode_switch(inp, opcode[1], self.pointer, 1, self.rel_base)  # never in immediate mode
                    inp[p1] = op3_input.pop(0)
                    self.pointer += 2

                # Opcode 4 outputs the value of its only parameter.
                # For example, the instruction 4,50 would output the value at address 50.
                elif opcode[0] == 4:
                    print(f"output instruction: {p1}")
                    self.pointer += 2
                    # return inp[p1]

            elif opcode[0] in {5, 6}:
                # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the
                # value from the second parameter. Otherwise, it does nothing.
                if opcode[0] == 5:
                    if p1:
                        self.pointer = p2
                    else:
                        self.pointer += 3

                # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                # from the second parameter. Otherwise, it does nothing.
                elif opcode[0] == 6:
                    if not p1:
                        self.pointer = p2
                    else:
                        self.pointer += 3

            elif opcode[0] in {7, 8}:
                p3 = self.position_relative_mode_switch(inp, opcode[3], self.pointer, 3, self.rel_base)  # never in immediate mode
                # Opcode 7 is less than: if the first parameter is less than the second parameter,
                # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                if opcode[0] == 7:
                    inp[p3] = 1 if p1 < p2 else 0

                # Opcode 8 is equals: if the first parameter is equal to the second parameter,
                # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                elif opcode[0] == 8:
                    inp[p3] = 1 if p1 == p2 else 0

                self.pointer += 4

            elif opcode[0] == 9:
                # Opcode 9 adjusts the relative base by the value of its only parameter.
                # The relative base increases (or decreases, if the value is negative) by the value of the parameter.
                self.rel_base += p1
                self.pointer += 2

# inp[26]
# self.read(inp, 0, 101)
# self.read(inp, 0, 17)
# p1




# part 2
if __name__ == "__main__":
    # got below test cases from https://www.reddit.com/r/adventofcode/comments/e8aw9j/2019_day_9_part_1_how_to_fix_203_error/fac3294
    for case, test_inp in dict(
            # red_tc1 = [109, -1, 4, 1, 99],  # outputs -1
            # red_tc2 = [109, -1, 104, 1, 99],  # outputs 1
            # red_tc3 = [109, -1, 204, 1, 99],  # outputs 109
            # red_tc4 = [109, 1, 9, 2, 204, -6, 99],  # outputs 204
            # red_tc5 = [109, 1, 109, 9, 204, -6, 99],  # outputs 204
            # red_tc6 = [109, 1, 209, -1, 204, -106, 99],  # outputs 204
            # red_tc7 = [109, 1, 3, 3, 204, 2, 99],  # outputs the input
            # red_tc8 = [109, 1, 203, 2, 204, 2, 99],  # outputs the input
    ).items():
        test_computer = IntcodeComputer(test_inp, )  # no param modes
        print(f"test case {case}", test_computer.run([5, 52]))

    # ex_comp = IntcodeComputer(inp=[109,19,204,-34], rel_base=2000)
    # ex_comp.run([])

    # tc1 takes no input, produces exact copy of itself
    # tc2 should output a 16-digit number
    # tc3 should output the large number in the middle
    # test_computer = IntcodeComputer(tc2, )  # no param modes
    # print(f"test case 2", test_computer.run([]))

    for num, test_case in dict(
            # tc1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
            # tc2 = [1102,34915192,34915192,7,4,7,99,0],
            # tc3 = [104,1125899906842624,99],
    ).items():
        test_computer = IntcodeComputer(test_case, )  # no param modes
        print(f"test case {num}", test_computer.run([]))

    computer = IntcodeComputer(clean_inp, )
    # print("part 1 answer", computer.run([1, ]))  # test mode single param mode of 1
    print("part 2 answer", computer.run([2, ]))  # sensor mode single param mode of 2



"""
    def write(self, inp, pointer, val):
        # UNUSED - can just use dictionary methods
        if isinstance(pointer, int):
            pointer = str(pointer)

        if pointer not in inp.keys():
            inp[pointer] = val
        else:
            inp[pointer] = val

        return inp
"""