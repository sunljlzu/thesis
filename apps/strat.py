import sys

import numpy as np
import pandas as pd
import backtrader as bt

class FirstStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        print('{} {}, {}'.format(self.datas[0].datetime.date(), self.datas[0].datetime.time(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return None

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: {:.3f}, Cost: {:.3f}, Comm: {:.3f}'.format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm
                    )
                )
            elif order.issell():
                self.log(
                    'SELL EXECUTED, Price: {:.3f}, Cost: {:.3f}, Comm: {:.3f}'.format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm
                    )
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return None
        self.log('OPERATION PROFIT, GROSS {:.4f}, NET {:.4f}'.format(trade.pnl, trade.pnlcomm))
        # self.log('PNL {:.1f}'.format(trade.cerebro.broker.getvalue()))

    def next(self):
        self.log('Close, {:.3f}'.format(self.dataclose[0]))


class MaStrat(FirstStrategy):

    def __init__(self, p1=20, p2=130, p3=200, p4=250, y1=0.1, y2=-0.03, size=100):
        super().__init__()
        self.holding = False
        self.open_price = 0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.y1 = y1
        self.y2 = y2
        self.size = size

    def get_history_data(self, index=0, period=30):
        _result = self.datas[index]
        result = []
        for i in range(-period, 1):
            result.append(_result.close[i])
        return np.array(result)

    def next(self):
        data = self.get_history_data(index=0, period=self.p4)
        ma1 = data[-self.p1:].mean()
        ma2 = data[-self.p2:].mean()
        ma3 = data[-self.p3:].mean()
        ma4 = data[-self.p4:].mean()

        x = data[-1]
        l_x = data[-2]

        signal1 = (x > ma1) and (l_x < ma1)
        signal2 = (ma1 > ma2)
        signal3 = (ma3 > ma4)

        stop_win = stop_loss = False

        if self.holding:
            stop_win = ((x - self.open_price) / self.open_price) > self.y1
            stop_loss = ((x - self.open_price) / self.open_price) < self.y2

        if self.order:
            return

        if not self.holding:
            if signal1 and signal2 and signal3:
                self.buy(data=self.datas[0], size=self.size)
                self.holding = True
        else:
            if stop_win or stop_loss:
                self.sell(data=self.datas[0], size=self.size)
                self.holding = False
