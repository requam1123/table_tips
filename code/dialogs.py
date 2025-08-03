import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
from tkinter import messagebox
import json
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


class TranslationServiceDialog(ttk.Toplevel):
    """一个包含输入、输出和历史记录的完整翻译工具对话框。"""
    HISTORY_FILE = 'translation_history.json'

    def __init__(self, parent):
        super().__init__(parent)
        self.title("翻译工具")
        self.geometry("700x550")

        self.history_data = self._load_history()

        # --- 主容器 ---
        main_pane = ttk.PanedWindow(self, orient=VERTICAL)
        main_pane.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- 翻译区域 ---
        translate_frame = ttk.Frame(main_pane, padding=10)
        main_pane.add(translate_frame, weight=3)

        # --- 历史记录区域 ---
        history_frame = ttk.Labelframe(main_pane, text="历史记录", padding=10)
        main_pane.add(history_frame, weight=2)
        
        # --- 翻译区域的内部布局 ---
        # 语言选择
        lang_frame = ttk.Frame(translate_frame)
        lang_frame.pack(fill=X, pady=5)
        ttk.Label(lang_frame, text="从:").pack(side=LEFT, padx=(0, 5))
        self.from_lang = ttk.Combobox(lang_frame, values=['auto', 'zh', 'en', 'jp', 'kor'], width=8)
        self.from_lang.set('auto')
        self.from_lang.pack(side=LEFT)

        ttk.Label(lang_frame, text="到:").pack(side=LEFT, padx=(20, 5))
        self.to_lang = ttk.Combobox(lang_frame, values=['en', 'zh', 'jp', 'kor'], width=8)
        self.to_lang.set('en')
        self.to_lang.pack(side=LEFT)

        # 输入框
        ttk.Label(translate_frame, text="输入内容:").pack(anchor="w", pady=(10, 0))
        self.source_text = ttk.Text(translate_frame, height=5, wrap="word")
        self.source_text.pack(fill=BOTH, expand=True, pady=5)
        
        # 翻译按钮
        translate_button = ttk.Button(translate_frame, text="翻  译", command=self._on_translate)
        translate_button.pack(pady=5)

        # 输出框
        ttk.Label(translate_frame, text="翻译结果:").pack(anchor="w", pady=(10, 0))
        self.result_text = ttk.Text(translate_frame, height=5, wrap="word", state="disabled")
        self.result_text.pack(fill=BOTH, expand=True, pady=5)

        # --- 历史记录区域的内部布局 ---
        cols = ('原文', '译文')
        self.history_tree = ttk.Treeview(history_frame, columns=cols, show='headings', height=5)
        for col in cols:
            self.history_tree.heading(col, text=col)
        self.history_tree.column('原文', width=250)
        self.history_tree.column('译文', width=250)
        self.history_tree.pack(fill=BOTH, expand=True)
        self.history_tree.bind('<<TreeviewSelect>>', self._on_history_select)

        # 加载历史记录到UI
        self._populate_history_tree()

    def _on_translate(self):
        """执行翻译"""
        from baidu_api import translate_text # 局部导入
        
        query = self.source_text.get("1.0", END).strip()
        if not query:
            return

        from_lang = self.from_lang.get()
        to_lang = self.to_lang.get()

        result = translate_text(query, to_lang, from_lang)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", END)
        if result:
            self.result_text.insert("1.0", result)
            # 添加到历史记录
            self._add_to_history(query, result)
        else:
            self.result_text.insert("1.0", "翻译失败，请检查网络或API设置。")
        self.result_text.config(state="disabled")

    def _add_to_history(self, source, translation):
        """添加新条目到历史记录并保存"""
        record = {'source': source, 'translation': translation}
        # 避免重复添加
        if record not in self.history_data:
            self.history_data.insert(0, record) # 插入到最前面
            self.history_data = self.history_data[:50] # 最多保存50条
            self._save_history()
            self._populate_history_tree()
    
    def _populate_history_tree(self):
        """用数据填充历史记录的Treeview"""
        # 清空现有内容
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        # 插入新内容
        for item in self.history_data:
            self.history_tree.insert('', END, values=(item['source'], item['translation']))

    def _on_history_select(self, event):
        """点击历史记录时，将内容填回输入输出框"""
        for selected_item in self.history_tree.selection():
            item = self.history_tree.item(selected_item)
            source, translation = item['values']
            
            self.source_text.delete("1.0", END)
            self.source_text.insert("1.0", source)
            
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", END)
            self.result_text.insert("1.0", translation)
            self.result_text.config(state="disabled")
            break # 只处理第一个选中的

    def _load_history(self):
        try:
            with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_history(self):
        try:
            with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"无法保存历史记录: {e}")