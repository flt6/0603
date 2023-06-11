import tkinter as tk

class FloatingWindow(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.overrideredirect(True)  # 去掉窗口边框
        self.attributes('-topmost', True)  # 窗口置顶

        # 获取屏幕大小
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 设置悬浮窗大小为屏幕高度的1/8
        window_height = screen_height // 8
        self.geometry(f'200x{window_height}+100+100')

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


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x300')

    # 创建一个按钮，点击按钮时显示悬浮窗口
    btn = tk.Button(root, text='显示悬浮窗口')
    btn.pack(pady=50)

    def show_floating_window():
        floating_window = FloatingWindow(root)
        floating_window.mainloop()

    btn.config(command=show_floating_window)

    root.mainloop()
