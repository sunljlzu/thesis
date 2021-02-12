import sys

import numpy as np
import pandas as pd
from tqdm import tqdm

import jqdatasdk as jq

from ths_slj.config import JQ_CONFIG, DATA_PATH

train_start_date = '2017-01-01'
train_end_date = '2018-12-31'

padding = 150
test_start_date = '2019-01-01'
test_end_date = '2019-12-31'

if __name__ == '__main__':


    if not jq.is_auth():
        jq.auth(JQ_CONFIG.get('id'), JQ_CONFIG.get('password'))

    codes = jq.get_index_stocks('000852.XSHG', date=test_end_date)
    all_codes = jq.get_all_securities('stock')

    active_codes = []
    # 筛选所有的股票
    for code in codes:
        _temp = all_codes.loc[code]
        code_start = pd.Timestamp(_temp.start_date)
        code_end = pd.Timestamp(_temp.end_date)
        if code_start < pd.Timestamp(train_start_date) and code_end > pd.Timestamp(test_end_date):
            active_codes.append(code)

    # 剩余846只

    df_train = None
    for code in tqdm(active_codes):
        df = jq.get_price(code, start_date=train_start_date, end_date=train_end_date)
        df['code'] = code
        if df_train is None:
            df_train = df.copy()
        else:
            df_train = pd.concat([df_train, df])
        del df
    df_train.to_csv('train.csv')


    # 获取padding后的测试日历
    trade_days = jq.get_price('000001.XSHG', start_date=train_start_date, end_date=train_end_date).index
    test_strt_pad = trade_days[np.searchsorted(trade_days, test_start_date)-149]


    df_test = None
    for code in tqdm(active_codes):
        df = jq.get_price(code, start_date=test_strt_pad, end_date=test_end_date)
        df['code'] = code
        if df_test is None:
            df_test = df.copy()
        else:
            df_test = pd.concat([df_test, df])
        del df
    df_test.to_csv('test.csv')



