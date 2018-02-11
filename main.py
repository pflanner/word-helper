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

image = Image.open('./resources/result.png')
copy = image.convert(mode='1')
copy.save('result.png')
output = pytesseract.image_to_string(copy, config=SINGLE_CHARACTER)
print(output)
