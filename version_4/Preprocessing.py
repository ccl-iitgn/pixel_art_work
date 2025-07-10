import Tiles
import numpy as np
import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

if not hasattr(np, 'asscalar'):
    np.asscalar = lambda x: x.item()

default_tiles = Tiles.get_tiles()


def convert_img_to_tiles(image_data):
    data = np.copy(image_data)
    rows, cols, n = data.shape
    temp_list = []
    for i in range(rows // 2):
        temprow = []
        for j in range(cols // 2):
            temprow.append(
                [data[i * 2][j * 2], data[i * 2][j * 2 + 1], data[i * 2 + 1][j * 2 + 1], data[i * 2 + 1][j * 2]])
        temp_list.append(temprow)
    return np.array(temp_list)


def convert_tiles_to_pixels(tiles):
    tiles = np.array(tiles)
    tile_rows, tile_cols = tiles.shape
    rows = tile_rows * 2
    cols = tile_cols * 2
    data = [[0] * cols for i in range(rows)]
    for i in range(tile_rows):
        for j in range(tile_cols):
            tile = tiles[i, j]['tile']
            data[i * 2][j * 2] = tile[0]
            data[i * 2][j * 2 + 1] = tile[1]
            data[i * 2 + 1][j * 2 + 1] = tile[2]
            data[i * 2 + 1][j * 2] = tile[3]
    return np.array(data)


def get_two_tiles_diff(default_tile, img_tile):
    # def get_color_difference(c1, c2):
    #     [r1, g1, b1] = c1
    #     [r2, g2, b2] = c2
    #     return math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

    # def get_color_difference(c1, c2):
    #     [r1, g1, b1] = c1
    #     [r2, g2, b2] = c2
    #     color1_rgb = sRGBColor(r1, g1, b1, is_upscaled=True)
    #     color2_rgb = sRGBColor(r2, g2, b2, is_upscaled=True)
    #     color1_lab = convert_color(color1_rgb, LabColor)
    #     color2_lab = convert_color(color2_rgb, LabColor)
    #     difference = delta_e_cie2000(color1_lab, color2_lab)
    #     return difference

    # def get_color_difference(c1, c2):
    #     [r1, g1, b1] = c1
    #     [r2, g2, b2] = c2
    #     dr = (r1 - r2) ** 2
    #     dg = (g1 - g2) ** 2
    #     db = (b1 - b2) ** 2
    #     r_ = 0.5 * (r1 + r2)
    #     if (r_ < 128):
    #         return math.sqrt(2 * dr + 4 * dg + 3 * db)
    #     return math.sqrt(3 * dr + 4 * dg + 2 * db)
    def get_color_difference(c1, c2):
        def rgb_to_lab_fast(r, g, b):
            r, g, b = r / 255.0, g / 255.0, b / 255.0
            l = 0.299 * r + 0.587 * g + 0.114 * b
            a = (r - g) * 0.5
            b = (0.5 * (r + g) - b) * 0.5
            return l * 100, a * 100, b * 100

        l1, a1, b1 = rgb_to_lab_fast(*c1)
        l2, a2, b2 = rgb_to_lab_fast(*c2)

        return math.sqrt((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2)

    def rotate(tile):
        return [tile[1], tile[2], tile[3], tile[0]]

    min_diff = float('inf')
    best_rotation = 0
    temp_tile = default_tile.copy()
    final_tile = default_tile.copy()
    for i in range(4):
        diff_sum = sum(get_color_difference(temp_tile[j], img_tile[j]) for j in range(4))
        avg_diff = diff_sum / 4
        if avg_diff < min_diff:
            min_diff = avg_diff
            best_rotation = i
            final_tile = temp_tile.copy()
        temp_tile = rotate(temp_tile)
    return (best_rotation, min_diff, final_tile)


def compute_diff_placement_tiles(image_tiles):
    diff_placement_tiles = dict()
    for i in range(len(image_tiles)):
        print(f"completed: {(i * 15 * 90) / 300}%")
        for j in range(len(image_tiles[0])):
            for k in range(1, 301):
                (best_rotation, min_diff, final_tile) = get_two_tiles_diff(default_tiles[k], image_tiles[i][j])
                diff_placement_tiles[(k, (i, j))] = {"n": k, "diff": min_diff, "rotations": best_rotation,
                                                     "tile": default_tiles[k]}

    return diff_placement_tiles
