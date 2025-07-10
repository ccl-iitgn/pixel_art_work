from Image_Processing import Image_Processing
from PixelModel import PixelModel
from Preprocessing import convert_img_to_tiles, convert_tiles_to_pixels, compute_diff_placement_tiles


def create_puzzle(Img_url):
    # Img_url = r"C:\Users\bhanu\OneDrive\Desktop\programming_languages\Full Stack Web Development\IITGN\jigsawImg\Main\images\abdul_kalam.png"

    (rows, cols) = 20, 15
    ip = Image_Processing(Img_url)
    image_tiles = convert_img_to_tiles(ip.dither_img)
    tile_placements = compute_diff_placement_tiles(image_tiles)

    p_model = PixelModel(
        rows=rows,
        cols=cols,
        tile_placements=tile_placements,
        grid_face_data=ip.grid_face_data,
    )

    solution_tiles = p_model.solve()
    return solution_tiles

# print(create_puzzle(""))