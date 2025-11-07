# Runtime hook: 設定嵌入式 tcl/tk 的環境變數，避免 tkinter 在打包後找不到動態資源
import os, sys

# dist 結構: 有一個 tcl 目錄包含 tcl8.x 與 tk8.x
_base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
_tcl_dir = os.path.join(_base, 'tcl')
if os.path.isdir(_tcl_dir):
    # 嘗試找出 tcl 與 tk 子目錄
    _tcl_sub = ''
    _tk_sub = ''
    for name in os.listdir(_tcl_dir):
        if name.startswith('tcl') and os.path.isdir(os.path.join(_tcl_dir, name)):
            _tcl_sub = os.path.join(_tcl_dir, name)
        if name.startswith('tk') and os.path.isdir(os.path.join(_tcl_dir, name)):
            _tk_sub = os.path.join(_tcl_dir, name)
    if _tcl_sub:
        os.environ['TCL_LIBRARY'] = _tcl_sub
    if _tk_sub:
        os.environ['TK_LIBRARY'] = _tk_sub

# 早期載入 tkinter 測試
try:
    import tkinter  # noqa: F401
except Exception as e:
    # 不阻斷主程式，只是記錄
    sys.stderr.write(f'[tk_rthook] tkinter preload failed: {e}\n')
