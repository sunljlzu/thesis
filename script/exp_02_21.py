import sys
from functools import partial

import numpy as np
import pandas as pd

from bayes_opt import BayesianOptimization
from tqdm import tqdm

from ths_slj.analysis import backtest, random_monte_test, bh_method

# 测试贝叶斯优化测试集， 能否战胜随机
# 训练集，测试集

df_train = pd.read_csv('../data/train.csv')
df_test = pd.read_csv('../data/test.csv')


print(df_train, df_test)


sys.exit()

codes = df_train.code.unique()

# 第二步试验可以跳过
ps = []

for code in tqdm(codes):
    _df = df_test.loc[df_test.code == code].set_index('Unnamed: 0')
    _df.index.name = 'date'

    res = random_monte_test(df=_df, hold_ratio=0.5, num_iter=100)
    bh = _df.close.iloc[150:].pct_change().dropna()

    res_bh = (bh.mean()*0.5)/(bh.std()+1e-12)*(252**0.5)
    if res is not None:
        ps.append((res > res_bh).sum()/len(res))

# exact test
# 只有0个股票通过了exact test

bh_method(
    np.sort(ps)
)

# todo sample Bayesian Optimization
# BO 用botorch构造

def _opt_fn(_tmp_df, ma1, ma2, ma3, y1, y2):
    ret = backtest(_tmp_df, ma1, ma2, ma3, y1, y2)[0]

    if ret is None:
        return -1e6
    else:
        return ret

def get_optimizer(func, pbounds):
    return BayesianOptimization(
        f=func,
        pbounds=pbounds,
        verbose=0,
        random_state=1
    )

pbounds = {
        'ma1': (0, 30),
        'ma2': (30, 60),
        'ma3': (60, 150),
        'y1': (0.005, 0.3),
        'y2': (-0.2, -0.005)
        }

ps = []
not_working = []
for code in tqdm(codes):
    _df = df_train.loc[df_train.code == code].set_index('Unnamed: 0')
    _df.index.name = 'date'
    _tmp_df = _df.copy()

    opt_fn = partial(_opt_fn, _tmp_df=_tmp_df)
    optimizer = get_optimizer(opt_fn, pbounds)
    try:
        optimizer.maximize(init_points=5, n_iter=15)
    except:
        not_working.append(code)
        continue

    _df_test = df_test.loc[df_test.code == code].set_index('Unnamed: 0')
    _df_test.index.name = 'date'
    _tmp_df = _df_test.copy()

    ir_test = backtest(_tmp_df, **optimizer.max['params'])[0]

    res = random_monte_test(df=_df, hold_ratio=0.5, num_iter=100)
    if res is not None:
        ps.append((ir_test, res.mean(), res.std(), (res > ir_test).sum()/len(res)))


df_ps = pd.DataFrame(ps, columns=['ir_test', 'ir_crl_mean', 'ir_crl_std', 'p_value'])

