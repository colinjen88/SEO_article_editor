# SEO 文章工具需求與規格說明

## 1. 主要目標
- 將 Word 檔（含 tp 標記）文章，轉換為完全符合 SEO 標準的 HTML。
- 產生的 HTML 結構、內容、樣式必須與指定模板（seo_layout.html）完全一致。

## 2. GUI 功能需求
- 以 tkinter 製作 GUI，欄位包含：
  - 作者（author_name）
  - 文章日期（TheDate）
  - 標題（headline）
  - 描述（description）
  - 組織（OrganizationName）
  - 文章編號（article_number，自動抓取並可確認更新）
  - Word 檔案選擇（word_path）
  - 模板檔案選擇（template_path，預設為 seo_layout.html）
- GUI 欄位內容必須正確填入模板對應 {{xxx}} 標籤。

## 3. FAQ Q&A 自動化
- FAQ Q&A 來源：Word 檔 tp_sec_qa 區塊。
  - 每組 FAQ 由 (tp_h3_q) 問題、(tp_ans) 答案組成。
  - FAQ 數量不限，依 Word 檔內容自動擴充。
- FAQ Q&A 需自動填入：
  - HTML FAQ 區塊（如有 {{QuestionN}}、{{AnswerN}} 標籤則取代，否則不動原文）
  - JSON-LD 結構化資料 mainEntity FAQ 區塊，動態生成所有 Question/Answer，內容正確填入。

### 3.1 JSON-LD 安全更新規範（新增）
- 禁用以正則式直接替換 JSON 文字的作法
- 流程：抽取 `<script type="application/ld+json">` → `json.loads` → 以物件方式更新 → `json.dumps` 回寫
- 更新欄位：`author/dateModified/datePublished/headline/description/mainEntityOfPage/publisher/mainEntity`

## 4. 樣式與結構
- 產生的 HTML 必須完整保留模板 <style> 區塊，不可覆蓋或遺失。
- 其他靜態內容（如 intro-summary、表格、footer）必須與模板一致。

### 4.1 FAQ 區塊缺失處理（新增）
- 若模板缺少 `<section id="faq-section">`，系統將自動在 `</article>` 前插入該區塊並填入 FAQ

## 5. 文章編號自動化
- 文章編號（article_number）自動抓取 article_number.txt，並可於 GUI 內確認更新。

## 6. 檔案命名
- 產生的 HTML 檔案自動命名：`output_YYYYMMDD[_N].html`（N 為流水號，避免覆蓋）

## 7. 錯誤處理
- 若 Word 檔、模板檔案未選擇或不存在，需提示錯誤。
- FAQ 標記格式錯誤時，需提示並不影響其他欄位填入。

## 8. 擴充性
- FAQ Q&A 數量不限，mainEntity FAQ 區塊可自動擴充。
- 模板欄位可自由新增 {{xxx}}，程式自動填入 GUI 對應欄位。

---

如有新需求或細節調整，請直接補充於本說明檔！
