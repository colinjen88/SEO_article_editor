import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime

# 產生 FAQ 結構化資料
FAQ_TEMPLATE = '{{"@type": "Question","acceptedAnswer": {{"@type": "Answer","text": "{answer}"}},"name": "{question}"}}'

# 產生 SEO 結構化資料
SEO_TEMPLATE = '''<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "Article",
    "author": {{"@type": "Organization", "name": "炫麗鑫"}},
    "dateModified": "{dateModified}",
    "datePublished": "{datePublished}",
    "description": "{description}",
    "headline": "{headline}",
    "image": "",
    "mainEntity": {{
        "@type": "FAQPage",
        "mainEntity": [
            {faq_json}
        ]
    }},
    "mainEntityOfPage": {{"@id": "https://pm.shiny.com.tw/news-detail.php?id={mainEntityId}", "@type": "WebPage"}},
    "publisher": {{"@type": "Organization", "logo": {{"@type": "ImageObject", "url": "https://pm.shiny.com.tw/images/logo.png"}}, "name": "Shiny黃金白銀"}}
}}
</script>'''

# GUI 主程式
class SEOArticleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SEO 文章 HTML 產生器")
        self.sections = []
        # SEO 基本欄位
        tk.Label(root, text="主標題 (h1)").grid(row=0, column=0)
        self.headline = tk.Entry(root, width=50)
        self.headline.grid(row=0, column=1, columnspan=3)
        today = datetime.today().strftime('%Y-%m-%d')
        tk.Label(root, text="文章日期 (YYYY-MM-DD)").grid(row=1, column=0)
        self.articleDate = tk.Entry(root)
        self.articleDate.insert(0, today)
        self.articleDate.grid(row=1, column=1)
        tk.Label(root, text="mainEntityOfPage id (數字)").grid(row=2, column=0)
        self.mainEntityId = tk.Entry(root)
        self.mainEntityId.grid(row=2, column=1)
        tk.Label(root, text="description").grid(row=2, column=2)
        self.description = tk.Entry(root, width=30)
        self.description.grid(row=2, column=3)
        # 段落區
        tk.Label(root, text="段落 (section)").grid(row=3, column=0)
        self.section_frame = tk.Frame(root)
        self.section_frame.grid(row=4, column=0, columnspan=4, sticky="w")
        self.add_section_btn = tk.Button(root, text="新增段落", command=self.add_section)
        self.add_section_btn.grid(row=3, column=1)
        # Q&A 區
        tk.Label(root, text="Q&A (FAQ)").grid(row=5, column=0)
        self.qa_entries = []
        for i in range(3):
            q_entry = tk.Entry(root, width=40)
            a_entry = tk.Entry(root, width=60)
            tk.Label(root, text=f"Q{i+1}").grid(row=6+i, column=0)
            q_entry.grid(row=6+i, column=1)
            tk.Label(root, text=f"A{i+1}").grid(row=6+i, column=2)
            a_entry.grid(row=6+i, column=3)
            self.qa_entries.append((q_entry, a_entry))
        # 產生 HTML
        tk.Button(root, text="產生 HTML", command=self.generate_html).grid(row=9, column=0, columnspan=4)

    def add_section(self):
        idx = len(self.sections)
        frame = tk.Frame(self.section_frame)
        tk.Label(frame, text=f"段落{idx+1} 標題(h2)").grid(row=0, column=0)
        h2_entry = tk.Entry(frame, width=40)
        h2_entry.grid(row=0, column=1)
        tk.Label(frame, text="內容").grid(row=1, column=0)
        content_text = scrolledtext.ScrolledText(frame, width=60, height=4)
        content_text.grid(row=1, column=1)
        frame.pack(anchor="w", pady=2)
        self.sections.append((h2_entry, content_text))

    def generate_html(self):
        headline = self.headline.get().strip()
        date_val = self.articleDate.get().strip()
        mainEntityId = self.mainEntityId.get().strip()
        description = self.description.get().strip()
        # FAQ JSON（使用 json.dumps 確保字元安全）
        faq_items = []
        for q, a in self.qa_entries:
            qv = q.get().strip()
            av = a.get().strip()
            if qv and av:
                faq_items.append({
                    "@type": "Question",
                    "acceptedAnswer": {"@type": "Answer", "text": av},
                    "name": qv
                })
        faq_json = ",\n            ".join([json.dumps(item, ensure_ascii=False) for item in faq_items])
        # SEO script
        seo_script = SEO_TEMPLATE.format(
            dateModified=date_val,
            datePublished=date_val,
            mainEntityId=mainEntityId,
            description=description,
            headline=headline,
            faq_json=faq_json
        )
        # HTML 主體
        html = [seo_script]
        html.append('<article class="seo-article-content">')
        html.append(f'<h1>{headline}</h1>')
        for h2_entry, content_text in self.sections:
            h2 = h2_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip().replace("\n", "<br>")
            if h2 and content:
                html.append(f'<section>\n<h2>{h2}</h2>\n<p>{content}</p>\n</section>')
        html.append('<hr />')
        html.append('<section>\n<h2>常見問答 (Q&amp;A)</h2>')
        for i, (q, a) in enumerate(self.qa_entries):
            qv = q.get().strip()
            av = a.get().strip()
            if qv and av:
                html.append(f'<h3>{qv}</h3>\n<p>{av}</p>')
        html.append('</section>')
        html.append('<div class="article-footer">\n<p><strong>炫麗Shiny 黃金白銀交易所</strong> <span data-article-author="炫麗小編" style="font-size: 12px;color: #cf79a6;">炫麗小編</span></p>\n<em>僅供參考，恕不代表本站立場</em>\n</div>')
        html.append('</article>')
        # 預設輸出檔名 output_YYYYMMDD[_N].html
        today_name = datetime.today().strftime('%Y%m%d')
        base = f"output_{today_name}.html"
        candidate = base
        idx = 1
        while os.path.exists(candidate):
            candidate = f"output_{today_name}_{idx}.html"
            idx += 1
        out_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")], initialfile=candidate)
        if out_path:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(html))
            messagebox.showinfo("完成", f"已產生 HTML：{out_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SEOArticleGUI(root)
    root.mainloop()
