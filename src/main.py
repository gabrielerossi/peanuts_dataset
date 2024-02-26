import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import re
from panel_extractor.panelExtractor import PanelExtractor
from scraper.scraper import Scraper

from utils import get_dates_list, create_dir

full_images = "../data/stripes/"
splitted_images = "../data/frame/"

if __name__ == "__main__":
    start_date = "2024/01/01"
    end_date = "2024/01/05"
    
    comic_urls = []
    full_images_paths = []
    for date in get_dates_list(start_date, end_date):
        comic_urls.append(f"https://www.gocomics.com/peanuts/{date}")
        date_str = re.sub(r"/", "_", date)
        full_images_paths.append(f"{full_images}/{date_str}.png")

    scraper = Scraper()
    urls = scraper.get_asset_urls(comic_urls)

    create_dir(full_images)
    scraper.scrape_and_save_singlethreaded(urls, full_images_paths)

    full_images_paths = [
        os.path.join(full_images, file) for file in os.listdir(full_images)
    ]
    
    create_dir(splitted_images)
    splitted_images_directory = splitted_images
    panel_extractor = PanelExtractor()
    splitted_images_paths = panel_extractor.extract_and_save_panels(
        full_images_paths, splitted_images_directory
    )