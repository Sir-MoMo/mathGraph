import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def simulate_betting(
    initial_capital=400, 
    bet_fraction=0.12, 
    win_rate=0.95, 
    win_profit_rate=0.10, 
    loss_rate=1.0, 
    num_bets=800, 
    num_simulations=1000  # 增加到1万次模拟以保证统计指标的准确性
):
    capital_paths = np.zeros((num_simulations, num_bets + 1))
    capital_paths[:, 0] = initial_capital
    
    for i in range(num_simulations):
        capital = initial_capital
        for j in range(1, num_bets + 1):
            bet_amount = capital * bet_fraction
            
            if np.random.rand() < win_rate:
                capital += bet_amount * win_profit_rate  # 盈利
            else:
                capital -= bet_amount * loss_rate        # 亏损
                
            capital_paths[i, j] = capital
            
    return capital_paths

# ================= 1. 运行模拟 =================
initial_cap = 100000
bets = 800
paths = simulate_betting(initial_capital=initial_cap, num_bets=bets, num_simulations=10000)
final_capitals = paths[:, -1]

# ================= 2. 统计指标计算 =================

# 理论期望值计算
# 单次期望乘数 = p * 盈利后乘数 + q * 亏损后乘数
expected_multiplier = 0.95 * (1 + 0.20 * 0.10) + 0.05 * (1 - 0.20 * 1.0)
theoretical_ev = initial_cap * (expected_multiplier ** bets)

# 模拟结果的统计值
mean_final = np.mean(final_capitals)
median_final = np.median(final_capitals)
variance_final = np.var(final_capitals)
std_dev = np.std(final_capitals)

# 破产统计
ruin_threshold = 10000
ruin_probability = np.sum(final_capitals < ruin_threshold) / len(final_capitals) * 100

# ================= 3. 打印统计结果 =================
print(f"=== 10,000 次蒙特卡洛模拟统计结果 ===")
print(f"初始本金: {initial_cap:,.2f}")
print("-" * 40)
print(f"理论期望值 (EV):   {theoretical_ev:,.2f}")
print(f"模拟平均值 (Mean): {mean_final:,.2f} (大数定律下应无限接近理论期望)")
print(f"模拟中位数 (Median):{median_final:,.2f} (50%的人能达到的真实水平)")
print("-" * 40)
print(f"资金方差 (Variance):{variance_final:,.2e}")
print(f"标准差 (Std Dev):  {std_dev:,.2f} (波动幅度极大)")
print("-" * 40)
print(f"最好情况 (Max):    {np.max(final_capitals):,.2f}")
print(f"最坏情况 (Min):    {np.min(final_capitals):,.2f}")
print(f"实质破产率 (<1万): {ruin_probability:.2f}%")

# ================= 4. 可视化资金曲线 =================
plt.figure(figsize=(10, 6))
plt.style.use('bmh')

# 仅绘制前 100 条路径保持图表清晰
for i in range(100):
    plt.plot(paths[i], lw=1.5, alpha=0.3)

# 绘制辅助线
plt.axhline(initial_cap, color='black', linestyle='--', label='Initial Capital (100k)')
plt.axhline(ruin_threshold, color='red', linestyle='-', linewidth=2, label='Ruin Threshold (10k)')
plt.axhline(median_final, color='blue', linestyle=':', linewidth=2, label=f'Median ({median_final:,.0f})')

ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:,.0f}'.format(y)))

# 线性坐标系，底部锁定在破产线
plt.ylim(bottom=ruin_threshold)

plt.title('Monte Carlo Simulation: 20% Bankroll Betting (Linear Scale)')
plt.xlabel('Number of Bets')
plt.ylabel('Capital Balance')
plt.legend()
plt.tight_layout()

plt.show()