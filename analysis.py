# 我的第一个股票分析脚本
# QingcheDi - stock_analysis

import os
os.environ['NO_PROXY'] = '*'  # 强制所有请求不走代理

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import date

# 自动获取今天日期，永远不会过期
today = date.today().strftime("%Y%m%d")

# 获取贵州茅台(600519)历史股价
# ak.stock_zh_a_hist = akshare 获取 A 股历史数据的函数
df = ak.stock_zh_a_hist(
    symbol="600519",        # 股票代码
    period="daily",         # 日线数据（还有 weekly 周线、monthly 月线）
    start_date="20250101",  # 开始日期
    end_date=today,         # 结束日期：自动取今天
    adjust="qfq"            # 前复权：消除分红除权对价格的影响
)

# 只保留我们关心的 6 列，其余列丢掉
df = df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]

# 打印最近 10 条数据
pd.set_option('display.unicode.east_asian_width', True)  # 让中文列名对齐
print("=== 贵州茅台 (600519) 历史股价 ===")
print(df.tail(10))
print(f"\n数据共 {len(df)} 条，从 {df['日期'].iloc[0]} 到 {df['日期'].iloc[-1]}")

# 画收盘价走势图
matplotlib.rcParams['font.family'] = 'Arial Unicode MS'  # 支持中文显示

plt.figure(figsize=(12, 5))
plt.plot(df["日期"], df["收盘"], color="red", linewidth=1.5)
plt.title("贵州茅台 (600519) 收盘价走势")
plt.xlabel("日期")
plt.ylabel("价格 (元)")
plt.xticks(df["日期"][::10], rotation=45)  # 每隔10天显示一个日期标签
plt.tight_layout()
plt.savefig("maotai_price.png", dpi=150, bbox_inches='tight')  # dpi=150 让图片更清晰
plt.show()
print("图表已保存为 maotai_price.png")