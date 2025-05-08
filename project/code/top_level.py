import tkinter as tk
from tkinter import ttk


font = ("宋体", 16)

def build(callback):
    top = tk.Toplevel()
    top.title("新建")
    top.geometry("500x300-300+300")
    
    
    def top_close():
        top.destroy()

    def top_confirm():
        final_item  = entry_item.get() +" "+  month_choose.get() + " "+ dates_choose.get()
        callback(final_item)
        top_close()
        

    entry_item = tk.Entry(top,font=font,fg="black")
    entry_item.place(x=50,y=50,width=200,height=50)

    months = [f"{i}月" for i in range(1,13)]
    month_choose = ttk.Combobox(top,font=font,values=months)
    month_choose.place(x=300,y=50,width=80,height=50)
    month_choose.current(0)

    dates = [f"{i}号" for i in range(1,32)]
    dates_choose = ttk.Combobox(top,font=font,values=dates)
    dates_choose.place(x=400,y=50,width=80,height=50)
    dates_choose.current(0)
    

    button_top_quit = tk.Button(top,text="close",font=font,relief=tk.FLAT,fg="black",bg="grey")
    button_top_quit.place(x=150,y=200,height=50,width=80)
    button_top_quit.config(command=top_close)

    button_top_confirm = tk.Button(top,text="确定",font=font,relief=tk.FLAT,fg="black",bg="grey")
    button_top_confirm.place(x=370,y=200,height=50,width=80)
    button_top_confirm.config(command=top_confirm)



    



