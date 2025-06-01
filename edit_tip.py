from tkinter import messagebox
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def edit_tip(inside_private_frame, inside_public_frame, label_widget, tip_data, all_tips, save_tips, update_label_counts, bind_right_click):
    top = ttk.Toplevel()
    top.title("编辑标签")
    top.geometry("500x400")

    # 标签组
    ttk.Label(top, text="标签组:").place(relx=0.1, rely=0.1)
    group_choose = ttk.Combobox(top, state="readonly", values=("公开", "私人"))
    group_choose.set(tip_data["group"])
    group_choose.place(relx=0.4, rely=0.1, relwidth=0.4)

    # 时间区域
    ddl_dt = datetime.datetime.strptime(tip_data["ddl"], "%Y-%m-%d %H:%M")
    ttk.Label(top, text="时间:").place(relx=0.1, rely=0.25)

    year_entry = ttk.Entry(top); year_entry.place(relx=0.25, rely=0.25, relwidth=0.12)
    ttk.Label(top, text="年").place(relx=0.38, rely=0.25)
    year_entry.insert(0, ddl_dt.year)

    month_entry = ttk.Entry(top); month_entry.place(relx=0.42, rely=0.25, relwidth=0.08)
    ttk.Label(top, text="月").place(relx=0.51, rely=0.25)
    month_entry.insert(0, ddl_dt.month)

    day_entry = ttk.Entry(top); day_entry.place(relx=0.55, rely=0.25, relwidth=0.08)
    ttk.Label(top, text="日").place(relx=0.64, rely=0.25)
    day_entry.insert(0, ddl_dt.day)

    hour_entry = ttk.Entry(top); hour_entry.place(relx=0.25, rely=0.33, relwidth=0.08)
    ttk.Label(top, text="时").place(relx=0.34, rely=0.33)
    hour_entry.insert(0, ddl_dt.hour)

    min_entry = ttk.Entry(top); min_entry.place(relx=0.38, rely=0.33, relwidth=0.08)
    ttk.Label(top, text="分").place(relx=0.47, rely=0.33)
    min_entry.insert(0, ddl_dt.minute)

    # 标题
    ttk.Label(top, text="标题:").place(relx=0.1, rely=0.5)
    title_entry = ttk.Entry(top)
    title_entry.insert(0, tip_data["title"])
    title_entry.place(relx=0.25, rely=0.5, relwidth=0.5)

    def is_valid_datetime():
        try:
            y = int(year_entry.get())
            m = int(month_entry.get())
            d = int(day_entry.get())
            H = int(hour_entry.get())
            M = int(min_entry.get())
            return True, datetime.datetime(y, m, d, H, M)
        except:
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
        new_text = f"{title}       |        ddl: {dt.strftime('%Y-%m-%d %H:%M')}"

        if group == tip_data["group"]:
            label_widget.config(text=new_text)
            bind_right_click(label_widget, tip_data)
        else:
            label_widget.destroy()
            label = ttk.Label(
                inside_private_frame if group == "私人" else inside_public_frame,
                text=new_text,
                anchor="w",
                padding=5,
                bootstyle="warning" if group == "私人" else "info",
                borderwidth=1,
                relief="solid"
            )
            label.pack(fill="x", padx=5, pady=2)
            bind_right_click(label, tip_data)

        # 更新数据
        tip_data["title"] = title
        tip_data["ddl"] = dt.strftime("%Y-%m-%d %H:%M")
        tip_data["group"] = group
        tip_data["cdate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        save_tips()
        update_label_counts()
        messagebox.showinfo("提示","编辑成功！")
        top.destroy()

    ttk.Button(top, text="提交", command=submit).place(relx=0.3, rely=0.7, anchor="center")
    ttk.Button(top, text="取消", command=top.destroy).place(relx=0.7, rely=0.7, anchor="center")