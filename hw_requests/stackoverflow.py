import requests
from pprint import pprint
import datetime as DT


def get_questions(fromdate, todate):
    url = 'https://api.stackexchange.com/2.3/questions'
    dict_params = {'fromdate': {fromdate},
                   'todate': {todate},
                   'order': 'desc',
                   'sort': 'activity',
                   'tagged': 'python',
                   'site': 'stackoverflow'}
    resp = requests.get(url, params=dict_params)
    return resp.json()


fromdate_str = input('Введите дату начала в формате 2022-05-22: ')
todate_str = input('Введите дату окончания в формате 2022-05-22: ')
fromdate_date = DT.datetime.strptime(f'{fromdate_str}  03:00:00', '%Y-%m-%d %H:%M:%S')
todate_date = DT.datetime.strptime(f'{todate_str}  03:00:00', '%Y-%m-%d %H:%M:%S')
fromdate = str(int(fromdate_date.timestamp()))
todate = str(int(todate_date.timestamp()))

response = get_questions(fromdate, todate)
pprint(response)
