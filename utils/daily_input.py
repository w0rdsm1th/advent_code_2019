#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import os
import numpy as np
import pandas as pd


def get_daily_input(input_name):
    # if not os.path.isfile()
    with open(input_name, "r") as f:
        return f.readlines()
