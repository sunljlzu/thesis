# Benjamini-Hochberg
import numpy as np
import copy

from ths_slj.strat_engine import MaStrat, RandomStrat


def backtest(df, ma1, ma2, ma3, y1, y2):
    ma1 = int(ma1) + 1
    ma2 = int(ma2) + 1
    ma3 = int(ma3) + 1

    _tmp_df = df.copy()

    strat = MaStrat(_tmp_df, ma1=ma1, ma2=ma2, ma3=ma3, y1=y1, y2=y2)
    strat.run()
    return strat.ir, strat.pnl


def random_monte_test(df, hold_ratio=0.5, m3=150, num_iter=1000):
    from tqdm import tqdm

    ret = df.close\
              .pct_change()\
              .iloc[m3:]\
        .dropna().values

    if len(ret) < 3:
        return

    res = []

    for i in range(num_iter):
        _ret = copy.deepcopy(ret)
        idx = np.random.choice(len(ret), len(ret) - int(len(ret)*hold_ratio), replace=False)
        _ret[idx] = 0
        res.append(_ret.mean()/(_ret.std()+1e-12)*(252**0.5))
    return np.array(res)


def bh_method(x: np.ndarray, threshold=0.05):
    """
    :param x:
        list of sorted p_values in np.ndarray.
    :return:
        list of adjusted p_values in np.ndarray.
    """
    if not isinstance(x, np.ndarray):
        raise ValueError('')

    nums = len(x)
    mask = np.arange(nums) + 1
    res = x * nums / mask
    k = 0
    for i, r in enumerate(res):
        if r < threshold:
            k = i + 1

    return res, k


if __name__ == '__main__':
    pass
