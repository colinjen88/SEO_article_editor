# -*- coding: utf-8 -*-
"""視覺化 SEO 文章編輯器"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os, json, webbrowser, re
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except Exception:
    HAS_BS4 = False
from datetime import datetime

try:
    import ttkbootstrap as tb
    HAS_TTK = True
except: HAS_TTK = False

BASE = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(BASE, "output")
ARTICLE_NUMBER_FILE = os.path.join(BASE, "article_number.txt")

def _read_app_version() -> str:
    """從 src/__init__.py 讀取 __version__，避免手動同步。
    若讀取失敗則回傳 'dev'。
    """
    try:
        init_path = os.path.join(BASE, "src", "__init__.py")
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
        return m.group(1) if m else "dev"
    except Exception:
        return "dev"

def get_article_number():
    if not os.path.exists(ARTICLE_NUMBER_FILE):
        with open(ARTICLE_NUMBER_FILE, "w", encoding="utf-8") as f:
            f.write("1")
        return 1
    with open(ARTICLE_NUMBER_FILE, "r", encoding="utf-8") as f:
        try:
            num = int(f.read().strip())
        except:
            num = 1
    return num

def set_article_number(num):
    with open(ARTICLE_NUMBER_FILE, "w", encoding="utf-8") as f:
        f.write(str(num))

# --- 簡易 HTML 高亮輔助 ---
TAG_PATTERN = re.compile(r"<[^>]+>")
ATTR_PATTERN = re.compile(r"\b([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?=\s*=)")
STRING_PATTERN = re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"")

def _index_from_offset(content: str, offset: int) -> str:
    """將字元 offset 轉成 Tk Text 索引（line.column）。"""
    line = content.count("\n", 0, offset) + 1
    prev_nl = content.rfind("\n", 0, offset)
    col = offset if prev_nl == -1 else offset - (prev_nl + 1)
    return f"{line}.{col}"

class H3Block:
    def __init__(self, p, oc, od):
        self.f = ttk.Frame(p, relief=tk.GROOVE, borderwidth=1)
        self.f.pack(fill=tk.X, padx=10, pady=3)
        ttk.Label(self.f, text="H3:", font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        self.h3 = tk.Entry(self.f, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10)); self.h3.pack(fill=tk.X, padx=5, pady=(0,3)); self.h3.bind("<KeyRelease>", lambda e: oc())
        ttk.Label(self.f, text="內容:", font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        self.ct = tk.Text(self.f, height=4, wrap=tk.WORD, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 9)); self.ct.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,3)); self.ct.bind("<KeyRelease>", lambda e: oc())
        ttk.Button(self.f, text="刪除H3", command=lambda: [self.f.destroy(), od(self)]).pack(anchor=tk.E, padx=5, pady=3)
    def get_h3(self): return self.h3.get().strip()
    def get_ct(self): return self.ct.get("1.0", tk.END).strip()
    def set_h3(self, t): self.h3.delete(0, tk.END); self.h3.insert(0, t)
    def set_ct(self, t): self.ct.delete("1.0", tk.END); self.ct.insert("1.0", t)
    def to_dict(self): return {"h3": self.get_h3(), "content": self.get_ct()}

class SecBlock:
    def __init__(self, p, oc, od):
        self.oc = oc
        self.h3s = []
        self.is_html = True  # 段落內容預設為 HTML 模式
        self.f = ttk.LabelFrame(p, text="段落", padding=10)
        self.f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.f, text="H2:").pack(anchor=tk.W)
        self.h2 = tk.Entry(self.f, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10)); self.h2.pack(fill=tk.X, pady=(0,5)); self.h2.bind("<KeyRelease>", lambda e: oc())

        ct_label_frame = ttk.Frame(self.f)
        ct_label_frame.pack(fill=tk.X, anchor=tk.W)
        ttk.Label(ct_label_frame, text="內容:").pack(side=tk.LEFT)
        # 簡易語法提示（HTML 模式時高亮可能常用標籤）
        tip = (
            "可用標籤: <p> <br> <table> <thead> <tbody> <tr> <th> <td> <ul> <li> <strong> <em>"
        )
        ttk.Label(ct_label_frame, text=tip, font=("Arial", 8), foreground="orange").pack(side=tk.LEFT, padx=5)

        self.ct = tk.Text(self.f, height=6, wrap=tk.WORD, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 9))
        self.ct.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        # 綁定更新與高亮
        self._init_highlight(self.ct)
        def _on_key(_):
            self._highlight_if_html()
            oc()
        self.ct.bind("<KeyRelease>", _on_key)

        self.h3_container = ttk.Frame(self.f)
        self.h3_container.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(self.f)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="+ H3", command=self.add_h3).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="刪除段落", command=lambda: [self.f.destroy(), od(self)]).pack(side=tk.RIGHT)
    
    def add_h3(self):
        h3 = H3Block(self.h3_container, self.oc, lambda x: [self.h3s.remove(x), self.oc()])
        self.h3s.append(h3)
        self.oc()
    
    def get_h2(self): return self.h2.get().strip()
    def get_ct(self): return self.ct.get("1.0", tk.END).strip()
    def set_h2(self, t): self.h2.delete(0, tk.END); self.h2.insert(0, t)
    def set_ct(self, t): self.ct.delete("1.0", tk.END); self.ct.insert("1.0", t)
    def to_dict(self): return {"h2": self.get_h2(), "content": self.get_ct(), "h3s": [h.to_dict() for h in self.h3s]}
    # --- 簡易 HTML 高亮 ---
    def _init_highlight(self, tw: tk.Text):
        try:
            tw.tag_config("html-tag", foreground="#0066cc")
            tw.tag_config("html-attr", foreground="#995500")
            tw.tag_config("html-string", foreground="#2a7b2e")
        except Exception:
            pass
    def _highlight_if_html(self):
        if not self.is_html:
            return
        tw = self.ct
        try:
            content = tw.get("1.0", tk.END)
            tw.tag_remove("html-tag", "1.0", tk.END)
            tw.tag_remove("html-attr", "1.0", tk.END)
            tw.tag_remove("html-string", "1.0", tk.END)
            for m in TAG_PATTERN.finditer(content):
                s = _index_from_offset(content, m.start())
                e = _index_from_offset(content, m.end())
                tw.tag_add("html-tag", s, e)
                # 標籤內再標示屬性與字串
                inner = content[m.start():m.end()]
                inner_base = m.start()
                for sm in ATTR_PATTERN.finditer(inner):
                    ss = _index_from_offset(content, inner_base + sm.start(1))
                    se = _index_from_offset(content, inner_base + sm.end(1))
                    tw.tag_add("html-attr", ss, se)
                for q in STRING_PATTERN.finditer(inner):
                    qs = _index_from_offset(content, inner_base + q.start())
                    qe = _index_from_offset(content, inner_base + q.end())
                    tw.tag_add("html-string", qs, qe)
        except Exception:
            pass

class FaqBlock:
    def __init__(self, p, oc, od):
        self.oc = oc
        self.is_html = tk.BooleanVar(value=False)  # 預設為純文字模式
        self.f = ttk.LabelFrame(p, text="QA", padding=10)
        self.f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.f, text="問題:").pack(anchor=tk.W)
        self.q = tk.Entry(self.f, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10)); self.q.pack(fill=tk.X, pady=(0,5)); self.q.bind("<KeyRelease>", lambda e: oc())
        
        a_label_frame = ttk.Frame(self.f)
        a_label_frame.pack(fill=tk.X, anchor=tk.W)
        ttk.Label(a_label_frame, text="答案:").pack(side=tk.LEFT)
        ttk.Checkbutton(a_label_frame, text="HTML 模式", variable=self.is_html, command=self._toggle_html).pack(side=tk.LEFT, padx=5)
        ttk.Label(a_label_frame, text="可用標籤: <p> <br> <strong> <em> <ul> <li>", font=("Arial", 8), foreground="orange").pack(side=tk.LEFT, padx=5)
        
        self.a = tk.Text(self.f, height=4, wrap=tk.WORD, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 9))
        self.a.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        self._init_highlight(self.a)
        def _on_key(_):
            if self.is_html.get():
                self._highlight()
            oc()
        self.a.bind("<KeyRelease>", _on_key)
        ttk.Button(self.f, text="刪除", command=lambda: [self.f.destroy(), od(self)]).pack(anchor=tk.E)
    
    def _toggle_html(self):
        if self.is_html.get():
            self.a.config(font=("Consolas", 9))
            self._highlight()
        else:
            self.a.config(font=("Microsoft JhengHei", 10))
        self.oc()
    
    def get_q(self): return self.q.get().strip()
    def get_a(self): return self.a.get("1.0", tk.END).strip()
    def get_is_html(self): return self.is_html.get()
    def set_q(self, t): self.q.delete(0, tk.END); self.q.insert(0, t)
    def set_a(self, t): self.a.delete("1.0", tk.END); self.a.insert("1.0", t)
    def set_is_html(self, v): self.is_html.set(v); self._toggle_html()
    def to_dict(self): return {"question": self.get_q(), "answer": self.get_a(), "is_html": self.get_is_html()}
    # --- 簡易 HTML 高亮 ---
    def _init_highlight(self, tw: tk.Text):
        try:
            tw.tag_config("html-tag", foreground="#0066cc")
            tw.tag_config("html-attr", foreground="#995500")
            tw.tag_config("html-string", foreground="#2a7b2e")
        except Exception:
            pass
    def _highlight(self):
        tw = self.a
        try:
            content = tw.get("1.0", tk.END)
            tw.tag_remove("html-tag", "1.0", tk.END)
            tw.tag_remove("html-attr", "1.0", tk.END)
            tw.tag_remove("html-string", "1.0", tk.END)
            for m in TAG_PATTERN.finditer(content):
                s = _index_from_offset(content, m.start())
                e = _index_from_offset(content, m.end())
                tw.tag_add("html-tag", s, e)
                inner = content[m.start():m.end()]
                inner_base = m.start()
                for sm in ATTR_PATTERN.finditer(inner):
                    ss = _index_from_offset(content, inner_base + sm.start(1))
                    se = _index_from_offset(content, inner_base + sm.end(1))
                    tw.tag_add("html-attr", ss, se)
                for q in STRING_PATTERN.finditer(inner):
                    qs = _index_from_offset(content, inner_base + q.start())
                    qe = _index_from_offset(content, inner_base + q.end())
                    tw.tag_add("html-string", qs, qe)
        except Exception:
            pass

class Editor:
    def __init__(self, root):
        self.root = root; self.root.title("SEO 文章編輯器"); self.root.geometry("1400x900")
        self.app_version = _read_app_version()
        
        # 立即覆蓋 ttkbootstrap 主題顏色
        bg_color = "#2c4c52"
        try:
            self.root.configure(bg=bg_color)
            style = ttk.Style()
            # 修改主題的核心顏色
            style.theme_settings('darkly', {
                'TFrame': {'configure': {'background': bg_color}},
                'TLabelframe': {'configure': {'background': bg_color, 'bordercolor': bg_color}},
                'TLabelframe.Label': {'configure': {'background': bg_color}},
                'TLabel': {'configure': {'background': bg_color}},
                'TNotebook': {'configure': {'background': bg_color, 'bordercolor': bg_color}},
                'TNotebook.Tab': {'configure': {'background': bg_color}},
                'TPanedwindow': {'configure': {'background': bg_color}},
            })
        except Exception as e:
            print(f"Theme override error: {e}")
        
        self.cf = None; self.mod = False; self.secs = []; self.faqs = []
        self.root.protocol("WM_DELETE_WINDOW", self._cls); self._ui()

    def _get_style_html(self, fallback_minimal: bool = False):
        """集中取得 <style> 或 <link> 標籤（含 fallback）。

        來源優先順序：
        1. 使用者編輯器中的 CSS (`css_editor`) 內容
        2. 若模式為 external 且有輸入網址，使用 <link>
        3. 若無編輯器內容則使用 templates/common.css 的內容（若存在）
        4. 若檔案不存在則自動建立並寫入預設 CSS，再載入

        參數 fallback_minimal=True 時，僅回傳一組基礎排版（供極簡預覽或錯誤降級）。
        """
        css_mode = getattr(self, 'css_mode', tk.StringVar(value="inline"))
        css_link = getattr(self, 'css_link_entry', None)

        # 取得編輯器內文字
        editor_css = self.css_editor.get("1.0", tk.END).strip() if hasattr(self, 'css_editor') else ""

        if fallback_minimal:
            base_css = (
                ".seo-article-content {font-family: 'Noto Sans TC', sans-serif; line-height:1.7; color:#343a40;}"
                ".seo-article-content h1 {font-size:2.2em; text-align:center; color:#b08d57;}"
            )
            return f"<style>{base_css}</style>"

        # 如果編輯器是空的，嘗試讀取 templates/common.css；若不存在則用 templates/default_common.css 建立
        if not editor_css:
            tpl_dir = os.path.join(BASE, "templates")
            tpl_path = os.path.join(tpl_dir, "common.css")
            default_path = os.path.join(tpl_dir, "default_common.css")
            if os.path.exists(tpl_path):
                try:
                    with open(tpl_path, "r", encoding="utf-8") as f:
                        editor_css = f.read().strip()
                except Exception:
                    editor_css = ""
            else:
                # 嘗試讀取 default_common.css，若存在則複製為 common.css
                try:
                    os.makedirs(tpl_dir, exist_ok=True)
                    if os.path.exists(default_path):
                        with open(default_path, "r", encoding="utf-8") as f:
                            default_css = f.read().strip()
                        # 建立 common.css
                        with open(tpl_path, "w", encoding="utf-8") as wf:
                            wf.write(default_css)
                        editor_css = default_css
                    else:
                        # default_common.css 不存在，使用極簡 fallback（不寫入檔案）
                        editor_css = "body{font-family:'Noto Sans TC',sans-serif;line-height:1.7;color:#343a40;} .seo-article-content{max-width:960px;margin:0 auto;padding:20px;}"
                except Exception:
                    editor_css = "body{font-family:'Noto Sans TC',sans-serif;line-height:1.7;color:#343a40;} .seo-article-content{max-width:960px;margin:0 auto;padding:20px;}"

        # external 模式
        if css_mode.get() == "external" and css_link:
            external_css = css_link.get().strip()
            if external_css:
                return f'<link rel="stylesheet" href="{external_css}">'  # 不加換行，交由呼叫端決定格式
        # inline 模式或未提供 external URL
        return f"<style>\n{editor_css}\n</style>"

    # --- HTML 格式化 ---
    def _format_html_string(self, s: str) -> str:
        if not isinstance(s, str) or not s.strip():
            return s
        if HAS_BS4:
            try:
                soup = BeautifulSoup(s, 'html.parser')
                return soup.prettify()
            except Exception:
                pass
        # 簡易 fallback：以標籤切分並縮排
        tokens = re.split(r'(</?[^>]+>)', s)
        indent = 0
        out_lines = []
        void_tags = {"br","hr","img","meta","link","input","source","area","col","embed","param","track","wbr"}
        for tok in tokens:
            if tok is None or tok == "":
                continue
            if tok.startswith('<') and tok.endswith('>'):
                tclean = tok.strip('<> ').lower()
                is_closing = tclean.startswith('/')
                name = tclean[1:].split()[0] if is_closing else tclean.split()[0].rstrip('/')
                is_self = tok.endswith('/>') or name in void_tags
                if is_closing:
                    indent = max(0, indent-1)
                line = ("    " * indent) + tok.strip()
                out_lines.append(line)
                if (not is_closing) and (not is_self):
                    indent += 1
            else:
                text = tok.strip()
                if text:
                    out_lines.append(("    " * indent) + text)
        return "\n".join(out_lines)

    def _format_preview_html(self):
        try:
            content = self.pv.get("1.0", tk.END)
            formatted = self._format_html_string(content)
            self.pv.config(state=tk.NORMAL)
            self.pv.delete("1.0", tk.END)
            self.pv.insert("1.0", formatted)
            self.pv.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("格式化失敗", str(e))
    
    def _ui(self):
        # 全域樣式：確保 ttk.Entry 也採用白底黑字，即使主題（如 ttkbootstrap darkly）會覆蓋
        self.root.option_add("*Entry.background", "#ffffff")
        self.root.option_add("*Entry.foreground", "black")
        self.root.option_add("*Entry.insertBackground", "black")
        self.root.option_add("*Text.background", "#ffffff")
        self.root.option_add("*Text.foreground", "black")
        self.root.option_add("*Text.insertBackground", "black")
        self.root.option_add("*TEntry*FieldBackground", "#ffffff")
        self.root.option_add("*TEntry*foreground", "black")
        try:
            st = ttk.Style()
            # 自訂背景色 #2c4c52
            bg_color = "#2c4c52"
            self.root.configure(bg=bg_color)
            
            # 設定所有主要元件的背景色
            st.configure(".", background=bg_color)
            st.configure("TFrame", background=bg_color)
            st.configure("TLabelframe", background=bg_color, bordercolor=bg_color)
            st.configure("TLabelframe.Label", background=bg_color)
            st.configure("TLabel", background=bg_color)
            st.configure("TButton", background=bg_color)
            st.configure("TRadiobutton", background=bg_color)
            st.configure("TCheckbutton", background=bg_color)
            st.configure("TNotebook", background=bg_color, bordercolor=bg_color)
            st.configure("TNotebook.Tab", background=bg_color)
            st.configure("TPanedwindow", background=bg_color)
            st.configure("Vertical.TScrollbar", background=bg_color, troughcolor=bg_color)
            st.configure("Horizontal.TScrollbar", background=bg_color, troughcolor=bg_color)
            
            st.configure("TEntry", fieldbackground="#ffffff", foreground="black")
            st.map(
                "TEntry",
                fieldbackground=[('disabled', '#eeeeee'), ('focus', '#ffffff'), ('!disabled', '#ffffff')],
                foreground=[('disabled', '#666666'), ('!disabled', 'black')]
            )
        except Exception:
            pass

        # 工具列
        tb = ttk.Frame(self.root)
        tb.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)
        ttk.Button(tb, text="開啟編輯檔", command=self.op).pack(side=tk.LEFT, padx=2)
        ttk.Button(tb, text="儲存編輯檔", command=self.sv).pack(side=tk.LEFT, padx=2)
        ttk.Button(tb, text="匯出HTML", command=self.ex).pack(side=tk.LEFT, padx=2)

        # 檔案路徑顯示
        self.file_path_label = ttk.Label(tb, text="未開啟檔案", font=("Arial", 8), foreground="gray")
        self.file_path_label.pack(side=tk.LEFT, padx=20)

        # SEO 資訊區
        seo_frame = ttk.LabelFrame(self.root, text="SEO 資訊", padding=10)
        seo_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)

        # 第一行：作者、組織名稱、文章編號
        row1 = ttk.Frame(seo_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="作者:", width=10).pack(side=tk.LEFT)
        self.author = tk.Entry(row1, width=15, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.author.insert(0, "炫麗黃金白銀交易所")
        self.author.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="組織名稱:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.org_name = tk.Entry(row1, width=20, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.org_name.insert(0, "炫麗黃金白銀交易所")
        self.org_name.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="文章編號:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.article_num = tk.Entry(row1, width=10, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.article_num.insert(0, str(get_article_number()))
        self.article_num.pack(side=tk.LEFT, padx=5)

        # 第二行：文章日期、修改日期
        row2 = ttk.Frame(seo_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="文章日期:", width=10).pack(side=tk.LEFT)
        self.pub_date = tk.Entry(row2, width=15, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.pub_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.pub_date.pack(side=tk.LEFT, padx=5)

        ttk.Label(row2, text="修改日期:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.mod_date = tk.Entry(row2, width=15, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.mod_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.mod_date.pack(side=tk.LEFT, padx=5)

        # 第三行：作者型別（Person/Organization）
        row3 = ttk.Frame(seo_frame)
        row3.pack(fill=tk.X, pady=2)
        ttk.Label(row3, text="作者型別:", width=10).pack(side=tk.LEFT)
        self.author_type = tk.StringVar(value="Organization")
        ttk.Radiobutton(row3, text="Organization", variable=self.author_type, value="Organization", command=self._chg).pack(side=tk.LEFT)
        ttk.Radiobutton(row3, text="Person", variable=self.author_type, value="Person", command=self._chg).pack(side=tk.LEFT, padx=10)

        # 第四行：標題
        row4 = ttk.Frame(seo_frame)
        row4.pack(fill=tk.X, pady=2)
        ttk.Label(row4, text="標題:", width=10).pack(side=tk.LEFT)
        self.headline = tk.Entry(row4, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.headline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第五行：描述
        row5 = ttk.Frame(seo_frame)
        row5.pack(fill=tk.X, pady=2)
        ttk.Label(row5, text="描述:", width=10).pack(side=tk.LEFT)
        self.description = tk.Entry(row5, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.description.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第六行：Publisher 設定（Logo/URL）
        row6 = ttk.Frame(seo_frame)
        row6.pack(fill=tk.X, pady=2)
        ttk.Label(row6, text="Publisher Logo:", width=14).pack(side=tk.LEFT)
        self.publisher_logo_url = tk.Entry(row6, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.publisher_logo_url.insert(0, "")
        self.publisher_logo_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(row6, text="Publisher URL:", width=12).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_url = tk.Entry(row6, width=28, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.publisher_url.insert(0, "")
        self.publisher_url.pack(side=tk.LEFT)

        # 第七行：Publisher Logo 寬高 + sameAs
        row7 = ttk.Frame(seo_frame)
        row7.pack(fill=tk.X, pady=2)
        ttk.Label(row7, text="Logo寬(px):", width=10).pack(side=tk.LEFT)
        self.publisher_logo_width = tk.Entry(row7, width=8, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.publisher_logo_width.insert(0, "")
        self.publisher_logo_width.pack(side=tk.LEFT)

        ttk.Label(row7, text="Logo高(px):", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_logo_height = tk.Entry(row7, width=8, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.publisher_logo_height.insert(0, "")
        self.publisher_logo_height.pack(side=tk.LEFT)

        ttk.Label(row7, text="Publisher sameAs:", width=16).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_sameas = tk.Entry(row7, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.publisher_sameas.insert(0, "")
        self.publisher_sameas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第八行：圖片路徑、寬、高
        row8 = ttk.Frame(seo_frame)
        row8.pack(fill=tk.X, pady=2)
        ttk.Label(row8, text="圖片路徑:", width=10).pack(side=tk.LEFT)
        self.image_path = tk.Entry(row8, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.image_path.insert(0, "")
        self.image_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(row8, text="寬度:", width=6).pack(side=tk.LEFT, padx=(10,0))
        self.image_width = tk.Entry(row8, width=10, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.image_width.insert(0, "100%")
        self.image_width.pack(side=tk.LEFT, padx=5)

        ttk.Label(row8, text="高度:", width=6).pack(side=tk.LEFT, padx=(10,0))
        self.image_height = tk.Entry(row8, width=10, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.image_height.insert(0, "auto")
        self.image_height.pack(side=tk.LEFT, padx=5)

        # 分頁介面
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # 內容編輯分頁
        edit_tab = ttk.Frame(notebook)
        notebook.add(edit_tab, text="內容編輯")

        pn = ttk.PanedWindow(edit_tab, orient=tk.HORIZONTAL)
        pn.pack(fill=tk.BOTH, expand=True)

        lf = ttk.Frame(pn)
        pn.add(lf, weight=1)
        cv = tk.Canvas(lf, bg="#2c4c52", highlightthickness=0)
        sb = ttk.Scrollbar(lf, command=cv.yview)
        self.sf = ttk.Frame(cv)
        self.sf.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=self.sf, anchor="nw")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        h1f = ttk.LabelFrame(self.sf, text="H1", padding=10)
        h1f.pack(fill=tk.X, padx=5, pady=5)
        self.h1 = tk.Entry(h1f, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 11))
        self.h1.pack(fill=tk.X)
        self.h1.bind("<KeyRelease>", lambda e: self._chg())

        inf = ttk.LabelFrame(self.sf, text="前言", padding=10)
        inf.pack(fill=tk.X, padx=5, pady=5)
        
        # 前言 H2 標題
        intro_h2_frame = ttk.Frame(inf)
        intro_h2_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(intro_h2_frame, text="H2 標題:", width=8).pack(side=tk.LEFT)
        self.intro_h2 = tk.Entry(intro_h2_frame, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 10))
        self.intro_h2.insert(0, "前言")
        self.intro_h2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.intro_h2.bind("<KeyRelease>", lambda e: self._chg())
        
        # 前言內容和 HTML 模式開關
        intro_ct_frame = ttk.Frame(inf)
        intro_ct_frame.pack(fill=tk.BOTH, expand=True)
        self.intro_is_html = tk.BooleanVar(value=False)
        ttk.Checkbutton(intro_ct_frame, text="HTML模式", variable=self.intro_is_html, command=lambda: [self._highlight_intro_if_html(), self._chg()]).pack(anchor="w")
        self.intro = tk.Text(intro_ct_frame, height=6, wrap=tk.WORD, bg="#f8f9f9", fg="black", insertbackground="black", font=("Consolas", 9))
        self.intro.pack(fill=tk.BOTH, expand=True)
        # Intro 高亮設定
        try:
            self.intro.tag_config("html-tag", foreground="#0066cc")
            self.intro.tag_config("html-attr", foreground="#995500")
            self.intro.tag_config("html-string", foreground="#2a7b2e")
        except Exception:
            pass
        def _on_intro_key(_):
            self._highlight_intro_if_html(); self._chg()
        self.intro.bind("<KeyRelease>", _on_intro_key)

        self.scf = ttk.LabelFrame(self.sf, text="主內容", padding=10)
        self.scf.pack(fill=tk.X, padx=5, pady=5)
        self.scc = ttk.Frame(self.scf)
        self.scc.pack(fill=tk.X)
        ttk.Button(self.scf, text="+ 段落", width=20, command=self.add_sec).pack()

        self.fqf = ttk.LabelFrame(self.sf, text="FAQ", padding=10)
        self.fqf.pack(fill=tk.X, padx=5, pady=5)
        self.fqc = ttk.Frame(self.fqf)
        self.fqc.pack(fill=tk.X)
        ttk.Button(self.fqf, text="+ QA", width=20, command=self.add_faq).pack()

        rf = ttk.LabelFrame(pn, text="HTML 預覽", padding=5)
        pn.add(rf, weight=1)

        # 預覽區工具列
        pv_toolbar = ttk.Frame(rf)
        pv_toolbar.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        ttk.Button(pv_toolbar, text="🌐 在瀏覽器開啟", command=self._preview_browser).pack(side=tk.LEFT)
        copy_btn = tk.Button(pv_toolbar, text="檢視輸出HTML", bg="#72a97c", fg="#fefefe", relief=tk.FLAT, padx=10, pady=2, command=self._copy_complete_html)
        copy_btn.pack(side=tk.LEFT, padx=10)
        ttk.Button(pv_toolbar, text="格式化HTML", command=self._format_preview_html).pack(side=tk.LEFT, padx=5)
        ttk.Label(pv_toolbar, text="(HTML 原始碼)", font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=10)

        self.pv = scrolledtext.ScrolledText(rf, wrap=tk.WORD, state=tk.DISABLED, bg="#f8f9f9", fg="black", insertbackground="black")
        self.pv.pack(fill=tk.BOTH, expand=True)

        # Schema 預覽分頁（JSON-LD）
        schema_tab = ttk.Frame(notebook)
        notebook.add(schema_tab, text="Schema 預覽")

        schema_toolbar = ttk.Frame(schema_tab)
        schema_toolbar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)
        ttk.Label(schema_toolbar, text="Schema JSON-LD", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(schema_toolbar, text="重新整理", command=self._update_schema_preview).pack(side=tk.RIGHT)

        self.schema_preview = scrolledtext.ScrolledText(schema_tab, wrap=tk.WORD, font=("Consolas", 10), bg="#f8f9f9", fg="black", insertbackground="black")
        self.schema_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # CSS 編輯分頁
        css_tab = ttk.Frame(notebook)
        notebook.add(css_tab, text="CSS")

        css_toolbar = ttk.Frame(css_tab)
        css_toolbar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)
        ttk.Label(css_toolbar, text="共用 CSS 樣式", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(css_toolbar, text="儲存 CSS", command=self._save_css).pack(side=tk.RIGHT, padx=5)
        ttk.Button(css_toolbar, text="載入 CSS", command=self._load_css).pack(side=tk.RIGHT)

        # CSS 模式選擇
        css_mode_frame = ttk.Frame(css_tab)
        css_mode_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Label(css_mode_frame, text="CSS 引入方式:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.css_mode = tk.StringVar(value="inline")
        ttk.Radiobutton(css_mode_frame, text="內置 Style", variable=self.css_mode, value="inline").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(css_mode_frame, text="外部 .css 檔", variable=self.css_mode, value="external").pack(side=tk.LEFT, padx=5)
        
        # 外部 CSS 連結輸入
        ttk.Label(css_mode_frame, text="外部 CSS URL:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(20, 5))
        self.css_link_entry = tk.Entry(css_mode_frame, width=40, bg="#f8f9f9", fg="black", font=("Consolas", 9))
        self.css_link_entry.pack(side=tk.LEFT, padx=5)
        self.css_link_entry.insert(0, "https://example.com/style.css")
        ttk.Button(css_mode_frame, text="瀏覽...", command=self._browse_css_file).pack(side=tk.LEFT, padx=2)

        self.css_editor = scrolledtext.ScrolledText(css_tab, wrap=tk.WORD, font=("Consolas", 10), bg="#f8f9f9", fg="black", insertbackground="black")
        self.css_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Footer 編輯分頁
        footer_tab = ttk.Frame(notebook)
        notebook.add(footer_tab, text="Footer")

        footer_toolbar = ttk.Frame(footer_tab)
        footer_toolbar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)
        ttk.Label(footer_toolbar, text="共用 Footer HTML", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(footer_toolbar, text="儲存 Footer", command=self._save_footer).pack(side=tk.RIGHT, padx=5)
        ttk.Button(footer_toolbar, text="載入 Footer", command=self._load_footer).pack(side=tk.RIGHT)

        self.footer_editor = scrolledtext.ScrolledText(footer_tab, wrap=tk.WORD, font=("Consolas", 10), bg="#f8f9f9", fg="black", insertbackground="black")
        self.footer_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 底部作者宣告
        footer = ttk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

        ttk.Label(footer, text=f"SEO Article Editor v{self.app_version} | Design by ", font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=(5, 0))

        author_link = ttk.Label(
            footer,
            text="Colinjen",
            font=("Arial", 8, "underline"),
            foreground="gray",
            cursor="hand2"
        )
        author_link.pack(side=tk.LEFT)
        author_link.bind("<Button-1>", lambda e: webbrowser.open("mailto:colinjen88@gmail.com"))

        self._load_ex()
        self.upd()
        
        # 載入共用檔案並收集訊息
        messages = []
        css_success, css_msg = self._load_css()
        messages.append(css_msg)
        
        footer_success, footer_msg = self._load_footer()
        messages.append(footer_msg)
        
        # 合併顯示一次提示
        combined_message = "\n".join(messages)
        if not css_success or not footer_success:
            messagebox.showinfo("載入狀態", combined_message)
        
        # 強制設定所有輸入欄位為白底黑字（在主題載入後執行）
        self.root.after(100, self._force_white_inputs)
    
    def add_sec(self): s = SecBlock(self.scc, self._chg, lambda x: [self.secs.remove(x), self._chg()]); self.secs.append(s); self._chg()
    def add_faq(self):
        f = FaqBlock(self.fqc, self._chg, lambda x: [self.faqs.remove(x), self._chg()])
        self.faqs.append(f)
        self._chg()
        # 確保新加入的 QA 輸入欄位立即套用白底黑字
        try:
            f.q.config(bg="#f8f9f9", fg="black", insertbackground="black")
            f.a.config(bg="#f8f9f9", fg="black", insertbackground="black")
        except Exception:
            pass
        # 再保險一次：排入事件迴圈後刷新所有輸入欄位為白底
        self.root.after(10, self._force_white_inputs)
    
    def _force_white_inputs(self):
        """強制將所有輸入欄位設定為白底黑字"""
        # 更新所有已存在的輸入欄位
        for widget in [self.author, self.pub_date, self.mod_date, self.org_name, self.article_num,
                      self.headline, self.description, self.publisher_logo_url, self.publisher_url,
                      self.publisher_logo_width, self.publisher_logo_height, self.publisher_sameas,
                      self.image_path, self.image_width, self.image_height,
                      self.h1, self.intro_h2]:
            try:
                widget.config(bg="#f8f9f9", fg="black", insertbackground="black")
            except:
                pass
        
        # 更新 Text 欄位
        try:
            self.intro.config(bg="#f8f9f9", fg="black", insertbackground="black")
            self.pv.config(bg="#f8f9f9", fg="black", insertbackground="black")
            self.schema_preview.config(bg="#f8f9f9", fg="black", insertbackground="black")
        except:
            pass
        
        # 更新動態產生的段落和 FAQ
        for sec in self.secs:
            try:
                sec.h2.config(bg="#f8f9f9", fg="black", insertbackground="black")
                sec.ct.config(bg="#f8f9f9", fg="black", insertbackground="black")
                for h3 in sec.h3s:
                    h3.h3.config(bg="#f8f9f9", fg="black", insertbackground="black")
                    h3.ct.config(bg="#f8f9f9", fg="black", insertbackground="black")
            except:
                pass
        
        for faq in self.faqs:
            try:
                faq.q.config(bg="#f8f9f9", fg="black", insertbackground="black")
                faq.a.config(bg="#f8f9f9", fg="black", insertbackground="black")
            except:
                pass
    
    def _chg(self):
        self.mod = True
        if hasattr(self, "_tm"): self.root.after_cancel(self._tm)
        self._tm = self.root.after(500, self.upd)
    
    def upd(self):
        h = self._gen()
        self.pv.config(state=tk.NORMAL); self.pv.delete("1.0", tk.END); self.pv.insert("1.0", h); self.pv.config(state=tk.DISABLED)
        self._update_schema_preview()
        # 預覽更新後，如有 HTML 模式則嘗試高亮（不影響主要輸入區）
        try:
            self._highlight_intro_if_html()
            for s in self.secs:
                s._highlight_if_html()
            for f in self.faqs:
                if f.get_is_html(): f._highlight()
        except Exception:
            pass
    
    def _update_schema_preview(self):
        """更新 Schema JSON-LD 預覽"""
        js = self._gen_schema_jsonld()
        self.schema_preview.delete("1.0", tk.END)
        self.schema_preview.insert("1.0", js)

    def _load_css(self):
        """從共用 CSS 檔案載入內容"""
        css_file = "templates/common.css"
        try:
            if os.path.exists(css_file):
                with open(css_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.css_editor.delete("1.0", tk.END)
                self.css_editor.insert("1.0", content)
                return True, f"已載入 CSS: {css_file}"
            else:
                # 如果檔案不存在，載入預設內容
                default_css = """/* 共用 CSS 樣式 */
.seo-article-content {max-width:960px; margin:0 auto; padding:20px;font-family:'Noto Sans TC',sans-serif; line-height:1.7; color:#343a40;}
.seo-article-content img{ width: 100%; height: auto;}
.seo-article-content h1 {font-size:2.5em; text-align:center; margin-bottom:20px; color:#b08d57;}
.seo-article-content h2 {font-size:1.8em; margin-top:8px; margin-bottom:20px; padding-bottom:10px; border-bottom:2px solid #b08d57;}
.seo-article-content h3 {font-size:1.3em; margin-top:20px; margin-bottom:10px; color:#343a40;}
.seo-article-content p {margin-bottom:1.2em;}
.intro-summary {background:#f8f9fa; border-left:5px solid #D8AB4C; padding:1rem 1.5rem; margin:1rem 0; font-size:1.05em;}
.intro-summary p {margin:0 0 4px;}
.seo-article-content table {width:100%; border-collapse:collapse; margin:30px 0; font-size:0.95em;}
.seo-article-content th,.seo-article-content td {padding:12px 15px; text-align:left; border-bottom:1px solid #dee2e6;}
.seo-article-content thead th {background:#343a40; color:#fff; font-weight:700;}
.seo-article-content tbody tr:nth-of-type(even) {background:#f8f9fa;}
.seo-article-content tbody tr:hover {background:#e9ecef;}
.seo-article-content hr {border:0; height:1px; background:#dee2e6; margin:60px 0;}
"""
                self.css_editor.delete("1.0", tk.END)
                self.css_editor.insert("1.0", default_css)
                return False, "CSS 檔案不存在，已載入預設樣式"
        except Exception as e:
            return False, f"載入 CSS 失敗: {e}"

    def _save_css(self):
        """儲存 CSS 內容到共用檔案"""
        css_file = "templates/common.css"
        try:
            os.makedirs("templates", exist_ok=True)
            content = self.css_editor.get("1.0", tk.END).strip()
            with open(css_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("成功", f"CSS 已儲存至: {css_file}")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存 CSS 失敗: {e}")

    def _browse_css_file(self):
        """瀏覽並選擇本地 CSS 檔案"""
        fp = filedialog.askopenfilename(filetypes=[("CSS Files", "*.css"), ("All Files", "*.*")])
        if fp:
            self.css_link_entry.delete(0, tk.END)
            self.css_link_entry.insert(0, fp)

    def _load_footer(self):
        """從共用 Footer 檔案載入內容"""
        footer_file = "templates/common_footer.html"
        try:
            if os.path.exists(footer_file):
                with open(footer_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.footer_editor.delete("1.0", tk.END)
                self.footer_editor.insert("1.0", content)
                return True, f"已載入 Footer: {footer_file}"
            else:
                # 如果檔案不存在，載入預設內容
                default_footer = """<section>
    <h3>1. 宏觀風險與避險需求（Safe-Haven Demand）</h3>
    <p>&lt;p&gt;黃金是對抗通膨、經濟放緩及貨幣貶值的主要避險工具。&lt;/p&gt;
        &lt;ul&gt;
            &lt;li&gt;**地緣政治不確定性：** 烏俄戰爭與中東局勢升溫。&lt;/li&gt;
            &lt;li&gt;**政策風險對沖：** 美國政策與貿易關稅變數持續，使黃金成為對沖「停滯性通膨＋衰退」風險的首選資產。&lt;/li&gt;
            &lt;li&gt;**貨幣政策影響：** 市場預期利率持續下降、美元維持弱勢，強化黃金吸引力。&lt;/li&gt;
        &lt;/ul&gt;</p>
</section>"""
                self.footer_editor.delete("1.0", tk.END)
                self.footer_editor.insert("1.0", default_footer)
                return False, "Footer 檔案不存在，已載入預設內容"
        except Exception as e:
            return False, f"載入 Footer 失敗: {e}"

    def _save_footer(self):
        """儲存 Footer 內容到共用檔案"""
        footer_file = "templates/common_footer.html"
        try:
            os.makedirs("templates", exist_ok=True)
            content = self.footer_editor.get("1.0", tk.END).strip()
            with open(footer_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("成功", f"Footer 已儲存至: {footer_file}")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存 Footer 失敗: {e}")

    def _strip_tags(self, html: str) -> str:
        """將 HTML 碼轉為純文字（用於 JSON-LD 的 text 欄位）"""
        if not html:
            return ""
        # 移除 script/style 內容
        html = re.sub(r"<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>", "", html, flags=re.I|re.S)
        # 移除所有標籤
        text = re.sub(r"<[^>]+>", "", html)
        # 轉換 HTML 實體的少數常見項
        text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        return text.strip()

    def _gen_schema_jsonld(self) -> str:
        """產生 JSON-LD（分離兩段 script：Article 與 FAQPage）供預覽/匯出"""
        author_name = self.author.get().strip() or "作者"
        org_name = self.org_name.get().strip() or "組織名稱（預設）"
        pub_date = self.pub_date.get().strip() or datetime.today().strftime('%Y-%m-%d')
        mod_date = self.mod_date.get().strip() or datetime.today().strftime('%Y-%m-%d')
        headline = self.headline.get().strip() or (self.h1.get().strip() or "文章標題")
        description = self.description.get().strip() or ""
        image_url = self.image_path.get().strip() if hasattr(self, 'image_path') else ""
        author_type = (self.author_type.get() if hasattr(self, 'author_type') else 'Organization') or 'Organization'
        publisher_logo = self.publisher_logo_url.get().strip() if hasattr(self, 'publisher_logo_url') else "https://example.com/logo.png"
        publisher_url = self.publisher_url.get().strip() if hasattr(self, 'publisher_url') else "https://example.com/"
        publisher_logo_width = self.publisher_logo_width.get().strip() if hasattr(self, 'publisher_logo_width') else ""
        publisher_logo_height = self.publisher_logo_height.get().strip() if hasattr(self, 'publisher_logo_height') else ""
        publisher_sameas_str = self.publisher_sameas.get().strip() if hasattr(self, 'publisher_sameas') else ""
        publisher_sameas = [u.strip() for u in publisher_sameas_str.split(",") if u.strip()]

        # 以文章編號推導頁面 URL（如: https://pm.shiny.com.tw/news-detail.php?id=XXXX）
        page_id = self.article_num.get().strip()
        main_entity_of_page = None
        if page_id and page_id.isdigit():
            main_entity_of_page = {
                "@id": f"https://example.com/news/{page_id}",
                "@type": "WebPage",
            }

        # FAQ 轉為 Question/Answer 陣列
        faq_entities = []
        for f in self.faqs:
            q = (f.get_q() or "").strip()
            a_raw = (f.get_a() or "").strip()
            a = self._strip_tags(a_raw) if f.get_is_html() else a_raw
            if q or a:
                faq_entities.append({
                    "@type": "Question",
                    "name": q or "問題",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a or ""
                    }
                })

        # Article JSON-LD
        author_obj = {"@type": author_type, "name": author_name}
        data_article = {
            "@context": "https://schema.org",
            "@type": "Article",
            "author": author_obj,
            "dateModified": mod_date,
            "datePublished": pub_date,
            "description": description,
            "headline": headline,
            "image": image_url,
        }

        # FAQPage JSON-LD（獨立 script）
        data_faq = None
        if faq_entities:
            data_faq = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_entities
            }

        if main_entity_of_page:
            data_article["mainEntityOfPage"] = main_entity_of_page

        publisher_obj = {
            "@type": "Organization",
            "logo": {
                "@type": "ImageObject",
                "url": publisher_logo
            },
            "name": org_name
        }
        # 加入 logo 寬高 (若提供)
        if publisher_logo_width:
            try:
                publisher_obj["logo"]["width"] = int(publisher_logo_width)
            except Exception:
                publisher_obj["logo"]["width"] = publisher_logo_width
        if publisher_logo_height:
            try:
                publisher_obj["logo"]["height"] = int(publisher_logo_height)
            except Exception:
                publisher_obj["logo"]["height"] = publisher_logo_height
        # 加入 sameAs 陣列
        if publisher_sameas:
            publisher_obj["sameAs"] = publisher_sameas
        if publisher_url:
            publisher_obj["url"] = publisher_url
        data_article["publisher"] = publisher_obj

        js_article = json.dumps(data_article, ensure_ascii=False, indent=4)
        scripts = [f"<script type=\"application/ld+json\">\n{js_article}\n</script>"]
        if data_faq is not None:
            js_faq = json.dumps(data_faq, ensure_ascii=False, indent=4)
            scripts.append(f"<script type=\"application/ld+json\">\n{js_faq}\n</script>")
        return "\n".join(scripts)
    
    def _gen(self):
        p = []
        p.append("<article class=\"seo-article-content\">")
        h1 = self.h1.get().strip()
        if h1:
            p.append(f"  <h1>{self._esc(h1)}</h1>")
            p.append("")
        
        intro = self.intro.get("1.0", tk.END).strip()
        if intro:
            p.append('<section class="intro-summary">')
            intro_h2 = self.intro_h2.get().strip()
            if intro_h2:
                p.append(f"  <h2>{self._esc(intro_h2)}</h2>")
            
            # 前言內容支援 HTML 模式
            if self.intro_is_html.get():
                # HTML 模式: 直接插入,按行處理
                for line in intro.split("\n"):
                    if line.strip(): p.append(f"  {line.strip()}")
            else:
                # 純文字模式: 轉義並包裹 <p> 標籤
                for pa in intro.split("\n\n"):
                    if pa.strip(): p.append(f"  <p>{self._esc(pa.strip())}</p>")
            p.append("</section>")
            p.append("")
        
        for s in self.secs:
            h2, ct = s.get_h2(), s.get_ct()
            if h2 or ct:
                p.append("<section>")
                if h2: p.append(f"  <h2>{self._esc(h2)}</h2>")
                if ct:
                    # 段落內容支援 HTML (不轉義)
                    if s.is_html:
                        # HTML 模式: 直接插入,按行處理
                        for line in ct.split("\n"):
                            if line.strip(): p.append(f"  {line.strip()}")
                    else:
                        # 純文字模式: 轉義並包裹 <p> 標籤
                        for pa in ct.split("\n\n"):
                            if pa.strip(): p.append(f"  <p>{self._esc(pa.strip())}</p>")
                
                for h3 in s.h3s:
                    h3t, h3c = h3.get_h3(), h3.get_ct()
                    if h3t or h3c:
                        p.append("")
                        p.append("  <section>")
                        if h3t: p.append(f"    <h3>{self._esc(h3t)}</h3>")
                        if h3c:
                            for pa in h3c.split("\n\n"):
                                if pa.strip(): p.append(f"      <p>{self._esc(pa.strip())}</p>")
                        p.append("  </section>")
                
                p.append("</section>")
                p.append("")
        
        if self.faqs:
            p.append("<hr />")
            p.append('<section id="faq">')
            p.append('  <h2>常見問答 (Q&A)</h2>')
            for f in self.faqs:
                q, a = f.get_q(), f.get_a()
                is_html = f.get_is_html()
                if q or a:
                    p.append("")
                    if q: p.append(f"  <h3>{self._esc(q)}</h3>")
                    if a:
                        if is_html:
                            # HTML 模式: 不轉義
                            for line in a.split("\n"):
                                if line.strip(): p.append(f"    {line.strip()}")
                        else:
                            # 純文字模式: 轉義
                            for pa in a.split("\n\n"):
                                if pa.strip(): p.append(f"    <p>{self._esc(pa.strip())}</p>")
            p.append("</section>")
        
        p.append("</article>")
        return "\n".join(p)
    
    def _esc(self, t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    
    def op(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if fp:
            with open(fp, encoding="utf-8") as f: d = json.load(f)
            self._load(d); self.cf = fp; self.mod = False
            self.file_path_label.config(text=f"檔案: {fp}")
            self.upd()
    
    def sv(self):
        if not self.cf: self.cf = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if self.cf:
            d = {
                "seo": {
                    "author": self.author.get().strip(),
                    "pub_date": self.pub_date.get().strip(),
                    "mod_date": self.mod_date.get().strip(),
                    "org_name": self.org_name.get().strip(),
                    "article_num": self.article_num.get().strip(),
                    "headline": self.headline.get().strip(),
                    "description": self.description.get().strip(),
                    "author_type": (self.author_type.get() if hasattr(self, 'author_type') else 'Organization'),
                    "publisher_logo_url": (self.publisher_logo_url.get().strip() if hasattr(self, 'publisher_logo_url') else "https://example.com/logo.png"),
                    "publisher_url": (self.publisher_url.get().strip() if hasattr(self, 'publisher_url') else "https://example.com/"),
                    "publisher_logo_width": (self.publisher_logo_width.get().strip() if hasattr(self, 'publisher_logo_width') else ""),
                    "publisher_logo_height": (self.publisher_logo_height.get().strip() if hasattr(self, 'publisher_logo_height') else ""),
                    "publisher_sameas": ([u.strip() for u in (self.publisher_sameas.get().split(',') if hasattr(self, 'publisher_sameas') else []) if u.strip()]),
                    "image_path": (self.image_path.get().strip() if hasattr(self, 'image_path') else ""),
                    "image_width": (self.image_width.get().strip() if hasattr(self, 'image_width') else "100%"),
                    "image_height": (self.image_height.get().strip() if hasattr(self, 'image_height') else "auto")
                },
                "h1": self.h1.get().strip(),
                "intro": self.intro.get("1.0", tk.END).strip(),
                "intro_h2": self.intro_h2.get().strip(),
                "intro_is_html": self.intro_is_html.get(),
                "sections": [s.to_dict() for s in self.secs],
                "faqs": [f.to_dict() for f in self.faqs]
            }
            with open(self.cf, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
            self.file_path_label.config(text=f"檔案: {self.cf}")
            self.mod = False
    
    def _load(self, d):
        # 載入 SEO 資訊
        seo = d.get("seo", {})
        self.author.delete(0, tk.END); self.author.insert(0, seo.get("author", "作者名稱（預設）"))
        self.pub_date.delete(0, tk.END); self.pub_date.insert(0, seo.get("pub_date", datetime.today().strftime('%Y-%m-%d')))
        self.mod_date.delete(0, tk.END); self.mod_date.insert(0, seo.get("mod_date", datetime.today().strftime('%Y-%m-%d')))
        self.org_name.delete(0, tk.END); self.org_name.insert(0, seo.get("org_name", "組織名稱（預設）"))
        self.article_num.delete(0, tk.END); self.article_num.insert(0, seo.get("article_num", str(get_article_number())))
        self.headline.delete(0, tk.END); self.headline.insert(0, seo.get("headline", ""))
        self.description.delete(0, tk.END); self.description.insert(0, seo.get("description", ""))
        # 新增欄位
        if hasattr(self, 'author_type'): self.author_type.set(seo.get("author_type", "Organization"))
        if hasattr(self, 'publisher_logo_url'):
            self.publisher_logo_url.delete(0, tk.END); self.publisher_logo_url.insert(0, seo.get("publisher_logo_url", "https://example.com/logo.png"))
        if hasattr(self, 'publisher_url'):
            self.publisher_url.delete(0, tk.END); self.publisher_url.insert(0, seo.get("publisher_url", "https://example.com/"))
        if hasattr(self, 'publisher_logo_width'):
            self.publisher_logo_width.delete(0, tk.END); self.publisher_logo_width.insert(0, seo.get("publisher_logo_width", ""))
        if hasattr(self, 'publisher_logo_height'):
            self.publisher_logo_height.delete(0, tk.END); self.publisher_logo_height.insert(0, seo.get("publisher_logo_height", ""))
        if hasattr(self, 'publisher_sameas'):
            sameas_val = seo.get("publisher_sameas", "")
            if isinstance(sameas_val, list):
                sameas_str = ", ".join(sameas_val)
            else:
                sameas_str = sameas_val or ""
            self.publisher_sameas.delete(0, tk.END); self.publisher_sameas.insert(0, sameas_str)
        
        if hasattr(self, 'image_path'):
            self.image_path.delete(0, tk.END); self.image_path.insert(0, seo.get("image_path", ""))
        if hasattr(self, 'image_width'):
            self.image_width.delete(0, tk.END); self.image_width.insert(0, seo.get("image_width", "100%"))
        if hasattr(self, 'image_height'):
            self.image_height.delete(0, tk.END); self.image_height.insert(0, seo.get("image_height", "auto"))
        
        # 載入內容
        self.h1.delete(0, tk.END); self.intro.delete("1.0", tk.END)
        self.intro_h2.delete(0, tk.END)
        for s in self.secs: s.f.destroy()
        for f in self.faqs: f.f.destroy()
        self.secs.clear(); self.faqs.clear()
        self.h1.insert(0, d.get("h1","")); self.intro.insert("1.0", d.get("intro",""))
        self.intro_h2.insert(0, d.get("intro_h2", "前言"))
        self.intro_is_html.set(d.get("intro_is_html", False))
        for sd in d.get("sections",[]):
            self.add_sec()
            self.secs[-1].set_h2(sd.get("h2",""))
            self.secs[-1].set_ct(sd.get("content",""))
            for h3d in sd.get("h3s",[]):
                self.secs[-1].add_h3()
                self.secs[-1].h3s[-1].set_h3(h3d.get("h3",""))
                self.secs[-1].h3s[-1].set_ct(h3d.get("content",""))
        for fd in d.get("faqs",[]): 
            self.add_faq()
            self.faqs[-1].set_q(fd.get("question",""))
            self.faqs[-1].set_a(fd.get("answer",""))
            self.faqs[-1].set_is_html(fd.get("is_html", False))
    
    def ex(self):
        # 產出完整 HTML：含語意化標記（<article>/<section>）與 JSON-LD 結構化資料
        body = self._gen()
        # 集中取得 style/link HTML
        style_html = self._get_style_html()
        schema = self._gen_schema_jsonld()
        title = self.h1.get().strip() or "文章"
        # 取得 Footer（從 Footer 編輯器）
        footer_content = self.footer_editor.get("1.0", tk.END).strip() if hasattr(self, 'footer_editor') else ""
        footer_html = footer_content if footer_content else ""
        body = self._gen()  # 重新取得 body，避免未定義
        html = (
            '<!DOCTYPE html>'
            '<html>'
            '<head>'
            '<meta charset="UTF-8">'
            f'<title>{title}</title>'
            f'{schema}'
            f'{style_html}'
            '</head>'
            '<body>'
            f'{body}'
            f'{footer_html}'
            '</body>'
            '</html>'
        )
        fp = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML","*.html")])
        if fp:
            with open(fp, "w", encoding="utf-8") as f: f.write(html)
            messagebox.showinfo("完成", f"已匯出: {fp}")
    
    def _copy_html(self):
        """複製 HTML 原始碼到剪貼簿"""
        try:
            html = self.pv.get("1.0", tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(html)
            messagebox.showinfo("成功", "HTML 原始碼已複製到剪貼簿!")
        except Exception as e:
            messagebox.showerror("錯誤", f"複製失敗: {e}")
    
    def _copy_complete_html(self):
        """檢視並複製完整 HTML（包含 Schema、CSS、HTML 和 Footer）"""
        try:
            # 生成完整 HTML
            complete_html = self._generate_complete_html()
            
            # 創建預覽視窗
            preview_window = tk.Toplevel(self.root)
            preview_window.title("檢視輸出 HTML")
            preview_window.geometry("900x700")
            
            # 工具列
            toolbar = ttk.Frame(preview_window)
            toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            
            ttk.Label(toolbar, text="完整 HTML 預覽", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
            
            def copy_to_clipboard():
                preview_window.clipboard_clear()
                preview_window.clipboard_append(complete_html)
                messagebox.showinfo("成功", "HTML 原始碼已複製到剪貼簿!", parent=preview_window)
            
            def fmt_preview():
                try:
                    current = html_preview.get("1.0", tk.END)
                    pretty = self._format_html_string(current)
                    html_preview.delete("1.0", tk.END)
                    html_preview.insert("1.0", pretty)
                except Exception as e:
                    messagebox.showerror("格式化失敗", str(e), parent=preview_window)

            ttk.Button(toolbar, text="格式化", command=fmt_preview).pack(side=tk.RIGHT, padx=5)
            ttk.Button(toolbar, text="複製 HTML 碼", command=copy_to_clipboard).pack(side=tk.RIGHT, padx=5)
            ttk.Button(toolbar, text="關閉", command=preview_window.destroy).pack(side=tk.RIGHT)
            
            # HTML 預覽區
            html_preview = scrolledtext.ScrolledText(
                preview_window, 
                wrap=tk.WORD, 
                font=("Consolas", 9), 
                bg="#f8f9f9", 
                fg="black"
            )
            html_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            html_preview.insert("1.0", complete_html)
            html_preview.config(state=tk.NORMAL)  # 允許選取複製
            
        except Exception as e:
            messagebox.showerror("錯誤", f"生成 HTML 失敗: {e}")
    
    def _generate_complete_html(self):
        """生成完整的 HTML（Schema 在前，Style 在後）"""
        # 生成主要內容
        body = self._gen()
        
        # 取得 CSS 樣式模式
        css_mode = getattr(self, 'css_mode', tk.StringVar(value="inline"))
        css_link = getattr(self, 'css_link_entry', None)
        
        # 取得 Footer（從 Footer 編輯器）
        footer_content = self.footer_editor.get("1.0", tk.END).strip() if hasattr(self, 'footer_editor') else ""
        
        # 生成 Schema JSON-LD
        schema = self._gen_schema_jsonld()
        
        # 根據 CSS 模式生成樣式標籤（集中使用 helper）
        style_tag = self._get_style_html()
        
        # 組合完整 HTML（Schema 在前，Style 在後）
        title = self.h1.get().strip() or "文章標題"
        complete_html = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-TW">\n'
            '<head>\n'
            '    <meta charset="UTF-8">\n'
            '    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'    <title>{title}</title>\n'
            f'{schema}\n'
            f'{style_tag}\n'
            '</head>\n'
            '<body>\n'
            f'{body}\n'
        )
        
        # 加入 Footer（如果有的話）
        if footer_content:
            complete_html += f'    {footer_content}\n'
        
        complete_html += '</body>\n</html>'
        
        return complete_html

    # --- Intro 區塊高亮 ---
    def _highlight_intro_if_html(self):
        if not hasattr(self, 'intro_is_html'): return
        if not self.intro_is_html.get():
            # 移除標籤
            try:
                self.intro.tag_remove("html-tag", "1.0", tk.END)
                self.intro.tag_remove("html-attr", "1.0", tk.END)
                self.intro.tag_remove("html-string", "1.0", tk.END)
            except Exception:
                pass
            return
        try:
            content = self.intro.get("1.0", tk.END)
            self.intro.tag_remove("html-tag", "1.0", tk.END)
            self.intro.tag_remove("html-attr", "1.0", tk.END)
            self.intro.tag_remove("html-string", "1.0", tk.END)
            for m in TAG_PATTERN.finditer(content):
                s = _index_from_offset(content, m.start())
                e = _index_from_offset(content, m.end())
                self.intro.tag_add("html-tag", s, e)
                inner = content[m.start():m.end()]
                inner_base = m.start()
                for sm in ATTR_PATTERN.finditer(inner):
                    ss = _index_from_offset(content, inner_base + sm.start(1))
                    se = _index_from_offset(content, inner_base + sm.end(1))
                    self.intro.tag_add("html-attr", ss, se)
                for q in STRING_PATTERN.finditer(inner):
                    qs = _index_from_offset(content, inner_base + q.start())
                    qe = _index_from_offset(content, inner_base + q.end())
                    self.intro.tag_add("html-string", qs, qe)
        except Exception:
            pass
    
    def _preview_browser(self):
        """從預覽窗格的 HTML 原始碼產生瀏覽器預覽"""
        body = self._gen()
        # 集中取得 style/link HTML
        style_html = self._get_style_html()
        schema = self._gen_schema_jsonld()
        title = self.h1.get().strip() or "預覽"
        html = (
            '<!DOCTYPE html>'
            '<html>'
            '<head>'
            '<meta charset="UTF-8">'
            f'<title>{title}</title>'
            f'{schema}'
            f'{style_html}'
            '</head>'
            '<body>'
            f'{body}'
            '</body>'
            '</html>'
        )
        os.makedirs(OUT, exist_ok=True)
        pp = os.path.join(OUT, "preview_temp.html")
        with open(pp, "w", encoding="utf-8") as f: f.write(html)
        webbrowser.open(pp)
    
    def _load_ex(self):
        """載入外部 defaults.json，若不存在使用內建 placeholder 並自動建立檔案。"""
        cfg_path = os.path.join(BASE, "config", "defaults.json")
        data = None
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = None
        if data is None:
            # 內建 placeholder 結構
            data = {
                "seo": {
                    "author": "炫麗黃金白銀交易所",
                    "pub_date": datetime.today().strftime('%Y-%m-%d'),
                    "mod_date": datetime.today().strftime('%Y-%m-%d'),
                    "org_name": "炫麗黃金白銀交易所",
                    "article_num": str(get_article_number()),
                    "headline": "請輸入文章標題",
                    "description": "請輸入文章描述",
                    "author_type": "Organization",
                    "publisher_logo_url": "https://example.com/logo.png",
                    "publisher_url": "https://example.com/",
                    "publisher_logo_width": "",
                    "publisher_logo_height": "",
                    "publisher_sameas": []
                },
                "h1": "請輸入 H1 標題",
                "intro": "這裡是前言內容…",
                "intro_h2": "前言",
                "sections": [{"h2": "第一段標題", "content": "第一段內容…", "h3s": []}],
                "faqs": [{"question": "常見問題 1?", "answer": "這是一個回答。", "is_html": False}]
            }
            try:
                os.makedirs(os.path.join(BASE, "config"), exist_ok=True)
                with open(cfg_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
        # 正規化資料鍵，補上缺值
        seo = data.get("seo", {})
        seo.setdefault("pub_date", datetime.today().strftime('%Y-%m-%d'))
        seo.setdefault("mod_date", datetime.today().strftime('%Y-%m-%d'))
        seo.setdefault("article_num", str(get_article_number()))
        data["seo"] = seo
        self._load(data); self.mod = False
    
    def _cls(self):
        if self.mod and messagebox.askyesno("未儲存", "要儲存嗎?"): self.sv()
        self.root.destroy()

def main():
    root = tk.Tk()
    Editor(root); root.mainloop()

if __name__ == "__main__": main()
