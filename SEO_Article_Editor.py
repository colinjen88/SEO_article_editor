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
    import runpy
    runpy.run_path(os.path.join(src_dir, 'tp_editor_gui.py'), run_name='__main__')


if __name__ == "__main__":
    main()
