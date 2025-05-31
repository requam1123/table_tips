import datetime
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_new_note(root, inside_public_frame, inside_private_frame, update_label_counts,all_tips,save_tips,bind_right_click):
    top = ttk.Toplevel()
    top.title("新建标签")
    top.geometry("500x400")

    ttk.Label(top, text="标签组:").place(relx=0.1, rely=0.1)
    group_choose = ttk.Combobox(top, state="readonly", values=("公开", "私人"))
    group_choose.current(0)
    group_choose.place(relx=0.4, rely=0.1, width=100)

    # 时间区域
    ttk.Label(top, text="时间:").place(relx=0.1, rely=0.25)
    year_entry = ttk.Entry(top); year_entry.place(relx=0.25, rely=0.25, width=50)
    ttk.Label(top, text="年").place(relx=0.35, rely=0.25)
    month_entry = ttk.Entry(top); month_entry.place(relx=0.43, rely=0.25, width=35)
    ttk.Label(top, text="月").place(relx=0.51, rely=0.25)
    day_entry = ttk.Entry(top); day_entry.place(relx=0.57, rely=0.25, width=35)
    ttk.Label(top, text="日").place(relx=0.65, rely=0.25)
    hour_entry = ttk.Entry(top); hour_entry.place(relx=0.25, rely=0.33, width=35)
    ttk.Label(top, text="时").place(relx=0.33, rely=0.33)
    min_entry = ttk.Entry(top); min_entry.place(relx=0.39, rely=0.33, width=35)
    ttk.Label(top, text="分").place(relx=0.47, rely=0.33)

    ttk.Label(top, text="标题:").place(relx=0.1, rely=0.5)
    title_entry = ttk.Entry(top); title_entry.place(relx=0.4, rely=0.5, width=150)

    def is_valid_datetime():
        try:
            y = int(year_entry.get())
            m = int(month_entry.get())
            d = int(day_entry.get())
            H = int(hour_entry.get())
            M = int(min_entry.get())
            dt = datetime.datetime(y, m, d, H, M)
            return True, dt
        except Exception:
            return False, None

    def submit():
        title = title_entry.get().strip()
        if not title:
            messagebox.showwarning("提示", "标题不能为空")
            return

        valid, dt = is_valid_datetime()
        if not valid:
            messagebox.showerror("时间错误", "请输入合法的时间")
            return

        group = group_choose.get()
        text = f"{title}       |        ddl: {dt.strftime('%Y-%m-%d %H:%M')}"

        if group == "私人":
            label = ttk.Label(inside_private_frame, text=text, anchor="w", padding=5,
                              bootstyle="warning", borderwidth=1, relief="solid")
            label.pack(fill="x", padx=5, pady=2)
        else:
            label = ttk.Label(inside_public_frame, text=text, anchor="w", padding=5,
                              bootstyle="info", borderwidth=1, relief="solid")
            label.pack(fill="x", padx=5, pady=2)
        tip_data = {
            "title": title,
            "ddl": dt.strftime("%Y-%m-%d %H:%M"),
            "group": group,
            "cdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        bind_right_click(label, tip_data)
        
        all_tips.append(tip_data)
        save_tips()
        update_label_counts()
        top.destroy()

    ttk.Button(top, text="提交", command=submit).place(relx=0.3, rely=0.7, anchor="center")
    ttk.Button(top, text="取消", command=top.destroy).place(relx=0.7, rely=0.7, anchor="center")