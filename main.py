import matplotlib.pyplot as plt
import numpy as np

# 生成x数据，范围为-10到10
x = np.linspace(-10, 10, 400)
# 计算对应的y值
y = x ** 2

fig, ax = plt.subplots()

# 绘制二次函数
ax.plot(x, y, label='y = x^2')

# 设置坐标轴范围
ax.set_xlim(-5, 5)
ax.set_ylim(-20, 40)

# 隐藏默认的坐标轴
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(left=False, bottom=False)

# 添加自定义箭头的坐标轴
# x轴箭头
ax.annotate('', xy=(5, 0), xytext=(-5, 0),
            arrowprops=dict(arrowstyle='->', color='black', linewidth=2.5))
# y轴箭头
ax.annotate('', xy=(0, 40), xytext=(0, -20),
            arrowprops=dict(arrowstyle='->', color='black', linewidth=2.5))

# 添加标签（可选）
ax.text(10.2, 0, 'x', fontsize=12, verticalalignment='center')
ax.text(0, 81, 'y', fontsize=12, horizontalalignment='center')

# 添加标题和标签
# ax.set_title('y = x^2 with axes arrows')

plt.show()
