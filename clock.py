import time
import tkinter as tk

# 设置时间（以秒为单位）
work_time = 25 * 60  # 25分钟
break_time = 5 * 60  # 5分钟

# 创建GUI窗口
window = tk.Tk()
window.title("专注时钟")

# 显示时间的标签
timer_label = tk.Label(window, text="")
timer_label.pack()

# 开始计时
def start_timer(count):
    # 更新标签的文本
    minutes, seconds = divmod(count, 60)
    timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    if count > 0:
        # 继续计时
        window.after(1000, start_timer, count-1)
    else:
        # 计时结束，开始休息
        timer_label.config(text="休息时间！")
        window.after(1000, start_break_timer, break_time)

# 开始休息
def start_break_timer(count):
    # 更新标签的文本
    minutes, seconds = divmod(count, 60)
    timer_label.config(text=f"休息 {minutes:02d}:{seconds:02d}")
    
    if count > 0:
        # 继续休息
        window.after(1000, start_break_timer, count-1)
    else:
        # 休息结束，开始工作
        timer_label.config(text="工作时间！")
        window.after(1000, start_timer, work_time)

# 开始专注时钟
start_timer(work_time)

# 运行GUI窗口
window.mainloop()
