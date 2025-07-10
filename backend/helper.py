# import os
# from pathlib import Path
#
# from Image_Processing import Image_Processing
# import numpy as np
#
#
# def get_all_files(path, recursive=True):
#     files = []
#     path = Path(path)
#
#     if not path.exists():
#         raise FileNotFoundError(f"Path '{path}' does not exist")
#
#     if not path.is_dir():
#         raise NotADirectoryError(f"Path '{path}' is not a directory")
#
#     if recursive:
#         for file_path in path.rglob('*'):
#             if file_path.is_file():
#                 files.append(str(file_path))
#     else:
#         for item in path.iterdir():
#             if item.is_file():
#                 files.append(str(item))
#
#     return sorted(files)
#
#
# def get_all_files_oswalk(path):
#     files = []
#
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"Path '{path}' does not exist")
#
#     if not os.path.isdir(path):
#         raise NotADirectoryError(f"Path '{path}' is not a directory")
#
#     for root, dirs, filenames in os.walk(path):
#         for filename in filenames:
#             files.append(os.path.join(root, filename))
#
#     return sorted(files)
#
#
# def convert_img_to_tiles(image_data):
#     data = np.copy(image_data)
#     rows, cols, n = data.shape
#     temp_list = []
#     for i in range(rows // 2):
#         temprow = []
#         for j in range(cols // 2):
#             temprow.append(
#                 [data[i * 2][j * 2], data[i * 2][j * 2 + 1], data[i * 2 + 1][j * 2 + 1], data[i * 2 + 1][j * 2]])
#         temp_list.append(temprow)
#     return temp_list
#
#
# def rotate(arr):
#     return (arr[1], arr[2], arr[3], arr[0])
#
#
# def generate_tiles_data(all_files):
#     data = dict()
#     num = 0
#     for file in all_files:
#         num += 1
#         ip = Image_Processing(file)
#         resized_img = ip.resized_img
#         tiles = convert_img_to_tiles(resized_img)
#
#         for i in range(len(tiles)):
#             for j in range(len(tiles[i])):
#                 tile = tiles[i][j]
#                 tile_float = ((i, j), tuple(tuple(float(x) for x in side) for side in tile))
#                 tempTile = tuple(tuple(float(x) for x in side) for side in tile)
#                 found = False
#                 for _ in range(4):
#                     if tempTile in data:
#                         data[tempTile] += 1
#                         found = True
#                         break
#                     tempTile = rotate(tempTile)
#
#                 if not found:
#                     data[tile_float] = 1
#         print(f"Image Processing completed for {num}")
#     k = 1
#
#     default_tiles = dict()
#     for i in range(len(tiles)):
#         for j in range(len(tiles[i])):
#             temp_list = {key[1]:val for key,val in data.items() if (i,j) in key}
#             sorted_data = sorted(temp_list.items(), key=lambda x: x[1], reverse=True)
#             default_tiles[k] = sorted_data[0][0]
#             print(f"{k}: {[list(sorted_data[0][0][0]), list(sorted_data[0][0][1]), list(sorted_data[0][0][2]), list(sorted_data[0][0][3])]},")
#             k += 1
#
#     return default_tiles
#
#
# try:
#     url = r"C:\Users\bhanu\OneDrive\Desktop\programming_languages\Full Stack Web Development\IITGN\jigsawImg\Main\images"
#     all_files = get_all_files(url)
#     generate_tiles_data(all_files)
# except (FileNotFoundError, NotADirectoryError) as e:
#     print(f"Error: {e}")


