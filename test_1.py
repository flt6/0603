import tkinter as tk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from os import listdir
from random import randint,shuffle
from time import time
import threading

DATA_ANALYTICS = False
CHANGE_TIME = 120
begin = None
last_win_size=[-1,-1]
start_change = threading.Event()

if DATA_ANALYTICS:
    # import numpy as np
    delay_arr = []
    chosen = np.ndarray((1000,), np.int16)
    chosen_i = 0


class FloatingWindow(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.overrideredirect(True)  # 去掉窗口边框
        self.attributes('-topmost', True)  # 窗口置顶

        # 获取屏幕大小
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 设置悬浮窗大小为屏幕高度的1/8
        window_height = screen_height // 16
    
        self.geometry(f'{window_height}x{window_height}+100+100')

        self.bind('<B1-Motion>', self.on_motion)  # 绑定鼠标左键移动事件
        self.bind('<Button-1>', self.on_drag_start)  # 绑定鼠标左键按下事件

        # 添加激活按钮
        btn_activate = tk.Button(self, text='激活', command=self.activate_main_window)
        btn_activate.pack(fill=tk.BOTH, expand=True)

    def on_drag_start(self, event):
        self._drag_data = {'x': event.x, 'y': event.y}

    def on_motion(self, event):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        self.geometry(f'+{new_x}+{new_y}')

    def activate_main_window(self):
        self.master.deiconify()
        self.master.lift()
        choose_image(True)
        print("Called")
##        print("Call")
##        start_change.set()
##        choose_image()
##        self.master.after(20,lambda :start_change.clear())

def show_floating_window():
        floating_window = FloatingWindow(root)
        floating_window.mainloop()

def on_st_button_click(event=None):
    global delay_id
    delay_id = root.after(CHANGE_TIME, choose_image)
    start_change.set()


def on_end_button_click(event=None):
    global delay_id
    start_change.clear()
    delay_id = None

img_i=0
def choose_image(force:bool=False):
    # print("Called choose_image")
    global img_i,dealed_imgs
    if not start_change.is_set() and not force:
        return
    r = img_i
    img_i+=1
    if img_i>=len(dealed_imgs):
        shuffle(dealed_imgs)
        img_i=0
    if DATA_ANALYTICS:
        global chosen, chosen_i
        chosen[chosen_i] = r
        chosen_i += 1
    update_image(dealed_imgs[r], time())


def update_image(img, bgn=None):
    global begin, photo_label, CHANGE_TIME, delay_id

    # 更新图像
    photo = ImageTk.PhotoImage(img)
    photo_label.config(image=photo)
    photo_label.image = photo
    photo_label.pack(fill=tk.BOTH, expand=True)
    if begin is None:
        begin = time()
    else:
        if DATA_ANALYTICS:
            # print(f"Duration: {(time() - begin) * 1000}")
            delay_arr.append((time() - begin) * 1000)
            begin = time()
    if bgn is None:
        return
    dur = (time() - bgn) * 1000
    delay = CHANGE_TIME - dur
    if delay < 0:
        CHANGE_TIME = round(dur + 10)
        delay = 10
        print("CHANGE_TIME is too short",CHANGE_TIME)
    # print(CHANGE_TIME,delay,dur)
    delay_id = root.after(round(delay), choose_image)


def load_images():
    global dealed_imgs, last_win_size

    # 处理按钮字体
    style.configure("Custom.TButton", font=("宋体", button1.winfo_width()//10))

    # 获取窗口的当前大小
    window_width = right_frame.winfo_width()
    window_height = right_frame.winfo_height()

    if window_height < 5:
        return    

    opened_img = []
    for now in all_img:
        opened_img.append(Image.open("imgs/" + now))
    opt = []
    for img in opened_img:
        # 处理旋转
        exif = img._getexif()
        if exif:
            orientation = exif.get(0x0112)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

        # 计算新的图像大小
        src_width, src_height = img.size
        if window_height < window_width * (src_height / src_width):
            wid = window_height * (src_width / src_height)
            hei = window_height
        else:
            wid = window_width
            hei = window_width * (src_height / src_width)

        resized_image = img.resize((round(wid), round(hei)))
        opt.append(resized_image)
    dealed_imgs = opt.copy()
    print("Done")
    root.after_idle(lambda: show_image(dealed_imgs[0]))


def show_image(img):
    # 更新图像
    photo = ImageTk.PhotoImage(img)
    photo_label.config(image=photo)
    photo_label.image = photo
    photo_label.pack(fill=tk.BOTH, expand=True)


def update_button_padding(event=None):
    global delay_id, last_win_size
    # 获取窗口的当前大小
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    if last_win_size == [window_width, window_height]:
        return
    else:
        print(last_win_size, (window_width, window_height))
        last_win_size = [window_width, window_height]

    # 计算按钮的新的padx和pady值
    padx = window_width // 40
    pady = window_height // 10

    # 设置按钮的padx和pady值
    button1.grid(row=0, column=0, padx=padx, pady=pady, sticky="nsew")
    button2.grid(row=1, column=0, padx=padx, pady=pady, sticky="nsew")

    # 处理图片
    if delay_id is not None:
        root.after_cancel(delay_id)
    delay_id = root.after(200, load_images)


root = tk.Tk()
root.option_add("*TButton.Style", "TButton")  # 添加样式

delay_id = None

# 设置窗口大小和位置
root.geometry("1500x800")

# 创建左侧的Frame
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky=tk.NSEW)
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# 创建按钮1
style = ttk.Style()
style.configure("Custom.TButton", font=("宋体", 12))

button1 = ttk.Button(left_frame, text="Start", command=on_st_button_click, style="Custom.TButton")
button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# 创建按钮2
button2 = ttk.Button(left_frame, text="End", command=on_end_button_click, style="Custom.TButton")
button2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# 创建右侧的Frame
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, sticky=tk.NSEW)

# 加载图片
all_img = listdir("imgs")

# 创建一个Label用于显示图片
photo_label = tk.Label(right_frame, text="Preparing")

# 设置网格布局的列权重和uniform参数，使左右Frame严格平分界面宽度
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1, uniform="group1")
root.grid_columnconfigure(1, weight=3, uniform="group1")

# 绑定按钮的事件
button1.bind("<Button-1>", on_st_button_click)
button2.bind("<Button-1>", on_end_button_click)

# 绑定窗口大小变化事件
root.bind('<Configure>', update_button_padding)

# root.after_idle(lambda: show_image(dealed_imgs[0]))

# 在后台线程加载图片
thread = threading.Thread(target=load_images)
thread.daemon = True
thread.start()

# float
root.after_idle(show_floating_window)

root.mainloop()

if not DATA_ANALYTICS:
    exit()

import matplotlib.pyplot as plt
import numpy as np

 # 假设已有delay_arr数组

 # 计算平均值和标准差
average_delay = np.mean(delay_arr)
std_delay = np.std(delay_arr)

 # 定义筛选条件
threshold = 1.0  # 设置偏差阈值为1.0
filtered_delay_arr = [x for x in delay_arr if abs(x - average_delay) <= threshold * std_delay]

average_delay = np.mean(filtered_delay_arr)
 # 创建x轴数据
x = np.arange(len(filtered_delay_arr))

 # 绘制散点图
plt.scatter(x, filtered_delay_arr)

 # 在图中标注平均值
plt.axhline(y=average_delay, color='r', linestyle='--', label='Average Delay')
plt.legend()

 # 显示方差和标准差的数值
plt.text(0.05, 0.95, f"^2: {np.var(filtered_delay_arr):.2f}", transform=plt.gca().transAxes, ha='left', va='top')
plt.text(0.05, 0.9, f"sqrt: {np.std(filtered_delay_arr):.2f}", transform=plt.gca().transAxes, ha='left', va='top')
plt.text(0.05, 0.85, f"max_min: {np.max(filtered_delay_arr):.2f}_{np.min(filtered_delay_arr):.2f}", transform=plt.gca().transAxes, ha='left', va='top')

plt.show()

counts, bins, _=plt.hist(chosen[:chosen_i+1], bins=range(0,len(all_img)), align='left', rwidth=0.8)

 # 设置图表标题和轴标签
plt.title("Frequency of Data")
plt.xlabel("Data")
plt.xticks(range(0,len(all_img)+3))
plt.ylabel("Frequency")

 # 计算平均出现频次
average_frequency = np.mean(counts)
plt.axhline(y=average_frequency, color='r', linestyle='--', label='Average Frequency')

 # 显示方差和标准差的数值
plt.text(0.05, 0.95, f"^2: {np.var(counts):.2f}", transform=plt.gca().transAxes, ha='left', va='top')
plt.text(0.05, 0.9, f"sqrt: {np.std(counts):.2f}", transform=plt.gca().transAxes, ha='left', va='top')
plt.text(0.05, 0.85, f"max_min: {np.max(counts):.2f}_{np.min(counts):.2f}", transform=plt.gca().transAxes, ha='left', va='top')


 # 显示图表
plt.show()

