import matplotlib.pyplot as plt
import numpy as np

def plot_quadratic(a, b, c):
    """
    绘制二次函数 y = ax^2 + bx + c 的图像
    """
    # 生成 x 的值
    # 根据顶点 -b/(2a) 自动选择范围
    if a != 0:
        vertex_x = -b / (2 * a)
        x = np.linspace(vertex_x - 10, vertex_x + 10, 400)
    else:
        x = np.linspace(-10, 10, 400)
    
    # 计算 y 的值
    y = a * x**2 + b * x + c

    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f'y = {a}x² + {b}x + {c}')
    
    # 设置坐标轴
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    
    # 添加标题和标签
    plt.title('Quadratic Function Graph')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    
    # 显示图像
    plt.show()

if __name__ == "__main__":
    # 示例：绘制 y = x^2 - 4x + 3
    plot_quadratic(1, -4, 3)

