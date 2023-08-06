import os
import inspect
import imageio
from PIL import Image, ImageDraw
import cv2
import numpy as np

def leds_2_image(leds, image_name=None, path_build_external=False):
    if not path_build_external:
        # https://stackoverflow.com/questions/50499/how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
        abspath = os.path.dirname(os.path.abspath(inspect.stack()[1][1])).replace('\\', '/')
        if image_name is None:
            image_name = abspath + '/image.png'
        image_name = (abspath + '/' + image_name).replace('\\', '/')

    background = 0xEFEBE7
    img = Image.new('RGB', (260, 260), color=background)
    draw = ImageDraw.Draw(img)

    # draw led on coordinate i j
    for i in range(0, 5, 1):
        for j in range(0, 5, 1):
            if leds[i][j]:
                color = 0x0000FF
            else:
                color = background - 0x101010

            box = [(j * 50 + 10), (i * 50 + 10), (j * 50 + 50), (i * 50 + 50)]
            draw.ellipse(box, outline=color, fill=color)

    img.save(image_name)


def leds_2_image_outro(frames=5, image_name='img/leds_outro_'):
    abspath = os.path.dirname(os.path.abspath(inspect.stack()[1][1])).replace('\\', '/')

    leds_ = [[False for i in range(5)] for n in range(5)]

    for i in range(0, frames, 1):
        image_name_start = (abspath + '/' + image_name + f'{i:d}.png').replace('\\', '/')
        # print(image_name_start)
        leds_2_image(leds_, image_name_start, path_build_external=True)


def find_files_4_gif(folder='', file_name_text_include='png'):
    path = os.getcwd().replace('\\', '/') + '/'
    filenames = []
    for file in os.listdir(path + folder):
        if file.find(file_name_text_include) >= 0:
            filenames.append((path + folder + '/' + file).replace('\\', '/'))
    return filenames


def images_2_gif(gif_name, filenames, duration):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))

    path = os.getcwd().replace('\\', '/') + '/'
    output_file = path + gif_name
    imageio.mimsave(output_file, images, duration=duration+0.05)  # Kommunikationsoffset


def images_2_solution(png_name, filenames):
    images = []
    for filename in filenames:
        if not 'outro' in filename:
            images.append(cv2.imread(filename))

    background = (0xFF, 0xFF, 0xFF)
    height = images[0].shape[0] + 55
    width = images[0].shape[1] + 20
    canvas = np.ones((height, width, 3), dtype="uint8") * background
    font = cv2.FONT_HERSHEY_SIMPLEX

    vstack = []
    rows = int(len(images) / 5)
    if (len(images) % 5) != 0:
        rows += 1

    for i in range(0, rows, 1):
        hstack = []
        for n in range(0, 5, 1):
            index = (i * 5) + n
            if index < len(images):
                canvas_copy = canvas.copy()
                canvas_copy[0:images[index].shape[0], 10:images[index].shape[1] + 10] = images[index]
                canvas_copy = cv2.putText(canvas_copy, str(index + 1), (int(width / 2) - 10, (height - 20)), font, 1.0,
                                          (0, 0, 0), 2, cv2.LINE_AA)
                hstack.append(canvas_copy)
            else:
                hstack.append(canvas)
        vstack.append(np.hstack(hstack))

    np_vstack = np.vstack(vstack)

    path = os.getcwd().replace('\\', '/') + '/'
    output_file = path + png_name
    cv2.imwrite(output_file, np_vstack)
