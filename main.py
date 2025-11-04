"""
SEO 文章工具 - 主程式
提供工具選單，讓使用者選擇要啟動的工具
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(BASE_DIR, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 嘗試匯入美化套件
try:
    import ttkbootstrap as tb
    HAS_TTKBOOTSTRAP = True
except Exception:
    HAS_TTKBOOTSTRAP = False


class MainLauncher:
    """主啟動器 - 工具選單"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SEO 文章工具 v1.3")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 建立 UI
        self._setup_ui()
        
    def _setup_ui(self):
        """建立使用者介面"""
        
        # 標題
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame,
            text="📝 SEO 文章工具",
            font=("Microsoft JhengHei", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="請選擇要使用的工具",
            font=("Microsoft JhengHei", 10)
        )
        subtitle_label.pack(pady=5)
        
        # 工具按鈕區域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        
        # 工具選項
        tools = [
            {
                "name": "⭐ SEO Layout GUI（推薦）",
                "desc": "Word 轉 HTML，完整 SEO 功能",
                "module": "seo_layout_gui"
            },
            {
                "name": "✏️ TP 標記編輯器（新）",
                "desc": "簡易文字編輯器，即時預覽",
                "module": "tp_editor_gui"
            },
            {
                "name": "📄 SEO 文章編輯",
                "desc": "手動編輯 SEO 文章",
                "module": "seo_article_gui"
            },
            {
                "name": "📋 TP 模板解析",
                "desc": "解析 tp 標記檔案",
                "module": "tp_template_gui"
            },
            {
                "name": "📑 Word 轉 HTML",
                "desc": "Word 文件轉換工具",
                "module": "docx_to_seo_html_gui"
            }
        ]
        
        for tool in tools:
            self._create_tool_button(button_frame, tool)
            
        # 底部資訊
        info_frame = ttk.Frame(self.root)
        info_frame.pack(side=tk.BOTTOM, pady=10)
        
        info_label = ttk.Label(
            info_frame,
            text="© 2025 SEO 文章工具 | 版本 v1.3",
            font=("Microsoft JhengHei", 8)
        )
        info_label.pack()
        
    def _create_tool_button(self, parent, tool):
        """建立工具按鈕"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        btn = ttk.Button(
            frame,
            text=tool["name"],
            command=lambda: self._launch_tool(tool["module"]),
            width=40
        )
        btn.pack(fill=tk.X)
        
        desc_label = ttk.Label(
            frame,
            text=tool["desc"],
            font=("Microsoft JhengHei", 8),
            foreground="gray"
        )
        desc_label.pack(anchor=tk.W, padx=20)
        
    def _launch_tool(self, module_name):
        """啟動選定的工具"""
        self.root.destroy()
        import runpy
        runpy.run_path(os.path.join(src_dir, f'{module_name}.py'), run_name='__main__')


def main():
    """主程式進入點"""
    # 檢查是否有命令列參數直接啟動特定工具
    if len(sys.argv) > 1:
        tool = sys.argv[1]
        import runpy
        tool_map = {
            'layout': 'seo_layout_gui.py',
            'editor': 'tp_editor_gui.py',
            'article': 'seo_article_gui.py',
            'template': 'tp_template_gui.py',
            'docx': 'docx_to_seo_html_gui.py'
        }
        if tool in tool_map:
            runpy.run_path(os.path.join(src_dir, tool_map[tool]), run_name='__main__')
            return
    
    # 顯示選單
    if HAS_TTKBOOTSTRAP:
        try:
            root = tb.Window(themename='flatly')
        except Exception:
            root = tk.Tk()
    else:
        root = tk.Tk()
        
    app = MainLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
