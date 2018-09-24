# Project-specific libraries
import base_client as Client

# External libraries
import datetime
from datetime import timedelta

business_days = Client.request("market", "get_business_days_in_range", { "start_date": "2018-01-01", "end_date": "2019-12-31" })["dates"]

# checks if a certain date is a business day
def is_business_day(date):
    return date.strftime("%Y-%m-%d") in business_days

# adds a certain number of business days to the current date
def add_business_days(current_date, number_of_business_days):
    ending_date = current_date
    while number_of_business_days > 0:
        ending_date += timedelta(days=1)
        if is_business_day(ending_date):
            number_of_business_days -= 1
    return ending_date
