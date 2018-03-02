from PIL import Image
import pytesseract

OSD_ONLY = '-psm 0'
SINGLE_TEXT_LINE = '-psm 7'
SINGLE_WORD = '-psm 8'
SINGLE_CHARACTER = '-psm 10'
SPARSE_TEXT = '-psm 11'
SPARSE_TEXT_OCR = '-psm 12'
RAW_LINE = '-psm 13'


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def clean_image(image):
    black = 0
    white = 255
    width, height = image.size
    for i in range(width):
        for j in range(height):
            pixel = image.getpixel((i, j))
            upper_tuple = (i, j - 1)
            lower_tuple = (i, j + 1)
            left_tuple = (i - 1, j)
            right_tuple = (i + 1, j)

            neighbors = {
                upper_tuple: image.getpixel(upper_tuple) if j != 0 else None,
                lower_tuple: image.getpixel(lower_tuple) if j != height - 1 else None,
                left_tuple:  image.getpixel(left_tuple) if i != 0 else None,
                right_tuple: image.getpixel(right_tuple) if i != width - 1 else None
            }

            same_color_count = 0
            same_color_neighbor = None
            for k, v in neighbors.items():
                if v == pixel:
                    same_color_count += 1
                    same_color_neighbor = k

            if same_color_count <= 1:
                image.putpixel((i, j), white if pixel == black else black)
            if same_color_count == 1:
                image.putpixel(same_color_neighbor, white if pixel == black else black)


def get_single_letter_from_image(image, clean=False):
    copy = image.convert(mode='1')
    if clean:
        clean_image(copy)

    return pytesseract.image_to_string(image, config=SINGLE_CHARACTER)


if __name__ == '__main__':
    image = Image.open('./resources/Screenshot.png')

    # left, upper, right, lower
    etile = image.crop((683, 1279, 753, 1346))
    jtile = image.crop((588, 1279, 658, 1346))

    # image.save('./resources/result2.png')

    print(get_single_letter_from_image(etile))
    print(get_single_letter_from_image(jtile))
