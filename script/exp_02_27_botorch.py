import sys
from functools import partial

import numpy as np
import pandas as pd

import torch
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_model
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import UpperConfidenceBound, ExpectedImprovement, NoisyExpectedImprovement, PosteriorMean, qKnowledgeGradient, ProbabilityOfImprovement, OneShotAcquisitionFunction, AnalyticAcquisitionFunction
from botorch.optim import optimize_acqf

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


def gen_params(pbounds):
    ret = []
    for idx in range(5):
        ret.append(np.random.uniform(pbounds[0][idx], pbounds[1][idx]))
    return ret

def _opt_fn(_tmp_df, ma1, ma2, ma3, y1, y2):
    ret = backtest(_tmp_df, ma1, ma2, ma3, y1, y2)[0]

    if ret is None:
        return -1e6
    else:
        return ret


pbounds = [
    [0, 30, 60, 0.005, -0.2],
    [30, 60, 150, 0.3, -0.005]
]

pbounds = torch.tensor(pbounds, dtype=torch.float)

df_train = df_train.set_index("Unnamed: 0")
df_train.index.name = "date"



res = []
_iter = 20
_mc = 100

for m in tqdm(range(_mc)):
    x = []
    y = []
    for i in range(5):
        _tmp_df = df_train.copy()
        _x = gen_params(pbounds)
        _y = _opt_fn(_tmp_df, ma1=_x[0], ma2=_x[1], ma3=_x[2], y1=_x[3], y2=_x[4])
        x.append(_x)
        y.append(_y)

    train_x = torch.tensor(x)
    train_y = torch.tensor(y).unsqueeze(1)
    gp = SingleTaskGP(train_x, train_y)
    mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
    fit_gpytorch_model(mll)
    # UCB = UpperConfidenceBound(gp, beta=0.1)
    # UCB = ExpectedImprovement(gp, np.array(y).max())
    UCB = qKnowledgeGradient(gp)



    for i in range(_iter):
        candidate, acq_value = optimize_acqf(
            UCB, bounds=pbounds, q=1, num_restarts=5, raw_samples=20,
        )
        candidate = candidate.numpy().tolist()[0]
        x.append(candidate)
        _tmp_df = df_train.copy()
        y.append(
            _opt_fn(_tmp_df, ma1=candidate[0],
                    ma2=candidate[1],
                    ma3=candidate[2],
                    y1=candidate[3],
                    y2=candidate[4])
        )

        train_x = torch.tensor(x)
        train_y = torch.tensor(y).unsqueeze(1)
        gp = SingleTaskGP(train_x, train_y)
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        fit_gpytorch_model(mll)
        # UCB = UpperConfidenceBound(gp, beta=0.1)
        # UCB = ExpectedImprovement(gp, np.array(y).max())
        CB = qKnowledgeGradient(gp)


    df = pd.DataFrame(
        {
            'a': x,
            'b': y
        }
    )

    y = np.array(y)
    res.append(y.max())

res = np.array(res)
print(res.mean(), res.std())













