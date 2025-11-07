"""
SEO 文章編輯器 - 主程式
直接啟動 SEO 文章編輯器
"""

import os
import sys
# 強制提早載入 tkinter，確保 PyInstaller 打包時被收集
try:
    import tkinter  # noqa: F401
    import tkinter.ttk  # noqa: F401
    import tkinter.scrolledtext  # noqa: F401
except Exception:
    # 在開發環境中若無 tkinter，也不阻擋；打包時仍由 hiddenimports 收集
    pass

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
        # 嘗試從 src 目錄 import（開發環境）
        import tp_editor_gui
        tp_editor_gui.main()
    except ImportError as e:
        # 顯示錯誤訊息以便診斷
        print(f"Import error: {e}")
        print(f"sys.path: {sys.path}")
        raise


if __name__ == "__main__":
    main()
