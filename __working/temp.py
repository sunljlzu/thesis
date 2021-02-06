report = pandas_profilings.ProfileReport(data)
report

from tqdm import notebook
notebook.tqdm().pandas()

df1.join(df2)

pd.concat([df1, df2], ignore_index=True, axis=0)

parallel = os.environ.get('VNPY_BUILD_PARALLEL', None)


from vnpy.trader.constant import Interval

interval=Interval.MINUTE

from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
from vnpy.app.cta_strategy.strategies.atr_rsi_strategy import AtrRsiStrategy
from datetime import datetime

