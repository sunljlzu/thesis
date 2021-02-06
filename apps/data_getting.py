import sys
from jqdatasdk import *
import pandas as pd
from tqdm import tqdm


YEAR_START = 2017

with open('auth_key.txt', 'r') as f:
    dict_auth = eval(f.read())
print(dict_auth)

if not is_auth():
    auth(dict_auth.get('id'), dict_auth.get('password'))
    print(get_query_count())

codes = get_index_weights('000905.XSHG', date=str(YEAR_START)+'-01-01').index.values

_df = []
for code in tqdm(codes):
    df = get_price(code, start_date=str(YEAR_START)+'-01-01', end_date=str(YEAR_START+1)+'-12-31', frequency='1d')
    df['code'] = code
    _df.append(df)
    del df

df_result = pd.concat(_df)
df_result.to_csv('../data/stocks'+str(YEAR_START)+'.csv')




