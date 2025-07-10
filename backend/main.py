tiles = []
colors = [0, 30, 60, 80, 120, 130, 150, 160, 180, 210, 240, 255]
for i in range(len(colors)):
    color = colors[i]
    while color < 255:
        tiles.append([colors[i], color])
        color += 10

n = 1
for tile in tiles:
    print(f"{n}: [{[tile[0]] * 3},{[tile[1]] * 3},{[tile[1]] * 3},{[tile[0]] * 3}],")
    n += 1
for tile in tiles:
    print(f"{n}: [{[tile[0]] * 3},{[(tile[0]+tile[1])//2] * 3},{[tile[1]] * 3},{[(tile[0]+tile[1])//2] * 3}],")
    n += 1
