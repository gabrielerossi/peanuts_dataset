import cv2
from tqdm import tqdm

from text_extractor.OCRPreprocessor import rescale_for_ocr, binarize_for_ocr
from text_extractor.OCRPostprocessor import cluster, clear_text, autocorrect_text
from text_extractor.TesseractOCR import TesseractOCR
from text_extractor.VisionOCR import VisionOCR

class OCR:

    #tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tesseract_path = r'/Users/marco/tesseract/tesseract'
    cloud_credentials = '../../credentials/credentials.json'

    def __init__(self, engine):
        if engine == "tesseract":
            self.extractor = TesseractOCR(self.tesseract_path)
        elif engine == "vision-api":
            self.extractor = VisionOCR(self.cloud_credentials)
        else:
            raise Exception("Invalid OCR engine: supported engines are ")


    def extract_text(self, img_paths, rescale=False, binarize=False, clustering=True, autocorrect=False):
        """
        Extracts text from images.
        :param img_paths: A list of paths to images for processing.
        :param rescale: Bool determining if re-scaling pre-processing step should be applied.
        :param binarize: Bool determining if binarization pre-processing step should be applied.
        :param clustering: Bool determining if clustering-based output ordering post-processing step should be applied.
        :param autocorrect: Bool determining if autocorrect post-processing step should be applied.
        :return: A dictionary mapping image paths to the extracted names.
        """

        result = {}
        for path in tqdm(img_paths):
            sub_result = []
            image = cv2.imread(path)

            if rescale:
                image = rescale_for_ocr(image, self.tesseract_path)

            if binarize:
                image = binarize_for_ocr(image)

            bboxes, words = self.extractor.extract_text(image)
            
            if clustering:
                text = cluster(words, bboxes, image, visualize=False)
            else:
                text = ' '.join(words)

            text = clear_text(text)

            if autocorrect:
                text = autocorrect_text(text)
            
            sub_result.append(text)
            sub_result.append(words)
            result[path] = sub_result

        return result

    def remove_text(self, image, words):
        return self.extractor.remove_text(image, words)

import matplotlib.pyplot as plt
import keras_ocr
import cv2
import math
import numpy as np

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)
    
def inpaint_text(img_path):

    pipeline = keras_ocr.pipeline.Pipeline()
    # read image
    img = keras_ocr.tools.read(img_path)
    # generate (word, box) tuples 
    prediction_groups = pipeline.recognize([img])
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1] 
        x2, y2 = box[1][2]
        x3, y3 = box[1][3] 
        
        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
        
        thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
        
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
        thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
    return(img)