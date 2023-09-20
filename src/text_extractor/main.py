import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import datetime
import cv2
from text_extractor.TextExtractor import OCR, inpaint_text
#from utils import get_dates_list, create_dir, check_img, resize_img
import numpy as np

from PIL import Image

full_images = "../../data/stripes"
splitted_images = "../../data/frame"
no_text = "../../data/notext"
resized = "../../data/resized"

def create_dir(dir_name):
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)

def check_img(path):
    i = 0
    if path.endswith('.png'):
            try:
                img = Image.open(path)  # open the image file
                img.verify()  # verify that it is, in fact an image
            except (IOError, SyntaxError) as e:
                print(path)
                #os.remove(path)
                i = i+1
    
    return i

def resize_img(cv2, path, output_path):

    create_dir(output_path)

    img = cv2.imread(path)

    file_name = os.path.basename(path)

    # Get original height and width
    print(f"Original Dimensions : {img.shape}")

    # resize image by specifying custom width and height
    resized = cv2.resize(img, (512, 512))

    output = output_path + file_name

    print(f"Resized Dimensions : {resized.shape}")
    cv2.imwrite(output, resized)

if __name__ == "__main__":
    # get transcriptions
    ocr = OCR("tesseract")
    splitted_images_paths = [os.path.join(splitted_images, file) for file in os.listdir(splitted_images)]
    transcriptions = ocr.extract_text(splitted_images_paths, clustering=True)

    create_dir(no_text)
    create_dir(resized)
    # save and visualize
    #for path in splitted_images_paths:
    for path in [os.path.join(no_text, file) for file in os.listdir(no_text)]:
        img = cv2.imread(path)
        head, tail = os.path.split(path)
        words = transcriptions[path][0]
        bbox = transcriptions[path][1]
        wds = words.split(" ")
        img = inpaint_text(img)
        
        cv2.imwrite(os.path.join(no_text, tail), img)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        check_img(path)
        resize_img(cv2, path, resized)
    