import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def set_up_main_ui(root):
    # ================================
    # 左侧 Public 标签区域
    # ================================
    public_container = ttk.Frame(root, bootstyle="secondary")
    public_container.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.8)

    public_canvas = ttk.Canvas(public_container)
    public_scrollbar = ttk.Scrollbar(public_container, orient=VERTICAL, command=public_canvas.yview)
    inside_public_frame = ttk.Frame(public_canvas)

    inside_public_frame.bind(
        "<Configure>",
        lambda e: public_canvas.configure(scrollregion=public_canvas.bbox("all"))
    )

    public_canvas.bind(
        "<Configure>",
        lambda e: public_canvas.itemconfig("public_window", width=e.width)
    )

    public_canvas.create_window((0, 0), window=inside_public_frame, anchor="nw", tags="public_window")
    public_canvas.configure(yscrollcommand=public_scrollbar.set)

    public_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    public_scrollbar.pack(side=RIGHT, fill=Y)

    public_label_counts = ttk.Label(inside_public_frame, text="共享tip数量 = 0", anchor="w", padding=5, bootstyle="info")
    public_label_counts.pack(fill=X, padx=5, pady=2)

    # ================================
    # 右侧 Private 标签区域
    # ================================
    private_container = ttk.Frame(root, bootstyle="info")
    private_container.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.8)

    private_canvas = ttk.Canvas(private_container)
    private_scrollbar = ttk.Scrollbar(private_container, orient=VERTICAL, command=private_canvas.yview)
    inside_private_frame = ttk.Frame(private_canvas)

    inside_private_frame.bind(
        "<Configure>",
        lambda e: private_canvas.configure(scrollregion=private_canvas.bbox("all"))
    )

    private_canvas.bind(
        "<Configure>",
        lambda e: private_canvas.itemconfig("private_window", width=e.width)
    )

    private_canvas.create_window((0, 0), window=inside_private_frame, anchor="nw", tags="private_window")
    private_canvas.configure(yscrollcommand=private_scrollbar.set)

    private_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    private_scrollbar.pack(side=RIGHT, fill=Y)


    private_label_counts = ttk.Label(inside_private_frame, 
                                    text="私人tip数量 = 0", 
                                    anchor="w", 
                                    padding=5, 
                                    bootstyle="warning"
                                    )

    private_label_counts.pack(fill=X, padx=5, pady=2)

    return inside_public_frame, inside_private_frame, public_label_counts, private_label_counts
