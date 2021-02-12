import warnings
from tqdm import tqdm

import numpy as np
import pandas as pd

from bayes_opt import BayesianOptimization
warnings.filterwarnings('ignore')

df_all = pd.read_csv('../data/stocks2009.csv', index_col=0)
# parameters
ITERATIONS_MONTECARLO = 1000

def backtest(A1=30, A2=50, A3=150, y1=0.05, y2=-0.01, train=True):

    A1 = int(A1)
    A2 = int(A2)
    A3 = int(A3)

    df_working = df_all.loc[df_all.code == code].drop('code', axis=1).copy()
    df_working.index = pd.to_datetime(df_working.index)

    close_x = df_working.close.values
    open_x = df_working.open.values

    MAX_A3 = 150

    split_idx = (len(close_x) - MAX_A3) // 2 + MAX_A3

    init_cash = 100000
    cash = init_cash
    stock = 0
    buy_signal = False
    holding = False
    pnl = []
    pnl_bh = []
    holding_time = 0

    start_idx = split_idx
    end_idx = len(close_x)-1
    if train:
        start_idx = MAX_A3
        end_idx = split_idx - 1
    open_bh = open_x[start_idx]

    for i in range(start_idx, end_idx):
        if not holding:
            if buy_signal:
                buy_signal = False
                open_price = open_x[i]
                holding = True
                stock = cash / open_price
                cash = 0
        else:
            holding_time += 1

        _x = close_x[i - A3: i + 1]
        ma1 = _x[-A1:].mean()
        ma2 = _x[-A2:].mean()
        ma3 = _x[-A3:].mean()
        signal1 = (_x[-1] > ma1) and (_x[-2] <= ma1)
        signal2 = (ma2 > ma3)
        signal3 = (_x[-A1].mean() - _x[-A1 - 1:-1].mean()) > 0

        if signal1 and signal2 and signal3:
            buy_signal = True

        if holding:
            diff_price = _x[-1] - open_price
            if diff_price / open_price > y1:
                holding = False
                cash = stock * _x[-1]
                stock = 0

            if diff_price / open_price < y2:
                holding = False
                cash = stock * _x[-1]
                stock = 0

        pnl.append(cash + stock * _x[-1])
        pnl_bh.append(init_cash * _x[-1] / open_bh)

    pnl_np = np.array(pnl)
    pnl_bh_np = np.array(pnl_bh)
    r = (pnl_np[1:] - pnl_np[:-1]) / pnl_np[:-1]
    r_bh = (pnl_bh_np[1:] - pnl_bh_np[:-1]) / pnl_bh_np[:-1]
    if train:
        return (r.mean() / (r.std()+0.0000000001) * 252 ** 0.5)

    # p_value
    pct_change_x = close_x[1:]/close_x[:-1]
    r_random = []
    for _idx in range(ITERATIONS_MONTECARLO):
        not_holding_idx = np.random.choice(np.arange(len(pct_change_x)), len(pct_change_x)-holding_time, replace=False)
        _pct_change_x = pct_change_x.copy()
        _pct_change_x[not_holding_idx] = 1

        ir_rt = (_pct_change_x.mean()-1)/(_pct_change_x.std()+0.00000000001)*252**0.5
        r_random.append(ir_rt)

    r_random = np.array(r_random)

    ir_bo = (r.mean()/(r.std()+0.0000000001)*252**0.5)
    p_value = (r_random>ir_bo).sum()/len(r_random)

    return  (ir_bo, r_random.mean(), p_value)

if __name__ == '__main__':
    codes = df_all.code.unique()
    result = []
    p_values = []
    result_p_value = []

    for code in tqdm(codes):
        pbounds = {
            'A1': (0, 30),
            'A2': (30, 60),
            'A3': (60, 150),
            'y1': (0.005, 0.3),
            'y2': (-0.2, -0.005)
        }
        optimizer = BayesianOptimization(
            f=backtest,
            pbounds=pbounds,
            verbose=0,
            random_state=1
        )
        try:
            optimizer.maximize(
                init_points=2,
                n_iter=15
            )
            result.append(optimizer.max)
            params = optimizer.max.get('params')
            a1 = params['A1']
            a2 = params['A2']
            a3 = params['A3']
            y1 = params['y1']
            y2 = params['y2']

            # print('train IR = ', optimizer.max['target'])
            ir_bo, ir_rd, p_value = backtest(A1=a1, A2=a2, A3=a3, y1=y1, y2=y2, train=False)
            result_p_value.append((code, ir_bo, ir_rd, p_value, params))
            # print('')
        except:
            pass
    df_result = pd.DataFrame(result_p_value)
    df_result.columns = ['code', 'ir_bo', 'ir_rd', 'p_value', 'params']
    df_result.set_index('code', inplace=True)
    print(df_result)


