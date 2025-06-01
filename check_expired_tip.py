import datetime
import tkinter.font as tkfont

def check_expired_tips(tip):
    ddl = datetime.datetime.strptime(tip["ddl"], "%Y-%m-%d %H:%M")
    now = datetime.datetime.now()
    if ddl < now :
        title = f"{tip["title"]} (已过期)"
        text = f"{title}       |        ddl: {tip["ddl"]}"
        font = tkfont.Font(family="Helvetica",  slant="italic", overstrike=1)
        tip["label"].config(text = text,bootstyle = "danger",font = font)
