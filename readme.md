本人将将于2021年2月7日开始全力做论文，目前thesis文件夹下包含了数据、论文、脚本、测试模块和一个专为毕业论文而设计的python包。当前`result.csv`被一次实验性的运行所覆盖了，因此结果并不正确，本人将修改完善。

主程序均为python脚本或notebook，安排再`script`文件夹下。


# todo
- 支持代码方面
    - strategy engine
    - 使用yaml进行贝叶斯优化
- 脚本
    - 试验脚本将保存到一个`notebook`之中
    - 使用`mlflow`保存机器学习试验
- 测试代码
    - 所有功能都会写测试代码，并运行自动化测试
- 论文写作
    - 理论方面大体不变，实验部分会有较大改动
  


# 运行环境
运行该项目，推荐配置对应的`conda`环境。

配置命令如下：
```bash
conda create -n thesis python=3.7
conda activate thesis
```

之后可通过`conda`或`pip`命令安装对应的依赖包，注意，`pandas`的版本不能超过`0.25`，`ipython`版本不能超过`6.13`。

# Function
## ths_slj
提供数据及策略引擎的支持，包含了运行所有脚本必要的支持代码。
### analysis
提供了一个分析模块和对应的功能，当前已实现：
- benjamini hochberg方法
- 贝叶斯优化等其他核心算法
### data
数据支持，提供tushare或jqdata的数据支持，两者均需要在官网注册，但具体的数据已经下载并储存在了`data`文件夹中。数据包含两年内所有中证800股票的日线走势数据。该模块仅在获取数据时需要使用。
### 其他功能
strat引擎功能可得到pnl曲线用以估计投资质量，config为配置文件。
## test
存放单元测试代码，确保每个模块的正确性。
## script
数据分析脚本，但代码量较大的模块将解藕存放于`ths_slj`模块中作为支持代码。

# Result
## storage
result.csv
## analysis
result_analysis.py
# paper
该文件夹装载论文源代码。
