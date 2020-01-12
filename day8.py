#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd

from PIL import Image

import utils

raw_inp = utils.get_daily_input(f"{__file__.strip('.py')}_input.txt")
clean_inp = [int(_) for _ in list(raw_inp[0])]


# part 1
"""
find the layer with the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
"""

len("123456789012")

image_dim = (25, 6)  # wide x tall

# layers = stride of 25 * tall
# find that with minimum 0 count
# then calculate number of 1s by number of 2s

def part1(inp, dims):

    def _freq_counter(inp_array, num):
        return len([_ for _ in inp_array if _ == num])

    layer_stride = (dims[0] * dims[1])

    running_lowest_0 = 0
    number_1s_times_2s = 0
    layer_found_tracker = 0

    for idxs in range(0, len(inp), layer_stride):
        layer = inp[idxs:idxs+layer_stride]
        each_0_count = _freq_counter(layer, 0)

        if (idxs == 0) or (each_0_count < running_lowest_0):
            running_lowest_0 = each_0_count
            number_1s_times_2s = _freq_counter(layer, 1) * _freq_counter(layer, 2)
            layer_found_tracker = int(idxs/layer_stride)

    return number_1s_times_2s, layer_found_tracker




# part 2
"""
0 is black, 1 is white, and 2 is transparent.

What message is produced after decoding your image?
"""
# translate? subtract 2 from all, and find first nonzero


def decode_image(inp, dims):

    black_rgb = [0, 0, 0]
    white_rgb = [255, 255, 255]

    def _parse_pixel_stack(stack):
        for pixel in stack:
            if pixel != 2:  # find the first non-transparent pixel
                if pixel == 0:
                    return black_rgb
                elif pixel == 1:
                    return white_rgb

    layer_stride = (dims[0] * dims[1])
    num_layers = len(inp) / layer_stride
    scaling = 150

    # transform to list of lists
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.fromarray
    data = np.zeros((dims[1]*scaling, dims[0]*scaling, 3), dtype=np.uint8)
    # out_track = np.zeros((dims[1], dims[0], 3), dtype=np.uint8)

    # find the first top visible pixel in each position
    for row in range(0, dims[1]):
        for col in range(0, dims[0]):
            slice_range = range(int(row*dims[0]+col), len(inp), layer_stride)
            pixel_stack = [inp[_] for _ in slice_range]
            parsed_pixel = _parse_pixel_stack(pixel_stack)

            row_scaled = row*scaling
            col_scaled = col*scaling

            data[row_scaled:row_scaled+scaling, col_scaled:col_scaled+scaling] = parsed_pixel
            # out_track[row, col] = parsed_pixel
            # out_track.append(parsed_pixel)

    # len(out_track)
    # len(pixel_stack)
    # render as image

    img = Image.fromarray(data)
    img.show()
    return "done!"


tc1 = [int(_) for _ in list("0222112222120000")]
print("part 2 test case 1", decode_image(tc1, (2, 2)))

if __name__ == "__main__":
    # print("pt 1 answer", part1(clean_inp, image_dim))
    print("pt 2 answer", decode_image(clean_inp, image_dim))

