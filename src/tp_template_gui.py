import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
from datetime import datetime
import docx
import json

# tp 標記解析規則
TP_H1 = r'\(tp_h1\)(.*)'
TP_H2 = r'\(tp_h2\)(.*)'
TP_H3 = r'\(tp_h3\)(.*)'
TP_SEC = r'\(tp_sec\)'
TP_SEC_QA = r'\(tp_sec_qa\)'
TP_H3_Q = r'\(tp_h3_q\)(.*)'
TP_ANS = r'\(tp_ans\)(.*)'
TP_MARK = r'\(tp_[a-zA-Z0-9_]+\)'

class TPTemplateParser:
    def __init__(self):
        self.faq_questions = []
        self.faq_answers = []

    def parse(self, lines):
        html = []
        i = 0
        n = len(lines)
        in_faq_section = False
        
        while i < n:
            line = lines[i].strip()
            if re.match(TP_H1, line):
                content = re.sub(TP_H1, r'\1', line).strip()
                html.append(f'<h1>{content}</h1>')
                i += 1
                continue
            if re.match(TP_H2, line):
                content = re.sub(TP_H2, r'\1', line).strip()
                html.append(f'<h2>{content}</h2>')
                i += 1
                continue
            if re.match(TP_H3, line):
                content = re.sub(TP_H3, r'\1', line).strip()
                html.append(f'<h3>{content}</h3>')
                i += 1
                continue
            if re.match(TP_SEC, line):
                sec_content = []
                i += 1
                while i < n and not re.match(TP_MARK, lines[i]):
                    sec_content.append(lines[i])
                    i += 1
                html.append('<section>')
                html.extend(sec_content)
                html.append('</section>')
                continue
            if re.match(TP_SEC_QA, line):
                if in_faq_section:
                    html.append('</section>')
                html.append('<section id="faq-section">')
                in_faq_section = True
                i += 1
                continue
            if re.match(TP_H3_Q, line):
                q = re.sub(TP_H3_Q, r'\1', line).strip()
                html.append(f'<h3>{q}</h3>')
                self.faq_questions.append(q)
                i += 1
                continue
            if re.match(TP_ANS, line):
                a = re.sub(TP_ANS, r'\1', line).strip()
                html.append(f'<p>{a}</p>')
                self.faq_answers.append(a)
                i += 1
                continue
            if not re.match(TP_MARK, line):
                html.append(line)
            i += 1
        
        # 確保FAQ section有結束標籤
        if in_faq_section:
            html.append('</section>')
        
        return html

    def build_faq_json(self):
        faq_json = []
        for idx, (q, a) in enumerate(zip(self.faq_questions, self.faq_answers)):
            faq_json.append(f'{{"@type": "Question", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}, "name": "{q}"}}')
        return ',\n'.join(faq_json)

# GUI
class TPTemplateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("tp 標記 Word 轉 SEO HTML 工具")
        tk.Label(root, text="選擇 Word 檔").grid(row=0, column=0)
        self.word_path = tk.Entry(root, width=50)
        self.word_path.grid(row=0, column=1)
        tk.Button(root, text="瀏覽", command=self.select_word).grid(row=0, column=2)
        tk.Button(root, text="產生 HTML", command=self.generate_html).grid(row=1, column=0, columnspan=3)

    def select_word(self):
        path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if path:
            self.word_path.delete(0, tk.END)
            self.word_path.insert(0, path)

    def generate_html(self):
        path = self.word_path.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("錯誤", "請選擇 Word 檔")
            return
        doc = docx.Document(path)
        # 只抓純文字內容
        lines = [p.text for p in doc.paragraphs if p.text.strip()]
        parser = TPTemplateParser()
        html_body = parser.parse(lines)
        # 安全組裝 JSON-LD（避免手動字串格式化）
        faq_items = []
        for q, a in zip(parser.faq_questions, parser.faq_answers):
            faq_items.append({
                "@type": "Question",
                "acceptedAnswer": {"@type": "Answer", "text": a},
                "name": q
            })
        article_json = {
            "@context": "https://schema.org",
            "@type": "Article",
            "dateModified": datetime.today().strftime('%Y%m%d'),
            "datePublished": datetime.today().strftime('%Y%m%d'),
            "mainEntity": {
                "@type": "FAQPage",
                "mainEntity": faq_items
            }
        }
        faq_json_text = json.dumps(article_json, ensure_ascii=False, indent=4)
        today = datetime.today().strftime('%Y%m%d')
        seo_json = f'<script type="application/ld+json">\n{faq_json_text}\n</script>'
        # 檔名自動加日期與流水號
        base_name = f"output_{today}.html"
        out_path = base_name
        idx = 1
        while os.path.exists(out_path):
            out_path = f"output_{today}_{idx}.html"
            idx += 1
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(seo_json + "\n" + "\n".join(html_body))
        messagebox.showinfo("完成", f"已產生 {out_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TPTemplateGUI(root)
    root.mainloop()
