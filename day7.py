#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import itertools
import functools
import string

import utils

import day5

raw_inp = utils.get_daily_input(f"{__file__.strip('.py')}_input.txt")
clean_inp = [int(_) for _ in raw_inp[0].split(",")]


# part 1
"""
phase setting (an integer from 0 to 4)
Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of phase settings on the amplifiers.

each is used once
"""



def amplifier_combinations(inp):

    amplifiers = {_:
                      {"amp": functools.partial(day5.process_int_code_pt2,
                                                inp=inp,
                                                amp_key=string.ascii_lowercase[_],
                                                ),
                       "opcode_queue": [],
                       "outputs": []}
                  for _ in range(5)}

    all_phase_settings = range(0, 5)
    current_max_permutation = None
    current_max_output = 0

    for each_permutation in itertools.permutations(all_phase_settings):
        amp_out = 0
        for amp_key, amp_val in amplifiers.items():
            # halt flag not handled this loop, assumes >1 loop
            if amp_key == 0:
                amp_out, halt_flag = next(amplifiers[amp_key]["amp"](op3_input=[each_permutation[amp_key], 0]))
            else:
                amp_out, halt_flag = next(amplifiers[amp_key]["amp"](op3_input=[each_permutation[amp_key], amp_out]))

            if amp_out > current_max_output:
                current_max_output = amp_out
                current_max_permutation = each_permutation

    return current_max_output, current_max_permutation

# test cases
tc1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
tc2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
       101,5,23,23,1,24,23,23,4,23,99,0,0]
tc3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
       1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

# part 2


# LESSON LEARNED - trying to be too clever for own good.
# - functools.partial "ruins" the decorator retaining internal state and instead the pointer is reset to 0 after every call

# - generator "send()" needs some syntactic sugar to "catch" the sent value
# If value provided by send method, update the op3_input
# taken from https://docs.python.org/3/howto/functional.html#passing-values-into-a-generator
# yield p1, False
# val = (yield p1, False)
# if val is not None:
#     op3_input = [val[0], ]

# - just use a class: need to record stateful execution, so much easier.... :/

# - more succinct 1-liner modulo increment
# amp_idx = (amp_idx + 1) % 5

# - bug that inp being shared between the amplifiers because passing the list object to run function!
# despite passing inp as a class instantiation arg, was using inp as function argument

class Amplifier:
    # incrementally feed arguments, remembering state of pointer execution and the input
    def __init__(self, inp, amp_key):
        self.pointer = 0
        self.inp = inp.copy()
        self.halted = False

        self.intcode_interpreter = functools.partial(day5.process_int_code_pt2,
                                                     inp=self.inp,
                                                     amp_key=amp_key,
                                                     )

    # set_phase method
    def set_phase(self, op3_input):
        out, self.inp, self.pointer, self.halted = self.intcode_interpreter(op3_input=op3_input)
        return out

    # run method to accept new op3_input
    def run(self, op3_input):
        # handle halted state
        out, self.inp, self.pointer, self.halted = self.intcode_interpreter(inp=self.inp,
                                                                            op3_input=op3_input,
                                                                            pointer=self.pointer)
        return out



def part2_amplifier_combinations(inp):

    all_phase_settings = range(5, 10)
    current_max_output = 0
    current_max_permutation = ()

    for each_permutation in itertools.permutations(all_phase_settings):

        print(f"new permutation: {each_permutation}")

        # create a list of generator amplifier int_code functions
        amplifiers = [Amplifier(inp=inp,
                                amp_key=string.ascii_lowercase[_])
                      for _ in range(5)]

        # FIRST the amplifiers get their own opcode, and then they take inputs from previous
        # first loop - run the amplifiers once to "set" the phase setting
        # To start the process, a 0 signal is sent to amplifier A's input exactly once
        amp_out = 0
        for idx, amp in enumerate(amplifiers):
            # halt flag not handled this loop, assumes >1 loop as below
            amp_out = amp.set_phase([each_permutation[idx], amp_out])

        amp_idx = 0
        cumulative_amp_idx = 0
        halt_flag = False
        outputs = []

        # feedback loops
        while not halt_flag:
            amp_out = amplifiers[amp_idx].run([amp_out, ])
            halt_flag = amplifiers[amp_idx].halted
            # [amplifiers[_].halted for _ in range(5)]
            # [amplifiers[_].pointer for _ in range(5)]

            if isinstance(amp_out, int):  # filter out case where halted and return the whole input
                outputs.append(amp_out)
            amp_idx = (amp_idx + 1) % 5  # keeping index in range 0 to 4
            cumulative_amp_idx += 1  # just for interest to see how many loops are performed

        # Eventually, the software on the amplifiers will halt after they have processed the final loop.
        # When this happens, the last output signal from amplifier E is sent to the thrusters.
        if (len(outputs) and (outputs[-1] > current_max_output)):
            current_max_output = outputs[-1]
            current_max_permutation = each_permutation

    return current_max_output, current_max_permutation



pt2_tc1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
           27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

pt2_tc2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
           -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
           53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

if __name__ == "__main__":
    # print(amplifier_combinations(tc1))
    # print(amplifier_combinations(tc2))
    # print(amplifier_combinations(tc3))

    # print(amplifier_combinations(clean_inp))

    print(part2_amplifier_combinations(pt2_tc1))
    print(part2_amplifier_combinations(pt2_tc2))
    print(part2_amplifier_combinations(clean_inp))

