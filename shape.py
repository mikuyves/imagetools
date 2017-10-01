import os

from PIL import Image

from config import WORKPATH


fmt = '{img.size}\t->\t{background.size}\t[{paste_points}]\t{filename}'


def check_files():
    jpg_filenames = []
    for folder, sub, filenames in os.walk(WORKPATH):
        res = [os.path.join(folder, filename) for filename in filenames
             if filename.endswith('.jpg') and not filename.endswith('_sq.jpg')]
        jpg_filenames = jpg_filenames + res
    return jpg_filenames


def change_filename(filename):
    path, name = os.path.split(filename)
    new_path = os.path.join(path, 'square')
    try:
        os.mkdir(new_path)
    except FileExistsError:
        pass
    new_name = name.replace('.jpg', '_sq.jpg')
    new_filename = os.path.join(new_path, new_name)
    return new_filename


def squarify(filename, border=0, is_replace=False):
    img = Image.open(filename)
    x, y = img.size
    side = max([x, y]) + border * 2  # Must add at both side.
    square_size = [side, side]
    dx = int(round((side - x) / 2, 0))
    dy = int(round((side - y) / 2, 0))
    # Position of the paste image.
    px0 = side - x - dx  # Left
    py0 = side - y - dy  # Top
    px1 = px0 + x  # Right
    py1 = py0 + y  # Bottom
    paste_points = (px0, py0, px1, py1)
    background = Image.new('RGBA', square_size, (255, 255, 255))
    background.paste(img, paste_points)
    if not is_replace:
        filename = change_filename(filename)
    background.save(filename)

    print(fmt.format(**locals()))


def squarify_many(filenames, *args):
    for filename in filenames:
        squarify(filename, *args)


def main():
    # Get arguments from command line.
    import sys
    args = []
    # border.
    try:
        border = int(sys.argv[1])
    except IndexError:
        border = 0
    except ValueError:
        print('The first argument is for border which is an <int>.')
        return
    finally:
        if border < 0:
            border = -border
        args.append(border)

    # is_replace.
    try:
        is_replace = bool(sys.argv[2])
    except IndexError:
        is_replace = False
    finally:
        args.append(is_replace)

    squarify_many(check_files(), *args)


if __name__ == '__main__':
    main()