import datetime

# generate date list from 2019-01-01 to 2019-12-31

def get_date_str_list(date_start:datetime.date, date_end:datetime.date)->list:
    date_list = [date_start + datetime.timedelta(days=x) for x in range(0, (date_end - date_start).days)]
    date_str_list = [date.strftime('%Y%m%d') for date in date_list]
    return date_str_list

print(get_date_str_list(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)))