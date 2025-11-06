# -*- coding: utf-8 -*-
"""視覺化 SEO 文章編輯器"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os, json, webbrowser, re
from datetime import datetime

try:
    import ttkbootstrap as tb
    HAS_TTK = True
except: HAS_TTK = False

BASE = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(BASE, "output")
ARTICLE_NUMBER_FILE = os.path.join(BASE, "article_number.txt")

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

class H3Block:
    def __init__(self, p, oc, od):
        self.f = ttk.Frame(p, relief=tk.GROOVE, borderwidth=1)
        self.f.pack(fill=tk.X, padx=10, pady=3)
        ttk.Label(self.f, text="H3:", font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        self.h3 = tk.Entry(self.f, bg="#ffffff", fg="black", font=("Consolas", 10)); self.h3.pack(fill=tk.X, padx=5, pady=(0,3)); self.h3.bind("<KeyRelease>", lambda e: oc())
        ttk.Label(self.f, text="內容:", font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        self.ct = tk.Text(self.f, height=4, wrap=tk.WORD, bg="#ffffff", fg="black", font=("Consolas", 9)); self.ct.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,3)); self.ct.bind("<KeyRelease>", lambda e: oc())
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
        self.h2 = tk.Entry(self.f, bg="#ffffff", fg="black", font=("Consolas", 10)); self.h2.pack(fill=tk.X, pady=(0,5)); self.h2.bind("<KeyRelease>", lambda e: oc())

        ct_label_frame = ttk.Frame(self.f)
        ct_label_frame.pack(fill=tk.X, anchor=tk.W)
        ttk.Label(ct_label_frame, text="內容:").pack(side=tk.LEFT)
        ttk.Label(ct_label_frame, text="[支援 HTML 表格]", font=("Arial", 8), foreground="orange").pack(side=tk.LEFT, padx=5)

        self.ct = tk.Text(self.f, height=6, wrap=tk.WORD, bg="#ffffff", fg="black", font=("Consolas", 9)); self.ct.pack(fill=tk.BOTH, expand=True, pady=(0,5)); self.ct.bind("<KeyRelease>", lambda e: oc())

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

class FaqBlock:
    def __init__(self, p, oc, od):
        self.oc = oc
        self.is_html = tk.BooleanVar(value=False)  # 預設為純文字模式
        self.f = ttk.LabelFrame(p, text="QA", padding=10)
        self.f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.f, text="問題:").pack(anchor=tk.W)
        self.q = tk.Entry(self.f, bg="#ffffff", fg="black", font=("Consolas", 10)); self.q.pack(fill=tk.X, pady=(0,5)); self.q.bind("<KeyRelease>", lambda e: oc())
        
        a_label_frame = ttk.Frame(self.f)
        a_label_frame.pack(fill=tk.X, anchor=tk.W)
        ttk.Label(a_label_frame, text="答案:").pack(side=tk.LEFT)
        ttk.Checkbutton(a_label_frame, text="HTML 模式", variable=self.is_html, command=self._toggle_html).pack(side=tk.LEFT, padx=5)
        
        self.a = tk.Text(self.f, height=4, wrap=tk.WORD, bg="#ffffff", fg="black", font=("Consolas", 9)); self.a.pack(fill=tk.BOTH, expand=True, pady=(0,5)); self.a.bind("<KeyRelease>", lambda e: oc())
        ttk.Button(self.f, text="刪除", command=lambda: [self.f.destroy(), od(self)]).pack(anchor=tk.E)
    
    def _toggle_html(self):
        if self.is_html.get():
            self.a.config(font=("Consolas", 9))
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

class Editor:
    def __init__(self, root):
        self.root = root; self.root.title("SEO 文章編輯器"); self.root.geometry("1400x900")
        self.cf = None; self.mod = False; self.secs = []; self.faqs = []
        self.root.protocol("WM_DELETE_WINDOW", self._cls); self._ui()
    
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

        # 第一行
        row1 = ttk.Frame(seo_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="作者:", width=10).pack(side=tk.LEFT)
        self.author = tk.Entry(row1, width=15, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.author.insert(0, "炫麗鑫")
        self.author.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="文章日期:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.pub_date = tk.Entry(row1, width=15, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.pub_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.pub_date.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="修改日期:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.mod_date = tk.Entry(row1, width=15, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.mod_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.mod_date.pack(side=tk.LEFT, padx=5)

        # 第二行
        row2 = ttk.Frame(seo_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="組織名稱:", width=10).pack(side=tk.LEFT)
        self.org_name = tk.Entry(row2, width=20, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.org_name.insert(0, "Shiny黃金白銀")
        self.org_name.pack(side=tk.LEFT, padx=5)

        ttk.Label(row2, text="文章編號:", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.article_num = tk.Entry(row2, width=10, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.article_num.insert(0, str(get_article_number()))
        self.article_num.pack(side=tk.LEFT, padx=5)

        # 第三行：作者型別（Person/Organization）
        row2b = ttk.Frame(seo_frame)
        row2b.pack(fill=tk.X, pady=2)
        ttk.Label(row2b, text="作者型別:", width=10).pack(side=tk.LEFT)
        self.author_type = tk.StringVar(value="Organization")
        ttk.Radiobutton(row2b, text="Organization", variable=self.author_type, value="Organization", command=self._chg).pack(side=tk.LEFT)
        ttk.Radiobutton(row2b, text="Person", variable=self.author_type, value="Person", command=self._chg).pack(side=tk.LEFT, padx=10)

        # 第三行
        row3 = ttk.Frame(seo_frame)
        row3.pack(fill=tk.X, pady=2)
        ttk.Label(row3, text="標題:", width=10).pack(side=tk.LEFT)
        self.headline = tk.Entry(row3, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.headline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第四行
        row4 = ttk.Frame(seo_frame)
        row4.pack(fill=tk.X, pady=2)
        ttk.Label(row4, text="描述:", width=10).pack(side=tk.LEFT)
        self.description = tk.Entry(row4, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.description.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第五行：Publisher 設定（Logo/URL）
        row5 = ttk.Frame(seo_frame)
        row5.pack(fill=tk.X, pady=2)
        ttk.Label(row5, text="Publisher Logo:", width=14).pack(side=tk.LEFT)
        self.publisher_logo_url = tk.Entry(row5, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.publisher_logo_url.insert(0, "https://pm.shiny.com.tw/images/logo.png")
        self.publisher_logo_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(row5, text="Publisher URL:", width=12).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_url = tk.Entry(row5, width=28, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.publisher_url.insert(0, "https://pm.shiny.com.tw/")
        self.publisher_url.pack(side=tk.LEFT)

        # 第六行：Publisher Logo 寬高 + sameAs
        row6 = ttk.Frame(seo_frame)
        row6.pack(fill=tk.X, pady=2)
        ttk.Label(row6, text="Logo寬(px):", width=10).pack(side=tk.LEFT)
        self.publisher_logo_width = tk.Entry(row6, width=8, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.publisher_logo_width.insert(0, "")
        self.publisher_logo_width.pack(side=tk.LEFT)

        ttk.Label(row6, text="Logo高(px):", width=10).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_logo_height = tk.Entry(row6, width=8, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.publisher_logo_height.insert(0, "")
        self.publisher_logo_height.pack(side=tk.LEFT)

        ttk.Label(row6, text="Publisher sameAs:", width=16).pack(side=tk.LEFT, padx=(10,0))
        self.publisher_sameas = tk.Entry(row6, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.publisher_sameas.insert(0, "")
        self.publisher_sameas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 分頁介面
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # 編輯分頁
        edit_tab = ttk.Frame(notebook)
        notebook.add(edit_tab, text="編輯")

        pn = ttk.PanedWindow(edit_tab, orient=tk.HORIZONTAL)
        pn.pack(fill=tk.BOTH, expand=True)

        lf = ttk.Frame(pn)
        pn.add(lf, weight=1)
        cv = tk.Canvas(lf)
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
        self.h1 = tk.Entry(h1f, bg="#ffffff", fg="black", font=("Consolas", 11))
        self.h1.pack(fill=tk.X)
        self.h1.bind("<KeyRelease>", lambda e: self._chg())

        inf = ttk.LabelFrame(self.sf, text="前言", padding=10)
        inf.pack(fill=tk.X, padx=5, pady=5)
        
        # 前言 H2 標題
        intro_h2_frame = ttk.Frame(inf)
        intro_h2_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(intro_h2_frame, text="H2 標題:", width=8).pack(side=tk.LEFT)
        self.intro_h2 = tk.Entry(intro_h2_frame, bg="#ffffff", fg="black", font=("Consolas", 10))
        self.intro_h2.insert(0, "前言")
        self.intro_h2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.intro_h2.bind("<KeyRelease>", lambda e: self._chg())
        
        # 前言內容和 HTML 模式開關
        intro_ct_frame = ttk.Frame(inf)
        intro_ct_frame.pack(fill=tk.BOTH, expand=True)
        self.intro_is_html = tk.BooleanVar(value=False)
        ttk.Checkbutton(intro_ct_frame, text="HTML模式", variable=self.intro_is_html, command=self._chg).pack(anchor="w")
        self.intro = tk.Text(intro_ct_frame, height=6, wrap=tk.WORD, bg="#ffffff", fg="black", font=("Consolas", 9))
        self.intro.pack(fill=tk.BOTH, expand=True)
        self.intro.bind("<KeyRelease>", lambda e: self._chg())

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
        ttk.Label(pv_toolbar, text="(HTML 原始碼)", font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=10)

        self.pv = scrolledtext.ScrolledText(rf, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", fg="black")
        self.pv.pack(fill=tk.BOTH, expand=True)

        # Schema 預覽分頁（JSON-LD）
        schema_tab = ttk.Frame(notebook)
        notebook.add(schema_tab, text="Schema 預覽")

        schema_toolbar = ttk.Frame(schema_tab)
        schema_toolbar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)
        ttk.Label(schema_toolbar, text="Schema JSON-LD", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(schema_toolbar, text="重新整理", command=self._update_schema_preview).pack(side=tk.RIGHT)

        self.schema_preview = scrolledtext.ScrolledText(schema_tab, wrap=tk.WORD, font=("Consolas", 10), bg="#ffffff", fg="black")
        self.schema_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 底部作者宣告
        footer = ttk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

        ttk.Label(footer, text="SEOArticleEditor product v1.8 produced by ", font=("Arial", 7), foreground="gray").pack(side=tk.LEFT, padx=(0, 0))

        author_link = ttk.Label(
            footer,
            text="Colinjen",
            font=("Arial", 7, "underline"),
            foreground="white",
            cursor="hand2"
        )
        author_link.pack(side=tk.LEFT)
        author_link.bind("<Button-1>", lambda e: webbrowser.open("mailto:colinjen88@gmail.com"))

        self._load_ex()
        self.upd()
    
    def add_sec(self): s = SecBlock(self.scc, self._chg, lambda x: [self.secs.remove(x), self._chg()]); self.secs.append(s); self._chg()
    def add_faq(self): f = FaqBlock(self.fqc, self._chg, lambda x: [self.faqs.remove(x), self._chg()]); self.faqs.append(f); self._chg()
    
    def _chg(self):
        self.mod = True
        if hasattr(self, "_tm"): self.root.after_cancel(self._tm)
        self._tm = self.root.after(500, self.upd)
    
    def upd(self):
        h = self._gen()
        self.pv.config(state=tk.NORMAL); self.pv.delete("1.0", tk.END); self.pv.insert("1.0", h); self.pv.config(state=tk.DISABLED)
        self._update_schema_preview()
    
    def _update_schema_preview(self):
        """更新 Schema JSON-LD 預覽"""
        js = self._gen_schema_jsonld()
        self.schema_preview.delete("1.0", tk.END)
        self.schema_preview.insert("1.0", js)

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
        org_name = self.org_name.get().strip() or "Shiny黃金白銀"
        pub_date = self.pub_date.get().strip() or datetime.today().strftime('%Y-%m-%d')
        mod_date = self.mod_date.get().strip() or datetime.today().strftime('%Y-%m-%d')
        headline = self.headline.get().strip() or (self.h1.get().strip() or "文章標題")
        description = self.description.get().strip() or ""
        image_url = ""
        author_type = (self.author_type.get() if hasattr(self, 'author_type') else 'Organization') or 'Organization'
        publisher_logo = self.publisher_logo_url.get().strip() if hasattr(self, 'publisher_logo_url') else "https://pm.shiny.com.tw/images/logo.png"
        publisher_url = self.publisher_url.get().strip() if hasattr(self, 'publisher_url') else "https://pm.shiny.com.tw/"
        publisher_logo_width = self.publisher_logo_width.get().strip() if hasattr(self, 'publisher_logo_width') else ""
        publisher_logo_height = self.publisher_logo_height.get().strip() if hasattr(self, 'publisher_logo_height') else ""
        publisher_sameas_str = self.publisher_sameas.get().strip() if hasattr(self, 'publisher_sameas') else ""
        publisher_sameas = [u.strip() for u in publisher_sameas_str.split(",") if u.strip()]

        # 以文章編號推導頁面 URL（如: https://pm.shiny.com.tw/news-detail.php?id=XXXX）
        page_id = self.article_num.get().strip()
        main_entity_of_page = None
        if page_id and page_id.isdigit():
            main_entity_of_page = {
                "@id": f"https://pm.shiny.com.tw/news-detail.php?id={page_id}",
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
        h1 = self.h1.get().strip()
        if h1:
            p.append(f"<h1>{self._esc(h1)}</h1>")
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
                    "publisher_logo_url": (self.publisher_logo_url.get().strip() if hasattr(self, 'publisher_logo_url') else "https://pm.shiny.com.tw/images/logo.png"),
                    "publisher_url": (self.publisher_url.get().strip() if hasattr(self, 'publisher_url') else "https://pm.shiny.com.tw/"),
                    "publisher_logo_width": (self.publisher_logo_width.get().strip() if hasattr(self, 'publisher_logo_width') else ""),
                    "publisher_logo_height": (self.publisher_logo_height.get().strip() if hasattr(self, 'publisher_logo_height') else ""),
                    "publisher_sameas": ([u.strip() for u in (self.publisher_sameas.get().split(',') if hasattr(self, 'publisher_sameas') else []) if u.strip()])
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
        self.author.delete(0, tk.END); self.author.insert(0, seo.get("author", "炫麗鑫"))
        self.pub_date.delete(0, tk.END); self.pub_date.insert(0, seo.get("pub_date", datetime.today().strftime('%Y-%m-%d')))
        self.mod_date.delete(0, tk.END); self.mod_date.insert(0, seo.get("mod_date", datetime.today().strftime('%Y-%m-%d')))
        self.org_name.delete(0, tk.END); self.org_name.insert(0, seo.get("org_name", "Shiny黃金白銀"))
        self.article_num.delete(0, tk.END); self.article_num.insert(0, seo.get("article_num", str(get_article_number())))
        self.headline.delete(0, tk.END); self.headline.insert(0, seo.get("headline", ""))
        self.description.delete(0, tk.END); self.description.insert(0, seo.get("description", ""))
        # 新增欄位
        if hasattr(self, 'author_type'): self.author_type.set(seo.get("author_type", "Organization"))
        if hasattr(self, 'publisher_logo_url'):
            self.publisher_logo_url.delete(0, tk.END); self.publisher_logo_url.insert(0, seo.get("publisher_logo_url", "https://pm.shiny.com.tw/images/logo.png"))
        if hasattr(self, 'publisher_url'):
            self.publisher_url.delete(0, tk.END); self.publisher_url.insert(0, seo.get("publisher_url", "https://pm.shiny.com.tw/"))
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
        css = (
            ".seo-article-content {"
            "font-family: 'Noto Sans TC', sans-serif; line-height: 1.7; color: #343a40; background-color: #ffffff; font-size: 16px;}"
            ".seo-article-content h1, .seo-article-content h2, .seo-article-content h3 {"
            "font-family: 'Noto Serif TC', serif; color: #1a1a1a; line-height: 1.3;}"
            ".seo-article-content h1 {font-size: 2.5em; text-align: center; margin-bottom: 20px; color: #b08d57;}"
            ".seo-article-content h2 {font-size: 1.8em; margin-top: 50px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #b08d57;}"
            ".seo-article-content h3 {font-size: 1.3em; margin-top: 30px; margin-bottom: 10px; color: #343a40;}"
            ".seo-article-content p {margin-bottom: 1.2em; font-size: 1em;}"
            ".seo-article-content ul {list-style-type: none; padding-left: 20px;}"
            ".seo-article-content ul li {position: relative; padding-left: 25px; margin-bottom: 10px;}"
            ".seo-article-content ul li::before {content: '•'; color: #b08d57; font-size: 1.5em; position: absolute; left: 0; top: -4px;}"
            ".seo-article-content .intro-summary {background-color: #f8f9fa; border-left: 5px solid #D8AB4C; padding: 1rem 1.5rem; margin: 1rem 0; font-size: 1.1em;}"
            "section.intro-summary p {margin: 0 0 4px;}"
            ".seo-article-content strong {color: #1a1a1a;}"
            ".seo-article-content img {max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 30px;}"
            ".seo-article-content table {width: 100%; border-collapse: collapse; margin: 30px 0; font-size: 0.95em;}"
            ".seo-article-content th, .seo-article-content td {padding: 12px 15px; text-align: left; border-bottom: 1px solid #dee2e6;}"
            ".seo-article-content thead th {background-color: #343a40; color: #ffffff; font-weight: 700;}"
            ".seo-article-content tbody tr:nth-of-type(even) {background-color: #f8f9fa;}"
            ".seo-article-content tbody tr:hover {background-color: #e9ecef;}"
            ".seo-article-content hr {border: 0; height: 1px; background-color: #dee2e6; margin: 60px 0;}"
            ".nowrap {white-space: nowrap;}"
        )
        schema = self._gen_schema_jsonld()
        title = self.h1.get().strip() or "文章"
        html = (
            '<!DOCTYPE html>'
            '<html>'
            '<head>'
            '<meta charset="UTF-8">'
            f'<title>{title}</title>'
            f'<style>{css}</style>'
            f'{schema}'
            '</head>'
            '<body>'
            f'<article class="seo-article-content">{body}</article>'
            '</body>'
            '</html>'
        )
        fp = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML","*.html")])
        if fp:
            with open(fp, "w", encoding="utf-8") as f: f.write(html)
            messagebox.showinfo("完成", f"已匯出: {fp}")
    
    def _preview_browser(self):
        """從預覽窗格的 HTML 原始碼產生瀏覽器預覽"""
        body = self._gen()
        css = (
            ".seo-article-content {"
            "font-family: 'Noto Sans TC', sans-serif; line-height: 1.7; color: #343a40; background-color: #ffffff; font-size: 16px;}"
            ".seo-article-content h1, .seo-article-content h2, .seo-article-content h3 {"
            "font-family: 'Noto Serif TC', serif; color: #1a1a1a; line-height: 1.3;}"
            ".seo-article-content h1 {font-size: 2.5em; text-align: center; margin-bottom: 20px; color: #b08d57;}"
            ".seo-article-content h2 {font-size: 1.8em; margin-top: 50px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #b08d57;}"
            ".seo-article-content h3 {font-size: 1.3em; margin-top: 30px; margin-bottom: 10px; color: #343a40;}"
            ".seo-article-content p {margin-bottom: 1.2em; font-size: 1em;}"
            ".seo-article-content ul {list-style-type: none; padding-left: 20px;}"
            ".seo-article-content ul li {position: relative; padding-left: 25px; margin-bottom: 10px;}"
            ".seo-article-content ul li::before {content: '•'; color: #b08d57; font-size: 1.5em; position: absolute; left: 0; top: -4px;}"
            ".seo-article-content .intro-summary {background-color: #f8f9fa; border-left: 5px solid #D8AB4C; padding: 1rem 1.5rem; margin: 1rem 0; font-size: 1.1em;}"
            "section.intro-summary p {margin: 0 0 4px;}"
            ".seo-article-content strong {color: #1a1a1a;}"
            ".seo-article-content img {max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 30px;}"
            ".seo-article-content table {width: 100%; border-collapse: collapse; margin: 30px 0; font-size: 0.95em;}"
            ".seo-article-content th, .seo-article-content td {padding: 12px 15px; text-align: left; border-bottom: 1px solid #dee2e6;}"
            ".seo-article-content thead th {background-color: #343a40; color: #ffffff; font-weight: 700;}"
            ".seo-article-content tbody tr:nth-of-type(even) {background-color: #f8f9fa;}"
            ".seo-article-content tbody tr:hover {background-color: #e9ecef;}"
            ".seo-article-content hr {border: 0; height: 1px; background-color: #dee2e6; margin: 60px 0;}"
            ".nowrap {white-space: nowrap;}"
        )
        schema = self._gen_schema_jsonld()
        title = self.h1.get().strip() or "預覽"
        html = (
            '<!DOCTYPE html>'
            '<html>'
            '<head>'
            '<meta charset="UTF-8">'
            f'<title>{title}</title>'
            f'<style>{css}</style>'
            f'{schema}'
            '</head>'
            '<body>'
            f'<article class="seo-article-content">{body}</article>'
            '</body>'
            '</html>'
        )
        os.makedirs(OUT, exist_ok=True)
        pp = os.path.join(OUT, "preview_temp.html")
        with open(pp, "w", encoding="utf-8") as f: f.write(html)
        webbrowser.open(pp)
    
    def _load_ex(self):
        ex = {
            "seo": {
                "author": "炫麗鑫",
                "pub_date": datetime.today().strftime('%Y-%m-%d'),
                "mod_date": datetime.today().strftime('%Y-%m-%d'),
                "org_name": "Shiny黃金白銀",
                "article_num": str(get_article_number()),
                "headline": "黃金投資完整指南",
                "description": "了解黃金投資的優勢與策略",
                "author_type": "Organization",
                "publisher_logo_url": "https://pm.shiny.com.tw/images/logo.png",
                "publisher_url": "https://pm.shiny.com.tw/",
                "publisher_logo_width": "",
                "publisher_logo_height": "",
                "publisher_sameas": []
            },
            "h1": "黃金投資指南",
            "intro": "黃金是重要的避險資產。",
            "sections": [{"h2": "為何投資?", "content": "保值、避險。", "h3s": []}],
            "faqs": [{"question": "適合新手嗎?", "answer": "適合。"}]
        }
        self._load(ex); self.mod = False
    
    def _cls(self):
        if self.mod and messagebox.askyesno("未儲存", "要儲存嗎?"): self.sv()
        self.root.destroy()

def main():
    root = tb.Window(themename="darkly") if HAS_TTK else tk.Tk()
    Editor(root); root.mainloop()

if __name__ == "__main__": main()
