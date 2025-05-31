from tkinter import messagebox
def delete_tip(label_widget,tip_data,all_tips,save_tips,update_label_counts):
    confirm = messagebox.askyesno("删除确认", "确定要删除这个tip吗？")
    if confirm :
        label_widget.destroy()
        if tip_data in all_tips:
            all_tips.remove(tip_data)
        save_tips()
        update_label_counts()