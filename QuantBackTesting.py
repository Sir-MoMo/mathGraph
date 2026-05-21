import ccxt
import pandas as pd
import vectorbt as vbt
import numpy as np
import warnings

# 忽略常规警告
warnings.filterwarnings('ignore')

# ==========================================
# 1. 核心参数配置
# ==========================================
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
LIMIT = 1000         # 单次获取K线数量上限
FEE_RATE = 0.001     # 假设单边吃单 (Taker) 手续费为 0.1%
LEVERAGE = 13        # 蒙特卡洛模拟杠杆倍数
INIT_CASH = 10000    # 初始回测测试资金

# ==========================================
# 2. 获取交易所数据
# ==========================================
print(f"[*] 正在从 OKX 获取 {SYMBOL} 的 {TIMEFRAME} K线数据...")
exchange = ccxt.okx()

try:
    ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
except Exception as e:
    print(f"[!] 网络或API请求错误: {e}")
    exit()

df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

print(f"[*] 成功获取 {len(df)} 条数据: {df.index.min()} -> {df.index.max()}")

# ==========================================
# 3. 计算技术指标 (纯 Pandas 原生实现)
# ==========================================
print("[*] 正在计算技术指标 (Pandas Native)...")

# 计算 SMA 88
df['sma88'] = df['close'].rolling(window=88).mean()

# 计算 MACD (12, 26, 9)
ema12 = df['close'].ewm(span=12, adjust=False).mean()
ema26 = df['close'].ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26
signal_line = macd_line.ewm(span=9, adjust=False).mean()
df['macd_hist'] = macd_line - signal_line

# 计算布林带带宽 (20, 2)
sma20 = df['close'].rolling(window=20).mean()
std20 = df['close'].rolling(window=20).std(ddof=0) 
bb_upper = sma20 + 2 * std20
bb_lower = sma20 - 2 * std20
df['bb_width'] = bb_upper - bb_lower

# 清理早期由于计算均线产生的 NaN 行
df.dropna(inplace=True)

# ==========================================
# 4. 生成买卖信号 (向量化条件)
# ==========================================
print("[*] 正在生成交易信号...")

close = df['close']
sma = df['sma88']
macd_h = df['macd_hist']
bb_w = df['bb_width']

# 入场条件:
# 1. 价格在 SMA 88 之上
# 2. MACD 为正 (绿柱) 且当前柱子 > 上一根柱子 (动量放大)
# 3. 布林带开口放大 (当前带宽 > 上一根带宽)
df['entry'] = (
    (close > sma) & 
    (macd_h > 0) & 
    (macd_h > macd_h.shift(1)) & 
    (bb_w > bb_w.shift(1))
)

# 出场条件:
# 1. MACD 柱体缩短 (动能减弱) 或
# 2. 价格跌破 SMA 88
df['exit'] = (
    (macd_h < macd_h.shift(1)) | 
    (close < sma)
)

# ==========================================
# 5. 执行量化回测 (VectorBT)
# ==========================================
print("[*] 正在执行历史数据回测...")
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=df['entry'],
    exits=df['exit'],
    fees=FEE_RATE,
    init_cash=INIT_CASH,
    freq=TIMEFRAME
)

print("\n" + "="*50)
print(">>> 历史回测表现 (无杠杆, 已扣手续费) <<<")
print("="*50)
# 提取并打印核心指标
stats = pf.stats(metrics=['total_return', 'win_rate', 'max_drawdown', 'total_trades', 'profit_factor'])
print(stats)

# ==========================================
# 6. 蒙特卡洛极端风险模拟 (带杠杆)
# ==========================================
print("\n" + "="*50)
print(f">>> 蒙特卡洛极端风险模拟 ({LEVERAGE}倍杠杆) <<<")
print("="*50)

# 提取回测中每笔交易的纯收益率序列
trade_returns = pf.trades.returns.values

if len(trade_returns) < 5:
    print("[!] 历史交易笔数过少，无法执行有效的蒙特卡洛模拟。需要积累更长时间的 1m 数据。")
else:
    n_simulations = 10000    # 万次平行宇宙
    n_trades_per_sim = 200   # 模拟连续执行 200 笔交易
    ruin_threshold = 0.05    # 净值跌至 5% 判定爆仓

    # 1. 重采样：打乱交易顺序
    random_indices = np.random.randint(0, len(trade_returns), size=(n_simulations, n_trades_per_sim))
    simulated_returns = trade_returns[random_indices]

    # 2. 施加杠杆
    leveraged_returns = simulated_returns * LEVERAGE

    # 3. 截断亏损：单笔亏损超过 100% 净值归零
    leveraged_returns = np.where(leveraged_returns <= -1.0, -1.0, leveraged_returns)

    # 4. 计算资金曲线
    equity_paths = np.cumprod(1 + leveraged_returns, axis=1)

    # 5. 爆仓判定
    is_liquidated = np.any(equity_paths <= ruin_threshold, axis=1)
    liquidation_prob = np.mean(is_liquidated) * 100

    # 6. 计算幸存路径的回撤
    surviving_paths = equity_paths[~is_liquidated]
    
    if len(surviving_paths) > 0:
        running_max = np.maximum.accumulate(surviving_paths, axis=1)
        drawdowns = (running_max - surviving_paths) / running_max
        max_drawdowns = np.max(drawdowns, axis=1)
        
        median_mdd = np.median(max_drawdowns) * 100
        worst_mdd = np.percentile(max_drawdowns, 99) * 100
    else:
        median_mdd = 100.0
        worst_mdd = 100.0

    print(f"模拟次数: {n_simulations} 次独立的 200 笔交易周期")
    print(f"绝对爆仓率 (归零风险): {liquidation_prob:.2f}%")
    
    if liquidation_prob < 100:
        print(f"中位数最大回撤 (幸存者): {median_mdd:.2f}%")
        print(f"99%极端最大回撤 (幸存者): {worst_mdd:.2f}%")
        
        if liquidation_prob > 10:
            print("\n[!] 警告: 爆仓风险极高。当前的盈亏比和胜率不足以支撑该杠杆倍数，建议调低杠杆或优化入场条件。")
    else:
        print("\n[!] 致命警告: 该策略在当前参数下全军覆没，请勿直接实盘。")

# 如果你在 Jupyter 笔记本中，可以取消注释以查看交互式图表
# pf.plot().show()