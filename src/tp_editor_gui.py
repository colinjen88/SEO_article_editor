# -*- coding: utf-8 -*-
"""視覺化 SEO 文章編輯器"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os, json, webbrowser
from datetime import datetime

try:
    import ttkbootstrap as tb
    HAS_TTK = True
except: HAS_TTK = False

BASE = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(BASE, "output")

class SecBlock:
    def __init__(self, p, oc, od):
        self.f = ttk.LabelFrame(p, text="段落", padding=10)
        self.f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.f, text="H2:").pack(anchor=tk.W)
        self.h2 = ttk.Entry(self.f); self.h2.pack(fill=tk.X, pady=(0,5)); self.h2.bind("<KeyRelease>", lambda e: oc())
        ttk.Label(self.f, text="內容:").pack(anchor=tk.W)
        self.ct = tk.Text(self.f, height=6, wrap=tk.WORD); self.ct.pack(fill=tk.BOTH, expand=True, pady=(0,5)); self.ct.bind("<KeyRelease>", lambda e: oc())
        ttk.Button(self.f, text="刪除", command=lambda: [self.f.destroy(), od(self)]).pack(anchor=tk.E)
    def get_h2(self): return self.h2.get().strip()
    def get_ct(self): return self.ct.get("1.0", tk.END).strip()
    def set_h2(self, t): self.h2.delete(0, tk.END); self.h2.insert(0, t)
    def set_ct(self, t): self.ct.delete("1.0", tk.END); self.ct.insert("1.0", t)
    def to_dict(self): return {"h2": self.get_h2(), "content": self.get_ct()}

class FaqBlock:
    def __init__(self, p, oc, od):
        self.f = ttk.LabelFrame(p, text="QA", padding=10)
        self.f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.f, text="問題:").pack(anchor=tk.W)
        self.q = ttk.Entry(self.f); self.q.pack(fill=tk.X, pady=(0,5)); self.q.bind("<KeyRelease>", lambda e: oc())
        ttk.Label(self.f, text="答案:").pack(anchor=tk.W)
        self.a = tk.Text(self.f, height=4, wrap=tk.WORD); self.a.pack(fill=tk.BOTH, expand=True, pady=(0,5)); self.a.bind("<KeyRelease>", lambda e: oc())
        ttk.Button(self.f, text="刪除", command=lambda: [self.f.destroy(), od(self)]).pack(anchor=tk.E)
    def get_q(self): return self.q.get().strip()
    def get_a(self): return self.a.get("1.0", tk.END).strip()
    def set_q(self, t): self.q.delete(0, tk.END); self.q.insert(0, t)
    def set_a(self, t): self.a.delete("1.0", tk.END); self.a.insert("1.0", t)
    def to_dict(self): return {"question": self.get_q(), "answer": self.get_a()}

class Editor:
    def __init__(self, root):
        self.root = root; self.root.title("視覺化編輯器"); self.root.geometry("1400x800")
        self.cf = None; self.mod = False; self.secs = []; self.faqs = []
        self.root.protocol("WM_DELETE_WINDOW", self._cls); self._ui()
    
    def _ui(self):
        tb = ttk.Frame(self.root); tb.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(tb, text="開啟", command=self.op).pack(side=tk.LEFT)
        ttk.Button(tb, text="儲存", command=self.sv).pack(side=tk.LEFT)
        ttk.Button(tb, text="匯出", command=self.ex).pack(side=tk.LEFT)
        ttk.Button(tb, text="預覽", command=self.prv).pack(side=tk.LEFT)
        
        pn = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        pn.pack(fill=tk.BOTH, expand=True)
        
        lf = ttk.Frame(pn); pn.add(lf, weight=1)
        cv = tk.Canvas(lf); sb = ttk.Scrollbar(lf, command=cv.yview)
        self.sf = ttk.Frame(cv)
        self.sf.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0,0), window=self.sf, anchor="nw"); cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        h1f = ttk.LabelFrame(self.sf, text="H1", padding=10); h1f.pack(fill=tk.X, padx=5, pady=5)
        self.h1 = ttk.Entry(h1f); self.h1.pack(fill=tk.X); self.h1.bind("<KeyRelease>", lambda e: self._chg())
        
        inf = ttk.LabelFrame(self.sf, text="前言", padding=10); inf.pack(fill=tk.X, padx=5, pady=5)
        self.intro = tk.Text(inf, height=6, wrap=tk.WORD); self.intro.pack(fill=tk.BOTH); self.intro.bind("<KeyRelease>", lambda e: self._chg())
        
        self.scf = ttk.LabelFrame(self.sf, text="主內容", padding=10); self.scf.pack(fill=tk.X, padx=5, pady=5)
        self.scc = ttk.Frame(self.scf); self.scc.pack(fill=tk.X)
        ttk.Button(self.scf, text="+ 段落", command=self.add_sec).pack()
        
        self.fqf = ttk.LabelFrame(self.sf, text="FAQ", padding=10); self.fqf.pack(fill=tk.X, padx=5, pady=5)
        self.fqc = ttk.Frame(self.fqf); self.fqc.pack(fill=tk.X)
        ttk.Button(self.fqf, text="+ QA", command=self.add_faq).pack()
        
        rf = ttk.LabelFrame(pn, text="預覽", padding=5); pn.add(rf, weight=1)
        self.pv = scrolledtext.ScrolledText(rf, wrap=tk.WORD, state=tk.DISABLED)
        self.pv.pack(fill=tk.BOTH, expand=True)
        
        self._load_ex(); self.upd()
    
    def add_sec(self): s = SecBlock(self.scc, self._chg, lambda x: [self.secs.remove(x), self._chg()]); self.secs.append(s); self._chg()
    def add_faq(self): f = FaqBlock(self.fqc, self._chg, lambda x: [self.faqs.remove(x), self._chg()]); self.faqs.append(f); self._chg()
    
    def _chg(self):
        self.mod = True
        if hasattr(self, "_tm"): self.root.after_cancel(self._tm)
        self._tm = self.root.after(500, self.upd)
    
    def upd(self):
        h = self._gen()
        self.pv.config(state=tk.NORMAL); self.pv.delete("1.0", tk.END); self.pv.insert("1.0", h); self.pv.config(state=tk.DISABLED)
    
    def _gen(self):
        p = []
        h1 = self.h1.get().strip()
        if h1: p.append(f"<h1>{self._esc(h1)}</h1>")
        intro = self.intro.get("1.0", tk.END).strip()
        if intro:
            p.append('<section class="intro">')
            for pa in intro.split("\n\n"):
                if pa.strip(): p.append(f"  <p>{self._esc(pa.strip())}</p>")
            p.append("</section>")
        for s in self.secs:
            h2, ct = s.get_h2(), s.get_ct()
            if h2 or ct:
                p.append("<section>")
                if h2: p.append(f"  <h2>{self._esc(h2)}</h2>")
                if ct:
                    for pa in ct.split("\n\n"):
                        if pa.strip(): p.append(f"  <p>{self._esc(pa.strip())}</p>")
                p.append("</section>")
        if self.faqs:
            p.append('<section id="faq">')
            p.append('  <h2 class="visually-hidden">FAQ</h2>')
            for f in self.faqs:
                q, a = f.get_q(), f.get_a()
                if q or a:
                    if q: p.append(f"  <h3>{self._esc(q)}</h3>")
                    if a:
                        for pa in a.split("\n\n"):
                            if pa.strip(): p.append(f"  <p>{self._esc(pa.strip())}</p>")
            p.append("</section>")
        return "\n".join(p)
    
    def _esc(self, t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    
    def op(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if fp:
            with open(fp, encoding="utf-8") as f: d = json.load(f)
            self._load(d); self.cf = fp; self.mod = False; self.upd()
    
    def sv(self):
        if not self.cf: self.cf = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if self.cf:
            d = {"h1": self.h1.get().strip(), "intro": self.intro.get("1.0", tk.END).strip(), "sections": [s.to_dict() for s in self.secs], "faqs": [f.to_dict() for f in self.faqs]}
            with open(self.cf, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
            self.mod = False
    
    def _load(self, d):
        self.h1.delete(0, tk.END); self.intro.delete("1.0", tk.END)
        for s in self.secs: s.f.destroy()
        for f in self.faqs: f.f.destroy()
        self.secs.clear(); self.faqs.clear()
        self.h1.insert(0, d.get("h1","")); self.intro.insert("1.0", d.get("intro",""))
        for sd in d.get("sections",[]): self.add_sec(); self.secs[-1].set_h2(sd.get("h2","")); self.secs[-1].set_ct(sd.get("content",""))
        for fd in d.get("faqs",[]): self.add_faq(); self.faqs[-1].set_q(fd.get("question","")); self.faqs[-1].set_a(fd.get("answer",""))
    
    def ex(self):
        body = self._gen()
        css = "body{font-family:Arial;max-width:900px;margin:0 auto;padding:20px}h1{color:#2c3e50}h2{color:#34495e}section{margin:20px 0}.visually-hidden{position:absolute;width:1px;height:1px;overflow:hidden}"
        html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{self.h1.get().strip()}</title><style>{css}</style></head><body>{body}</body></html>'
        fp = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML","*.html")])
        if fp:
            with open(fp, "w", encoding="utf-8") as f: f.write(html)
            messagebox.showinfo("完成", f"已匯出: {fp}")
    
    def prv(self):
        body = self._gen()
        css = "body{font-family:Arial;max-width:900px;margin:0 auto;padding:20px}h1{color:#2c3e50}h2{color:#34495e}section{margin:20px 0}.visually-hidden{position:absolute;width:1px;height:1px;overflow:hidden}"
        html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>預覽</title><style>{css}</style></head><body>{body}</body></html>'
        os.makedirs(OUT, exist_ok=True); pp = os.path.join(OUT, "preview.html")
        with open(pp, "w", encoding="utf-8") as f: f.write(html)
        webbrowser.open(pp)
    
    def _load_ex(self):
        ex = {"h1":"黃金投資指南","intro":"黃金是重要的避險資產。","sections":[{"h2":"為何投資?","content":"保值、避險。"}],"faqs":[{"question":"適合新手嗎?","answer":"適合。"}]}
        self._load(ex); self.mod = False
    
    def _cls(self):
        if self.mod and messagebox.askyesno("未儲存", "要儲存嗎?"): self.sv()
        self.root.destroy()

def main():
    root = tb.Window(themename="flatly") if HAS_TTK else tk.Tk()
    Editor(root); root.mainloop()

if __name__ == "__main__": main()
