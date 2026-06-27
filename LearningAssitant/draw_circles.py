import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_concentric_circles(center1, radii1, center2, radii2):
    # 创建画布和坐标系
    fig, ax = plt.subplots(figsize=(8, 8))

    # 绘制两个圆心
    ax.plot(*center1, 'ro', label=f'圆心 1 {center1}')
    ax.plot(*center2, 'bo', label=f'圆心 2 {center2}')

    # 为圆心1绘制同心圆
    for r in radii1:
        circle = patches.Circle(center1, r, fill=False, edgecolor='red', linestyle='-', alpha=0.7)
        ax.add_patch(circle)

    # 为圆心2绘制同心圆
    for r in radii2:
        circle = patches.Circle(center2, r, fill=False, edgecolor='blue', linestyle='--', alpha=0.7)
        ax.add_patch(circle)

    # 保持横纵坐标比例为 1:1，这样圆才不会变成椭圆
    ax.set_aspect('equal')

    # 自动计算并设置坐标轴的显示范围
    max_r1 = max(radii1) if radii1 else 0
    max_r2 = max(radii2) if radii2 else 0
    min_x = min(center1[0] - max_r1, center2[0] - max_r2) - 1
    max_x = max(center1[0] + max_r1, center2[0] + max_r2) + 1
    min_y = min(center1[1] - max_r1, center2[1] - max_r2) - 1
    max_y = max(center1[1] + max_r1, center2[1] + max_r2) + 1
    
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # 添加网格线和坐标轴
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.axhline(0, color='black', linewidth=1) # X轴
    ax.axvline(0, color='black', linewidth=1) # Y轴
    
    # 解决部分系统matplotlib中文显示问题
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_title('双圆心同心圆可视化')
    ax.legend()

    # 显示图像
    plt.show()

# ================= 设定你的参数 =================
# 圆心1的坐标 (x, y) 和 它的半径列表
point_A = (0, 0)
radii_A = [1, 2, 3]

# 圆心2的坐标 (x, y) 和 它的半径列表
point_B = (1, 0)
radii_B = radii_A

# 运行绘制函数
plot_concentric_circles(point_A, radii_A, point_B, radii_B)