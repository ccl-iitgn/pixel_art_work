import numpy as np
import cv2
from default_tiles import Default_tiles
import math


def grid_to_tiles(data):
    rows, cols, n = data.shape
    list = []
    for i in range(rows // 2):
        temprow = []
        for j in range(cols // 2):
            temprow.append(
                [data[i * 2][j * 2], data[i * 2][j * 2 + 1], data[i * 2 + 1][j * 2 + 1], data[i * 2 + 1][j * 2]])
        list.append(temprow)
    return np.array(list)


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


def getDeference(default_tile, img_tile):
    target = np.array([[12, 56, 102], [10, 39, 65], [15, 39, 60], [9, 61, 91]])
    if np.array_equal(img_tile, target) and f"{default_tile}" == f"{Default_tiles[0]}":
        print("hello")

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
    return (best_rotation, min_diff, final_tile)


def get_final_tiles(default_tiles, img_tiles):
    final_tiles = [[None] * img_tiles.shape[1] for i in range(img_tiles.shape[0])]
    global_min_diff = float('inf')
    prev_data = [[[None for k in range(300)] for i in range(img_tiles.shape[1])] for j in range(img_tiles.shape[0])]
    def get_next_tile(x, y):
        dy = y + 1
        if (dy >= img_tiles.shape[1]):
            return [x + 1, 0]
        return [x, dy]

    n = 0

    def get_solution(x, y, diff, tilesGrid, tiles_rem):
        nonlocal global_min_diff, final_tiles, n
        # if (global_min_diff < 1600):
        #     return
        if (x >= img_tiles.shape[0]):
            if (len(tiles_rem) == 0):
                n += 1
                if (diff < global_min_diff):
                    print(diff, n)
                    global_min_diff = diff
                    final_tiles = [row[:] for row in tilesGrid]
            return
        if (y >= img_tiles.shape[1]):
            return
        if (len(tiles_rem) == 0):
            return

        current_img_tile = img_tiles[x][y]
        dx, dy = get_next_tile(x, y)
        movable_tiles = []
        for i in range(len(tiles_rem)):
            if (prev_data[x][y][tiles_rem[i]["n"]-1]):
                (best_rotation, tile_diff, rotated_tile) = prev_data[x][y][tiles_rem[i]["n"]-1]
                if (tile_diff + diff < global_min_diff):
                    movable_tiles.append(
                        {"rotation": best_rotation, "diff": tile_diff, "tile": rotated_tile, "n": tiles_rem[i]["n"],
                         "num": i})
            else:
                (best_rotation, tile_diff, rotated_tile) = getDeference(tiles_rem[i]["tile"], current_img_tile)
                prev_data[x][y][tiles_rem[i]["n"]-1] = (best_rotation, tile_diff, rotated_tile)
                if (tile_diff + diff < global_min_diff):
                    movable_tiles.append(
                        {"rotation": best_rotation, "diff": tile_diff, "tile": rotated_tile, "n": tiles_rem[i]["n"],
                         "num": i})
        movable_tiles.sort(key=lambda x: x["diff"])
        for tile in movable_tiles:
            tilesGrid[x][y] = tile
            temp_rem_tiles = tiles_rem.copy()
            temp_rem_tiles.pop(tile["num"])
            get_solution(dx, dy, diff + tile["diff"], tilesGrid, temp_rem_tiles)
            tilesGrid[x][y] = None

    get_solution(0, 0, 0, final_tiles, default_tiles.copy())
    return final_tiles, global_min_diff


def create_puzzle():
    tileW = 15
    tileH = 20
    org_img = cv2.imread("Main/images/test.png", cv2.COLOR_BGR2RGB)
    if org_img is None:
        print("Error: Could not load image 'test.png'")
        return

    resize_img = cv2.resize(org_img, (tileW * 2, tileH * 2))
    image_tiles = grid_to_tiles(resize_img)

    result = get_final_tiles(Default_tiles, image_tiles)
    final_tiles = np.array(result[0])
    converted_img = tiles_to_grid(final_tiles)
    converted_img_display = np.zeros_like(converted_img, dtype=np.uint8)
    converted_img_display[:] = np.clip(converted_img, 0, 255)
    converted_img_display = cv2.resize(cv2.cvtColor(converted_img_display, cv2.COLOR_RGB2BGR), (tileW * 10, tileH * 10))
    cv2.imshow("Hello Test", converted_img_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


create_puzzle()

# arr = np.array([[1, 2, 3, 4, 5, 6], [6, 7, 8, 9, 10, 11]])
# list = []
# for i in range(arr.shape[0]):
#     list.append(np.array_split(arr[i], 3))
# arr = np.array(list)
# print(np.stack(arr,axis=1))
