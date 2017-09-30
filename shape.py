import os

from PIL import Image

from config import WORKPATH


fmt = '{img.size}\t->\t{background.size}\t[{paste_points}]\t{new_filename}'


def check_files():
    jpg_filenames = []
    for folder, sub, filenames in os.walk(WORKPATH):
        res = [os.path.join(folder, filename) for filename in filenames
             if filename.endswith('.jpg') and not filename.endswith('_sq.jpg')]
        jpg_filenames = jpg_filenames + res
    return jpg_filenames


def squarify(filename, border=0):
    img = Image.open(filename)
    x, y = img.size
    side = max([x, y]) + border * 2  # Must add at both side.
    square_size = [side, side]
    dx = int(round((side - x) / 2, 0))
    dy = int(round((side - y) / 2, 0))
    # Position of the paste image.
    paste_points = (
        side - x - dx,
        side - y - dy,
        dx + x,
        dy + y
    )
    background = Image.new('RGBA', square_size, (255, 255, 255))
    background.paste(img, paste_points)
    new_filename = filename.replace('.jpg', '_sq.jpg')
    background.save(new_filename)

    print(fmt.format(**locals()))


def squarify_many(filenames, border):
    for filename in filenames:
        squarify(filename, border)


def main():
    import sys
    try:
        border = int(sys.argv[1])
    except IndexError:
        border = 0
    except ValueError:
        print('The first argument is for border which is an <int>.')
        return
    if border < 0:
        border = -border
    squarify_many(check_files(), border=border)


if __name__ == '__main__':
    main()