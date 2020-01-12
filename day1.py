#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import utils

def calc_module_fuel(module):
    """
    Fuel required to launch a given module is based on its mass.
    Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
    :param module:
    :return:
    """
    return int(module / 3) - 2

inp = utils.get_daily_input("day1_input.txt")

print(sum([calc_module_fuel(int(_.strip())) for _ in inp]))

calc_module_fuel(83133)
calc_module_fuel(1969)
calc_module_fuel(100756)

##################################################################################
# part 2
##################################################################################

def calc_module_fuel_incl_fuel_weight(module):
    """
    However, that fuel also requires fuel, and that fuel requires fuel, and so on.
    Any mass that would require negative fuel should instead be treated as if it requires zero fuel;
    :param module:
    :return:
    """

    total_fuel_weight = calc_module_fuel(module)

    recursive_fuel = total_fuel_weight
    while True:
        recursive_fuel = calc_module_fuel(recursive_fuel)
        if recursive_fuel <= 0:
            break
        total_fuel_weight += recursive_fuel

    return total_fuel_weight


print(sum([calc_module_fuel_incl_fuel_weight(int(_.strip())) for _ in inp]))
