from paddleocr import PaddleOCR
from PIL import Image

class OCROutput:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def __repr__(self):
        return (f"OCROutput(x={self.x}, y={self.y}, "
                f"width={self.width}, height={self.height}) and text: {self.text}")

def process_ocr_output(data):
    coordinates, text_info = data
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = coordinates
    width = max(x2 - x1, x3 - x4) + 20
    height = max(y3 - y1, y4 - y2) + 10
    x = min(x1, x4)
    y = min(y1, y4)
    text, confidence = text_info
    return OCROutput(x, y, width, height, text)

def runOCR(imagePath):
    ocr = PaddleOCR(use_angle_cls=True, lang='hu')
    result = ocr.ocr(imagePath, cls=True)
    with Image.open(imagePath) as img:
        width, height = img.size
    ocr_outputs = []
    for line_list in result:
        for line in line_list:
            ocr_output = process_ocr_output(line)
            ocr_outputs.append(ocr_output)
    return ocr_outputs, width, height