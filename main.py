import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import shuffle
import pathlib
from enum import Enum
from time import time

CHANGE_TIME=80
IMG_DIR=pathlib.Path("imgs")
DBG=True

class Event(Enum):
    SHOW_IMG=1
    NEXT_IMG=2
    STOP=3
    ADD_IMG=4
    START=5
    SAVE_DATA=6

class Events:
    def __init__(self):
        self._front_ev = []
        self._back_ev = []
        self._global_ev=[]
        if DBG:
            import numpy as np
            self.delay=np.zeros((10000,),np.float16)
            self.delay_i=0
            self.add_event(2,Event.SAVE_DATA,at=time()+5)
    def add_event(self, recv:int ,event:Event, args:tuple=(), at=0):
        '''
        Add a new event

        @arg recv:
            0: Fronted event
            1: Backend event
            2: Global  event, will send at top.
        '''
        if recv==0:
            self._front_ev.append((event, args, at))
        elif recv==1:
            self._back_ev.append((event, args, at))
        elif recv == 2:
            self._global_ev.append((event, args, at, 0))
        else:
            raise ValueError("recv must be 0 or 1")
    def get_events(self, typ:int):
        sent=False
        tem=[]
        for eve,args,at,cnt in self._global_ev:
            if time()>at:
                if DBG and at!=0:
                    self.delay[self.delay_i]=time()-at
                if DBG and eve == Event.SAVE_DATA:
                    import numpy as np
                    np.save("data.npy",self.delay)
                    self.add_event(2,Event.SAVE_DATA,at=time()+5)
                    continue
                sent=True
                cnt+=1
                if cnt<=2:tem.append((eve, args, at, cnt))
                yield (eve,args)
            else:
                tem.append((eve, args, at, cnt))
        self._global_ev=tem
        
        tem=[]
        if typ==0:
            for eve,args,at in self._front_ev:
                if time()>at:
                    if DBG and at!=0:
                        self.delay[self.delay_i]=time()-at
                    sent=True
                    yield (eve,args)
                else:
                    tem.append((eve, args, at))
            self._front_ev=tem
        elif typ==1:
            for eve,args,at in self._back_ev:
                if time()>at:
                    if DBG and at!=0:
                        self.delay[self.delay_i]=time()-at
                    sent=True
                    yield (eve,args)
                else:
                    tem.append((eve, args, at))
            self._back_ev=tem
        else:
            raise ValueError("typ must be 0 or 1")
        if not sent:return []

class BackendApp:
    def __init__(self,events:Events):
        self.imgs:list[Image.Image] = []
        self.dealed_imgs_bk = []
        self.img_i = 0
        self._last_win_size=(-1,-1)
        self.events=events
        self.start=False
    
    def deal_events(self):
        for typ,args in self.events.get_events(1):
            if typ == Event.NEXT_IMG:
                if self.start:
                    self.choose_image()
            elif typ == Event.STOP:
                self.start=False
                img = self.imgs.pop(self.img_i)
                self.events.add_event(1,Event.ADD_IMG,args=(img,),at=time()+40*60)
            elif typ == Event.ADD_IMG:
                self.imgs.append(args[0])
            elif typ==Event.START:
                self.start=True

    def load_images(self,right_frame):
        # width and height must be get after window shadered.
        win_wid = right_frame.winfo_width()
        win_hei = right_frame.winfo_height()

        # Check if the window size had a big change.
        last_win_wid,last_win_hei = self._last_win_size
        if abs(last_win_wid-win_wid)+abs(last_win_hei-win_hei)<10:
            print("May not change size. Won't reload images")
            return
        else:
            self._last_win_size = (win_wid,win_hei)

        imgs:list[Image.Image]=[]
        for img_file in IMG_DIR.iterdir():
            imgs.append(Image.open(img_file))
        # deal images
        print("Loading images",end='')
        for img in imgs:
            print(".",end='',flush=True)
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
            if win_wid < win_hei * (src_height / src_width):
                wid = win_wid * (src_width / src_height)
                hei = win_wid
            else:
                wid = win_hei
                hei = win_hei * (src_height / src_width)

            resized_image = img.resize((round(wid), round(hei)))
            self.imgs.append(resized_image)
        print()
        shuffle(self.imgs)
        self.events.add_event(0,Event.SHOW_IMG,(self.imgs[0],))
        
    def choose_image(self):
        print(self.img_i,len(self.imgs))
        if self.img_i>=len(self.imgs):
            self.img_i=0
            shuffle(self.imgs)
            print("update")
        self.events.add_event(0, Event.SHOW_IMG, args=(self.imgs[self.img_i],))
        self.events.add_event(1, Event.NEXT_IMG, at=time()+CHANGE_TIME/1000)
        self.img_i+=1


class FrontendApp:
    def __init__(self, root:tk.Tk,backend:BackendApp,events:Events):
        self.backend=backend
        self.events=events
        
        self.root = root
        self.root.geometry("1500x800")
        self._init_styles()

        self.left_frame = tk.Frame(root)
        self.right_frame = tk.Frame(root)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=3, uniform="group1")

        self._init_buttons()
        self.right_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.img_label = tk.Label(self.right_frame, text="Preparing",font=("宋体",100))
        self.img_label.pack(fill=tk.BOTH, expand=True)

        self.root.bind('<Configure>', self.update_button_padding)

        self.start_change=False
        self.delay_id=None


    def _init_styles(self):
        style = ttk.Style()
        style.configure("Custom.TButton", font=("宋体", 12))

    def _init_buttons(self):
        self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.button1 = ttk.Button(self.left_frame, text="Start", style="Custom.TButton")
        self.button1.bind("<Button-1>", self.on_st_button_click)
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button2 = ttk.Button(self.left_frame, text="End", style="Custom.TButton",)
        self.button2.bind("<Button-1>", self.on_end_button_click)
        self.button2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def deal_events(self):
        for typ,args in self.events.get_events(0):
            if typ == Event.SHOW_IMG:
                self.show_image(*args)
            elif typ == Event.STOP:
                self.start_change=False
    
    def on_st_button_click(self, event):
        if self.start_change:
            messagebox.showwarning("循环已启动","循环已启动，请勿反复点击此按钮。")
            return
        self.backend.choose_image()
        self.events.add_event(1,Event.START)
        self.start_change=True

    def on_end_button_click(self, event):
        if not self.start_change:
            return
        self.start_change=False
        print("END EVENT")
        self.events.add_event(2,Event.STOP)

    def show_image(self, img:Image.Image):
        tkimg=ImageTk.PhotoImage(img)
        self.img_label.config(image=tkimg)
        self.img_label.photo=tkimg
        self.img_label.pack(fill=tk.BOTH, expand=True)

    def update_button_padding(self, event):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        padx = window_width // 40
        pady = window_height // 10

        self.button1.grid(row=0, column=0, padx=padx, pady=pady, sticky="nsew")
        self.button2.grid(row=1, column=0, padx=padx, pady=pady, sticky="nsew")

        if self.start_change:
            # Stop all exents and reset.
            # After moving the window most objects will be changed.
            self.img_label.config(image=None)
            self.start_change = False
            self.root.after_cancel(self.delay_id)
            self.delay_id=None
            self.events.add_event(2,Event.STOP)
        if self.delay_id is not None:
            # If the window is still moving, do not load images.
            self.root.after_cancel(self.delay_id)
        # After the window stopped changing.
        self.delay_id = self.root.after(200, self.backend.load_images,self.right_frame)


if __name__ == "__main__":
    root = tk.Tk()
    eve=Events()
    backend = BackendApp(eve)
    frontend = FrontendApp(root,backend,eve)
    while True:
        root.update()
        frontend.deal_events()
        backend.deal_events()
