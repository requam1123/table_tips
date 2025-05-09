import tkinter as tk
import pathlib as pl
import top_level as tl
from tkinter import messagebox


root = tk.Tk()
root.title("tips")
root.geometry("1200x1000-300+300")
root["background"] = "#ffffff"

p = pl.Path("node.txt")
font_16 = ("宋体",16)
font_24 = ("宋体",24)


canva = tk.Canvas(root,bg="grey")
canva.place(relx=0,rely=0,height=800,width=1200)

scr = tk.Scrollbar(root,orient=tk.VERTICAL,command=canva.yview)
scr.place(relx=1,rely=0,height=800,width=20)
canva.config(yscrollcommand=scr.set)

note_frame = tk.Frame(canva,bg="black",width=1200,height=800)
canva.create_window((0,0),window=note_frame,anchor="nw")

button_build = tk.Button(note_frame,text="新建",font=font_16,relief=tk.FLAT,fg="black",bg="grey")
button_build.place(x=320,y=450,height=50,width=150)


root.mainloop()