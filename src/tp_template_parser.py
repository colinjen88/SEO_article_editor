import re
from datetime import datetime
import json

# 模板解析規則
TP_H1 = r'\(tp_h1\)(.*)'
TP_H2 = r'\(tp_h2\)(.*)'
TP_H3 = r'\(tp_h3\)(.*)'
TP_SEC = r'\(tp_sec\)'
TP_SEC_QA = r'\(tp_sec_qa\)'
TP_H3_Q = r'\(tp_h3_q\)(.*)'
TP_ANS = r'\(tp_ans\)(.*)'
TP_MARK = r'\(tp_[a-zA-Z0-9_]+\)'

# FAQ 區塊暫存（避免跨次呼叫殘留狀態，於 parse_template 開頭重置）
faq_questions = []
faq_answers = []

# 解析主函式
def parse_template(lines):
    global faq_questions, faq_answers
    faq_questions = []
    faq_answers = []
    html = []
    i = 0
    n = len(lines)
    in_faq_section = False
    
    while i < n:
        line = lines[i].strip()
        # h1~h3 標題
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
        # section 區塊
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
        # FAQ section 開始
        if re.match(TP_SEC_QA, line):
            if in_faq_section:
                html.append('</section>')
            html.append('<section id="faq-section">')
            in_faq_section = True
            i += 1
            continue
        # FAQ 問題
        if re.match(TP_H3_Q, line):
            q = re.sub(TP_H3_Q, r'\1', line).strip()
            html.append(f'<h3>{q}</h3>')
            faq_questions.append(q)
            i += 1
            continue
        # FAQ 答案
        if re.match(TP_ANS, line):
            a = re.sub(TP_ANS, r'\1', line).strip()
            html.append(f'<p>{a}</p>')
            faq_answers.append(a)
            i += 1
            continue
        # 其他內容
        if not re.match(TP_MARK, line):
            html.append(line)
        i += 1
    
    # 確保FAQ section有結束標籤
    if in_faq_section:
        html.append('</section>')
    
    return html

def build_faq_json():
    items = []
    for q, a in zip(faq_questions, faq_answers):
        items.append({
            "@type": "Question",
            "acceptedAnswer": {"@type": "Answer", "text": a},
            "name": q
        })
    return json.dumps(items, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 範例：讀取模板檔
    with open("template.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    html_body = parse_template(lines)
    faq_items_text = build_faq_json()
    # 產生 SEO 結構化資料（JSON 安全）
    today = datetime.today().strftime('%Y%m%d')
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "dateModified": today,
        "datePublished": today,
        "mainEntity": {
            "@type": "FAQPage",
            "mainEntity": json.loads(faq_items_text)
        }
    }
    seo_json = '<script type="application/ld+json">\n' + json.dumps(article_json, ensure_ascii=False, indent=4) + '\n</script>'
    # 檔名自動加日期與流水號
    base_name = f"output_{today}.html"
    out_path = base_name
    idx = 1
    import os
    while os.path.exists(out_path):
        out_path = f"output_{today}_{idx}.html"
        idx += 1
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(seo_json + "\n" + "\n".join(html_body))
    print(f"已產生 {out_path}")
