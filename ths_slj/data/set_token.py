import tushare as ts

# set token of tushare api
# ts.set_token('4d1e9083d215f40dc005fff76f6be3429f24d6507e7213478dc69a77')
pro = ts.pro_api()

# test to retrieve a dataframe.
df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date', is_open='0')


