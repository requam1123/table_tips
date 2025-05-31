import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
import datetime
from ui import set_up_main_ui
from create_tip import create_new_note
from delete_tip import delete_tip
import json

root = ttk.Window(title="桌面标签应用", themename="darkly")
root.geometry("800x600+200+200")

# 设置窗口图标
img = Image.open("p.jpg") 
icon = ImageTk.PhotoImage(img)
root.iconphoto(False, icon)

#数据保存模块
all_tips = []  # 用来保存所有 tip 的结构化数据
SAVE_FILE = "tips.json"
def save_tips():
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump(all_tips,f,ensure_ascii=False,indent=2)

inside_public_frame, inside_private_frame, public_label_counts, private_label_counts = set_up_main_ui(root)
#定义右键
def bind_right_click(label, tip):
    label.bind("<Button-3>", lambda e: on_right_click(e, label, tip))               # Windows / Linux
    label.bind("<Button-2>", lambda e: on_right_click(e, label, tip))               # 某些 macOS 右键为 Button-2
    label.bind("<Control-Button-1>", lambda e: on_right_click(e, label, tip))       # macOS 模拟右键

def on_right_click(event, label_widget, tip_data):
    menu = ttk.Menu(root, tearoff=0)
    menu.add_command(
        label="删除", 
        command=lambda: delete_tip(label_widget, tip_data, all_tips, save_tips, update_label_counts)
    )
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def load_tips():
    try:
        with open(SAVE_FILE,'r',encoding="utf-8") as f:
            tips = json.load(f)
    except FileNotFoundError:
        return

    for tip in tips:
        title = tip["title"]
        ddl = tip["ddl"]
        group = tip["group"]
        create_date = tip["cdate"]

        text = f"{title}       |        ddl: {ddl}"
        label = ttk.Label(
            inside_private_frame if group == "私人" else inside_public_frame,
            text=text,
            anchor="w",
            padding=5,
            bootstyle="warning" if group == "私人" else "info",
            borderwidth=1,
            relief="solid"
        )
        label.pack(fill=X, padx=5, pady=2)

        bind_right_click(label, tip)

        all_tips.append(tip)

    update_label_counts()
# 顶部状态栏

status = ttk.StringVar()
root_base_condition_label = ttk.Label(root, textvariable=status, anchor="w")
root_base_condition_label.place(relx=0, rely=0, relwidth=1.0, height=50)

def update_condition(event=None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    size = f"size: {root.winfo_width()}x{root.winfo_height()}"
    status.set(f"{now}   |   {size}")

def clk():
    update_condition()
    root.after(1000, clk)

root.bind("<Configure>", update_condition)
clk()

# ================================
# 标签数量统计函数
# ================================
def update_label_counts():
    public_count = len(inside_public_frame.winfo_children()) - 1
    private_count = len(inside_private_frame.winfo_children()) - 1
    public_label_counts.config(text=f"共享tip数量 = {public_count}")
    private_label_counts.config(text=f"私人tip数量 = {private_count}")

# 菜单功能栏
menubar = ttk.Menu(root)
file_menu = ttk.Menu(menubar, tearoff=1)
file_menu.add_command(
                    label="新建", 
                    command=lambda : create_new_note(root,
                                                     inside_private_frame,
                                                     inside_public_frame,
                                                     update_label_counts,
                                                     all_tips,
                                                     save_tips,
                                                     bind_right_click
                    )
)
menubar.add_cascade(label="文件", menu=file_menu)
root.config(menu=menubar)


1·11

# 启动主循环
load_tips()
root.mainloop()