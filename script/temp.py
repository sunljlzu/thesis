import sys

import alphalens
import pandas as pd
import numpy as np

def get_data():
    import jqdatasdk


    jqdatasdk.auth('18374980021', 'asdfasdf1')
    codes = ['000905.XSHG', '000001.XSHE', '600001.XSHG', '600547.XSHG']
    df = jqdatasdk.get_price(codes, start_date='2020-01-01', end_date='2020-03-01')
    df.to_csv('sample_data.csv')

    print(jqdatasdk.get_query_count())


df = pd.read_csv('sample_data.csv', index_col=[0, 1])


factor_data = alphalens.utils.get_clean_factor_and_forward_returns(

)

