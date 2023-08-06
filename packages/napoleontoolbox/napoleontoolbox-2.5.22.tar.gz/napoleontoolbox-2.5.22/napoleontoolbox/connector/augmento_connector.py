#!/usr/bin/env python3
# coding: utf-8

import requests
import pandas as pd
import math
import datetime


def convert_string(s):
    from dateutil import parser
    dt_object = parser.parse(s)
    return dt_object.timestamp()


def get_events_augmento(currency='bitcoin', startdate='2018-01-01T00:00:00Z', enddate='2019-10-01T00:00:00Z', source='twitter', precision='24H', local_root_directory=None):
    r = requests.request("GET", "http://api-dev.augmento.ai/v0.1/coins")
    # print('Coins available\n', r.content, '\n')
    r = requests.request("GET", "http://api-dev.augmento.ai/v0.1/sources")
    # print('Sources available\n', r.content, '\n')
    topics = requests.request("GET", "http://api-dev.augmento.ai/v0.1/topics").json()
    # print('Topics available\n', topics, '\n')
    topics = topics.values()

    startdate_unix, enddate_unix = convert_string(startdate), convert_string(enddate)
    precision_dct = {'1H':3600, '24H':3600*24, 'hour': 3600, 'daily': 3600*24}
    currency_dict = {'bitcoin':'BTC', 'ethereum':'ETH'}

    start_datetime = datetime.datetime.fromtimestamp(startdate_unix).date()
    end_datetime = datetime.datetime.fromtimestamp(enddate_unix).date()

    pickle_saving_path = local_root_directory + source + '_' + currency_dict[currency] + '_' + str(start_datetime) + '_'+ str(end_datetime)+'_'+'augmento.pkl'
    runs, rest = divmod((enddate_unix-startdate_unix)/precision_dct[precision], 1000)
    rest = int(math.ceil(rest))
    url = "http://api-dev.augmento.ai/v0.1/events/aggregated"
    params = {
      "source" : source,
      "coin" : currency,
      "bin_size" : precision,
      "count_ptr" : 1000,
      "start_ptr" : 0,
      "start_datetime": startdate,
      "end_datetime" : enddate} # "start_datetime" : "2019-05-01T00:00:00Z",
    output = pd.DataFrame()
    if runs != 0:
        for run in range(int(runs)):
            r = requests.request("GET", url, params=params)
            if r.status_code != 200:
                raise RuntimeError(r.json()['error']['message']) #resp.json()['error']['message']
            tmp = pd.DataFrame(r.json())
            tmp = pd.DataFrame(tmp['counts'].tolist(),index = tmp.datetime, columns = topics)
            output = pd.concat([output, tmp])
            params.update({'start_datetime': output.index.max()})
    #params['start_datetime'] = startdate
    params.update({'count_ptr': rest})
    print(params)
    r = requests.request("GET", url, params=params)
    if r.status_code != 200:
        raise RuntimeError(r.json()['error']['message'])
    elif len(r.json()) == 0:
        pass
    else:
        tmp = pd.DataFrame(r.json())
        tmp = pd.DataFrame(tmp['counts'].tolist(),index = tmp.datetime, columns = topics)
        output = pd.concat([output, tmp])
        output.to_pickle(pickle_saving_path)
    return output

