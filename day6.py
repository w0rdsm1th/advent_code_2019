#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

good:
- realised that breadth first search will always return the shortest path first

"""

import numpy as np
import pandas as pd

from collections import defaultdict

import utils

raw_inp = utils.get_daily_input("day6_input.txt")
clean_inp = [_.strip() for _ in raw_inp]


centre_mass_key = "COM"

# part 1
def recur_orbit(inp):
    # Terminology
    # cen: lhs of input pair
    # orb: rhs of input pair
    cen_orbs = [_.split(")") for _ in inp]
    unique_orbs = set([_[1] for _ in cen_orbs])
    out_dict = defaultdict(int)

    def _rec_helper(orb):
        cen = [_[0] for _ in cen_orbs if _[1] == orb][0]
        # recursive stopping criterion
        if cen == centre_mass_key:
            return 1
        else:
            return 1 + _rec_helper(cen)

    # Question: can an orb only orbit 1 object?

    for each_orb in unique_orbs:
        out_dict[each_orb] = _rec_helper(each_orb)

    return out_dict


# efficiency improvement: find the leaf nodes (those only on RHS)
# only loop over them but then cumulatively increment count for every node on path



# test case
t1 = ['COM)B', 	'B)C', 	'C)D', 	'D)E', 	'E)F', 	'B)G', 	'G)H', 	'D)I', 	'E)J', 	'J)K', 	'K)L',]
# sum(recur_orbit(t1).values())

# print(sum(recur_orbit(clean_inp).values()))

# part 2
you_key = "YOU"
santa_key = "SAN"


def bfs_paths_borrow(graph, start, goal):
    # borrowed from
    # https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for nxt in graph[vertex] - set(path):
            if nxt == goal:
                yield path + [nxt]
            else:
                queue.append((nxt, path + [nxt]))


def bfs_paths_adapted(graph, start, goal):

    cen_orbs = [_.split(")") for _ in graph]

    queue = [(start, [start])]

    while queue:
        (vertex, path) = queue.pop(0)

        # needs to return a set of possible moves from this node
        poss_cens = [_[0] for _ in cen_orbs if vertex in _[1]]
        poss_orbs = [_[1] for _ in cen_orbs if vertex in _[0]]
        poss_transfers = set(poss_cens).union(set(poss_orbs))

        for nxt in poss_transfers - set(path):
            if nxt == goal:
                yield path + [nxt]
            else:
                queue.append((nxt, path + [nxt]))


def find_shortest_path(inp):

    cen_orbs = [_.split(")") for _ in inp]
    start = [_ for _ in cen_orbs if _[1] == you_key]
    finish = [_ for _ in cen_orbs if _[1] == santa_key]  # only need to move to same cen as Santa, not orbit Santa

    def _breadth_first(orb):
        """
        K -> L  # leaf node, dead search

        K -> J
        K -> J -> E
        K -> J -> E -> F  # leaf node, dead search

        K -> J -> E -> D
        K -> J -> E -> D -> C
        K -> J -> E -> D -> C -> B  # moving away from SAN

        K -> J -> E -> D -> I -> SAN!!

        """
        poss_transfers = [_ for _ in cen_orbs if orb in _]

        # identify leaf nodes -> stop searching
        # if not poss_transfers:

        # identify santa
        if santa_key in poss_transfers:
            print(f"found santa!")

        return poss_transfers

    pass

# test cases
# t2 = ['COM)B', 	'B)C', 	'C)D', 	'D)E', 	'E)F', 	'B)G', 	'G)H', 	'D)I', 	'E)J', 	'J)K', 	'K)L', 	'K)YOU', 	'I)SAN',]


if __name__ == "__main__":
    t2 = ['COM)B', 	'B)C', 	'C)D', 	'D)E', 	'E)F', 	'B)G', 	'G)H', 	'D)I', 	'E)J', 	'J)K', 	'K)L', 	'K)YOU', 	'I)SAN',]
    gen = bfs_paths_adapted(t2, you_key, santa_key)
    sol = next(gen)
    print("test case", len(sol) - 3)

    gen = bfs_paths_adapted(clean_inp, you_key, santa_key)
    sol = next(gen)
    print("actual", len(sol) - 3)  # -3 bc dont include steps for YOU and SAN


