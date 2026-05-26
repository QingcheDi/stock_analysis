import os
os.environ['NO_PROXY'] = '*'

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import date

today = date.today().strftime("%Y%m%d")

df = ak.stock_zh_a_hist(
    symbol="600519",
    period="daily",
    start_date="20250101",
    end_date=today,
    adjust="qfq"
)

df = df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]

df["MA5"] = df["收盘"].rolling(window=5).mean()
df["MA20"] = df["收盘"].rolling(window=20).mean()

df["金叉"] = (df["MA5"] > df["MA20"]) & (df["MA5"].shift(1) <= df["MA20"].shift(1))
df["死叉"] = (df["MA5"] < df["MA20"]) & (df["MA5"].shift(1) >= df["MA20"].shift(1))

pd.set_option('display.unicode.east_asian_width', True)
print("=== 贵州茅台 (600519) 均线策略信号 ===")
print(df[["日期", "收盘", "MA5", "MA20", "金叉", "死叉"]].tail(10))

golden = df[df["金叉"] == True]
death = df[df["死叉"] == True]
print(f"\n金叉出现 {len(golden)} 次，死叉出现 {len(death)} 次")

matplotlib.rcParams['font.family'] = 'Arial Unicode MS'

plt.figure(figsize=(14, 6))
plt.plot(df["日期"], df["收盘"], color="black", linewidth=1, label="收盘价", alpha=0.6)
plt.plot(df["日期"], df["MA5"], color="blue", linewidth=1.2, label="MA5")
plt.plot(df["日期"], df["MA20"], color="orange", linewidth=1.2, label="MA20")

plt.scatter(golden["日期"], golden["收盘"], marker="^", color="red", s=100, label="金叉(买入)", zorder=5)
plt.scatter(death["日期"], death["收盘"], marker="v", color="green", s=100, label="死叉(卖出)", zorder=5)

plt.title("贵州茅台 (600519) 双均线策略")
plt.xlabel("日期")
plt.ylabel("价格 (元)")
plt.xticks(df["日期"][::10], rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("maotai_ma.png", dpi=150, bbox_inches='tight')
plt.show()
print("图表已保存为 maotai_ma.png")