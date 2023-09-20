import sys
import datetime
from scraper import Scraper


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


def main():
    # Create an instance of the Scraper class
    scraper = Scraper()

    start_date = "2023/09/10"
    end_date = "2023/09/20"

    urls = generate_urls(start_date, end_date)

    image_urls = scraper.get_asset_urls(urls)

    paths = []
    for i in range(len(image_urls)):
        paths.append(f"../../data/stripes/peanuts_{i}.png")

    scraper.scrape_and_save_singlethreaded(image_urls, paths)
    # scraper.scrape_and_save_multithreaded(
    #    image_urls, paths, 10)


if __name__ == "__main__":
    main()
