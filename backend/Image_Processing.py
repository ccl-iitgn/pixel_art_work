import cv2
import numpy as np
from skimage import feature
import os
from Tiles import get_colors
from scipy.spatial.distance import cdist


class Image_Processing:
    def __init__(self, img_path):
        self.width = 30
        self.height = 40
        self.img = cv2.imread(img_path)
        if self.img is None:
            raise ValueError("Image not found or invalid image path.")
        self.dither_img = self.resize_image(self.img)
        self.resized_img = self.resize_image(self.img)
        self.grid_face_data = self.detect_facial_features(self.img)

    def optimized_floyd_steinberg_dither(self):
        img = self.img.astype(np.float32)
        palette = np.array(get_colors(), dtype=np.float32)
        print("floyd steinberg dither...")
        height, width = img.shape[:2]
        lookup = {}
        step = 8
        for r in range(0, 256, step):
            for g in range(0, 256, step):
                for b in range(0, 256, step):
                    test_color = np.array([r, g, b], dtype=np.float32)
                    distances = np.sum((palette - test_color) ** 2, axis=1)
                    closest_idx = np.argmin(distances)
                    lookup[(r, g, b)] = palette[closest_idx]

        def find_closest_color_fast(pixel):
            key = (
                int(pixel[0] // step) * step,
                int(pixel[1] // step) * step,
                int(pixel[2] // step) * step
            )
            key = (min(255, max(0, key[0])), min(255, max(0, key[1])), min(255, max(0, key[2])))

            if key in lookup:
                return lookup[key]
            else:
                distances = np.sum((palette - pixel) ** 2, axis=1)
                return palette[np.argmin(distances)]

        for y in range(height):
            for x in range(width):
                old_pixel = img[y, x].copy()
                new_pixel = find_closest_color_fast(old_pixel)
                img[y, x] = new_pixel
                error = old_pixel - new_pixel
                if x + 1 < width:
                    img[y, x + 1] += error * 7 / 16
                if y + 1 < height:
                    if x - 1 >= 0:
                        img[y + 1, x - 1] += error * 3 / 16
                    img[y + 1, x] += error * 5 / 16
                    if x + 1 < width:
                        img[y + 1, x + 1] += error * 1 / 16
        img = np.clip(img, 0, 255).astype(np.uint8)
        img = self.resize_image(img)
        return img

    def detect_facial_features(self, img_data):
        gray = cv2.cvtColor(img_data, cv2.COLOR_RGB2GRAY)
        edges = feature.canny(gray, sigma=2)
        feature_map = np.zeros_like(gray, dtype=np.float32)
        feature_map[edges] = 1.0
        kernel = np.ones((5, 5), np.uint8)
        feature_map = cv2.dilate(feature_map, kernel, iterations=3)

        feature_map = np.clip(feature_map, 0, 1)
        feature_map = cv2.GaussianBlur(feature_map, (15, 15), 0)
        feature_map = 1.0 - feature_map
        feature_map_uint8 = (feature_map * 255).astype(np.uint8)
        feature_map_colored = cv2.applyColorMap(feature_map_uint8, cv2.COLORMAP_JET)
        feature_map_colored = self.resize_image(feature_map_colored)

        grid_img_data = [[None for i in range(self.width // 2)] for j in range(self.height // 2)]
        dup_data =grid_img_data.copy()
        num=0
        # for i in range(len(feature_map_colored)):
        #     n = i // 2
        #     for j in range(len(feature_map_colored[i])):
        #         pixel = feature_map_colored[i][j]
        #         m = j // 2
        #         if (pixel[0] != 0):
        #             if (grid_img_data[n][m]):
        #                 grid_img_data[n][m] = 2
        #                 num += 1
        #                 grid_img_data[n][m] += 2
        #                 num+=1
        #             else:
        #                 grid_img_data[n][m] = 2
        #                 num+=1

        # cv2.imshow("facial", feature_map_colored)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print(num)
        return grid_img_data

    def resize_image(self, img_data):
        img = img_data.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width = img.shape[:2]
        target_ratio = 3 / 4
        if width / height > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            img_cropped = img[:, start_x:start_x + new_width]
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            img_cropped = img[start_y:start_y + new_height, :]

        img_resized = cv2.resize(img_cropped, (self.width, self.height), interpolation=cv2.INTER_AREA)
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        return img_resized

    def get_convert_dtype(self, solution_img):
        solution_img_display = np.zeros_like(solution_img, dtype=np.uint8)
        solution_img_display[:] = np.clip(solution_img, 0, 255)
        solution_img_display = cv2.resize(solution_img_display,
                                          (self.width, self.height))
        return solution_img_display

    def show_image(self, img_data):
        if img_data is None:
            raise ValueError("Image not found or invalid image path.")
        img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
        output_filename = "saved_image.png"
        cv2.imwrite(output_filename, img_data)
        cv2.imshow("Image", img_data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
