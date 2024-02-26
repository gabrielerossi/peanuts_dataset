import os
import datetime
from PIL import Image

def get_dates_list(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y/%m/%d"))
        start_date += datetime.timedelta(days=1)
    return dates
    #return [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]


def create_dir(dir_name):
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)
