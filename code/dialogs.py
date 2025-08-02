import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
from tkinter import messagebox

class CreateTipDialog(ttk.Toplevel):
    def __init__(self,parent:ttk.Window):
        super().__init__(parent)
        self.title("新建tip")
        self.geometry("500x400")
        self.result = None

        ttk.Label(self, text="标签组:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.group_choose = ttk.Combobox(self, state="readonly", values=("公开", "私人"))
        self.group_choose.current(0)
        self.group_choose.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self, text="截止日期:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ddl_date = ttk.DateEntry(self, bootstyle="primary")
        self.ddl_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        ttk.Label(self, text="标题:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        submit_button = ttk.Button(button_frame, text="提交", command=self.submit, bootstyle="success")
        submit_button.pack(side=LEFT, padx=10)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=self.destroy, bootstyle="danger-outline")
        cancel_button.pack(side=LEFT, padx=10)

        # 让第二列可以伸展
        self.grid_columnconfigure(1, weight=1)

    def submit(self):
        """当用户点击提交按钮时调用。"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("输入错误", "标题不能为空！", parent=self)
            return

        group = self.group_choose.get()
        ddl_dt = self.ddl_date.entry.get()

        # 将结果打包成一个字典
        self.result = {
            "title": title,
            "ddl": ddl_dt,
            "group": group,
            "cdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.destroy() # 关闭自己

    def show(self):
        """显示窗口并等待它关闭，然后返回结果。"""
        # transient使窗口浮在父窗口之上
        self.transient(self.master)
        # grab_set使窗口变为模态，阻止与其他窗口交互
        self.grab_set()
        # wait_window会暂停执行，直到这个窗口被destroy
        self.wait_window(self)
        return self.result