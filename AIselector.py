
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def plot_function():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        d = float(entry_d.get())
        
        x = np.linspace(-10, 10, 400)
        y = a * x**3 + b * x**2 + c * x + d
        
        # 创建图像
        plt.figure(figsize=(8, 6))
        
        # 优化图例显示的字符串格式
        equation = f"y = {a}x³ "
        equation += f"+ {b}x² " if b >= 0 else f"- {abs(b)}x² "
        equation += f"+ {c}x " if c >= 0 else f"- {abs(c)}x "
        equation += f"+ {d}" if d >= 0 else f"- {abs(d)}"
        
        plt.plot(x, y, label=equation, color='blue')
        
                # 添加标题和坐标轴标签
        plt.title('Cubic Function Graph')
        plt.xlabel('x')
        plt.ylabel('y')
        
        # 限制 y 轴的显示范围为 -100 到 100
        plt.ylim(-10, 10)
        
        # 添加坐标轴
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        
        # 添加网格和图例
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()
        
        # 显示图像
        plt.show()
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的数字！")

# 创建 GUI 界面
root = tk.Tk()
root.title("三次函数绘制器")
root.geometry("250x200")

# a, b, c, d 的输入框
tk.Label(root, text="a:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_a = tk.Entry(root, width=10)
entry_a.grid(row=0, column=1, pady=5)
entry_a.insert(0, "1")

tk.Label(root, text="b:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=1, column=1, pady=5)
entry_b.insert(0, "0")

tk.Label(root, text="c:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_c = tk.Entry(root, width=10)
entry_c.grid(row=2, column=1, pady=5)
entry_c.insert(0, "-3")

tk.Label(root, text="d:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_d = tk.Entry(root, width=10)
entry_d.grid(row=3, column=1, pady=5)
entry_d.insert(0, "0")

# 绘制按钮
plot_button = tk.Button(root, text="绘制图像", command=plot_function)
plot_button.grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()
