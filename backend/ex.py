import os
from PIL import Image
import math


def find_closest_color(pixel, average_colors):
    closest_color_name = None
    closest_color = None
    closest_distance = float("inf")
    for color_name, color in average_colors.items():
        r, g, b = pixel
        ar, ag, ab = color
        distance = math.sqrt((r - ar) ** 2 + (g - ag) ** 2 + (b - ab) ** 2)
        if distance < closest_distance:
            closest_color = color
            closest_color_name = color_name
            closest_distance = distance
    return closest_color_name, closest_color


def dither_floyd_steinberg(pixels, width, height, average_colors):
    for y in range(height):
        for x in range(width):
            old_r, old_g, old_b = pixels[x, y]
            closest_color_name, closest_color = find_closest_color(
                (old_r, old_g, old_b), average_colors
            )
            new_r, new_g, new_b = closest_color
            pixels[x, y] = (new_r, new_g, new_b)
            error_r = old_r - new_r
            error_g = old_g - new_g
            error_b = old_b - new_b
            if x + 1 < width:
                pixels[x + 1, y] = (
                    int(pixels[x + 1, y][0] + error_r * 7 / 16),
                    int(pixels[x + 1, y][1] + error_g * 7 / 16),
                    int(pixels[x + 1, y][2] + error_b * 7 / 16),
                )
            if x > 0 and y + 1 < height:
                pixels[x - 1, y + 1] = (
                    int(pixels[x - 1, y + 1][0] + error_r * 3 / 16),
                    int(pixels[x - 1, y + 1][1] + error_g * 3 / 16),
                    int(pixels[x - 1, y + 1][2] + error_b * 3 / 16),
                )
            if y + 1 < height:
                pixels[x, y + 1] = (
                    int(pixels[x, y + 1][0] + error_r * 5 / 16),
                    int(pixels[x, y + 1][1] + error_g * 5 / 16),
                    int(pixels[x, y + 1][2] + error_b * 5 / 16),
                )
            if x + 1 < width and y + 1 < height:
                pixels[x + 1, y + 1] = (
                    int(pixels[x + 1, y + 1][0] + error_r * 1 / 16),
                    int(pixels[x + 1, y + 1][1] + error_g * 1 / 16),
                    int(pixels[x + 1, y + 1][2] + error_b * 1 / 16),
                )
