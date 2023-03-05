from flask import Flask, request, jsonify, send_file
from tempfile import NamedTemporaryFile
from amulet_nbt import *
from PIL import Image
from ex import *
import os

app = Flask(__name__)

folder = "./images/16x16"
average_colors = {}

if not os.listdir(folder):
    print("The colour palette folder is empty")
for image_file in os.listdir(folder):
    with Image.open(os.path.join(folder, image_file)) as img:
        pixels = img.getdata()
        red_sum = 0
        green_sum = 0
        blue_sum = 0
        if img.mode != "RGB":
            img = img.convert("RGB")
            pixels = img.getdata()
        for r, g, b in pixels:
            red_sum += r
            green_sum += g
            blue_sum += b
        red_avg = red_sum / len(pixels)
        green_avg = green_sum / len(pixels)
        blue_avg = blue_sum / len(pixels)
        average_colors[image_file] = (int(red_avg), int(green_avg), int(blue_avg))


@app.route("/convert", methods=["POST"])
def convert():
    with NamedTemporaryFile(delete=True, mode="wb") as a:
        dither = request.form.get("dither")
        if dither == "true":
            dither = True
        else:
            dither = False

        image_file = request.files["image"]
        if image_file.content_length > 200 * 1024:
            return jsonify({"error": "File size exceeds 200kb"}), 400

        if image_file.mimetype != "image/png":
            return jsonify({"error": "Only PNG images are supported."}), 400

        image_file.save(a.name)

        try:
            image = Image.open(a.name)
            image.verify()
        except Exception:
            return jsonify({"error": "Invalid image file."}), 400

        image_array = []

        if dither:
            with Image.open(a.name) as original_img:
                original_img.thumbnail((128, 128))
                original_img = original_img.convert("RGB")
                original_pixels = original_img.load()
                width, height = original_img.size
                dither_floyd_steinberg(original_pixels, width, height, average_colors)
                new_image = Image.new("RGB", original_img.size)
                for y in range(height):
                    for x in range(width):
                        closest_color_name, closest_color = find_closest_color(
                            original_pixels[x, y], average_colors
                        )
                        new_image.putpixel((x, y), closest_color)
                        image_array.append(closest_color_name.strip(".png"))
        else:
            with Image.open(a.name) as original_img:
                original_img.thumbnail((128, 128))
                original_img = original_img.convert("RGB")
                original_pixels = original_img.getdata()
                new_image = Image.new("RGB", original_img.size)
                for i, pixel in enumerate(original_pixels):
                    closest_color_name, closest_color = find_closest_color(
                        pixel, average_colors
                    )
                    new_image.putpixel((i % 128, i // 128), closest_color)
                    image_array.append(int(closest_color_name.strip(".png")))

        tag = CompoundTag(
            {
                "data": CompoundTag(
                    {
                        "dimension": ByteTag(0),
                        "height": ShortTag(128),
                        "scale": ByteTag(3),
                        "width": ShortTag(128),
                        "xCenter": IntTag(2147483648),
                        "zCenter": IntTag(2147483648),
                        "colors": ByteArrayTag(image_array),
                    }
                )
            }
        )

        with NamedTemporaryFile(delete=True, mode="wb") as f:
            tag.save_to(
                f.name,
                compressed=True,
                little_endian=False,
                string_encoder=utf8_encoder,
            )
            file_path = f.name
        return send_file(
            file_path, download_name="map_0.dat", mimetype="application/octet-stream"
        )


if __name__ == "__main__":
    app.run(debug=True)
