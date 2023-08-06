import datetime
import numpy as np


def calculate_business_days_delta(date_1: datetime.datetime, date_2: datetime.datetime):
    if date_1 is None or date_2 is None:
        return None
    return np.busday_count(date_1.strftime("%Y-%m-%d"), date_2.strftime("%Y-%m-%d"))
