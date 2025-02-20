from pathlib import Path
import os
import math
import fontforge


def _hex_or_bin_to_str(number):
    return str(number)[2:]


def _hex_to_bin(input_char):
    return bin(int(input_char[2:], base=16))


def _bin_to_truth_table(binary_code):
    binary_str = str(binary_code)[2:]
    binary_str = binary_str.zfill(8)
    le = reversed([bool(int(binary_str[i])) for i in range(len(binary_str))])
    return [x for x in le]


def _print_test(in_var, output, function_name=None):
    if function_name:
        print("Testing function:\t{}\n".format(function_name))
    else:
        print("Testing function:\n")
    print("Input:\t\t\t{}\n".format(in_var))
    print("Output:\t\t\t{}\n".format(output))


def _hex_to_char_name(hex_code="2800"):
    hex_address = _hex_or_bin_to_str(hex_code).zfill(5)
    char_name = fontforge.nameFromUnicode(int(hex_address, base=16))
    return char_name


def _get_active_dots(truth_table):
    assert len(truth_table) == 8
    active_dots = []
    for i in range(8):
        if truth_table[i]:
            active_dots.append(str(i + 1))
    return active_dots


def calculate_coordinates(width=1.0,
                          height=1.0,
                          x_bias=0,
                          y_bias=0):
    coordinates = {}
    x_range = width - x_bias
    y_range = height - y_bias
    xs = [float((x_range * i / 4) + x_bias) for i in range(1, 4, 2)]
    ys = [float((y_range * i / 8) + y_bias) for i in range(7, 0, -2)]
    # Left side
    x = int(xs[0])
    for i, j in enumerate([1, 2, 3, 7]):  # This ordering is strange 'cause...
        y = int(ys[i])
        coordinates[j] = (x, y)
    # Right side
    x = int(xs[1])
    for i, j in enumerate([4, 5, 6, 8]):  # ...of the braille standard.
        y = int(ys[i])
        coordinates[j] = (x, y)
    return coordinates


def add_loop(old_name="./AnonymousPowerline.ttf",
             new_name="./AnonymousPowerlineWithBraille.ttf",
             width=1118,
             height=1305,
             dot_radius=64):
    font = fontforge.open(old_name)
    coordinates = calculate_coordinates(width, height)
    for i in range(256):
        truth_table = _bin_to_truth_table(_hex_to_bin(hex(i)))
        active_dots = _get_active_dots(truth_table)
        cn_var ="".join(["DOTS-"] + active_dots)
        cn_var = "BLANK" if i == 0 else cn_var
        char_name = " ".join(["BRAILLE PATTERN", cn_var])
        hex_n = "28{}".format(str(hex(i))[2:].zfill(2))
        font.createChar(int(hex_n, base=16), char_name)
        pen = font[char_name].glyphPen()
        for dot in active_dots:
            j = int(dot)
            (x, y) = coordinates[j]
            xm, xp = x - dot_radius, x + dot_radius
            ym, yp = y - dot_radius, y + dot_radius
            pen.moveTo((xm, y))
            pen.qCurveTo((xm, yp), (x, yp))
            pen.qCurveTo((xp, yp), (xp, y))
            pen.qCurveTo((xp, ym), (x, ym))
            pen.qCurveTo((xm, ym), (xm, y))
            pen.endPath()
        font[char_name].draw(pen)
        font[char_name].width = 1118
        font[char_name].vwidth = 1305
        pen = None
        if i == 256: # This is for testing. To see the output, make it a lower integer.
            print(font["A"])
            print(font["A"].layers["Fore"])
            print(font["A"].anchorPoints)
            print(font["A"].manualHints)
            print(font["A"].width)
            print(font["A"].vwidth)
            print(font["A"].left_side_bearing)
            print(font["A"].right_side_bearing)
            print(font[char_name])
            print(font[char_name].layers["Fore"])
            print(font[char_name].anchorPoints)
            print(font[char_name].manualHints)
            print(font[char_name].width)
            print(font[char_name].vwidth)
            print(font[char_name].left_side_bearing)
            print(font[char_name].right_side_bearing)
    font.validate
    font.generate(new_name)


def main():
    input_dir = Path("./fonts-in")
    output_dir = Path("./fonts-out")

    for f in [f.name for f in input_dir.iterdir() if f.is_file()]:
        read_path = "/".join([str(input_dir), f])
        nn, ext = os.path.splitext(f)
        new_name = "".join([nn, " With Braille", ext])
        write_path = "/".join([str(output_dir), new_name])
        add_loop(read_path, write_path)


if __name__ == "__main__":
    run_tests = False
    function_name = "_hex_to_bin"
    in_vars = [str(hex(i)) for i in range(0, 8, 3)]
    if run_tests is True:
        for i in in_vars:
            _print_test(i, _hex_to_bin(i), function_name)
    function_name = "_bin_to_truth_table"
    in_var = bin(170)
    if run_tests is True:
        _print_test(in_var, _bin_to_truth_table(in_var), function_name)
    else:
        main()
