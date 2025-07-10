import numpy as np
import cv2
from default_tiles import Default_tiles
import math


def grid_to_tiles(data):
    rows, cols, n = data.shape
    temp_list = []
    for i in range(rows // 2):
        temprow = []
        for j in range(cols // 2):
            temprow.append(
                [data[i * 2][j * 2], data[i * 2][j * 2 + 1], data[i * 2 + 1][j * 2 + 1], data[i * 2 + 1][j * 2]])
        temp_list.append(temprow)
    return np.array(temp_list)


def tiles_to_grid(tiles):
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


def get_deference(default_tile, img_tile):
    def get_color_difference(c1, c2):
        [r1, g1, b1] = c1
        [r2, g2, b2] = c2
        return math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

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
    return best_rotation, min_diff, final_tile


def get_final_tiles(default_tiles, img_tiles):
    final_tiles = [[None] * img_tiles.shape[1] for i in range(img_tiles.shape[0])]
    prev_data = [[[None for k in range(300)] for i in range(img_tiles.shape[1])] for j in range(img_tiles.shape[0])]
    tiles_used_data = [None for i in range(300)]

    def get_next_tile(x, y):
        dy = y + 1
        if (dy >= img_tiles.shape[1]):
            return [x + 1, 0]
        return [x, dy]

    def get_solution(x, y, data_full, tiles_to_place):
        nonlocal final_tiles, prev_data, tiles_used_data
        if x >= img_tiles.shape[0]:
            return
        dx, dy = get_next_tile(x, y)
        if (final_tiles[x][y] is not None):
            get_solution(dx, dy, data_full, tiles_to_place)
            return
        current_img_tile = img_tiles[x][y]

        movable_tiles = []
        for i in range(len(tiles_to_place)):
            if prev_data[x][y][tiles_to_place[i]["n"] - 1]:
                (best_rotation, tile_diff, rotated_tile) = prev_data[x][y][tiles_to_place[i]["n"] - 1]
                movable_tiles.append(
                    {"rotation": best_rotation, "diff": tile_diff, "tile": rotated_tile, "n": tiles_to_place[i]["n"],
                     "num": i})
            else:
                (best_rotation, tile_diff, rotated_tile) = get_deference(tiles_to_place[i]["tile"], current_img_tile)
                prev_data[x][y][tiles_to_place[i]["n"] - 1] = (best_rotation, tile_diff, rotated_tile)
                movable_tiles.append(
                    {"rotation": best_rotation, "diff": tile_diff, "tile": rotated_tile, "n": tiles_to_place[i]["n"],
                     "num": i})
        movable_tiles.sort(key=lambda x: x["diff"])
        for tile in movable_tiles:
            if not tiles_used_data[tile["n"] - 1]:
                tiles_used_data[tile["n"] - 1] = [x, y]
                final_tiles[x][y] = tile
                get_solution(dx, dy, True, tiles_to_place)
                return
            else:
                min_diff = tile["diff"]
                [a, b] = tiles_used_data[tile["n"] - 1]
                if min_diff < final_tiles[a][b]["diff"]:
                    final_tiles[a][b] = None
                    final_tiles[x][y] = tile
                    tiles_used_data[tile["n"] - 1] = [x, y]
                    get_solution(dx, dy, False, tiles_to_place)
                    return
    n=0
    while True:
        temp_tiles = [default_tiles[i] for i in range(len(tiles_used_data)) if tiles_used_data[i] is None]
        if(len(temp_tiles)!=n):
            n=len(temp_tiles)
        if len(temp_tiles) > 0:
            get_solution(0, 0, True, temp_tiles)
        else:
            break
    global_error = 0
    for row in final_tiles:
        for tile in row:
            global_error += tile["diff"]
    print(global_error)
    return final_tiles, 0


def create_puzzle():
    tile_w = 15
    tile_h = 20
    org_img = cv2.imread("Main/images/test.png", cv2.COLOR_BGR2RGB)
    if org_img is None:
        print("Error: Could not load image 'test.png'")
        return

    resize_img = cv2.resize(org_img, (tile_w * 2, tile_h * 2))
    image_tiles = grid_to_tiles(resize_img)
    # i = 1
    # def_tiles = []
    # for row in image_tiles:
    #     for tile in row:
    #         def_tiles.append({"n": i, "tile": tile})
    #         i+=1


    result = get_final_tiles(Default_tiles, image_tiles)
    final_tiles = np.array(result[0])
    converted_img = tiles_to_grid(final_tiles)
    converted_img_display = np.zeros_like(converted_img, dtype=np.uint8)
    converted_img_display[:] = np.clip(converted_img, 0, 255)
    converted_img_display = cv2.resize(converted_img_display,
                                       (tile_w * 10, tile_h * 10))
    cv2.imshow("Hello Test", converted_img_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


create_puzzle()

