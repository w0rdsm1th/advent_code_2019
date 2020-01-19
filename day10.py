#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lessons learned

part 2:
- initially tried to walk  the perimeter of the asteroid belt input shape
however this not "high enough granularity". iterating over it skips points on the interior
COULD use this if perimeter were "far enough out" and had common factors with all the interior points...? would have
to find a LCF perimeter for all interior levels

found it easier to convert to polar coordinates, and use the optimal landing space as the centre :)

"""

import numpy as np
import pandas as pd

import math

import utils

raw_inp = utils.get_daily_input(f"{__file__.strip('.py')}_input.txt")
# raw_inp = utils.get_daily_input(f"{day10_input.txt")
clean_inp = [_.strip() for _ in raw_inp]  # if want to cast or transform the indiv elements

# part 1

# def

"""SUDO
- for each possible asteroid in set
- how many other asteroids can you see from that asteroid?
"""


def _generate_asteroid_coords(inp: list):

    out_list = list()
    # assigning coords to each asteroid
    # (0, 0) is top left point,
    for row_idx, row in enumerate(inp):
        for col_idx, col in enumerate(row):
            if col != ".":
                out_list.append((col_idx, row_idx))

    return out_list


def _make_line_sight(ast1, ast2):
    # find the 2-d vector describing the difference between ast1 and ast2
    coord_diff = (ast1[0] - ast2[0], ast1[1] - ast2[1])

    # vertically aligned, cannot calculate gradient
    if coord_diff[0] == 0:
        if coord_diff[1] < 0:  # ast1 is NORTH of ast2
            line_sight = [(ast1[0], ast1[1] + incr) for incr in range(0, -coord_diff[1])]
        else:  # ast1 is SOUTH of ast2
            line_sight = [(ast1[0], ast1[1] - incr) for incr in range(0, coord_diff[1])]

    else:
        gradient = coord_diff[1] / coord_diff[0]  # rise over the run

        line_sight = [ast1, ]
        for loop_incr in range(1, abs(coord_diff[0])+1):
            if coord_diff[0] < 0:  # ast1 is WEST of ast2, INCREMENT x-coord
                incr_point = (ast1[0] + loop_incr, ast1[1] + loop_incr*gradient)

            else:  # ast1 is EAST of ast2, DECREMENT x-coord
                incr_point = (ast1[0] - loop_incr, ast1[1] - loop_incr*gradient)

            if incr_point[-1] % 1 == 0:  # y-coord is a round number, is a possible number in the grid
                line_sight.append(incr_point)
    return line_sight


def _blocked_line_sight(all_asteroids, ast1, ast2):
    line_sight = _make_line_sight(ast1, ast2)
    # if another asteroid between ast1 and ast2 on line_sight, then return False, else return True
    blocked_check = [_ for _ in line_sight if _ in all_asteroids and _ not in [ast1, ast2]]
    return blocked_check



def find_optimal_asteroid(inp):
    asteroids = _generate_asteroid_coords(inp)

    best_asteroid_count = 0
    best_asteroid_coord = asteroids[0]
    for each_ast in asteroids:
        each_asteroid_count = 0
        for other_ast in asteroids:
            if each_ast == other_ast:
                continue

            if not _blocked_line_sight(asteroids, each_ast, other_ast):
                each_asteroid_count += 1

        if each_asteroid_count > best_asteroid_count:
            best_asteroid_count = each_asteroid_count
            best_asteroid_coord = each_ast

    print(f"Best is {best_asteroid_coord} with {best_asteroid_count} other asteroids detected")
    return best_asteroid_coord, best_asteroid_count


def _plot_num_visible(inp: list):
    # helper debug method to check example 1
    coords = _generate_asteroid_coords(inp)

    for row_idx, row in enumerate(inp):
        for col_idx, col in enumerate(row):
            if col == "#":
                this_ast = (col_idx, row_idx)
                this_ast_count = 0
                for other_ast in coords:
                    if this_ast == other_ast:
                        continue
                    if not _blocked_line_sight(coords, this_ast, other_ast):
                        this_ast_count += 1
                print(this_ast_count, end=" ")
            else:
                print(col, end=" ")
        print("", end="\n")

    return None


def _recenter_cartesian(cartesian, centre_coords):
    # helper to recenter cartesian on new centre, separated out so can use separately
    recentered_x = cartesian[0] - centre_coords[0]
    recentered_y = centre_coords[1] - cartesian[1]
    return (recentered_x, recentered_y)


def _convert_cartesian_to_polar(cartesian, centre_coords):

    x, y = _recenter_cartesian(cartesian, centre_coords)
    if x == y == 0:
        return 0, 0

    # TODO - is it necessary to special case points on same axis?
    if x == 0:
        if y > 0:
            return y, 0
        elif y < 0:
            return abs(y), math.pi

    elif y == 0:
        if x > 0:
            return x, 0.5*math.pi
        elif x < 0:
            return abs(x), 1.5*math.pi

    distance = math.sqrt(x**2 + y**2)
    # quadrant 1
    if x > 0 and y > 0:
        # getting offset from "north"
        radial = 0.5*math.pi - math.atan(y/x)

    # quadrant 2
    elif x > 0 and y < 0:
        radial = 0.5*math.pi + math.atan(abs(y)/x)

    # quadrant 3
    elif x < 0 and y < 0:
        radial = math.pi + math.atan(x/y)

    # quadrant 4
    elif x < 0 and y > 0:
        radial = 1.5*math.pi + math.atan(y/abs(x))

    return distance, radial


def _plot_cartesian_offset(inp: list, new_centre):
    # helper debug method to check example 1
    for row_idx, row in enumerate(inp):
        for col_idx, col in enumerate(row):
            new_coord = _convert_cartesian_to_polar((col_idx, row_idx), new_centre)
            print(new_coord, end=" ")
        print("", end="\n")


def laser_elimination(inp, monitor_station_coord, target_blast):
    # find dimensions of the input
    n_row, n_col = len(inp), len(inp[0])

    # the effective end-point steps of laser is the perimeter of the inp
    asteroids = _generate_asteroid_coords(inp)
    asteroids.remove(monitor_station_coord)

    cartestian_polar_zip = [(_, _convert_cartesian_to_polar(_, monitor_station_coord)) for _ in asteroids]
    unique_radian_offsets = sorted(set([_[1][1] for _ in cartestian_polar_zip]))

    # get the unique sorted radian offsets
    # iterate through, find any asteroids on that offset. blast the one that is closest by distance

    count_blasted = 0
    rotation_count = 0
    while cartestian_polar_zip:
        rotation_count += 1

        for radian in unique_radian_offsets:
            matching_asteroids = [_ for _ in cartestian_polar_zip if _[1][1] == radian]
            to_vaporize = min(matching_asteroids, key=lambda x: x[1][0])

            if count_blasted == target_blast:
                print(f"Number {target_blast} asteroid to be blasted coords are {to_vaporize[0]}")
                return to_vaporize[0]

            cartestian_polar_zip = [_ for _ in cartestian_polar_zip if _ != to_vaporize]
            count_blasted += 1

    print("blasted everything before reaching threshold, returning None")
    return None


ex1 = ['.#..#',
       '.....',
       '#####',
       '....#',
       '...##',
       ]


tc1 = ['......#.#.',  # Best is 5,8 with 33 other asteroids detected
       '#..#.#....',
       '..#######.',
       '.#.#.###..',
       '.#..#.....',
       '..#....#.#',
       '#..#....#.',
       '.##.#..###',
       '##...#..#.',
       '.#....####',
       ]

tc2 = ['#.#...#.#.',  # Best is 1,2 with 35 other asteroids detected
       '.###....#.',
       '.#....#...',
       '##.#.#.#.#',
       '....#.#.#.',
       '.##..###.#',
       '..#...##..',
       '..##....##',
       '......#...',
       '.####.###.',
       ]

tc3 = ['.#..#..###',  # Best is 6,3 with 41 other asteroids detected
       '####.###.#',
       '....###.#.',
       '..###.##.#',
       '##.##.#.#.',
       '....###..#',
       '..#.#..#.#',
       '#..#.#.###',
       '.##...##.#',
       '.....#.#..',
       ]

tc4 = ['.#..##.###...#######',  # Best is 11,13 with 210 other asteroids detected
       '##.############..##.',
       '.#.######.########.#',
       '.###.#######.####.#.',
       '#####.##.#.##.###.##',
       '..#####..#.#########',
       '####################',
       '#.####....###.#.#.##',
       '##.#################',
       '#####.##.###..####..',
       '..######..##.#######',
       '####.##.####...##..#',
       '.#####..#.######.###',
       '##...#.##########...',
       '#.##########.#######',
       '.####.#.###.###.#.##',
       '....##.##.###..#####',
       '.#.#.###########.###',
       '#.#.#.#####.####.###',
       '###.##.####.##.#..##',
       ]

# part 2

tc5 = ['.#....#####...#..',
       '##...##.#####..##',
       '##...#...#.#####.',
       '..#.....X...###..',
       '..#.#.....#....##',
       ]

if __name__ == "__main__":
    # debugging part 1
    # _plot_num_visible(ex1)

    # part 1
    # for key, case in {"ex1": ex1, "tc1": tc1, "tc2": tc2, "tc3": tc3, "tc4": tc4}.items():
    #     print(f"case: {key}")
    #     find_optimal_asteroid(case)
    # part1 = find_optimal_asteroid(clean_inp)

    # debugging cartesian offset
    # _plot_cartesian_offset(ex1, (3,3))
    # print("-"*20)
    # _plot_cartesian_offset(ex1, (1,1))

    # part 2
    # laser_elimination(tc5, (8, 3), len(_generate_asteroid_coords(tc5)))

    print("test case 4: ", laser_elimination(tc4, (11, 13), 199))

    laser_elimination(clean_inp, (26, 36), 199)

