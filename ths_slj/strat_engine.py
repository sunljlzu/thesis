import abc

import numpy as np
import pandas as pd


class BaseMaStrategy:

    def __init__(self, data, ma1=5, ma2=10, ma3=15, y1=0.07, y2=-0.02):
        self.data = data
        self.ma1 = ma1
        self.ma2 = ma2
        self.ma3 = ma3
        self.y1 = y1
        self.y2 = y2

        self.fields = ['ma1', 'ma2', 'ma3']
        self._gen_factor()

        self.holding = False
        self.order = None

        self.pnl = []
        self.total_value = 1

    def _gen_factor(self):
        for f in self.fields:
            m = getattr(self, f)
            self.data[f] = self.data \
                .rolling(m) \
                .mean() \
                .close.values

    @abc.abstractmethod
    def on_bar(self, idx):
        pass

    def _process_order(self, order: str, idx):
        if order=='buy':
            self.holding = True
            self.open_quantity = self.total_value / self.data.open.iloc[idx]
            self.open_price = self.data.open.iloc[idx]
        else:
            self.holding = False

    def buy(self):
        self.order = 'buy'

    def sell(self):
        self.order = 'sell'

    def run(self):
        self.data.dropna(inplace=True)
        for idx in range(len(self.data.index)):

            # ma3之前的数据不会被使用
            if idx < self.ma3:
                continue

            if self.order is not None:
                self._process_order(self.order, idx)
                self.order = None

            self.on_bar(idx)

            if self.holding:
                self.total_value = self.open_quantity * self.data.close.iloc[idx]
            self.pnl.append(self.total_value)

        self.pnl = np.array(self.pnl)

        self._gen_ir()

    def _gen_ir(self):
        ret = np.diff(np.log(self.pnl))
        if len(self.pnl) == 0:
            self.ir = None
            return
        self.ir = ret.mean() / ( ret.std() + 1e-12) * (252**0.5)


class MaStrat(BaseMaStrategy):

    def on_bar(self, idx):
        ma1 = self.data.ma1.iloc[idx]
        ref_ma1 = self.data.ma1.iloc[idx-1]

        ma2 = self.data.ma2.iloc[idx]
        ma3 = self.data.ma3.iloc[idx]

        close = self.data.close.iloc[idx]
        ref_close = self.data.close.iloc[idx-1]

        if self.holding:
            diff_price = close - self.open_price
            if diff_price / self.open_price > self.y1:
                self.sell()
            if diff_price / self.open_price < self.y2:
                self.sell()
        else:
            signal1 = ma2 > ma3
            signal2 = ma1 > ma2
            signal3 = (ref_close < ref_ma1) & (close > ma1)
            if signal1 and signal2 and signal3:
                self.buy()


class RandomStrat(BaseMaStrategy):

    def on_bar(self, idx):
        signal = np.random.randn() > 0
        if self.holding:
            if signal:
                self.sell()
        else:
            if signal:
                self.buy()





if __name__ == '__main__':
    df = pd.read_csv('../data/stocks2017.csv')
    code = '002277.XSHE'
    df = df.loc[df.code == code].set_index('Unnamed: 0')
    df.index.name = 'date'

    es = RandomStrat(df)
    es.run()

    print(es.ir)


