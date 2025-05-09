import tkinter as tk

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("便签应用")

        # 创建Canvas和Scrollbar，允许滚动查看多个便签
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # 创建一个Frame来容纳所有的便签
        self.notepad_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.notepad_frame, anchor="nw")

        # 按钮：每次点击会新建一个便签区域
        self.new_note_button = tk.Button(root, text="新建便签", command=self.create_note)
        self.new_note_button.pack(pady=10)

        # 绑定事件：更新Canvas的滚动区域
        self.notepad_frame.bind("<Configure>", self.update_scroll_region)

    def create_note(self):
        # 为每个便签创建一个新的Frame，里面放置一个Text小部件
        note_frame = tk.Frame(self.notepad_frame)
        note_frame.pack(pady=5, fill=tk.X)  # 新建的便签在垂直方向有一些间距

        # 创建Text小部件
        text_widget = tk.Text(note_frame, height=5, wrap=tk.WORD)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # 新建便签时，也可以自动插入一段默认文本
        text_widget.insert(tk.END, "请输入便签内容...")

        # 给每个Text区域添加滚动条
        scrollbar = tk.Scrollbar(note_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        # 添加删除按钮
        delete_button = tk.Button(note_frame, text="删除", command=lambda: self.delete_note(note_frame))
        delete_button.pack(pady=5)

    def update_scroll_region(self, event):
        # 更新Canvas的滚动区域
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def delete_note(self, note_frame):
        """删除指定的便签Frame"""
        note_frame.destroy()

def main():
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
