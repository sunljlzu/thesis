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

code = '300502.XSHE'

# 没有缺失值

df_train = df_train.loc[df_train.code == code]
df_test = df_test.loc[df_test.code == code]


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
        # verbose=True,
        # random_state=1
    )




pbounds = {
        'ma1': (0, 30),
        'ma2': (30, 60),
        'ma3': (60, 150),
        'y1': (0.005, 0.3),
        'y2': (-0.2, -0.005)
        }

df_train = df_train.set_index("Unnamed: 0")
df_train.index.name = "date"
_tmp_df = df_train.copy()

opt_fn = partial(_opt_fn, _tmp_df=_tmp_df)

targets = []
for i in range(1):
    optimizer = get_optimizer(opt_fn, pbounds)
    optimizer.maximize(init_points=5, n_iter=15)
    targets.append(optimizer.max['target'])

targets = np.array(targets)
print(targets.mean(), targets.std())


