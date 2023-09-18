import cv2
import pytesseract as tess
from tqdm import tqdm


class TesseractOCR:
    def __init__(self, tesseract_path):
        """
        Constructor
        :param tesseract_path:
        """
        tess.pytesseract.tesseract_cmd = tesseract_path

    def extract_text(self, image):
        """
        Performs OCR text extraction using Tesseract OCR.
        :param image: image to detect text in.
        :return: tuple of lists, one containing the detected strings, the other containing the b-boxes.
        """
        config = r'-c tessedit_char_whitelist' \
                        r"='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,?!-$% '"
        #config = '--psm 3'
        boxes = tess.image_to_data(image, config=config)
        words = []
        bboxes = []

        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    bboxes.append((x, y, x + w, y + h))
                    words.append(b[11])
        return words, bboxes

    def remove_text(self, image, words):
        """
        Removes texts from the selected image
        :param image: image to remove the text
        :param words: words to remove
        :return: cleaned image
        """
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        inverted_thresh = 255 - thresh
        dilate = cv2.dilate(inverted_thresh, kernel, iterations=4)
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ROI = thresh[y:y+h, x:x+w]
            data = tess.image_to_string(ROI, lang='eng',config='--psm 6').lower()
            if words[0] in data:
                img[y:y+h, x:x+w] = [255,255,255]
        
        return img