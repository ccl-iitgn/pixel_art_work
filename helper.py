def permutations(arr, l):
    tiles = []

    def generate(tile):
        if (len(tile) == l):
            tiles.append(tile.copy())
            return
        for i in range(len(arr)):
            tile.append(arr[i])
            generate(tile)
            tile.pop()

    generate([])
    return tiles


def getDefaultTiles(colors):
    tiles = []
    tilesSet = set()

    def rotate_arr(arr):
        return [arr[1], arr[2], arr[3], arr[0]]

    def canplace(arr):
        tempArr = arr.copy()
        for i in range(len(arr)):
            key = f"{tempArr}"
            if key in tilesSet:
                return False
            tempArr = rotate_arr(tempArr)
        return True

    for i in range(len(colors)):
        perms = []
        for j in range(i + 1, len(colors)):
            tempperms = permutations([colors[i], colors[j]], 4)
            perms = perms + tempperms
        for tile in perms:
            if canplace(tile):
                tiles.append(tile.copy())
                tilesSet.add(f"{tile}")

    return tiles


# colors = [
#     [0, 0, 0],  # Black
#     [50, 50, 50],  # Very dark gray
#     [90, 90, 90],  # Dark gray
#     [130, 130, 130],  # Medium gray
#     [170, 170, 170],  # Light gray
#     [210, 210, 210],  # Very light gray
#     [255, 255, 255]  # White
# ]

colors = [
    [0, 0, 0],  # Black
    [90, 90, 90],  # Dark gray
    [130, 130, 130],  # Medium gray
    [170, 170, 170],  # Light gray
    [210, 210, 210],  # Very light gray
    [255, 255, 255]  # White
]

tiles = getDefaultTiles(colors)
i = 1
l = len(tiles)
for j in range(5):
    for k in range(l):
        if (k % 11 == 0):
            continue
        tile = tiles[k]
        print(f"{i}:{tiles[k]},")
        i += 1


def get_generated_tiles():
    return tiles
