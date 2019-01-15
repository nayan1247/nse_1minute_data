#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:26:37 2019

@author: nayandharamshi
"""


import requests
import json
import pandas as pd
from pandas.io.json import json_normalize


cookies = {
    '_ga': 'GA1.2.51575146.1547524241',
    '_gid': 'GA1.2.1717918822.1547524241',
    '__gads': 'ID=253f5f958d48fcf8:T=1547524259:S=ALNI_MbxsH1mN0Y78HGEMdySl6beNRgHbA',
}

headers = {
    'Pragma': 'no-cache',
    'Origin': 'http://charting.bseindia.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'http://charting.bseindia.com/',
    'Content-Length': '0',
    'DNT': '1',
}



## Master List for Stock ID's
response = requests.get('http://charting.bseindia.com/charting/RestDataProvider.svc/LoadMaster/B', headers=headers, cookies=cookies)
jsonResponse = json.loads(response.content)
table=jsonResponse['LoadMasterResult']['ScripInfo']
table_final=json_normalize(table[:])



params = (
    ('exch', 'N'),
    ('scode', '16'),
    ('type', 'i'), # i, b
    ('mode', 'bseL'),
    ('fromdate', '15-01-2019-9:15:22-AM'),
)

## Fetch for the Specific Stock or Index based on the params
response = requests.post('http://charting.bseindia.com/charting/RestDataProvider.svc/getDatI', headers=headers, params=params, cookies=cookies)
#response = requests.post('http://charting.bseindia.com/charting/RestDataProvider.svc/getDatI?exch=N&scode=16&type=i&mode=bseL&fromdate=15-01-2019-09:45:22-AM', headers=headers, cookies=cookies)
jsonResponse = json.loads(response.content)
#print(jsonResponse)

#pd_data=pd.DataFrame.from_dict(jsonResponse)

t=json.loads(jsonResponse['getDatIResult'])
s=pd.DataFrame.from_dict(t['DataInputValues'][0])
open_data=s['OpenData'][0]['Open'].split(',')
high_data=s['HighData'][0]['High'].split(',')
low_data=s['LowData'][0]['Low'].split(',')
close_data=s['CloseData'][0]['Close'].split(',')
volume_data=s['VolumeData'][0]['Volume'].split(',')
date_data=s['DateData'][0]['Date'].split(',')


df = pd.DataFrame({'date':date_data,
                   'open':open_data,
                   'high':high_data,
                   'low':low_data,
                   'close':close_data,
                   'volume':volume_data})
