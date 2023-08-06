from PIL import Image, ImageDraw, ImageFont

WIDTHS = {
    "0": 212222, "1": 222122, "2": 222221,
    "3": 121223, "4": 121322, "5": 131222,
    "6": 122213, "7": 122312, "8": 132212,
    "9": 221213, "10": 221312, "11": 231212, "12": 112232,
    "13": 122132, "14": 122231, "15": 113222,
    "16": 123122, "17": 123221, "18": 223211,
    "19": 221132, "20": 221231,  "21": 213212,
    "22": 223112, "23": 312131,  "24": 311222,
    "25": 321122, "26": 321221, "27": 312212,
    "28": 322112,  "29": 322211, "30": 212123,
    "31": 212321, "32": 232121, "33": 111323,
    "34": 131123, "35": 131321, "36": 112313,
    "37": 132113, "38": 132311, "39": 211313,
    "40": 231113, "41": 231311,  "42": 112133,
    "43": 112331, "44": 132131, "45": 113123,
    "46": 113321, "47": 133121, "48": 313121,
    "49": 211331, "50": 231131, "51": 213113,
    "52": 213311, "53": 213131, "54": 311123,
    "55": 311321, "56": 331121, "57": 312113,
    "58": 312311, "59": 332111, "60": 314111,
    "61": 221411, "62": 431111, "63": 111224,
    "64": 111422, "65": 121124, "66": 121421,
    "67": 141122, "68": 141221, "69": 112214,
    "70": 112412, "71": 122114, "72": 122411,
    "73": 142112, "74": 142211, "75": 241211,
    "76": 221114, "77": 413111, "78": 241112,
    "79": 134111, "80": 111242, "81": 121142,
    "82": 121241, "83": 114212, "84": 124112,
    "85": 124211, "86": 411212, "87": 421112,
    "88": 421211, "89": 212141, "90": 214121,
    "91": 412121, "92": 111143, "93": 111341,
    "94": 131141, "95": 114113, "96": 114311,
    "97": 411113, "98": 411311, "99": 113141,
    "100": 114131, "101": 311141, "102": 411131,
    "103": 211412, "104": 211214, "105": 211232,
    "106": 2331112,
}

START_CODE = "103"
STOP_CODE = "106"
CODE_B = "100"
FNC4 = "101"
FNC1 = "102"


def write_barcode_to_image(barcode, height=100, thickness=3, quiet_zone=True, **kwargs):
    """
    Writes out the barcode as an image.

    :param barcode:
    :param height:
    :param thickness:
    :param quiet_zone:
    :return:
    """
    barcode_widths = []
    for weight in barcode:
        barcode_widths.append(int(weight) * thickness)
    width = sum(barcode_widths)
    x = 0
    padding_y = 10

    if quiet_zone:
        width += 20 * thickness
        x = 10 * thickness

    # Monochrome Image
    img = Image.new('1', (width, height), 1)
    draw = ImageDraw.Draw(img)
    draw_bar = True
    for bar_width in barcode_widths:
        if draw_bar:
            draw.rectangle(((x, padding_y), (x + bar_width - 1, height - padding_y)), fill=0)
        draw_bar = not draw_bar
        x += bar_width

    add_text = kwargs.get('text', None)
    if add_text is not None:
        draw_text = ImageDraw.Draw(img)
        text_box_width = int(width / 3)
        text_box_height = int(height / 3)
        position = ((text_box_width, text_box_height * 2), (text_box_width * 2, text_box_height * 3))
        draw_text.rectangle(position, fill=1)
        w, h = draw.textsize(add_text)
        draw_text.text(
            (text_box_width + int((text_box_width - w) / 2), text_box_height * 2 + int((text_box_height - h) / 2)),
            add_text,
            0,
            font=ImageFont.load_default()
        )
    return img


def write_barcode_to_image_file(barcode, out_file, **kwargs):
    """
    writes out barcode to image file.

    :param barcode:
    :param out_file:
    :param kwargs:
    :return:
    """
    barcode_kwargs = {}
    if kwargs.get('text', None):
        barcode_kwargs = kwargs.get('text')
        del kwargs['text']
    img = write_barcode_to_image(barcode, **barcode_kwargs)
    img.save(out_file, **kwargs)


def generate_raw_bar_widths(build_barcode):
    """
    Generates a barcode from raw codes, allows for FNC1 use.

    :param build_barcode: array of codes excluding start, check-digit and stop.
    :return:
    """
    build_barcode.insert(0, START_CODE)
    build_barcode.append(build_check_digit(build_barcode))
    build_barcode.append(STOP_CODE)
    return "".join(str(WIDTHS[str(i)]) for i in build_barcode)


def build_check_digit(build_barcode):
    """
    Calculates the check digit.

    :param build_barcode: array of codes including start code.
    :return:
    """
    checksum = 0
    for i, item in enumerate(build_barcode):
        checksum += max(i, 1) * int(item)
    return str(checksum % 103)


def generate_bar_widths(raw_string):
    """
    Generates the widths for each bar by a lookup table.

    :param raw_string:
    :return:
    """

    build_barcode = [START_CODE]  # START

    # CONTENT
    for i in raw_string:
        ord_num = ord(i.encode('iso-8859-1'))
        if 0 <= ord_num <= 31:
            build_barcode.append(str(ord_num + 32))
        elif 96 <= ord_num <= 126:  # invalid character range (requires raw mode)
            raise ValueError('invalid character for code128a barcode from string, try raw mode using codes instead.')
        else:
            ord_num -= 32
            if ord_num > 99:
                build_barcode.append(FNC4)
                build_barcode.append(str(ord_num - 128))
            else:
                build_barcode.append(str(ord_num))

    build_barcode.append(build_check_digit(build_barcode))  # CHECKSUM

    build_barcode.append(STOP_CODE)  # STOP
    return "".join(str(WIDTHS[i]) for i in build_barcode)


if __name__ == '__main__':
    bar_widths_str = generate_bar_widths('12345678ÐEª2345FD')
    print(bar_widths_str)
    write_barcode_to_image_file(bar_widths_str, 'test_str.png')
    bar_widths_raw = generate_raw_bar_widths([FNC1, 42, 18, 40, 20, 50, CODE_B, 16])
    print(bar_widths_raw)
    write_barcode_to_image_file(bar_widths_raw, 'test_raw.png')

