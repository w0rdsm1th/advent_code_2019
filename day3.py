#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

- manhattan path

- intersection locations of the 2x wire paths
    *only intersect twice

-

"""

import numpy as np
import pandas as pd
import utils

raw_inp = utils.get_daily_input("day3_input.txt")
day2_inp = [_.split(",") for _ in raw_inp]


"""
- build set of all points covered
- do set intersection   
"""


def trace_path(inp):
    out_path = []
    current_pos = (0, 0)
    for instruction in inp:
        if instruction[0] == "R":
            out_path.extend([(current_pos[0] + _, current_pos[1]) for _ in range(1, int(instruction[1:]) + 1)])

        elif instruction[0] == "L":
            out_path.extend([(current_pos[0] - _, current_pos[1]) for _ in range(1, int(instruction[1:]) + 1)])

        elif instruction[0] == "U":
            out_path.extend([(current_pos[0], current_pos[1] + _) for _ in range(1, int(instruction[1:]) + 1)])

        elif instruction[0] == "D":
            out_path.extend([(current_pos[0], current_pos[1] - _) for _ in range(1, int(instruction[1:]) + 1)])

        current_pos = out_path[-1]
    return out_path


def get_path_intersections(path1, path2):
    # nor does a wire count as crossing with itself
    return set.intersection(set(path1), set(path2))


def get_min_manhatten_intersection(*intersections):
    return min([sum([abs(_) for _ in intersection]) for intersection in intersections])

#####################################################################################
# part 1
#####################################################################################
if __name__ == '__main__':

    # demo cases
    d1 = "R8,U5,L5,D3"
    d2 = "U7,R6,D4,L4"

    d = [d1.split(","), d2.split(",")]

    # wire_paths = [trace_path(_) for _ in d]
    # intersections = get_path_intersections(*wire_paths)

    # test case 1
    "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    "U62,R66,U55,R34,D71,R55,D58,R83"

    # test case 2
    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"


    wire_paths = [trace_path(_) for _ in day2_inp]
    intersections = get_path_intersections(*wire_paths)
    print(get_min_manhatten_intersection(*intersections))


#####################################################################################
# part 2
#####################################################################################
"""
- get the intersections
- get the number of combined steps 
"""

def get_intersection_steps(intersections, path1, path2):
    out_steps = []
    for intersection in intersections:
        # + 2 because indexing is 0-based
        out_steps.append(path1.index(intersection) + path2.index(intersection) + 2)

    return min(out_steps)

print(get_intersection_steps(intersections, wire_paths[0], wire_paths[1]))
