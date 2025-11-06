"""
SEO 文章編輯器 - 主程式
直接啟動 SEO 文章編輯器
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(BASE_DIR, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def main():
    """主程式進入點 - 直接啟動 SEO 文章編輯器"""
    # 直接 import 並執行，而非使用 runpy（pyinstaller 相容）
    from tp_editor_gui import main as editor_main
    editor_main()


if __name__ == "__main__":
    main()
