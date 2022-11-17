import datetime

# generate date list from 2019-01-01 to 2019-12-31

def get_date_str_list(date_start:datetime.date, date_end:datetime.date)->list:
    date_list = [date_start + datetime.timedelta(days=x) for x in range(0, (date_end - date_start).days)]
    date_str_list = [date.strftime('%Y%m%d') for date in date_list]
    return date_str_list

def clean_url(token_string_list, date_string):
    #convert each item in list to string
    # date_string_list = [str(date) for date in date_string_list]
    #concatenate each item in list
    # date_string = ''.join(date_string_list)
    token = token_string_list[0] 
    # print(token_string_list)
    template_url = f'https://web.archive.org/web/{date_string}{token}/cnn.com/business/tech'
    return template_url
# clean_url([130328, 200, 1])