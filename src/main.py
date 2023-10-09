import os
import sys
import re
from frame_extractor.frameExtractor import FrameExtractor
import datetime
import cv2
from text_extractor.TextExtractor import OCR, inpaint_text
from scraper.scraper import Scraper

# from utils import get_dates_list, create_dir, check_img, resize_img
import numpy as np

from PIL import Image

full_images = "../data/stripes/"
splitted_images = "../data/frame/"
no_text = "../data/notext/"
resized = "../data/resized/"


def generate_urls(start_date, end_date):
    """Generates an array of URLs for Peanuts comics between the given start and end dates.

    Args:
      start_date: The start date (YYYY/MM/DD) of the range.
      end_date: The end date (YYYY/MM/DD) of the range.

    Returns:
      A list of URLs.
    """
    urls = []
    for date in _generate_dates(start_date, end_date):
        urls.append(f"https://www.gocomics.com/peanuts/{date}")
    return urls


def _generate_dates(start_date, end_date):
    """Generates a list of dates between the given start and end dates.

    Args:
      start_date: The start date (YYYY/MM/DD) of the range.
      end_date: The end date (YYYY/MM/DD) of the range.

    Returns:
      A list of dates.
    """
    start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y/%m/%d"))
        start_date += datetime.timedelta(days=1)
    return dates


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def check_img(path):
    i = 0
    if path.endswith(".png"):
        try:
            img = Image.open(path)  # open the image file
            img.verify()  # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            print(path)
            # os.remove(path)
            i = i + 1

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


def main():
    # Create an instance of the Scraper class
    create_dir(full_images)
    scraper = Scraper()

    start_date = "2023/09/18"
    end_date = "2023/09/20"

    urls = []
    paths = []
    for date in _generate_dates(start_date, end_date):
        urls.append(f"https://www.gocomics.com/peanuts/{date}")
        date_str = re.sub(r"/", "_", date)
        paths.append(f"../data/stripes/{date_str}.png")

    # urls = generate_urls(start_date, end_date)

    image_urls = scraper.get_asset_urls(urls)

    # paths = []
    # for i in range(len(image_urls)):
    #     paths.append(f"../data/stripes/peanuts_{i}.png")

    scraper.scrape_and_save_singlethreaded(image_urls, paths)
    # extract frame from each full illustration
    # full_images_paths = [
    #     os.path.join(full_images, file) for file in os.listdir(full_images)
    # ]
    create_dir(splitted_images)
    splitted_images_directory = splitted_images
    frame_extractor = FrameExtractor()
    splitted_images_paths = frame_extractor.extract_and_save_panels(
        paths, splitted_images_directory
    )

    # splitted_images_paths = [
    #     os.path.join(splitted_images, file) for file in os.listdir(splitted_images)
    # ]

    ocr = OCR("tesseract")
    transcriptions = ocr.extract_text(splitted_images_paths, clustering=True)

    create_dir(no_text)
    # save and visualize
    for path in splitted_images_paths:
        # for path in [os.path.join(no_text, file) for file in os.listdir(no_text)]:
        img = cv2.imread(path)
        head, tail = os.path.split(path)
        words = transcriptions[path][0]
        bbox = transcriptions[path][1]
        wds = words.split(" ")
        img = inpaint_text(img)

        cv2.imwrite(os.path.join(no_text, tail), img)
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        check_img(no_text)
        resize_img(cv2, no_text + os.path.basename(path), "../data/resized/")


if __name__ == "__main__":
    main()
