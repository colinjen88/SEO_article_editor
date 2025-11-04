# HTML 模式使用說明

## 功能更新 (2025-11-04)

### 1. 段落內容支援 HTML 表格

**位置**: H2 段落的「內容」區塊

**功能**: 
- ✅ 預設為 **HTML 模式**
- ✅ 可直接貼上 HTML 表格碼
- ✅ 支援所有 HTML 標籤 (`<table>`, `<tr>`, `<td>`, `<strong>`, `<em>`, `<a>` 等)

**使用方式**:
```html
<!-- 直接在「內容」框中貼上 HTML 碼 -->
<table>
  <tr>
    <th>商品</th>
    <th>價格</th>
  </tr>
  <tr>
    <td>黃金條塊</td>
    <td>NT$50,000</td>
  </tr>
</table>
```

**輸出結果**:
- HTML 碼會直接插入,不做轉義
- 保留原始格式和標籤

---

### 2. FAQ 答案支援文字/HTML 切換

**位置**: FAQ 區塊的「答案」欄位

**功能**:
- ✅ 預設為 **純文字模式** (安全模式)
- ✅ 可勾選「HTML 模式」切換
- ✅ HTML 模式支援連結 `<a>` 標籤

**使用方式**:

#### 純文字模式 (預設)
```
這是一般文字答案。
會自動轉義 HTML 標籤,確保安全。
```

#### HTML 模式 (勾選後)
```html
請參考 <a href="https://example.com">官方網站</a> 獲取更多資訊。
或撥打 <strong>0800-123-456</strong> 聯絡我們。
```

**切換方式**:
1. 找到 FAQ 區塊的「答案」標籤旁邊
2. 勾選「HTML 模式」核取方塊
3. 字體會自動切換為等寬字體 (Consolas),方便編輯 HTML

---

### 3. 所有輸入框改為灰底黑字

**範圍**: 
- ✅ SEO 資訊區所有欄位
- ✅ H1 標題
- ✅ 前言
- ✅ H2 段落標題
- ✅ H2 段落內容
- ✅ H3 子段落標題
- ✅ H3 子段落內容
- ✅ FAQ 問題
- ✅ FAQ 答案

**樣式**:
- 背景色: `#fafafa` (淺灰色)
- 文字色: `black` (黑色)
- 字體: `Consolas` (等寬字體,方便編輯程式碼)

**優點**:
- 🎨 視覺清晰,與深色主題形成對比
- 📝 等寬字體適合 HTML 碼編輯
- 👀 提升可讀性

---

## HTML 模式注意事項

### ⚠️ 安全性
- **段落內容**: 預設 HTML 模式,請確保來源可信
- **FAQ 答案**: 預設純文字模式,需手動開啟 HTML 模式

### 📋 HTML 標籤建議

**段落內容適用標籤**:
- `<table>`, `<tr>`, `<th>`, `<td>` - 表格
- `<ul>`, `<ol>`, `<li>` - 清單
- `<strong>`, `<em>` - 粗體/斜體
- `<a href="...">` - 連結
- `<br>` - 換行

**FAQ 答案適用標籤**:
- `<a href="...">` - 連結
- `<strong>`, `<em>` - 強調
- `<br>` - 換行
- `<span style="...">` - 自訂樣式

### 🔍 HTML 輸入格式

**建議做法**:
```html
<!-- 每行保持適當縮排 -->
<table>
  <tr>
    <td>內容</td>
  </tr>
</table>
```

**避免做法**:
```html
<!-- 不要全部擠在一行 -->
<table><tr><td>內容</td></tr></table>
```

---

## 範例

### 範例 1: 段落包含表格

**H2**: 黃金價格比較

**內容** (HTML 模式):
```html
<p>以下是各種黃金商品的價格比較:</p>
<table border="1">
  <tr>
    <th>商品名稱</th>
    <th>重量</th>
    <th>價格</th>
  </tr>
  <tr>
    <td>黃金條塊</td>
    <td>1 兩</td>
    <td>NT$18,000</td>
  </tr>
  <tr>
    <td>黃金飾品</td>
    <td>1 錢</td>
    <td>NT$6,500</td>
  </tr>
</table>
```

### 範例 2: FAQ 包含連結

**問題**: 如何聯絡客服?

**答案** (勾選 HTML 模式):
```html
<p>您可以透過以下方式聯絡我們:</p>
<ul>
  <li>電話: <strong>0800-123-456</strong></li>
  <li>官網: <a href="https://example.com/contact">聯絡我們</a></li>
  <li>Email: <a href="mailto:service@example.com">service@example.com</a></li>
</ul>
```

---

## 儲存格式

JSON 檔案會記錄:
```json
{
  "sections": [
    {
      "h2": "段落標題",
      "content": "<table>...</table>"
    }
  ],
  "faqs": [
    {
      "question": "問題",
      "answer": "<a href=\"...\">連結</a>",
      "is_html": true
    }
  ]
}
```

---

**文件更新**: 2025-11-04  
**相關工具**: SEO Article Editor v2.0
