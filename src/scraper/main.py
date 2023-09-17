import sys
import datetime
import scraper

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
    #global scraper
    global scraper
    scraper =  scraper.Scraper()
    start_date = "2023/09/01"
    end_date = "2023/09/15"
    urls = generate_urls(start_date, end_date)
    #image_urls = scraper.get_asset_urls_multithreaded(urls, 10)
    image_urls = scraper.get_asset_urls(urls)
    #print(urls)
    paths = []
    i = 0
    for path in image_urls:
      paths.append(f"../../data/stripes/peanuts_{i}.png")
      i += 1
    
    scraper.scrape_and_save_singlethreaded(
        image_urls, paths)
    #scraper.scrape_and_save_multithreaded(
    #    image_urls, paths, 10)


if __name__ == '__main__':
    main()
