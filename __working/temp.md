specific tasks related to well-defined, concrete goals.
continually self-examining and changing ones behavior to adapt to the markets.

risk? kelly formula?
risk management.

45 stocks with the help of assistants, execution traders, and analysts. 否则必须依赖技术分析, 很容易亏钱.

讲义 时间序列

时间序列讲义 page 34 nonlinear prediction.

page 213 time series- likelihood.
230 model selection


model selection: 双均线策略；


模拟退火算法选择参数：

最简单的模拟退火算法：
`
def accepct(delta_e, t):
  if delta_e<0:
    return 1
  else:
    d = exp(-(delta_e/t))
    if (d>rand):
      return 1
    else:
      return 0
`
贝叶斯优化
机器学习领域比较好的解决超参数搜索的方案。栅格点搜索（grid search）的效率较低。采用高斯过程，考虑之前的参数信息，不断地更新先验；迭代次数少，速度快；而栅格点搜索速度慢，当参数多时可能引发维度爆炸; 对于非凸问题表现稳健;

贝叶斯优化的python实现；

practical bayesian optimization of machine learning algorithms

Gaussian process(GP)

exploration-exploitation trade-off;


sigopt: 自动调参；

gpyopt: two-sigma所用的sigopt的免费版，sota
