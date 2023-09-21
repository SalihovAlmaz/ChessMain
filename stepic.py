from datetime import date,timedelta
from calendar import monthrange,month_name
def get_all_mondays(year):
    start_date = date(year, 1, 1)
    l = []
    while start_date != date(year+1, 1, 1):
        if start_date.weekday() == 0:
            l.append(start_date)
        start_date = start_date + timedelta(days=1)
    return l
print(get_all_mondays(2021))