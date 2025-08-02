import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import datetime
from PIL import Image, ImageTk
from dialogs import CreateTipDialog
from tkinter import messagebox

# 稍后我们会在这里导入你的其他模块，比如 dialogs.py

class TipApp:
    """
    桌面标签应用的主类。
    """
    def __init__(self, root:ttk.Window):
        # --- 1. 初始化核心属性 ---
        self.root = root
        self.all_tips = []
        self.SAVE_FILE = "tips.json"
        self.BACKGROUND_IMG = "src/background.jpg"

        # --- 2. 配置主窗口 ---
        self.root.title("桌面标签应用 (类版本)")
        self.root.geometry("800x600+200+200")
        
        # 设置窗口图标
        try:
            img = Image.open(self.BACKGROUND_IMG)
            icon = ImageTk.PhotoImage(img)
            self.root.iconphoto(False, icon)
        except FileNotFoundError:
            print(f"警告: 图标文件未找到 {self.BACKGROUND_IMG}")

        # --- 3. 创建UI界面 ---
        self.setup_ui()
        
        # --- 4. 创建菜单 (目前是占位) ---
        self.create_menu()

        self.update_status()
        


        self.load_tips()


    def setup_ui(self):
        """负责创建主界面的所有控件。"""

        """the main part"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH,expand=True)

        """the top controller , show the time and size"""
        self.status = ttk.StringVar()
        status_bar = ttk.Label(main_frame,textvariable=self.status,anchor='w', padding=(10, 5))
        status_bar.place(relx=0, rely=0, relwidth=1.0, height=50)
        self.root.bind("<Configure>",self.update_status)

        """left part"""
        public_container = ttk.Frame(main_frame, bootstyle="secondary")
        public_container.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.8)

        public_canvas = ttk.Canvas(public_container)
        public_scrollbar = ttk.Scrollbar(public_container, orient=VERTICAL, command=public_canvas.yview)
        self.inside_public_frame = ttk.Frame(public_canvas)

        self.inside_public_frame.bind(
            "<Configure>",
            lambda e: public_canvas.configure(scrollregion=public_canvas.bbox("all"))
        )

        public_canvas.bind(
            "<Configure>",
            lambda e: public_canvas.itemconfig("public_window", width=e.width)
        )

        public_canvas.create_window((0, 0), window=self.inside_public_frame, anchor="nw", tags="public_window")
        public_canvas.configure(yscrollcommand=public_scrollbar.set)

        public_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        public_scrollbar.pack(side=RIGHT, fill=Y)

        self.public_label_counts = ttk.Label(self.inside_public_frame, 
                                        text="共享tip", 
                                        anchor="w", 
                                        padding=5, 
                                        bootstyle="info"
        )
        self.public_label_counts.pack(fill=X, padx=5, pady=2)


        """the right part"""
        private_container = ttk.Frame(main_frame, bootstyle="info")
        private_container.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.8)

        private_canvas = ttk.Canvas(private_container)
        private_scrollbar = ttk.Scrollbar(private_container, orient=VERTICAL, command=private_canvas.yview)
        self.inside_private_frame = ttk.Frame(private_canvas)

        self.inside_private_frame.bind(
            "<Configure>",
            lambda e: private_canvas.configure(scrollregion=private_canvas.bbox("all"))
        )

        private_canvas.bind(
            "<Configure>",
            lambda e: private_canvas.itemconfig("private_window", width=e.width)
        )

        private_canvas.create_window((0, 0), window=self.inside_private_frame, anchor="nw", tags="private_window")
        private_canvas.configure(yscrollcommand=private_scrollbar.set)

        private_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        private_scrollbar.pack(side=RIGHT, fill=Y)

        self.private_label_counts = ttk.Label(self.inside_private_frame, 
                                        text="私人tip", 
                                        anchor="w", 
                                        padding=5, 
                                        bootstyle="warning"
                                        )

        self.private_label_counts.pack(fill=X, padx=5, pady=2)



    def update_status(self,event=None):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        size = f"size: {self.root.winfo_width()}x{self.root.winfo_height()}"
        self.status.set(f"{now}   |   {size}")
        self.root.after(1000,self.update_status)

    def update_label_counts(self):
        public_count = sum(1 for tip in self.all_tips if tip['group'] == '公开')
        private_count = sum(1 for tip in self.all_tips if tip['group'] == '私人')
        self.public_label_counts.config(text=f"共享tip数量 = {public_count}")
        self.private_label_counts.config(text=f"私人tip数量 = {private_count}")
    
    def create_menu(self):
        """负责创建顶部的菜单栏。"""
        
        menubar = ttk.Menu(self.root)
        file_menu = ttk.Menu(menubar,tearoff=0)
        file_menu.add_command(label="新建",command=self.create_new_tip)

        menubar.add_cascade(label="文件", menu=file_menu)
        self.root.config(menu=menubar)

    def create_new_tip(self):
        dialog = CreateTipDialog(self.root)
        new_tip = dialog.show()

        if new_tip :
            self.all_tips.append(new_tip)
            self.add_new_to_tip(new_tip)
            self.save_tips()
            self.update_label_counts()

    def add_new_to_tip(self , new_tip:dict):
        """将单个便签数据添加到UI界面上"""
        text = f"{new_tip['title']}      |      ddl: {new_tip['ddl']}"
        group = new_tip['group']
        
        parent_frame = self.inside_private_frame if group == "私人" else self.inside_public_frame
        bootstyle = "warning" if group == "私人" else "info"

        label = ttk.Label(
            parent_frame,
            text=text,
            anchor="w",
            padding=5,
            bootstyle=bootstyle,
            borderwidth=1,
            relief="solid"
        )
        label.pack(fill=X, padx=5, pady=2)
        self._bind_right_click(label, new_tip)


    def save_tips(self):
        try:
            with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.all_tips, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存失败: {e}")

    def load_tips(self):
        try:
            with open(self.SAVE_FILE, 'r', encoding="utf-8") as f:
                tips_from_file = json.load(f)
            self.all_tips = tips_from_file
            
            # 清理旧的UI
            for widget in self.inside_public_frame.winfo_children():
                if widget != self.public_label_counts: widget.destroy()
            for widget in self.inside_private_frame.winfo_children():
                if widget != self.private_label_counts: widget.destroy()

            # 创建新的UI
            for tip in self.all_tips:
                self.add_new_to_tip(tip)
            
            self.update_label_counts()

        except (FileNotFoundError, json.JSONDecodeError):
            self.all_tips = []
    

    def _bind_right_click(self, label: ttk.Label, tip_data: dict):
        """为标签绑定右键删除事件"""
        menu = ttk.Menu(self.root, tearoff=0)
        menu.add_command(label="删除", command=lambda: self.delete_tip(label, tip_data))
        
        def on_right_click(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        label.bind("<Button-3>", on_right_click)
        label.bind("<Button-2>", on_right_click)

    def delete_tip(self, label_widget: ttk.Label, tip_data: dict):
        """删除一个便签（数据和UI）"""
        if messagebox.askyesno("确认删除", f"确定要删除便签 '{tip_data['title']}' 吗?", parent=self.root):
            if tip_data in self.all_tips:
                self.all_tips.remove(tip_data)
            
            label_widget.destroy()
            self.save_tips()
            self.update_label_counts()

# ==================================
# 程序主入口
# ==================================
if __name__ == "__main__":
    # 1. 创建主窗口实例
    window = ttk.Window(themename="darkly")
    
    # 2. 实例化我们的应用类，并将主窗口传入
    app = TipApp(window)
    
    # 3. 启动Tkinter的主事件循环
    window.mainloop()