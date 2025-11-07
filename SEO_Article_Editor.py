"""
SEO 文章編輯器 - 主程式
直接啟動 SEO 文章編輯器
"""

import os
import sys

# 取得當前腳本的絕對路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(BASE_DIR, 'src')

# 將 src 目錄加入 Python 路徑
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 確保當前目錄也在路徑中
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def main():
    """主程式進入點 - 直接啟動 SEO 文章編輯器"""
    try:
        # 直接 import 並執行
        from src.tp_editor_gui import main as editor_main
        editor_main()
    except ImportError:
        # 如果上面失敗，嘗試直接 import（適用於打包後的執行檔）
        import tp_editor_gui
        tp_editor_gui.main()


if __name__ == "__main__":
    main()
